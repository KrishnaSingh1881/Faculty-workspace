import React from 'react'

function labelFor(key: string) {
  return key.replace(/_/g, ' ').replace(/\b\w/g, value => value.toUpperCase())
}

export function ReadableData({ value }: { value: any }) {
  if (value === null || value === undefined) return <span>None</span>
  if (typeof value === 'boolean') return <span>{value ? 'Yes' : 'No'}</span>
  if (typeof value === 'string' || typeof value === 'number') return <span>{String(value)}</span>
  if (Array.isArray(value)) {
    return value.length ? <ul className="readable-list">{value.map((item, index) => <li key={index}><ReadableData value={item}/></li>)}</ul> : <span>None</span>
  }
  if (typeof value !== 'object') return null

  const entries = Object.entries(value).filter(([key, item]) => item !== undefined && key !== 'success'
    && !/^(call_id|request_id|trace_id|_?id|.*_id)$/i.test(key))
  if (!entries.length) return value.success === true ? <span>Completed successfully</span> : null
  return <div className="readable-data">
    {value.success === true && <strong>Completed</strong>}
    {entries.map(([key, item]) => <div className="readable-row" key={key}>
      <span>{labelFor(key)}</span>
      {/.*_ids?$/i.test(key) && Array.isArray(item)
        ? <span>{item.length} selected</span>
        : <ReadableData value={item}/>}
    </div>)}
  </div>
}
