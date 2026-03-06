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

const setCsrfHeader = (token?: string) => {
  if (token) {
    apiClient.defaults.headers['x-csrf-token'] = token
  } else {
    delete apiClient.defaults.headers['x-csrf-token']
  }
}

export const SessionProvider = ({ children }: { children: React.ReactNode }) => {
  const [status, setStatus] = useState<SessionStatus>('loading')
  const [user, setUser] = useState<SessionUser | undefined>()
  const [csrfToken, setCsrfToken] = useState<string | undefined>()

  const refresh = useCallback(async () => {
    setStatus('loading')
    try {
      const response = await apiClient.get('/session/current')
      const payload = response.data ?? {}
      setUser(payload.user)
      setCsrfToken(payload.csrfToken)
      setCsrfHeader(payload.csrfToken)
      setStatus(payload.user ? 'authenticated' : 'anonymous')
    } catch (error) {
      console.warn('Session refresh failed', unwrapApiError(error))
      setUser(undefined)
      setCsrfToken(undefined)
      setCsrfHeader(undefined)
      setStatus('anonymous')
    }
  }, [])

  const login = useCallback(async (payload: { email: string; password: string }) => {
    try {
      const response = await apiClient.post('/session/login', payload)
      const data = response.data ?? {}
      setUser(data.user)
      setCsrfToken(data.csrfToken)
      setCsrfHeader(data.csrfToken)
      setStatus('authenticated')
    } catch (error) {
      setStatus('anonymous')
      throw unwrapApiError(error)
    }
  }, [])

  const logout = useCallback(async () => {
    try {
      await apiClient.post('/session/logout')
    } finally {
      setUser(undefined)
      setCsrfToken(undefined)
      setCsrfHeader(undefined)
      setStatus('anonymous')
    }
  }, [])

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
