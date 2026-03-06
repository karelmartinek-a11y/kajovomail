import React from 'react'

interface StandaloneLayoutProps {
  children: React.ReactNode
}

export const StandaloneLayout = ({ children }: StandaloneLayoutProps) => (
  <div className="standalone-layout">
    <div className="standalone-layout__panel">{children}</div>
  </div>
)
