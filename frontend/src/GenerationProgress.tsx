import { useEffect, useState } from 'react'
import { ComparisonProgress } from './ActivityTimeline'

type Draft = { title:string; questions:{id:number; number:string; text:string}[]; generation?:{status:string; stage?:string; progress?:number; total?:number; error?:string; comparison_id?:number; outcome_counts?:Record<string,number>} }
export function GenerationProgress({paperId}:{paperId:number}) {
  const [paper,setPaper]=useState<Draft|null>(null)
  const [error,setError]=useState('')
  const [retrying,setRetrying]=useState(false)
  const retry=async()=>{setRetrying(true);setError('');try{const response=await fetch(`/api/papers/${paperId}/generation/retry`,{method:'POST'});if(!response.ok)throw new Error((await response.json()).detail||'Could not retry');setPaper(old=>old?{...old,generation:{...old.generation!,status:'queued',stage:'Queued to resume',error:undefined}}:old)}catch(e){setError(String(e))}finally{setRetrying(false)}}
  useEffect(()=>{let active=true; const refresh=async()=>{try{const response=await fetch(`/api/papers/${paperId}`);if(!response.ok)throw new Error(`Could not load draft (${response.status})`);const data=await response.json();if(active){setPaper(data);setError('')}}catch(e){if(active)setError(String(e))}};void refresh();const timer=window.setInterval(refresh,3000);return()=>{active=false;window.clearInterval(timer)}},[paperId])
  const g=paper?.generation
  return <div className="inline-form"><strong>{paper?.title||'Generating paper'}</strong><p className="hint">{g?.stage||g?.status||'Connecting'} · {g?.progress||0}/{g?.total||0} questions</p>{error&&<p className="error">{error}</p>}{g?.error&&<p className="error">{g.error}</p>}{g?.status==='failed'&&<button className="primary" disabled={retrying} onClick={()=>void retry()}>{retrying?'Retrying…':'Retry generation'}</button>}{paper?.questions.map(q=><p key={q.id}><strong>{q.number}</strong> {q.text}</p>)}{g?.outcome_counts&&<p>Screening: {g.outcome_counts.A||0} A · {g.outcome_counts.B||0} B · {g.outcome_counts.C||0} C · {g.outcome_counts.review||0} need review. Check all results before using the paper.</p>}{g?.comparison_id&&<ComparisonProgress comparisonId={g.comparison_id}/>}</div>
}
