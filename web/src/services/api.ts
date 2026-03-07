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

export const unwrapApiError = (error: unknown): ApiError => {
  if (error instanceof AxiosError && error.response) {
    return {
      code: error.response.data?.code,
      message: error.response.data?.message || error.message,
      details: error.response.data?.details,
    }
  }

  return { message: (error as Error).message }
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
