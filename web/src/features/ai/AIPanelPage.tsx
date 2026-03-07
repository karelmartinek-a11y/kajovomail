import React, { useState } from 'react'

import { FeaturePanel } from '@app/components/FeaturePanel'
import { StatusMessage } from '@app/components/StatusMessage'

const initial = {
  prompt: 'Shrň nové nabídky',
  status: 'ukládání: ne',
}

export const AIPanelPage = () => {
  const [prompt, setPrompt] = useState(initial.prompt)
  const [submitted, setSubmitted] = useState(false)

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setSubmitted(true)
  }

  return (
    <div className="page-container">
      <FeaturePanel title="AI orchestrace" lead="Strukturovaný výstup · audit soukromí">
        <form className="form" onSubmit={handleSubmit}>
          <label className="form__field">
            <span>Prompt</span>
            <input value={prompt} onChange={(event) => setPrompt(event.target.value)} />
          </label>
          <div className="form__helper">Výchozí politika odpovědi: {initial.status}</div>
          <button type="submit" className="primary-button">
            Spustit orchestraci
          </button>
        </form>
        {submitted && (
          <StatusMessage
            variant="empty"
            title="Strukturovaná odpověď je připravená"
            description="Ze schématu vznikl prostý text, HTML náhled i metadata."
          />
        )}
      </FeaturePanel>
    </div>
  )
}
