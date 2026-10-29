import { useEffect, useState } from 'react'
import { LoaderCircle } from 'lucide-react'

type Event = {id:number;event:string;payload:Record<string,any>}
type Status = {status?:string;progress?:number;total?:number;activity?:Event[]}

export function MaterialMappingActivity({materialId}:{materialId:number}){
 const [state,setState]=useState<Status>({}),[events,setEvents]=useState<Event[]>([])
 useEffect(()=>{let active=true;const load=async()=>{try{const response=await fetch(`/api/materials/${materialId}/review`);if(!response.ok)return;const data=await response.json();if(active){setState(data.enrichment||{});setEvents(data.enrichment?.activity||[])}}catch{}};void load();const timer=window.setInterval(()=>void load(),3000);return()=>{active=false;clearInterval(timer)}},[materialId])
 useEffect(()=>{if(!['queued','running'].includes(state.status||''))return;const stream=new EventSource(`/api/materials/${materialId}/events`);stream.addEventListener('activity',message=>{const item=JSON.parse((message as MessageEvent).data) as Event;setEvents(old=>old.some(row=>row.id===item.id)?old:[...old,item].slice(-30))});stream.addEventListener('complete',()=>stream.close());return()=>stream.close()},[materialId,state.status])
 if(!['queued','running'].includes(state.status||''))return null
 const latest=events.at(-1)
 const detail=latest?.event==='topic_matched'&&latest.payload.topic?`Found ${latest.payload.topic}`:latest?.event==='mapping_complete'?`Found ${latest.payload.topics} topics`:'Matching extracted text to syllabus topics'
 return <div className="material-activity-flow" aria-live="polite"><div className="material-activity-title"><LoaderCircle size={14} className="activity-spinner"/><strong>Mapping material</strong><span>{state.total?`${state.progress||0} / ${state.total} topics`:''}</span></div><p>{detail}</p></div>
}
