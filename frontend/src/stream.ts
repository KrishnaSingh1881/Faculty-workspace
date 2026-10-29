export type Activity = {
  id?: number
  agent: string
  event: string
  payload: Record<string, any>
  created_at?: string
  target_id?: number
  reference_id?: number
}

export function appendActivity(events: Activity[], event: Activity): Activity[] {
  const previous = events.at(-1)
  if (previous && ['thinking', 'content'].includes(event.event)
    && previous.event === event.event && previous.agent === event.agent
    && previous.payload.request_id === event.payload.request_id) {
    return [...events.slice(0, -1), { ...previous, payload: { ...previous.payload, text: previous.payload.text + event.payload.text } }]
  }
  return [...events, event]
}

// Only render the model's actual answer field; incomplete JSON stays in the activity trace.
export function answerPrefix(content: string): string {
  const match = content.match(/"answer"\s*:\s*"((?:\\[\s\S]|[^"\\])*)/)
  if (!match) return ''
  let value = match[1]
  while (value) {
    try { return JSON.parse('"' + value + '"') } catch { value = value.slice(0, -1) }
  }
  return ''
}

export async function streamChat<T>(body: unknown, onActivity: (event: Activity) => void): Promise<T> {
  const response = await fetch('/api/chat/stream', {
    method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body),
  })
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: response.statusText }))
    throw new Error(typeof error.detail === 'string' ? error.detail : JSON.stringify(error.detail))
  }
  if (!response.body) throw new Error('This browser cannot read the response stream.')
  const reader = response.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''
  try {
    while (true) {
      const { done, value } = await reader.read()
      buffer += decoder.decode(value, { stream: !done })
      let boundary: RegExpMatchArray | null
      while ((boundary = buffer.match(/\r?\n\r?\n/))) {
        const frame = buffer.slice(0, boundary.index)
        buffer = buffer.slice(boundary.index! + boundary[0].length)
        const lines = frame.split(/\r?\n/)
        const kind = lines.find(line => line.startsWith('event:'))?.slice(6).trim()
        const data = lines.filter(line => line.startsWith('data:')).map(line => line.slice(5).trimStart()).join('\n')
        if (!data) continue
        const payload = JSON.parse(data)
        if (kind === 'complete') return payload as T
        if (kind === 'error') throw new Error(payload.message || 'The assistant could not finish this turn.')
        if (kind === 'activity') onActivity(payload)
      }
      if (done) throw new Error('Connection closed. Reopen the saved conversation to check the result before repeating an action.')
    }
  } finally {
    await reader.cancel().catch(() => {})
    reader.releaseLock()
  }
}
