import axios, { AxiosError } from 'axios'

const API_BASE = 'https://mail.hcasc.cz/api/v1'

export const apiClient = axios.create({
  baseURL: API_BASE,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
})

export type ApiError = {
  code?: string
  message: string
  details?: Record<string, unknown>
}

const mapStatusToCzech = (status?: number): string | undefined => {
  if (!status) return undefined
  if (status === 400) return 'Požadavek není platný.'
  if (status === 401) return 'Neplatné přihlašovací údaje.'
  if (status === 403) return 'Nemáte oprávnění k této akci.'
  if (status === 404) return 'Požadovaný endpoint na serveru nebyl nalezen.'
  if (status >= 500) return 'Na serveru došlo k chybě. Zkuste to prosím znovu.'
  return undefined
}

const translateMessage = (message?: string): string | undefined => {
  if (!message) return undefined
  const lower = message.toLowerCase()
  if (lower.includes('request failed with status code 404')) return 'Požadovaný endpoint na serveru nebyl nalezen.'
  if (lower.includes('request failed with status code 401')) return 'Neplatné přihlašovací údaje.'
  if (lower.includes('network error')) return 'Nepodařilo se spojit se serverem.'
  if (lower.includes('invalid credentials')) return 'Neplatné přihlašovací údaje.'
  if (lower.includes('missing x-correlation-id')) return 'Chybí identifikátor relace. Přihlaste se znovu.'
  return message
}

export const unwrapApiError = (error: unknown): ApiError => {
  if (error instanceof AxiosError && error.response) {
    const status = error.response.status
    const rawMessage =
      error.response.data?.message || error.response.data?.detail || error.message
    return {
      code: error.response.data?.code,
      message: mapStatusToCzech(status) || translateMessage(rawMessage) || 'Nastala chyba požadavku.',
      details: error.response.data?.details,
    }
  }

  const message = (error as Error).message
  return { message: translateMessage(message) || 'Nastala neočekávaná chyba.' }
}

export type AISettings = {
  has_openai_api_key: boolean
  openai_api_key_masked?: string | null
  response_style: 'concise' | 'balanced' | 'detailed'
  model?: string | null
}

export type AIKeyTestResult = {
  valid: boolean
  message: string
  models: string[]
}

export const getAISettings = async () => {
  const response = await apiClient.get<AISettings>('/settings/ai')
  return response.data
}

export const updateAISettings = async (payload: {
  openai_api_key?: string
  response_style?: string
  model?: string
}) => {
  const response = await apiClient.put<AISettings>('/settings/ai', payload)
  return response.data
}

export const testOpenAIKey = async (openai_api_key?: string) => {
  const response = await apiClient.post<AIKeyTestResult>('/settings/ai/test-key', { openai_api_key })
  return response.data
}

export const listOpenAIModels = async () => {
  const response = await apiClient.get<{ models: string[] }>('/settings/ai/models')
  return response.data.models
}
