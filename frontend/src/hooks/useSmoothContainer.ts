import { useEffect, useRef } from 'react'

export function useSmoothContainer() {
  const ref = useRef<HTMLDivElement>(null)
  const target = useRef(0)
  const current = useRef(0)
  const rafId = useRef(0)

  const lerp = (a: number, b: number, t: number) => a + (b - a) * t

  useEffect(() => {
    const el = ref.current
    if (!el) return

    const animate = () => {
      current.current = lerp(current.current, target.current, 0.12)

      const diff = Math.abs(target.current - current.current)
      if (diff > 0.5) {
        el.scrollTop = current.current
        rafId.current = requestAnimationFrame(animate)
      } else {
        el.scrollTop = target.current
        current.current = target.current
      }
    }

    const onWheel = (e: WheelEvent) => {
      e.preventDefault()
      target.current = Math.max(
        0,
        Math.min(
          target.current + e.deltaY,
          el.scrollHeight - el.clientHeight
        )
      )
      current.current = el.scrollTop
      cancelAnimationFrame(rafId.current)
      rafId.current = requestAnimationFrame(animate)
    }

    el.addEventListener('wheel', onWheel, { passive: false })
    return () => {
      el.removeEventListener('wheel', onWheel)
      cancelAnimationFrame(rafId.current)
    }
  }, [])

  return ref
}