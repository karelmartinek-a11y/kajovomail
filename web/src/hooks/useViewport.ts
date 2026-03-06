import { useEffect, useState } from 'react'

import tokens from '@brand/ui-tokens/tokens.json'

export const useViewport = () => {
  const [width, setWidth] = useState(() => {
    if (typeof window === 'undefined') return tokens.breakpoints.md[0]
    return window.innerWidth
  })

  useEffect(() => {
    const update = () => setWidth(window.innerWidth)
    window.addEventListener('resize', update)
    return () => window.removeEventListener('resize', update)
  }, [])

  const { breakpoints } = tokens
  const isMobile = width <= breakpoints.sm[1]
  const isTablet = width >= breakpoints.md[0] && width <= breakpoints.md[1]
  const isDesktop = width >= breakpoints.lg[0]

  return { width, isMobile, isTablet, isDesktop }
}
