import { FeaturePanel } from '@app/components/FeaturePanel'

const drafts = [
  { id: 'draft-01', subject: 'Navazující nabídka', saved: 'před 2 min' },
  { id: 'draft-02', subject: 'Kontrola AI shrnutí', saved: 'před 7 min' },
]

export const DraftsPage = () => (
  <div className="page-container">
    <FeaturePanel title="Koncepty" lead="Automatické ukládání · verze · odpovědi">
      <ul className="drafts-list">
        {drafts.map((draft) => (
          <li key={draft.id} className="drafts-list__item">
            <p className="drafts-list__subject">{draft.subject}</p>
            <p className="drafts-list__meta">{draft.saved}</p>
            <button type="button">Otevřít</button>
          </li>
        ))}
      </ul>
    </FeaturePanel>
  </div>
)
