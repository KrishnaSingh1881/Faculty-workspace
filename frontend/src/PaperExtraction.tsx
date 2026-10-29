import { useEffect, useState } from 'react'

type Tagging = {id:number;status:string;progress:number;total:number;error:string|null;created_at?:string;finished_at?:string;paper?:any;tagging?:{pattern?:string;phase?:string;questions?:string[];needs_review?:Record<string,string>}}

export function PaperExtraction({upload,tagging,reveal=false}:{upload:any;tagging?:Tagging|null;reveal?:boolean}) {
  const [paper,setPaper]=useState(upload.paper)
  const [job,setJob]=useState<Tagging|null>(null)
  const [pollError,setPollError]=useState('')
  const [now,setNow]=useState(Date.now())
  const [cursor,setCursor]=useState(()=>({index:reveal&&!sessionStorage.getItem('paper-revealed:'+upload.paper.id)?0:upload.paper.questions.length,chars:0}))
  useEffect(()=>{if(reveal)sessionStorage.setItem('paper-revealed:'+upload.paper.id,'true')},[reveal,upload.paper.id])
  const questions=paper.questions||[]
  const jobId=tagging?.id||upload.tagging_job_id
  const active=job??tagging
  const running=!!active&&['queued','running'].includes(active.status)
  const revealing=cursor.index<questions.length
  const ready=questions.filter((q:any)=>q.confirmed&&q.unit&&q.topic_ids?.length).length
  useEffect(()=>{
    if(!jobId)return
    let stopped=false
    let timer:ReturnType<typeof setTimeout>
    async function poll(){
      try{
        const response=await fetch('/api/jobs/'+jobId)
        if(!response.ok)throw new Error('Status is unavailable')
        const next=await response.json() as Tagging
        if(stopped)return
        setJob(next);setPollError('')
        if(next.paper)setPaper(next.paper)
        if(['queued','running','cancel_requested'].includes(next.status))timer=setTimeout(poll,1500)
      }catch{
        if(!stopped){setPollError('Cannot refresh tagging status. Reconnecting…');timer=setTimeout(poll,3000)}
      }
    }
    void poll()
    return()=>{stopped=true;clearTimeout(timer)}
  },[jobId])
  useEffect(()=>{
    if(!revealing)return
    if(window.matchMedia('(prefers-reduced-motion: reduce)').matches){setCursor({index:questions.length,chars:0});return}
    const text=questions[cursor.index].text
    const finished=cursor.chars>=text.length
    const timer=setTimeout(()=>setCursor(old=>finished?{index:old.index+1,chars:0}:{...old,chars:Math.min(text.length,old.chars+6)}),finished?450:45)
    return()=>clearTimeout(timer)
  },[cursor,questions.length,revealing])
  useEffect(()=>{if(!running)return;const timer=setInterval(()=>setNow(Date.now()),1000);return()=>clearInterval(timer)},[running])
  const started=active?.created_at?Date.parse(active.created_at):NaN
  const seconds=Number.isFinite(started)?Math.max(0,Math.floor(((active?.finished_at?Date.parse(active.finished_at):now)-started)/1000)):null
  const elapsed=seconds===null?'':seconds<60?`${seconds}s`:`${Math.floor(seconds/60)}m ${seconds%60}s`
  const current=active?.tagging?.questions?.map(label=>/^q/i.test(label)?label:`Q${label}`).join(', ')
  const status=active?.status==='queued'?'Waiting for the local model'
    :running?`${active?.tagging?.phase==='working'?'Tagging':'Waiting for model output'}${current?' · '+current:''}`
    :active?.status==='complete'?`Tagging complete · ${ready}/${questions.length} ready${ready<questions.length?` · ${questions.length-ready} need topic review`:''}`
    :active?.status==='failed'?'Tagging failed · saved tags kept'
    :active?.status==='cancelled'?'Tagging cancelled · saved tags kept'
    :jobId?'Connecting to tagging status…':'Extracted · ready to review'
  return <section className="paper-extraction" aria-label="Extracted paper questions">
    <header><div><strong>Extracted questions</strong><span>{questions.length} found · {paper.title}</span></div><div className="paper-extraction-status"><small role="status">{status}</small>{active&&<small>{active.progress}/{active.total} processed{elapsed?' · '+elapsed:''}</small>}{active?.tagging?.pattern&&<small>Units from {active.tagging.pattern}</small>}</div></header>
    {active&&<progress className="paper-tag-progress" aria-label="Question tagging progress" value={active.progress} max={Math.max(1,active.total)}/>}
    {revealing&&<div className="paper-reveal-controls"><small>Revealing question {cursor.index+1} of {questions.length}</small><button className="subtle" onClick={()=>setCursor({index:questions.length,chars:0})}>Show all questions</button></div>}
    <ol>{questions.slice(0,Math.min(questions.length,cursor.index+1)).map((q:any,index:number)=><li key={q.id||index}><b>{/^q/i.test(q.number)?'':'Q'}{q.number}</b><div><p>{index===cursor.index?q.text.slice(0,cursor.chars):q.text}</p>{q.unit&&<small className="hint">Unit {q.unit}{q.confirmed?' · Topic assigned':running?' · Topic pending':' · Needs topic review'}</small>}{active?.tagging?.needs_review?.[q.id]&&<small className="hint">Needs review: {active.tagging.needs_review[q.id]}</small>}</div></li>)}</ol>
    {pollError&&<p className="paper-extraction-hint" role="status">{pollError}</p>}
    {active?.status==='failed'&&<p className="error" role="status">{active.error||'The local model could not tag every question.'} Retry tagging from Papers.</p>}
    {!!upload.warnings?.length&&<details className="paper-extraction-notes"><summary>Extraction notes ({upload.warnings.length})</summary><ul>{upload.warnings.map((warning:string,index:number)=><li key={index}>{warning}</li>)}</ul></details>}
    <p className="paper-extraction-hint">Check the wording against the PDF. Tell me any corrections, or say “set as base” when it’s ready.</p>
  </section>
}
