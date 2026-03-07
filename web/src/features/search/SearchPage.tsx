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
      <FeaturePanel title="Hledání" lead="AND · OR · NOT · fráze · rozsah">
        <form className="form" onSubmit={handleSubmit}>
          <label className="form__field">
            <span>Vyhledávací dotaz</span>
            <input
              type="text"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder='"Důležité" AND (projekt OR termín)'
            />
          </label>
          <button className="primary-button" type="submit">
            Spustit serverové hledání
          </button>
        </form>
        {submitted && (
          <StatusMessage
            variant="empty"
            title="Výsledky připraveny"
            description="Serverové hledání kombinuje schopnosti poskytovatele a serverový index."
          />
        )}
      </FeaturePanel>
    </div>
  )
}
