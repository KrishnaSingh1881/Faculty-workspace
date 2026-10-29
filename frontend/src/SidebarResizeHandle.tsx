import { useEffect, useRef } from 'react'

const MIN_WIDTH = 220
const MAX_WIDTH = 420

function limit(width: number) {
  return Math.max(MIN_WIDTH, Math.min(width, MAX_WIDTH, window.innerWidth - 440))
}

export function SidebarResizeHandle({ width, onChange }: { width: number; onChange: (width: number) => void }) {
  const drag = useRef<{ x: number; width: number } | null>(null)
  const mouseCleanup = useRef<(() => void) | null>(null)

  useEffect(() => () => mouseCleanup.current?.(), [])

  return <div
    className="sidebar-resize-handle"
    role="separator"
    aria-label="Resize sidebar"
    aria-orientation="vertical"
    aria-valuemin={MIN_WIDTH}
    aria-valuemax={Math.max(MIN_WIDTH, Math.min(MAX_WIDTH, window.innerWidth - 440))}
    aria-valuenow={limit(width)}
    tabIndex={0}
    title="Drag to resize the sidebar. Double-click to reset."
    onPointerDown={event => {
      if (event.button !== 0) return
      drag.current = { x: event.clientX, width: limit(width) }
      event.currentTarget.setPointerCapture(event.pointerId)
    }}
    onPointerMove={event => {
      if (drag.current) onChange(limit(drag.current.width + event.clientX - drag.current.x))
    }}
    onPointerUp={event => {
      drag.current = null
      if (event.currentTarget.hasPointerCapture(event.pointerId)) event.currentTarget.releasePointerCapture(event.pointerId)
    }}
    onLostPointerCapture={() => { drag.current = null }}
    onMouseDown={event => {
      if (event.button !== 0) return
      event.preventDefault()
      mouseCleanup.current?.()
      const startX = event.clientX
      const startWidth = limit(width)
      const move = (moveEvent: MouseEvent) => onChange(limit(startWidth + moveEvent.clientX - startX))
      const stop = () => mouseCleanup.current?.()
      window.addEventListener('mousemove', move)
      window.addEventListener('mouseup', stop, { once: true })
      mouseCleanup.current = () => {
        window.removeEventListener('mousemove', move)
        window.removeEventListener('mouseup', stop)
        mouseCleanup.current = null
      }
    }}
    onDoubleClick={() => onChange(limit(264))}
    onKeyDown={event => {
      if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') {
        event.preventDefault()
        onChange(limit(width + (event.key === 'ArrowRight' ? 16 : -16)))
      } else if (event.key === 'Home' || event.key === 'End') {
        event.preventDefault()
        onChange(limit(event.key === 'Home' ? MIN_WIDTH : MAX_WIDTH))
      }
    }}
  />
}
