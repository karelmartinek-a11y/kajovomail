
import { FeaturePanel } from '@app/components/FeaturePanel'

const offers = [
  { thread: '#421', title: 'Offer for automation suite', state: 'draft' },
  { thread: '#387', title: 'Upgrade to premium', state: 'sent' },
]

export const OffersPage = () => (
  <div className="page-container">
    <FeaturePanel title="Nabídky" lead="Mandatory fields · thread linkage · audit">
      <ul className="offers-list">
        {offers.map((offer) => (
          <li key={offer.thread} className="offers-list__item">
            <div>
              <p className="offers-list__thread">{offer.thread}</p>
              <p className="offers-list__title">{offer.title}</p>
            </div>
            <p className="offers-list__state">{offer.state}</p>
          </li>
        ))}
      </ul>
    </FeaturePanel>
  </div>
)
