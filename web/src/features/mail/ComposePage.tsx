import React, { useEffect, useMemo, useState } from 'react'

import { FeaturePanel } from '@app/components/FeaturePanel'
import { StatusMessage } from '@app/components/StatusMessage'
import { useSession } from '@app/providers/SessionProvider'
import { listAccounts, saveDraft, unwrapApiError } from '@services/api'
import type { AccountRead } from '@services/api'

const INITIAL_FIELDS = {
  to: '',
  subject: '',
  body: '',
}

export const ComposePage = () => {
  const { user } = useSession()
  const [accounts, setAccounts] = useState<AccountRead[]>([])
  const [selectedAccount, setSelectedAccount] = useState<number | null>(null)
  const [fields, setFields] = useState(INITIAL_FIELDS)
  const [status, setStatus] = useState('Načítám účty…')
  const [saving, setSaving] = useState(false)

  const loadAccounts = async () => {
    try {
      const loaded = await listAccounts()
      setAccounts(loaded)
      setSelectedAccount((prev) => prev ?? loaded[0]?.id ?? null)
      setStatus(loaded.length ? 'Účty připravené k výběru.' : 'Přidejte nejprve účet.')
    } catch (error) {
      setStatus(unwrapApiError(error).message)
    }
  }

  useEffect(() => {
    loadAccounts()
  }, [])

  const handleChange = (key: keyof typeof fields) => (
    event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    setFields((prev) => ({ ...prev, [key]: event.target.value }))
  }

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (!selectedAccount) {
      setStatus('Vyberte účet, ke kterému ukládáte koncept.')
      return
    }
    if (!user) {
      setStatus('Uživatel není přihlášen.')
      return
    }
    setSaving(true)
    setStatus('Ukládám koncept…')
    try {
      await saveDraft({
        user_id: Number(user.id),
        account_id: selectedAccount,
        plaintext: fields.body,
        html: fields.body,
      })
      setFields(INITIAL_FIELDS)
      setStatus('Koncept uložen. Backend jej synchronizuje.')
    } catch (error) {
      setStatus(unwrapApiError(error).message)
    } finally {
      setSaving(false)
    }
  }

  const accountOptions = useMemo(() => accounts, [accounts])

  return (
    <div className="page-container">
      <FeaturePanel title="Napsat zprávu" lead="Koncepty · Odpověď · Synchronizovaný draft">
        <form className="form" onSubmit={handleSubmit}>
          <label className="form__field">
            <span>Účet</span>
            <select
              value={selectedAccount ?? ''}
              onChange={(event) => setSelectedAccount(event.target.value ? Number(event.target.value) : null)}
            >
              <option value="" disabled>
                Vyberte účet
              </option>
              {accountOptions.map((account) => (
                <option key={account.id} value={account.id}>
                  {account.email} · {account.provider.toUpperCase()}
                </option>
              ))}
            </select>
          </label>
          <label className="form__field">
            <span>Komu</span>
            <input value={fields.to} onChange={handleChange('to')} placeholder="příjemce@email.cz" required />
          </label>
          <label className="form__field">
            <span>Předmět</span>
            <input value={fields.subject} onChange={handleChange('subject')} placeholder="Předmět" required />
          </label>
          <label className="form__field">
            <span>Text</span>
            <textarea
              value={fields.body}
              onChange={handleChange('body')}
              rows={4}
              placeholder="Napište text zprávy…"
            />
          </label>
          <div className="form__actions">
            <button className="primary-button" type="submit" disabled={saving}>
              {saving ? 'Ukládám…' : 'Uložit koncept'}
            </button>
          </div>
        </form>
        <StatusMessage variant="empty" title="Stav konceptu" description={status} />
      </FeaturePanel>
    </div>
  )
}
