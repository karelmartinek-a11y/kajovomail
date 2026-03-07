import React from 'react'

import brandMeta from '@brand/brand/brand.json'
import signace from '@brand/signace/signace.svg?url'
import mark from '@brand/logo/exports/mark/svg/kajovo-mail_mark.svg?url'

interface StandaloneLayoutProps {
  children: React.ReactNode
}

export const StandaloneLayout = ({ children }: StandaloneLayoutProps) => (
  <div className="standalone-layout">
    <div className="standalone-layout__panel">
      <header className="standalone-layout__header">
        <div className="brand-compact" aria-label={`${brandMeta.appName} značka`}>
          <img src={signace} alt={`${brandMeta.appName} signace`} className="brand-compact__signace" />
          <img src={mark} alt={`${brandMeta.appName} mark`} className="brand-compact__mark" />
        </div>
        <div>
          <p className="brand-mark__name">{brandMeta.appName}</p>
          <p className="brand-mark__tagline">mail.hcasc.cz</p>
        </div>
      </header>
      {children}
    </div>
  </div>
)
