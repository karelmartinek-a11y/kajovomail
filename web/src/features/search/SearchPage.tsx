import React, { useState } from 'react'

import { FeaturePanel } from '@app/components/FeaturePanel'
import { StatusMessage } from '@app/components/StatusMessage'

export const SearchPage = () => {
  const [query, setQuery] = useState('')
  const [submitted, setSubmitted] = useState(false)

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setSubmitted(true)
  }

  return (
    <div className="page-container">
      <FeaturePanel title="Search" lead="AND · OR · NOT · phrase · scope">
        <form className="form" onSubmit={handleSubmit}>
          <label className="form__field">
            <span>Search query</span>
            <input
              type="text"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder='"Important" AND (project OR deadline)'
            />
          </label>
          <button className="primary-button" type="submit">
            Run server search
          </button>
        </form>
        {submitted && (
          <StatusMessage
            variant="empty"
            title="Results ready"
            description="Server search combines provider capability and server index."
          />
        )}
      </FeaturePanel>
    </div>
  )
}
