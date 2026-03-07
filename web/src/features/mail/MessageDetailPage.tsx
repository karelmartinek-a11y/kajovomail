import { FeaturePanel } from '@app/components/FeaturePanel'

export const MessageDetailPage = () => (
  <div className="page-container">
    <FeaturePanel title="Detail zprávy" lead="Vlákna · příznaky · přesun · kopie">
      <article className="message-detail">
        <header>
          <p className="message-detail__subject">Aktualizace orchestrátoru serveru</p>
          <p className="message-detail__meta">od orchestration@hcasc.cz · vlákno #312</p>
        </header>
        <section>
          <p>
            Toto je zástupný text pro data vláken parsovaná z RFC hlaviček včetně příznaků,
            archivace a přesunu zpráv. Pro živou aktualizaci používejte event stream.
          </p>
        </section>
        <div className="message-detail__actions">
          <button type="button">Označit jako přečtené</button>
          <button type="button" className="secondary-button">
            Připnout příznak
          </button>
          <button type="button">Přesunout</button>
        </div>
      </article>
    </FeaturePanel>
  </div>
)
