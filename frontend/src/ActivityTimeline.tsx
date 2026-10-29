import { useEffect, useMemo, useState } from 'react'
import { Check, ChevronRight, Circle, LoaderCircle, Wrench } from 'lucide-react'
import { type Activity, appendActivity } from './stream'
import { ReadableData } from './ReadableData'

const roles: Record<string, string> = { workspace: 'Assistant', helper: 'Helper', judge: 'Judge', extractor: 'Requirement extraction', system: 'Workspace' }
const humanize = (value: string) => value.replaceAll('_', ' ').replace(/\b\w/g, letter => letter.toUpperCase())

type ChatComparison = { title:string; strategy?:string; status:string; progress:number; total:number; error:string|null; job?:{status:string}|null; results:{id:number; label:string; reason:string; source:string; stale?:boolean; target:{number:string; text:string; unit:number|null}; reference:{number:string; text:string}; block?:{unit:number; questions:{id:number; number:string; text:string}[]}|null; evidence:unknown[]}[] }

function ReviewResult({ resultId, onSaved }: { resultId:number; onSaved:()=>void }) {
  const [label, setLabel] = useState('A')
  const [reason, setReason] = useState('')
  const [message, setMessage] = useState('')
  const save = async () => {
    try {
      const response = await fetch(`/api/results/${resultId}/resolve`, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({label, reason})})
      if (!response.ok) throw new Error((await response.json()).detail || 'Could not save review')
      setMessage('Review saved.'); setReason(''); onSaved()
    } catch (error) { setMessage(String(error)) }
  }
  return <details><summary>Review this result</summary><div className="inline-form"><label>Classification<select value={label} onChange={e=>setLabel(e.target.value)}><option value="A">A · Repeat</option><option value="B">B · Related</option><option value="C">C · Unrelated</option></select></label><label>Reason<textarea value={reason} onChange={e=>setReason(e.target.value)}/></label><button className="primary" disabled={!reason.trim()} onClick={()=>void save()}>Save review</button>{message&&<p role="status">{message}</p>}</div></details>
}

export function ComparisonProgress({ comparisonId }: { comparisonId: number }) {
  const [events, setEvents] = useState<Activity[]>([])
  const [comparison, setComparison] = useState<ChatComparison | null>(null)
  const [error, setError] = useState('')
  const [cancelling, setCancelling] = useState(false)
  const [version, setVersion] = useState(0)
  useEffect(() => {
    let active = true
    const refresh = async () => {
      try {
        const response = await fetch(`/api/comparisons/${comparisonId}`)
        if (!response.ok) throw new Error(`Could not load comparison (${response.status})`)
        const data = await response.json() as ChatComparison
        if (active) { setComparison(data); setError('') }
      } catch (e) { if (active) setError(String(e)) }
    }
    setEvents([])
    void refresh()
    const timer = window.setInterval(refresh, 3000)
    const stream = new EventSource(`/api/comparisons/${comparisonId}/events`)
    stream.addEventListener('activity', event => {
      const row = JSON.parse((event as MessageEvent).data) as Activity
      setEvents(old => appendActivity(old, row))
      if (row.event === 'pair_finished' || row.event === 'cache_hit') void refresh()
    })
    stream.addEventListener('complete', () => { void refresh(); stream.close() })
    return () => { active = false; window.clearInterval(timer); stream.close() }
  }, [comparisonId, version])
  const cancel = async () => {
    setCancelling(true)
    try {
      const response = await fetch(`/api/comparisons/${comparisonId}/cancel`, { method:'POST' })
      if (!response.ok) throw new Error((await response.json()).detail || 'Could not cancel comparison')
      setVersion(value => value + 1)
    } catch (e) { setError(String(e)) } finally { setCancelling(false) }
  }
  const active = comparison && ['queued', 'running'].includes(comparison.status)
  const pendingCancel = comparison?.job?.status === 'cancel_requested'
  return <div className="chat-comparison">
    <div className="content-actions"><div><strong>{comparison?.title || `Comparison #${comparisonId}`}</strong><p className="hint">{pendingCancel ? 'Stopping this comparison after the current model response' : comparison?.status || 'Connecting'} · {comparison?.progress || 0}/{comparison?.total || 0} {comparison?.strategy ? 'unit checks' : 'pairs'}</p></div>{active && <button className="subtle" disabled={cancelling || pendingCancel} onClick={() => void cancel()}>{pendingCancel ? 'Stopping…' : cancelling ? 'Cancelling…' : 'Cancel entire comparison'}</button>}</div>
    {error && <p className="error" role="alert">{error}</p>}
    {comparison?.error && <p className="hint">{comparison.error}</p>}
    <details className="comparison-activity" open={!!active}><summary>Comparison activity</summary><ActivityTimeline events={events} live={!!active && !pendingCancel} /></details>
    {!!comparison?.results.length && <section className="chat-comparison-results" aria-label="Comparison results">
      <div className="results-heading"><div><h3>Comparison results</h3><p>{comparison.results.length} {comparison.results.length === 1 ? 'result' : 'results'} available</p></div><div className="results-counts" aria-label="Classification counts">{(['A','B','C','review'] as const).map(label => <span key={label}><b>{comparison.results.filter(result => result.label === label).length}</b> {label === 'review' ? 'Review' : label}</span>)}</div></div>
      {comparison.results.map(result => <article className="chat-result" key={result.id}>
        <div className="result-card-heading"><div className="result-card-meta"><span className="result-number">Q{result.target.number}</span><span>{result.block ? `Unit ${result.block.unit} · Past paper block` : `Unit ${result.target.unit ?? '—'} · Compared with Q${result.reference.number}`}</span></div><span className={'label '+result.label.toLowerCase()}>{result.label === 'A' ? (result.block?'A · Same topic and depth':'A · Repeat') : result.label === 'B' ? (result.block?'B · Different or partial':'B · Related') : result.label === 'C' ? (result.block?'C · Topic absent':'C · Unrelated') : 'Needs review'}</span></div>
        <div className="result-card-question"><span>Base question</span><p>{result.target.text}</p></div>
        <div className="result-card-reason"><span>Why {result.label === 'review' ? 'review is needed' : result.label}</span><p>{result.reason || 'No reason was recorded for this result.'}</p></div>
        {result.stale && <p className="result-stale">This result was created with an earlier version or changed source material. Run a new comparison to update it.</p>}
        <details className="result-evidence"><summary><span>{result.block ? 'View past paper block' : 'View comparison question'}</span><ChevronRight size={16}/></summary>{result.block ? <div className="result-block">{result.block.questions.map(question=><div key={question.id}><strong>Q{question.number}</strong><p>{question.text}</p></div>)}</div> : <p>{result.reference.text}</p>}</details>
        <details className="result-evidence"><summary><span>Evidence and checks</span><ChevronRight size={16}/></summary><ReadableData value={result.evidence}/></details>
        {(result.label==='review'||result.source==='faculty_case_review')&&<ReviewResult resultId={result.id} onSaved={()=>setVersion(value=>value+1)}/>}
      </article>)}
    </section>}
  </div>
}

