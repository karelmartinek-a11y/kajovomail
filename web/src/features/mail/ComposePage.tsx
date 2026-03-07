import React, { useState } from 'react'

import { FeaturePanel } from '@app/components/FeaturePanel'
import { StatusMessage } from '@app/components/StatusMessage'

export const ComposePage = () => {
  const [fields, setFields] = useState({ to: '', subject: '', body: '' })
  const [draftSaved, setDraftSaved] = useState(true)
  const [submitted, setSubmitted] = useState(false)

  const handleChange = (key: keyof typeof fields) => (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFields((previous) => ({ ...previous, [key]: event.target.value }))
    setDraftSaved(false)
  }

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setDraftSaved(true)
    setSubmitted(true)
  }

  return (
    <div className="page-container">
      <FeaturePanel title="Napsat zprávu" lead="Koncepty · Odpověď · Přeposlání v multipart variantách">
        <form className="form" onSubmit={handleSubmit}>
          <label className="form__field">
            <span>Komu</span>
            <input value={fields.to} onChange={handleChange('to')} placeholder="prijemce@poskytovatel" required />
          </label>
          <label className="form__field">
            <span>Předmět</span>
            <input value={fields.subject} onChange={handleChange('subject')} placeholder="Předmět" required />
          </label>
          <label className="form__field">
            <span>Prostý text</span>
            <textarea value={fields.body} onChange={handleChange('body')} rows={4} placeholder="Napište text zprávy..." />
          </label>
          <div className="form__helper">Pořadí multipart: text/plain · text/html (generováno)</div>
          <div className="form__actions">
            <button className="primary-button" type="submit">
              Odeslat
            </button>
            <button type="button" className="secondary-button">
              Uložit koncept
            </button>
            <span className="form__autosave">{draftSaved ? 'Uloženo automaticky' : 'Koncept čeká na uložení'}</span>
          </div>
        </form>
        {submitted && (
          <StatusMessage
            variant="empty"
            title="Zpráva zařazena do fronty"
            description="Backend zajistí idempotentní multipart doručení."
          />
        )}
      </FeaturePanel>
    </div>
  )
}
