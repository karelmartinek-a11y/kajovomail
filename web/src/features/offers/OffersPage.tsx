import { FeaturePanel } from '@app/components/FeaturePanel'

const offers = [
  { thread: '#421', title: 'Nabídka automatizačního balíčku', state: 'koncept' },
  { thread: '#387', title: 'Upgrade na premium', state: 'odesláno' },
]

export const OffersPage = () => (
  <div className="page-container">
    <FeaturePanel title="Nabídky" lead="Povinná pole · navázání na vlákno · audit">
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
