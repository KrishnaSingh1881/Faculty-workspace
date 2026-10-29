import { useState } from 'react'
import { Search, X } from 'lucide-react'

type Topic = {id:string;label:string;description?:string;scope_terms?:string[];synonyms?:string[]}

export function TopicPicker({topics,selected,unit,onChange}:{topics:Topic[];selected:string[];unit:number|null;onChange:(ids:string[])=>void}) {
  const [query,setQuery]=useState('')
  const term=query.trim().toLocaleLowerCase()
  const filtered=topics.filter(topic=>[topic.label,topic.description,...(topic.scope_terms||[]),...(topic.synonyms||[])].filter(Boolean).join(' ').toLocaleLowerCase().includes(term))
  const toggle=(id:string)=>onChange(selected.includes(id)?selected.filter(value=>value!==id):[...selected,id])
  return <fieldset className="topic-picker">
    <legend>Topics{unit?` · Unit ${unit}`:''}</legend>
    <p className="topic-picker-help">Select one or more topics. Click a row to select or remove it.</p>
    <div className="topic-picker-search"><Search size={18} aria-hidden="true"/><input aria-label="Search topics in this unit" type="search" placeholder="Search topics, e.g. scheduling" value={query} disabled={!unit} onChange={event=>setQuery(event.target.value)}/></div>
    <div className="topic-picker-selected"><span role="status">{selected.length} selected</span>{selected.map(id=><button type="button" key={id} onClick={()=>toggle(id)} aria-label={`Remove ${topics.find(topic=>topic.id===id)?.label||id}`}><span>{topics.find(topic=>topic.id===id)?.label||id}</span><X size={14} aria-hidden="true"/></button>)}</div>
    <div className="topic-picker-options" role="group" aria-label="Available syllabus topics" tabIndex={0}>
      {filtered.map(topic=><label key={topic.id} className={'topic-picker-option'+(selected.includes(topic.id)?' is-selected':'')}><input type="checkbox" checked={selected.includes(topic.id)} onChange={()=>toggle(topic.id)}/><span><strong>{topic.label}</strong>{topic.description&&<small>{topic.description}</small>}</span></label>)}
      {!filtered.length&&<p className="topic-picker-empty">{!unit?'Choose a unit to see its topics.':topics.length?`No topics match “${query}”. Try another word or clear the search.`:'No topics are available in this unit. Check the syllabus in Knowledge.'}</p>}
    </div>
    {!!topics.length&&<p className="topic-picker-count">{filtered.length} of {topics.length} topics shown{term?' · Selections are kept when you search':''}</p>}
  </fieldset>
}