export function ActivityTimeline({ events, live = false }: { events: Activity[]; live?: boolean }) {
  const rows = useMemo(() => {
    let result: Activity[] = []
    for (const event of events) {
      if (event.event === 'tool' && event.payload.call_id) {
        const index = result.findIndex(row => row.event === 'tool_started' && row.agent === event.agent
          && row.payload.call_id === event.payload.call_id && row.target_id === event.target_id && row.reference_id === event.reference_id)
        if (index >= 0) { result[index] = event; continue }
      }
      if (['thinking', 'tool_started', 'tool', 'finished', 'repair', 'failed', 'cache_hit', 'pair_started', 'pair_finished', 'helper_requested', 'block_started', 'content'].includes(event.event)) result = appendActivity(result, event)
    }
    return result
  }, [events])
  if (!rows.length && !live) return null
  const latest = events.at(-1)
  const status = latest?.event === 'thinking' ? 'Thinking' : latest?.event === 'content' ? 'Writing response'
    : latest?.event === 'tool_started' ? 'Using ' + latest.payload.name.replaceAll('_', ' ') : 'Working'
  return <section className="agent-activity" aria-label="Model thinking and tool activity">
    {rows.map((event, index) => {
      const name = roles[event.agent] || event.agent
      const isTool = ['tool', 'tool_started'].includes(event.event)
      const running = live && event.event === 'tool_started'
      if (event.event === 'content') return <details className="thinking-block" key={index}><summary><ChevronRight size={14} /><span>{name} · model output</span></summary><div className="model-thinking">{event.payload.text}</div></details>
      if (event.event === 'thinking') return <details className="thinking-block" key={index}>
        <summary><ChevronRight size={14} /><span>{name} thinking</span>{event.payload.model && <small>{event.payload.model}</small>}</summary>
        <div className="model-thinking">{event.payload.text}</div>
      </details>
      if (event.event === 'finished') return <details className="agent-message" key={index}>
        <summary><Check size={14} /><span>{name} · response</span><small>{event.payload.tool_calls ?? 0} tools</small></summary>
        <div className="tool-detail"><ReadableData value={event.payload.summary}/></div>
      </details>
      if (isTool) return <details className={'tool-step' + (event.payload.result?.error ? ' tool-failed' : '')} key={index}>
        <summary>{running ? <LoaderCircle size={14} className="activity-spinner" /> : event.payload.result?.error ? <Circle size={14} /> : <Check size={14} />}<span>{name} · {humanize(event.payload.name || 'Workspace action')}</span><small>{running ? 'Running' : event.payload.result?.error ? 'Failed' : event.payload.duration_ms !== undefined ? `${event.payload.duration_ms} ms` : event.payload.name==='upload_paper' ? 'Extracted' : 'Finished'}</small></summary>
        <div className="tool-detail"><span>What it used</span><ReadableData value={event.payload.arguments}/>{event.event === 'tool' && <><span>What it found</span><ReadableData value={event.payload.result}/></>}</div>
      </details>
      const text = event.event === 'block_started' ? `Checking Q${event.payload.number} against ${event.payload.paper}, unit ${event.payload.unit} (${event.payload.questions} questions)`
        : event.event === 'pair_started' ? `Comparing questions ${event.payload.target_id} and ${event.payload.reference_id}`
        : event.event === 'cache_hit' ? `Reused a current saved result · ${event.payload.label}`
        : event.event === 'pair_finished' ? `Pair completed · ${event.payload.label}`
        : event.event === 'helper_requested' ? event.payload.reason
        : event.payload.error || event.payload.reason || event.event
      return <div className="activity-note" key={index}><Wrench size={13} /><span>{name} · {text}</span></div>
    })}
    {live && <div className="live-status" role="status"><LoaderCircle size={14} className="activity-spinner" /><span>{roles[latest?.agent || 'workspace'] || 'Assistant'} · {status}…</span></div>}
  </section>
}
