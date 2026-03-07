import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react'

import { apiClient, unwrapApiError } from '@services/api'
import { startEventStream } from '@services/eventStream'

export type SessionStatus = 'loading' | 'authenticated' | 'anonymous'

export interface SessionUser {
  id: string
  email: string
  name: string
  roles: string[]
}

interface SessionContextValue {
  status: SessionStatus
  user?: SessionUser
  csrfToken?: string
  refresh: () => Promise<void>
  login: (payload: { email: string; password: string }) => Promise<void>
  logout: () => Promise<void>
}

const SessionContext = createContext<SessionContextValue | undefined>(undefined)
const LEGACY_TOKEN_KEY = 'kajovomail_legacy_session_token'
const LEGACY_USER_KEY = 'kajovomail_legacy_user_email'

type AuthMode = 'session' | 'legacy-auth'

const setCsrfHeader = (token?: string) => {
  if (token) {
    apiClient.defaults.headers['x-csrf-token'] = token
  } else {
    delete apiClient.defaults.headers['x-csrf-token']
  }
}

const setCorrelationHeader = (token?: string) => {
  if (token) {
    apiClient.defaults.headers['x-correlation-id'] = token
  } else {
    delete apiClient.defaults.headers['x-correlation-id']
  }
}

export const SessionProvider = ({ children }: { children: React.ReactNode }) => {
  const [status, setStatus] = useState<SessionStatus>('loading')
  const [user, setUser] = useState<SessionUser | undefined>()
  const [csrfToken, setCsrfToken] = useState<string | undefined>()
  const [authMode, setAuthMode] = useState<AuthMode>('session')

  const refresh = useCallback(async () => {
    setStatus('loading')
    try {
      const response = await apiClient.get('/session/current')
      const payload = response.data ?? {}
      setUser(payload.user)
      setCsrfToken(payload.csrfToken)
      setCsrfHeader(payload.csrfToken)
      setCorrelationHeader(undefined)
      localStorage.removeItem(LEGACY_TOKEN_KEY)
      localStorage.removeItem(LEGACY_USER_KEY)
      setAuthMode('session')
      setStatus(payload.user ? 'authenticated' : 'anonymous')
    } catch (error) {
      if ((error as { response?: { status?: number } })?.response?.status === 404) {
        const token = localStorage.getItem(LEGACY_TOKEN_KEY) || undefined
        const email = localStorage.getItem(LEGACY_USER_KEY) || undefined
        setAuthMode('legacy-auth')
        setCsrfToken(undefined)
        setCsrfHeader(undefined)
        setCorrelationHeader(token)
        if (token && email) {
          setUser({ id: 'legacy', email, name: email, roles: ['admin'] })
          setStatus('authenticated')
        } else {
          setUser(undefined)
          setStatus('anonymous')
        }
        return
      }
      console.warn('Session refresh failed', unwrapApiError(error))
      setUser(undefined)
      setCsrfToken(undefined)
      setCsrfHeader(undefined)
      setCorrelationHeader(undefined)
      setStatus('anonymous')
    }
  }, [])

  const login = useCallback(
    async (payload: { email: string; password: string }) => {
      try {
        if (authMode === 'legacy-auth') {
          const response = await apiClient.post('/auth/login', payload)
          const token = response.data?.session_token as string | undefined
          if (!token) {
            throw new Error('Server nevrátil token relace.')
          }
          localStorage.setItem(LEGACY_TOKEN_KEY, token)
          localStorage.setItem(LEGACY_USER_KEY, payload.email)
          setCorrelationHeader(token)
          setUser({ id: 'legacy', email: payload.email, name: payload.email, roles: ['admin'] })
          setCsrfToken(undefined)
          setCsrfHeader(undefined)
          setStatus('authenticated')
          return
        }
        const response = await apiClient.post('/session/login', payload)
        const data = response.data ?? {}
        setUser(data.user)
        setCsrfToken(data.csrfToken)
        setCsrfHeader(data.csrfToken)
        setStatus('authenticated')
      } catch (error) {
        if ((error as { response?: { status?: number } })?.response?.status === 404) {
          setAuthMode('legacy-auth')
          try {
            const response = await apiClient.post('/auth/login', payload)
            const token = response.data?.session_token as string | undefined
            if (!token) {
              throw new Error('Server nevrátil token relace.')
            }
            localStorage.setItem(LEGACY_TOKEN_KEY, token)
            localStorage.setItem(LEGACY_USER_KEY, payload.email)
            setCorrelationHeader(token)
            setUser({ id: 'legacy', email: payload.email, name: payload.email, roles: ['admin'] })
            setCsrfToken(undefined)
            setCsrfHeader(undefined)
            setStatus('authenticated')
            return
          } catch (fallbackError) {
            setStatus('anonymous')
            throw unwrapApiError(fallbackError)
          }
        }
        setStatus('anonymous')
        throw unwrapApiError(error)
      }
    },
    [authMode]
  )

  const logout = useCallback(
    async () => {
      try {
        if (authMode === 'legacy-auth') {
          await apiClient.post('/auth/logout')
        } else {
          await apiClient.post('/session/logout')
        }
      } finally {
        setUser(undefined)
        setCsrfToken(undefined)
        setCsrfHeader(undefined)
        setCorrelationHeader(undefined)
        localStorage.removeItem(LEGACY_TOKEN_KEY)
        localStorage.removeItem(LEGACY_USER_KEY)
        setStatus('anonymous')
      }
    },
    [authMode]
  )

  useEffect(() => {
    refresh()
    const stopStream = startEventStream(
      (payload) => {
        if (payload?.type === 'session.update') {
          refresh()
        }
      },
      (error) => {
        console.warn('Event stream error', error)
      }
    )
    return () => stopStream()
  }, [refresh])

  const value = useMemo(
    () => ({
      status,
      user,
      csrfToken,
      refresh,
      login,
      logout,
    }),
    [status, user, csrfToken, refresh, login, logout]
  )

  return <SessionContext.Provider value={value}>{children}</SessionContext.Provider>
}

export const useSession = () => {
  const context = useContext(SessionContext)
  if (!context) {
    throw new Error('useSession must be used within SessionProvider')
  }
  return context
}
