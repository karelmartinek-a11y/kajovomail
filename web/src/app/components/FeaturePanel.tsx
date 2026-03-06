import type { ReactNode } from 'react'

interface FeaturePanelProps {
  title: string
  lead?: string
  children?: ReactNode
}

export const FeaturePanel = ({ title, lead, children }: FeaturePanelProps) => (
  <section className="feature-panel">
    <header>
      <h2 className="feature-panel__title">{title}</h2>
      {lead && <p className="feature-panel__lead">{lead}</p>}
    </header>
    <div className="feature-panel__body">{children}</div>
  </section>
)
