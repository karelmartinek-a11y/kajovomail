import { Navigate, Route, Routes } from 'react-router-dom'
import type { ReactElement } from 'react'

import { CoreLayout } from '@app/layout/CoreLayout'
import { StandaloneLayout } from '@app/layout/StandaloneLayout'
import { useSession } from '@app/providers/SessionProvider'
import { LoginPage } from '@features/auth/LoginPage'
import { AccountsPage } from '@features/accounts/AccountsPage'
import { ComposePage } from '@features/mail/ComposePage'
import { DraftsPage } from '@features/mail/DraftsPage'
import { MailHubPage } from '@features/mail/MailHubPage'
import { MessageDetailPage } from '@features/mail/MessageDetailPage'
import { SearchPage } from '@features/search/SearchPage'
import { AIPanelPage } from '@features/ai/AIPanelPage'
import { OffersPage } from '@features/offers/OffersPage'
import { SettingsPage } from '@features/settings/SettingsPage'

const RequireAuthenticated = ({ children }: { children: ReactElement }) => {
  const { status } = useSession()
  if (status === 'loading') {
    return null
  }
  if (status !== 'authenticated') {
    return <Navigate to="/login" replace />
  }
  return children
}

const RequireAnonymous = ({ children }: { children: ReactElement }) => {
  const { status } = useSession()
  if (status === 'loading') {
    return null
  }
  if (status === 'authenticated') {
    return <Navigate to="/" replace />
  }
  return children
}

export const AppRoutes = () => (
  <Routes>
    <Route
      path="/login"
      element={
        <RequireAnonymous>
          <StandaloneLayout>
            <LoginPage />
          </StandaloneLayout>
        </RequireAnonymous>
      }
    />
    <Route
      path="/"
      element={
        <RequireAuthenticated>
          <CoreLayout />
        </RequireAuthenticated>
      }
    >
      <Route index element={<MailHubPage />} />
      <Route path="accounts" element={<AccountsPage />} />
      <Route path="compose" element={<ComposePage />} />
      <Route path="drafts" element={<DraftsPage />} />
      <Route path="search" element={<SearchPage />} />
      <Route path="ai" element={<AIPanelPage />} />
      <Route path="offers" element={<OffersPage />} />
      <Route path="settings" element={<SettingsPage />} />
      <Route path="messages/:messageId" element={<MessageDetailPage />} />
    </Route>
    <Route path="*" element={<Navigate to="/" replace />} />
  </Routes>
)
