import React, { useCallback, useEffect, useMemo, useState } from 'react'

import { FeaturePanel } from '@app/components/FeaturePanel'
import { StatusMessage } from '@app/components/StatusMessage'
import {
  createAccount,
  listAccounts,
  testAccountConnection,
  unwrapApiError,
} from '@services/api'
import type { AccountRead, AccountCreatePayload } from '@services/api'

const PROVIDER_OPTIONS = [
  { label: 'IMAP', value: 'imap' },
  { label: 'POP3', value: 'pop3' },
]

const PROTOCOL_OPTIONS = [
  { label: 'IMAP', value: 'imap' },
  { label: 'POP3', value: 'pop3' },
]

const EMPTY_FORM = {
  provider: 'imap',
  email: '',
  server: '',
  display_name: '',
  protocol: 'imap',
}

export const AccountsPage = () => {
  const [accounts, setAccounts] = useState<AccountRead[]>([])
  const [form, setForm] = useState(EMPTY_FORM)
  const [loading, setLoading] = useState(true)
  const [status, setStatus] = useState('Načítám připojené účty…')
  const [saving, setSaving] = useState(false)
  const [testLoadingId, setTestLoadingId] = useState<number | null>(null)
  const [testStatus, setTestStatus] = useState<Record<number, string>>({})

  const refreshAccounts = useCallback(async () => {
    setLoading(true)
    try {
      const loaded = await listAccounts()
      setAccounts(loaded)
      setStatus(loaded.length ? `Načteno ${loaded.length} účtů.` : 'Žádné připojené účty.')
    } catch (error) {
      setStatus(unwrapApiError(error).message)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    refreshAccounts()
  }, [refreshAccounts])

  const handleChange = (field: keyof typeof EMPTY_FORM) => (event: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setForm((prev) => ({ ...prev, [field]: event.target.value }))
  }

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (!form.email.trim() || !form.server.trim()) {
      setStatus('Vyplňte e-mail a server.')
      return
    }
    setSaving(true)
    setStatus('Ukládám účet…')
    const payload: AccountCreatePayload = {
      provider: form.provider,
      email: form.email.trim(),
      credentials: {
        server: form.server.trim(),
        protocol: form.protocol,
        display_name: form.display_name.trim() || undefined,
      },
      capability_flags: [],
    }
    try {
      await createAccount(payload)
      setForm(EMPTY_FORM)
      setStatus('Účet uložen, načítám seznam.')
      await refreshAccounts()
    } catch (error) {
      setStatus(unwrapApiError(error).message)
    } finally {
      setSaving(false)
    }
  }

  const handleTestConnection = async (account: AccountRead) => {
    setTestStatus((prev) => ({ ...prev, [account.id]: 'Testuji spojení…' }))
    setTestLoadingId(account.id)
    try {
      const ok = await testAccountConnection(account.id)
      setTestStatus((prev) => ({
        ...prev,
        [account.id]: ok ? 'Spojení funguje.' : 'Spojení selhalo.',
      }))
    } catch (error) {
      setTestStatus((prev) => ({ ...prev, [account.id]: unwrapApiError(error).message }))
    } finally {
      setTestLoadingId(null)
    }
  }

  const accountsContent = useMemo(() => {
    if (loading) {
      return <StatusMessage variant="loading" title="Aktualizuji seznam" description="Kontaktují se služby účtů." />
    }
    if (!accounts.length) {
      return <StatusMessage variant="empty" title="Žádné účty" description="Přidejte první poskytovatele." />
    }
    return (
      <ul className="accounts-list">
        {accounts.map((account) => (
          <li key={account.id} className="accounts-card">
            <div>
              <p className="accounts-card__provider">{account.provider.toUpperCase()}</p>
              <p className="accounts-card__email">{account.email}</p>
              <p className="accounts-card__capability">
                {account.display_name ?? 'Nezadané jméno'} · {account.capability_flags.join(', ') || 'základní'}
              </p>
            </div>
            <div className="accounts-card__actions">
              <button
                type="button"
                className="secondary-button"
                onClick={() => handleTestConnection(account)}
                disabled={testLoadingId === account.id}
              >
                {testLoadingId === account.id ? 'Testuji…' : 'Otestovat připojení'}
              </button>
              <p className="accounts-card__status">{testStatus[account.id]}</p>
            </div>
          </li>
        ))}
      </ul>
    )
  }, [accounts, loading, handleTestConnection, testLoadingId, testStatus])

  return (
    <div className="page-container">
      <FeaturePanel title="Připojené účty" lead="Více poskytovatelů na jednu relaci">
        {accountsContent}
        <StatusMessage variant="empty" title="Stav" description={status} />
      </FeaturePanel>
      <FeaturePanel title="Přidat účet" lead="Zadejte poskytovatele, server a přihlašovací údaje">
        <form className="form" onSubmit={handleSubmit}>
          <label className="form__field">
            <span>Provider</span>
            <select value={form.provider} onChange={handleChange('provider')}>
              {PROVIDER_OPTIONS.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </label>
          <label className="form__field">
            <span>E-mail</span>
            <input type="email" value={form.email} onChange={handleChange('email')} required />
          </label>
          <label className="form__field">
            <span>Server</span>
            <input type="text" value={form.server} onChange={handleChange('server')} required />
          </label>
          <label className="form__field">
            <span>Výchozí jméno</span>
            <input type="text" value={form.display_name} onChange={handleChange('display_name')} />
          </label>
          <label className="form__field">
            <span>Protocol</span>
            <select value={form.protocol} onChange={handleChange('protocol')}>
              {PROTOCOL_OPTIONS.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          </label>
          <button type="submit" className="primary-button" disabled={saving}>
            {saving ? 'Ukládám…' : 'Přidat účet'}
          </button>
        </form>
      </FeaturePanel>
    </div>
  )
}
