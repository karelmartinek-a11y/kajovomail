import React, { useState } from 'react'

import { FeaturePanel } from '@app/components/FeaturePanel'
import { StatusMessage } from '@app/components/StatusMessage'
import type { ApiError } from '@services/api'
import { useSession } from '@app/providers/SessionProvider'

type LoginForm = {
  email: string
  password: string
  remember: boolean
}

export const LoginPage = () => {
  const { status, login } = useSession()
  const [form, setForm] = useState<LoginForm>({
    email: '',
    password: '',
    remember: true,
  })
  const [error, setError] = useState<ApiError | null>(null)
  const [pending, setPending] = useState(false)

  const hasErrors = form.email.trim() === '' || form.password.trim() === ''

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    setError(null)
    if (hasErrors) {
      setError({ message: 'E-mail i heslo jsou povinné.' })
      return
    }

    setPending(true)
    try {
      await login({ email: form.email, password: form.password })
    } catch (err) {
      setError(err as ApiError)
    } finally {
      setPending(false)
    }
  }

  return (
    <div className="page-container">
      <FeaturePanel title="Bezpečné přihlášení" lead="Serverem řízené relace s HttpOnly cookies">
        <form className="form" onSubmit={handleSubmit}>
          <label className="form__field">
            <span>E-mail</span>
            <input
              type="email"
              name="email"
              value={form.email}
              onChange={(event) => setForm({ ...form, email: event.target.value })}
              required
              autoComplete="username"
            />
          </label>
          <label className="form__field">
            <span>Heslo</span>
            <input
              type="password"
              name="password"
              value={form.password}
              onChange={(event) => setForm({ ...form, password: event.target.value })}
              required
              minLength={8}
              autoComplete="current-password"
            />
          </label>
          <label className="form__field form__field--checkbox">
            <input
              type="checkbox"
              checked={form.remember}
              onChange={(event) => setForm({ ...form, remember: event.target.checked })}
            />
            <span>Zůstat přihlášen</span>
          </label>
          <button type="submit" className="primary-button" disabled={pending}>
            {pending ? 'Přihlašuji…' : 'Přihlásit'}
          </button>
        </form>
        {status === 'loading' && (
          <StatusMessage variant="loading" title="Kontrola relace" description="Načítám CSRF token ze serveru." />
        )}
        {status === 'authenticated' && (
          <StatusMessage variant="empty" title="Relace připravena" description="HttpOnly cookie relace je aktivní." />
        )}
        {error && <StatusMessage variant="error" title="Problém s přihlášením" description={error.message} />}
      </FeaturePanel>
    </div>
  )
}
