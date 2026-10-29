import { useState } from 'react'

export function ReportCard({ conversationId }: { conversationId:number|null }) {
  const [error, setError] = useState('')
  const [busy, setBusy] = useState(false)
  const [notice, setNotice] = useState('')
  const download = async (format:'txt'|'xlsx') => {
    if (!conversationId) return
    setBusy(true); setError(''); setNotice('')
    try {
      const response = await fetch(`/api/conversations/${conversationId}/report?format=${format}`)
      if (!response.ok) { const body=await response.json(); throw new Error(body.detail || 'Could not generate report') }
      const url=URL.createObjectURL(await response.blob())
      const link=document.createElement('a'); link.href=url; link.download=`chat-report.${format}`; link.click(); URL.revokeObjectURL(url); setNotice(`${format==='xlsx'?'Excel':'Text'} report downloaded.`)
    } catch (e) { setError(e instanceof Error ? e.message : String(e)) } finally { setBusy(false) }
  }
  return <div className="inline-form"><strong>Report for this chat</strong><p className="hint">Excel has two sheets: the papers in each saved comparison, then A/B/C classifications with reasons, a summary chart and predictability scores. It includes completed results from this chat.</p>{!conversationId&&<p className="hint">Start a comparison in this chat to create a report.</p>}{error&&<p className="error" role="alert">{error}</p>}{notice&&<p className="hint" role="status">{notice}</p>}<div className="format-choices"><button disabled={!conversationId||busy} onClick={()=>void download('xlsx')}>Download Excel report</button><button disabled={!conversationId||busy} onClick={()=>void download('txt')}>Download text report</button></div></div>
}
