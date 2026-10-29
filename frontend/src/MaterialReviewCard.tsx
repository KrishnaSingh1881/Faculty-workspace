import { useEffect, useState } from 'react'
import { BookOpen, ChevronDown, Upload } from 'lucide-react'

type Citation = {file:string;page:number;quote:string}
type Proposal = {topic_id:string;topic_label:string;summaries?:string[];citations?:Citation[]}
type Review = {id:number;filename:string;warnings:string[];pages:{page:number;preview:string;characters:number}[];proposals:Proposal[];enrichment:{status?:string;progress?:number;total?:number;error?:string;tree_version?:number}}
async function request<T>(path:string,init?:RequestInit):Promise<T>{const response=await fetch('/api'+path,{headers:{...(init?.body?{'Content-Type':'application/json'}:{})},...init});if(!response.ok){const data=await response.json().catch(()=>({detail:response.statusText}));throw new Error(data.detail||response.statusText)}return response.json()}

export function MaterialReviewCard({materialId}:{materialId:number;onApplied?:()=>void}){
 const [review,setReview]=useState<Review|null>(null),[expanded,setExpanded]=useState<Record<number,string>>({}),[busy,setBusy]=useState(false),[error,setError]=useState('')
 async function reload(){try{setReview(await request<Review>(`/materials/${materialId}/review`))}catch(e){setError(String(e))}}
 useEffect(()=>{void reload()},[materialId])
 useEffect(()=>{if(!['queued','running'].includes(review?.enrichment.status||''))return;const timer=window.setInterval(()=>void reload(),1000);return()=>window.clearInterval(timer)},[review?.enrichment.status,materialId])
 async function prepare(){setBusy(true);setError('');try{await request(`/materials/${materialId}/enrich`,{method:'POST'});await reload()}catch(e){setError(String(e))}finally{setBusy(false)}}
 async function fullPage(page:number){if(expanded[page]){setExpanded(old=>({...old,[page]:''}));return}try{const result=await request<{text:string}>(`/materials/${materialId}/pages/${page}`);setExpanded(old=>({...old,[page]:result.text}))}catch(e){setError(String(e))}}
 if(!review)return <div className="material-review-card">{error||'Loading material…'}</div>
 const status=review.enrichment.status||'not_started'
 const ready=status==='review_ready'||status==='applied'

 return <section className="material-review-card" aria-label={`Material ${review.filename}`}>
  <div className="material-review-head"><div><h3>{review.filename}</h3><p>{review.pages.length} extracted {review.pages.length===1?'page or section':'pages or sections'} · {status==='applied'?'Added to syllabus tree':ready?'Topic matches ready':status==='running'||status==='queued'?'Mapping material':'Extraction ready'}</p></div><BookOpen size={20}/></div>
  {review.warnings.map((warning,i)=><p className="material-warning" key={i}>{warning}</p>)}
  <details className="material-extraction" open={status==='not_started'}><summary>Extracted text <ChevronDown size={15}/></summary><div className="material-pages">{review.pages.map(page=><div className="material-page" key={page.page}><strong>Page {page.page}</strong><p>{expanded[page.page]||page.preview||'No readable text found.'}{!expanded[page.page]&&page.characters>1200?'…':''}</p>{page.characters>1200&&<button type="button" className="subtle" onClick={()=>void fullPage(page.page)}>{expanded[page.page]?'Show preview':'Read full page'}</button>}</div>)}</div></details>
  {['not_started','failed','cancelled'].includes(status)&&<div className="material-review-actions"><p>Find where this material appears in the active syllabus.</p><button className="primary" disabled={busy} onClick={()=>void prepare()}><Upload size={15}/>{busy?'Mapping…':'Map to syllabus'}</button></div>}
  {['queued','running'].includes(status)&&<p className="material-review-state">Matching the extracted text to syllabus topics…</p>}
  {review.enrichment.error&&<p role="alert" className="material-warning">{review.enrichment.error}</p>}
  {ready&&<div className="material-mappings"><div className="material-mapping-head"><div><h4>{review.proposals.length} syllabus {review.proposals.length===1?'topic':'topics'} found</h4><p>{status==='applied'?'These matches are now part of the syllabus tree.':'Review the topics and pages below. Say “go ahead, enrich” in chat to add all matches to the tree.'}</p></div></div>
   <div className="material-match-list">{review.proposals.length?review.proposals.map(proposal=><details className="material-match" key={proposal.topic_id}><summary><strong>{proposal.topic_label}</strong><span>{[...new Set((proposal.citations||[]).map(item=>item.page))].map(page=>`Page ${page}`).join(' · ')}</span><ChevronDown size={15}/></summary><div className="material-match-evidence">{proposal.citations?.map((citation,i)=><blockquote key={`${citation.page}-${i}`}><small>Page {citation.page}</small><p>“{citation.quote}”</p></blockquote>)}</div></details>):<p>No syllabus topics matched this material.</p>}</div>
  </div>}
  {error&&<p role="alert" className="material-warning">{error}</p>}
 </section>
}
