
import { FeaturePanel } from '@app/components/FeaturePanel'
import { StatusMessage } from '@app/components/StatusMessage'

const folders = ['Inbox', 'VIP', 'Drafts', 'Sent', 'Archive', 'Offers']
const messages = [
  { id: 'msg-01', subject: 'Quarterly recap attached', sender: 'finance@hcasc.cz', status: 'unread' },
  { id: 'msg-02', subject: 'Meeting minutes', sender: 'team@hcasc.cz', status: 'flagged' },
  { id: 'msg-03', subject: 'AI assistant update', sender: 'ai@hcasc.cz', status: 'seen' },
]

const virtualViews = [
  { label: 'Unread', count: 12 },
  { label: 'Flagged', count: 3 },
  { label: 'With attachments', count: 8 },
]

export const MailHubPage = () => (
  <div className="page-container">
    <FeaturePanel title="Folders & threads" lead="Default and user folders" >
      <div className="folders-grid">
        {folders.map((folder) => (
          <span key={folder} className="folders-chip">
            {folder}
          </span>
        ))}
      </div>
    </FeaturePanel>
    <FeaturePanel title="Message preview" lead="List, flags, marks, threading">
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
    <FeaturePanel title="Virtual views" lead="Unread, flagged, attachments">
      <div className="virtual-view-grid">
        {virtualViews.map((view) => (
          <article key={view.label} className="virtual-view">
            <p className="virtual-view__count">{view.count}</p>
            <p className="virtual-view__label">{view.label}</p>
          </article>
        ))}
      </div>
    </FeaturePanel>
    <FeaturePanel title="Sync status" lead="Incremental sync · retry · idempotence">
      <StatusMessage
        variant="loading"
        title="Sync worker aligning mailbox"
        description="Initial sync in progress across IMAP accounts."
      />
    </FeaturePanel>
  </div>
)
