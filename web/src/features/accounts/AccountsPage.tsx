
import { FeaturePanel } from '@app/components/FeaturePanel'
import { StatusMessage } from '@app/components/StatusMessage'

const accounts = [
  { provider: 'IMAP (Primary)', email: 'petr@hcasc.cz', capability: 'sync + search' },
  { provider: 'POP3 (Archive)', email: 'archiv@hcasc.cz', capability: 'download-only' },
]

export const AccountsPage = () => (
  <div className="page-container">
    <FeaturePanel title="Connected accounts" lead="Multiple providers per user">
      <div className="accounts-grid">
        {accounts.map((account) => (
          <article key={account.email} className="accounts-card">
            <p className="accounts-card__provider">{account.provider}</p>
            <p className="accounts-card__email">{account.email}</p>
            <p className="accounts-card__capability">{account.capability}</p>
            <div className="accounts-card__actions">
              <button type="button">Test connection</button>
              <button type="button" className="secondary-button">
                Manage credentials
              </button>
            </div>
          </article>
        ))}
      </div>
    </FeaturePanel>
    <FeaturePanel title="Capability discovery" lead="Backend registers IMAP/POP3 modes">
      <StatusMessage
        variant="offline"
        title="Waiting for capability data"
        description="Sync workers are warming up; the admin configuration will appear when ready."
      />
    </FeaturePanel>
  </div>
)
