
import { FeaturePanel } from '@app/components/FeaturePanel'

const drafts = [
  { id: 'draft-01', subject: 'Follow-up offer', saved: '2m ago' },
  { id: 'draft-02', subject: 'AI summary review', saved: '7m ago' },
]

export const DraftsPage = () => (
  <div className="page-container">
    <FeaturePanel title="Drafts" lead="Autosave · versions · replies">
      <ul className="drafts-list">
        {drafts.map((draft) => (
          <li key={draft.id} className="drafts-list__item">
            <p className="drafts-list__subject">{draft.subject}</p>
            <p className="drafts-list__meta">{draft.saved}</p>
            <button type="button">Open</button>
          </li>
        ))}
      </ul>
    </FeaturePanel>
  </div>
)
