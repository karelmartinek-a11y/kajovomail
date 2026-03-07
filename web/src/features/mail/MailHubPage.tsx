import { FeaturePanel } from '@app/components/FeaturePanel'
import { StatusMessage } from '@app/components/StatusMessage'

const folders = ['Doručená pošta', 'VIP', 'Koncepty', 'Odeslané', 'Archiv', 'Nabídky']
const messages = [
  { id: 'msg-01', subject: 'Přiložené čtvrtletní shrnutí', sender: 'finance@hcasc.cz', status: 'nepřečteno' },
  { id: 'msg-02', subject: 'Zápis z porady', sender: 'team@hcasc.cz', status: 'označeno' },
  { id: 'msg-03', subject: 'Aktualizace AI asistenta', sender: 'ai@hcasc.cz', status: 'přečteno' },
]

const virtualViews = [
  { label: 'Nepřečtené', count: 12 },
  { label: 'Označené', count: 3 },
  { label: 'S přílohami', count: 8 },
]

export const MailHubPage = () => (
  <div className="page-container">
    <FeaturePanel title="Složky a vlákna" lead="Výchozí i uživatelské složky">
      <div className="folders-grid">
        {folders.map((folder) => (
          <span key={folder} className="folders-chip">
            {folder}
          </span>
        ))}
      </div>
    </FeaturePanel>
    <FeaturePanel title="Náhled zpráv" lead="Seznam, příznaky, značky, vlákna">
      <ul className="message-list">
        {messages.map((message) => (
          <li key={message.id} className="message-list__item">
            <div>
              <p className="message-list__subject">{message.subject}</p>
              <p className="message-list__meta">{message.sender}</p>
            </div>
            <div className="message-list__status">
              <span>{message.status}</span>
            </div>
          </li>
        ))}
      </ul>
    </FeaturePanel>
    <FeaturePanel title="Virtuální pohledy" lead="Nepřečtené, označené, s přílohami">
      <div className="virtual-view-grid">
        {virtualViews.map((view) => (
          <article key={view.label} className="virtual-view">
            <p className="virtual-view__count">{view.count}</p>
            <p className="virtual-view__label">{view.label}</p>
          </article>
        ))}
      </div>
    </FeaturePanel>
    <FeaturePanel title="Stav synchronizace" lead="Inkrementální sync · retry · idempotence">
      <StatusMessage
        variant="loading"
        title="Synchronizační worker zarovnává schránku"
        description="Počáteční synchronizace běží napříč IMAP účty."
      />
    </FeaturePanel>
  </div>
)
