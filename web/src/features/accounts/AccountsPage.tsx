import { FeaturePanel } from '@app/components/FeaturePanel'
import { StatusMessage } from '@app/components/StatusMessage'

const accounts = [
  { provider: 'IMAP (primární)', email: 'petr@hcasc.cz', capability: 'synchronizace + hledání' },
  { provider: 'POP3 (archiv)', email: 'archiv@hcasc.cz', capability: 'pouze stahování' },
]

export const AccountsPage = () => (
  <div className="page-container">
    <FeaturePanel title="Připojené účty" lead="Více poskytovatelů na jednoho uživatele">
      <div className="accounts-grid">
        {accounts.map((account) => (
          <article key={account.email} className="accounts-card">
            <p className="accounts-card__provider">{account.provider}</p>
            <p className="accounts-card__email">{account.email}</p>
            <p className="accounts-card__capability">{account.capability}</p>
            <div className="accounts-card__actions">
              <button type="button">Otestovat připojení</button>
              <button type="button" className="secondary-button">
                Spravovat přihlašovací údaje
              </button>
            </div>
          </article>
        ))}
      </div>
    </FeaturePanel>
    <FeaturePanel title="Detekce schopností" lead="Backend registruje režimy IMAP/POP3">
      <StatusMessage
        variant="offline"
        title="Čekám na data schopností"
        description="Synchronizační workery se inicializují, konfigurace se zobrazí po dokončení." 
      />
    </FeaturePanel>
  </div>
)
