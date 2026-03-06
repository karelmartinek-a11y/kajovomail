import axios, { AxiosError } from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE_URL ?? '/api/v1'

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
