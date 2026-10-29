import { useEffect, useState } from 'react'
import { ComparisonProgress } from './ActivityTimeline'

type Question = { id: number; number: string; text: string; unit?: number | null }
type Screen = { status: string; reason: string }
type Draft = {
  title: string
  questions: Question[]
  generation?: {
    status: string
    stage?: string
    progress?: number
    total?: number
    error?: string
    comparison_id?: number
    outcome_counts?: Record<string, number>
    quick_counts?: Record<string, number>
    quick_screens?: Record<string, Screen>
  }
}

const screenLabel: Record<string, string> = {
  different: 'Different',
  too_close: 'Too close',
  review: 'Review',
}

export function GenerationProgress({ paperId }: { paperId: number }) {
  const [paper, setPaper] = useState<Draft | null>(null)
  const [error, setError] = useState('')
  const [retrying, setRetrying] = useState(false)
  const retry = async () => {
    setRetrying(true)
    setError('')
    try {
      const response = await fetch(`/api/papers/${paperId}/generation/retry`, { method: 'POST' })
      if (!response.ok) throw new Error((await response.json()).detail || 'Could not retry')
      setPaper(old => old ? { ...old, generation: { ...old.generation!, status: 'queued', stage: 'Queued to resume', error: undefined } } : old)
    } catch (e) { setError(String(e)) }
    finally { setRetrying(false) }
  }

  useEffect(() => {
    let active = true
    const refresh = async () => {
      try {
        const response = await fetch(`/api/papers/${paperId}`)
        if (!response.ok) throw new Error(`Could not load draft (${response.status})`)
        const data = await response.json() as Draft
        if (active) { setPaper(data); setError('') }
      } catch (e) { if (active) setError(String(e)) }
    }
    void refresh()
    const timer = window.setInterval(refresh, 3000)
    return () => { active = false; window.clearInterval(timer) }
  }, [paperId])

  const g = paper?.generation
  const total = g?.total || paper?.questions.length || 0
  const progress = Math.min(total, g?.progress ?? paper?.questions.length ?? 0)
  const groups = new Map<string, Question[]>()
  for (const question of paper?.questions || []) {
    const name = question.unit ? `Unit ${question.unit}` : 'Questions'
    groups.set(name, [...(groups.get(name) || []), question])
  }

  return <>
    <article className="generation-preview" aria-label="Generated paper preview">
      <header className="generation-preview-head">
        <div><h3>{paper?.title || 'Generating paper'}</h3><p>{g?.stage || g?.status || 'Connecting to generation'}</p></div>
        <span className="generation-preview-count">{progress}<span> / {total} questions</span></span>
      </header>
      {total > 0 && <div className="generation-progress-track" role="progressbar" aria-label="Questions generated" aria-valuenow={progress} aria-valuemin={0} aria-valuemax={total}><span style={{ transform: `scaleX(${progress / total})` }}/></div>}
      {error && <p className="error" role="alert">{error}</p>}
      {g?.error && <p className="error" role="alert">{g.error}</p>}
      {g?.status === 'failed' && <button className="primary" disabled={retrying} onClick={() => void retry()}>{retrying ? 'Retrying…' : 'Retry generation'}</button>}
      {groups.size === 0 && <p className="generation-preview-empty">Questions will appear here as each batch finishes.</p>}
      {[...groups].map(([unit, questions]) => <section className="generation-unit" key={unit} aria-label={unit}>
        <div className="generation-unit-head"><h4>{unit}</h4><span>{questions.length} questions</span></div>
        <div className="generation-question-grid">{questions.map(question => {
          const screen = g?.quick_screens?.[question.number]
          return <div className="generation-question" key={question.id}>
            <span className="generation-question-number">{question.number}</span>
            <div><p>{question.text}</p>{screen && <div className="generation-question-screen"><span className={`generation-screen-${screen.status}`}>{screenLabel[screen.status] || screen.status.replaceAll('_', ' ')}</span><small>{screen.reason}</small></div>}</div>
          </div>
        })}</div>
      </section>)}
      {g?.quick_counts && <p className="generation-summary">Checked against one past paper: {g.quick_counts.different || 0} different · {g.quick_counts.too_close || 0} too close · {g.quick_counts.review || 0} need review. Review questions before use.</p>}
      {g?.outcome_counts && <p className="generation-summary">Screening: {g.outcome_counts.A || 0} A · {g.outcome_counts.B || 0} B · {g.outcome_counts.C || 0} C · {g.outcome_counts.review || 0} need review. Check all results before using the paper.</p>}
    </article>
    {g?.comparison_id && <ComparisonProgress comparisonId={g.comparison_id} />}
  </>
}
