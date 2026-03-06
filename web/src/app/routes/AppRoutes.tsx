import { Navigate, Route, Routes } from 'react-router-dom'

import { CoreLayout } from '@app/layout/CoreLayout'
import { StandaloneLayout } from '@app/layout/StandaloneLayout'
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

export const AppRoutes = () => (
  <Routes>
    <Route
      path="/login"
      element={
        <StandaloneLayout>
          <LoginPage />
        </StandaloneLayout>
      }
    />
    <Route path="/" element={<CoreLayout />}>
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
