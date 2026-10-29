type TraceEvent = { name?: string; result?: Record<string, any> }
export type ChatChoice = { kind: string; id: number | string; label: string }

const sources: Record<string, { field: string; kind: string; label: (item: any) => string }> = {
  search_papers: { field: 'papers', kind: 'paper', label: item => `${item.title}${item.year ? ` · ${item.year}` : ''}` },
  search_questions: { field: 'questions', kind: 'question', label: item => `${item.paper} · ${item.number}` },
  semantic_search_questions: { field: 'questions', kind: 'question', label: item => `Question ${item.number}` },
  lookup_syllabus: { field: 'topics', kind: 'syllabus topic', label: item => `${item.label}${item.unit ? ` · Unit ${item.unit}` : ''}` },
  list_materials: { field: 'materials', kind: 'teaching material', label: item => item.filename },
  list_templates: { field: 'templates', kind: 'template', label: item => `${item.name} · ${item.kind}` },
  list_comparisons: { field: 'comparisons', kind: 'comparison', label: item => item.title },
  list_comparison_results: { field: 'results', kind: 'comparison result', label: item => `${item.label} · Q${item.target_number} vs Q${item.reference_number}` },
  list_jobs: { field: 'jobs', kind: 'background job', label: item => `${item.kind} · ${item.status}` },
}

const readOnly = new Set([...Object.keys(sources), 'analyze_paper', 'analyze_subject_coverage', 'workspace_operations', 'prepare_report'])

export function chatChoices(answer: string, trace?: TraceEvent[]): ChatChoice[] {
  if (!trace?.length || !/(\?|\bwhich\b|\bchoose\b|\bselect\b|\bmultiple\b|\bseveral\b|\bmean\b)/i.test(answer)) return []
  if (trace.some(event => event.result?.success && !readOnly.has(event.name || '') && !(event.name === 'manage_job' && event.result?.action === 'status'))) return []
  for (const event of [...trace].reverse()) {
    const source = sources[event.name || '']
    if (!source) continue
    const items = event.result?.[source.field]
    if (!Array.isArray(items) || items.length < 2) continue
    const answerLower = answer.toLocaleLowerCase()
    const cited = items.filter(item => {
      if (!item || (typeof item.id !== 'number' && typeof item.id !== 'string')) return false
      const title = item.label || item.title || item.name || item.filename
      return answer.includes(String(item.id)) || (typeof title === 'string' && title.length > 4 && answerLower.includes(title.toLocaleLowerCase()))
    })
    const candidates = cited.length >= 2 ? cited : items
    if (candidates.length > 8) continue
    const choices = candidates.filter(item => item && (typeof item.id === 'number' || typeof item.id === 'string'))
      .map(item => ({ kind: source.kind, id: item.id, label: String(source.label(item) || item.id) }))
    if (choices.length >= 2) return choices
  }
  return []
}

export function ChatChoices({ answer, trace, disabled, onChoose }: { answer: string; trace?: TraceEvent[]; disabled: boolean; onChoose: (choice: ChatChoice) => void }) {
  const choices = chatChoices(answer, trace)
  if (!choices.length) return null
  return <div className="chat-choices" role="group" aria-label="Choose a search result">
    {choices.map(choice => <button type="button" key={`${choice.kind}:${choice.id}`} disabled={disabled} onClick={() => onChoose(choice)}>
      <strong>{choice.label}</strong><small>{choice.kind} · {choice.id}</small>
    </button>)}
  </div>
}
