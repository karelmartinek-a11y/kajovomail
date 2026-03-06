import React, { useState } from 'react'

import { FeaturePanel } from '@app/components/FeaturePanel'
import { StatusMessage } from '@app/components/StatusMessage'

const initial = {
  prompt: 'Summarize new offers',
  status: 'store: false',
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
      <FeaturePanel title="AI orchestration" lead="Structured output · privacy audit">
        <form className="form" onSubmit={handleSubmit}>
          <label className="form__field">
            <span>Prompt</span>
            <input value={prompt} onChange={(event) => setPrompt(event.target.value)} />
          </label>
          <div className="form__helper">Default response policy: {initial.status}</div>
          <button type="submit" className="primary-button">
            Run orchestration
          </button>
        </form>
        {submitted && (
          <StatusMessage
            variant="empty"
            title="Structured response available"
            description="Plain text, HTML preview, and metadata generated from the schema."
          />
        )}
      </FeaturePanel>
    </div>
  )
}
