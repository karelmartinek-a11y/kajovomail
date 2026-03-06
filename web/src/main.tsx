import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

import { AppRoutes } from '@app/routes/AppRoutes'
import { SessionProvider } from '@app/providers/SessionProvider'
import { applyBrandTokens } from '@styles/brand'
import '@styles/global.css'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60,
      retry: (failureCount) => failureCount < 3,
    },
  },
})

applyBrandTokens()

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <SessionProvider>
        <QueryClientProvider client={queryClient}>
          <AppRoutes />
        </QueryClientProvider>
      </SessionProvider>
    </BrowserRouter>
  </React.StrictMode>
)
