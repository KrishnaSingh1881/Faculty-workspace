import { useEffect, useMemo, useState } from 'react'
import { ArrowLeft, ChevronRight, GitBranch, Search } from 'lucide-react'
import { Button } from './components/ui/button'
import { Input } from './components/ui/input'

type Node = {
  id: string
  kind: 'course' | 'unit' | 'heading' | 'topic'
  label: string
  parent?: string | null
  order?: number
  description?: string
  source_text?: string
  distinguish_from?: { node: string; how?: string; note?: string; review_status?: string }[]
}
type Tree = {
  nodes: Node[]
  cross_links?: { a: string; b: string; reason?: string }[]
  review_questions?: { node: string; question: string }[]
}

function shortLabel(label: string) {
  const words = label.split(/\s+/)
  const lines: string[] = []
  let line = ''
  for (const word of words) {
    if (line && `${line} ${word}`.length > 16) { lines.push(line); line = word }
    else line = line ? `${line} ${word}` : word
  }
  if (line) lines.push(line)
  return lines.slice(0, 2).map((part, index) => index === 1 && lines.length > 2 ? `${part.slice(0, 14)}…` : part)
}

export function SyllabusOrbit({ tree }: { tree: Tree | null }) {
  const nodes = tree?.nodes || []
  const index = useMemo(() => new Map(nodes.map(node => [node.id, node])), [nodes])
  const children = useMemo(() => {
    const map = new Map<string, Node[]>()
    for (const node of nodes) if (node.parent) map.set(node.parent, [...(map.get(node.parent) || []), node])
    for (const list of map.values()) list.sort((a, b) => (a.order ?? 0) - (b.order ?? 0))
    return map
  }, [nodes])
  const units = useMemo(() => nodes.filter(node => node.kind === 'unit'), [nodes])
  const [focusId, setFocusId] = useState<string | null>(null)
  const [selectedId, setSelectedId] = useState<string | null>(null)
  const [query, setQuery] = useState('')
  useEffect(() => {
    const first = units[0]
    setFocusId(first?.id ?? null)
    setSelectedId(first ? (children.get(first.id)?.[0]?.id ?? first.id) : null)
    setQuery('')
  }, [tree])
  if (!tree || !units.length) return <div className="orbit-empty">The syllabus map will appear when a tree is loaded.</div>

  const focus = index.get(focusId || '') || units[0]
  const visible = children.get(focus.id) || []
  const selected = index.get(selectedId || '') || focus
  const activeUnit = units.find(unit => focus.id === unit.id || focus.id.startsWith(`${unit.id}/`)) || units[0]
  const ancestors: Node[] = []
  let cursor: Node | undefined = focus
  while (cursor) { ancestors.unshift(cursor); cursor = cursor.parent ? index.get(cursor.parent) : undefined }
  const results = query.trim().length > 1
    ? nodes.filter(node => node.kind !== 'course' && `${node.label} ${node.description || ''}`.toLowerCase().includes(query.trim().toLowerCase())).slice(0, 24)
    : []
  const distinctions = (selected.distinguish_from || []).filter(item => index.has(item.node))
  const related = (tree.cross_links || []).filter(link => link.a === selected.id || link.b === selected.id)
  const reviewNotes = (tree.review_questions || []).filter(note => note.node === selected.id)

  function choose(node: Node) {
    setSelectedId(node.id)
    if ((children.get(node.id) || []).length) setFocusId(node.id)
  }
  function jump(node: Node) {
    setSelectedId(node.id)
    setFocusId(node.kind === 'unit' ? node.id : node.parent || activeUnit.id)
    setQuery('')
  }
  const centerLabel = shortLabel(focus.label)
  const radius = visible.length > 7 ? 212 : 196
  const positions = visible.map((node, i) => {
    const angle = -Math.PI / 2 + i * Math.PI * 2 / visible.length
    return { node, x: 380 + Math.cos(angle) * radius, y: 277 + Math.sin(angle) * radius }
  })

  return <div className="syllabus-orbit">
    <div className="orbit-unit-tabs" aria-label="Syllabus units">{units.map((unit, index) => {
      const count = nodes.filter(node => node.kind === 'topic' && node.id.startsWith(`${unit.id}/`)).length
      return <button type="button" key={unit.id} className={activeUnit.id === unit.id ? 'active' : ''} onClick={() => { setFocusId(unit.id); setSelectedId(children.get(unit.id)?.[0]?.id || unit.id); setQuery('') }}><span>Unit {index + 1}</span><strong>{unit.label}</strong><small>{count} topics</small></button>
    })}</div>
    <div className="orbit-toolbar"><div className="orbit-breadcrumb"><Button variant="ghost" size="icon" aria-label="Go to parent" disabled={!focus.parent || index.get(focus.parent)?.kind === 'course'} onClick={() => { if (focus.parent) { setFocusId(focus.parent); setSelectedId(focus.id) } }}><ArrowLeft size={17}/></Button>{ancestors.filter(node => node.kind !== 'course').map((node, i) => <span key={node.id}>{i > 0 && <ChevronRight size={14}/>}<button type="button" onClick={() => { setFocusId(node.id); setSelectedId(node.id) }}>{node.label}</button></span>)}</div><div className="orbit-search"><Search size={17}/><Input aria-label="Find syllabus topic" placeholder="Find a topic…" value={query} onChange={event => setQuery(event.target.value)}/></div></div>
    {query.trim().length > 1 && <div className="orbit-search-results" aria-live="polite">{results.length ? results.map(node => <button type="button" key={node.id} onClick={() => jump(node)}><strong>{node.label}</strong><span>{units.find(unit => node.id.startsWith(`${unit.id}/`))?.label || ''}</span></button>) : <p>No matching topic.</p>}</div>}
    <div className="orbit-workbench"><div className="orbit-canvas"><div className="orbit-canvas-head"><span>{focus.kind === 'unit' ? 'Unit map' : 'Topic map'}</span><span>{visible.length} connected {visible.length === 1 ? 'item' : 'items'}</span></div><div className="orbit-svg-scroll"><svg viewBox="0 0 760 560" width="760" height="560" role="group" aria-label={`${focus.label} and its ${visible.length} direct syllabus items`}>
      <circle cx="380" cy="277" r={radius} className="orbit-guide"/>
      {positions.map(({ node, x, y }) => <line key={`edge-${node.id}`} x1="380" y1="277" x2={x} y2={y} className={selected.id === node.id ? 'orbit-edge active' : 'orbit-edge'}/>)}
      <g className="orbit-center" transform="translate(380 277)"><circle r="47"/><text textAnchor="middle" y={centerLabel.length === 1 ? 5 : -5}>{centerLabel.map((line, i) => <tspan key={i} x="0" dy={i ? 17 : 0}>{line}</tspan>)}</text></g>
      {positions.map(({ node, x, y }) => {
        const hasChildren = (children.get(node.id) || []).length > 0
        const lines = shortLabel(node.label)
        return <g key={node.id} className={`orbit-node${selected.id === node.id ? ' selected' : ''}`} transform={`translate(${x} ${y})`} role="button" tabIndex={0} aria-label={`${node.label}${hasChildren ? ', open subtopics' : ''}`} onClick={() => choose(node)} onKeyDown={event => { if (event.key === 'Enter' || event.key === ' ') { event.preventDefault(); choose(node) } }}><circle r={hasChildren ? 23 : 19}/><text className="orbit-node-symbol" textAnchor="middle" y="5">{hasChildren ? '+' : '•'}</text><text className="orbit-node-label" textAnchor="middle" y="39">{lines.map((line, i) => <tspan key={i} x="0" dy={i ? 15 : 0}>{line}</tspan>)}</text></g>
      })}
    </svg></div><p className="orbit-canvas-foot">Select a node for its source and meaning. Nodes with + open a deeper level.</p></div>
    <aside className="orbit-inspector"><div className="orbit-inspector-head"><span>{selected.kind === 'unit' ? 'Unit' : selected.kind === 'heading' ? 'Heading' : 'Topic'}</span><span>{selected.id.split('/').slice(1).join(' / ')}</span></div><h3>{selected.label}</h3>{selected.description && <p className="orbit-description">{selected.description}</p>}{selected.source_text && <div className="orbit-source"><strong>Source wording</strong><p>{selected.source_text}</p></div>}{reviewNotes.map((note, i) => <div className="orbit-note" key={i}><strong>Interpretation note</strong><p>{note.question}</p></div>)}{distinctions.length > 0 && <div className="orbit-relations"><h4>Distinguish from</h4>{distinctions.map(item => { const target = index.get(item.node)!; return <details key={item.node}><summary>{target.label}</summary><p>{item.how || item.note || 'The tree records a distinction between these topics.'}</p><button type="button" onClick={() => jump(target)}>View topic <ChevronRight size={14}/></button></details> })}</div>}{related.length > 0 && <div className="orbit-relations"><h4><GitBranch size={15}/> Related links</h4>{related.map((link, i) => { const target = index.get(link.a === selected.id ? link.b : link.a); return target && <div className="orbit-related" key={i}><button type="button" onClick={() => jump(target)}>{target.label} <ChevronRight size={14}/></button>{link.reason && <p>{link.reason}</p>}</div> })}<small>These links help navigation and do not affect comparison judgments.</small></div>}</aside></div>
  </div>
}
