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
      <FeaturePanel title="Compose" lead="Drafts · Reply · Forward in multipart alternatives">
        <form className="form" onSubmit={handleSubmit}>
          <label className="form__field">
            <span>To</span>
            <input value={fields.to} onChange={handleChange('to')} placeholder="recipient@provider" required />
          </label>
          <label className="form__field">
            <span>Subject</span>
            <input value={fields.subject} onChange={handleChange('subject')} placeholder="Subject" required />
          </label>
          <label className="form__field">
            <span>Plain text</span>
            <textarea value={fields.body} onChange={handleChange('body')} rows={4} placeholder="Write the plain text..." />
          </label>
          <div className="form__helper">Multi-part order: text/plain · text/html (generated)</div>
          <div className="form__actions">
            <button className="primary-button" type="submit">
              Send
            </button>
            <button type="button" className="secondary-button">
              Save draft
            </button>
            <span className="form__autosave">{draftSaved ? 'Autosaved' : 'Draft pending'}</span>
          </div>
        </form>
        {submitted && (
          <StatusMessage
            variant="empty"
            title="Message queued"
            description="The backend will handle idempotent multipart dispatch."
          />
        )}
      </FeaturePanel>
    </div>
  )
}
