import React, { useEffect, useState } from 'react'

import fullLogo from '@brand/logo/exports/full/svg/kajovo-mail_full.svg?url'
import signace from '@brand/signace/signace.svg?url'

interface AppFrameProps {
  children: React.ReactNode
}

export const AppFrame = ({ children }: AppFrameProps) => {
  const [showIntro, setShowIntro] = useState(true)

  useEffect(() => {
    const timer = window.setTimeout(() => setShowIntro(false), 1400)
    return () => window.clearTimeout(timer)
  }, [])

  return (
    <>
      {children}
      <img src={signace} alt="KÁJOVO signace" className="floating-signace" />
      {showIntro && (
        <div className="intro-overlay" role="status" aria-label="Načítání KajovoMail">
          <img src={fullLogo} alt="KajovoMail plné logo" className="intro-overlay__logo" />
        </div>
      )}
    </>
  )
}
