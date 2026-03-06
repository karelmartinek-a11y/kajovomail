
import { FeaturePanel } from '@app/components/FeaturePanel'

export const MessageDetailPage = () => (
  <div className="page-container">
    <FeaturePanel title="Message detail" lead="Threading · flags · move · copy">
      <article className="message-detail">
        <header>
          <p className="message-detail__subject">Server orchestration update</p>
          <p className="message-detail__meta">from orchestration@hcasc.cz · thread #312</p>
        </header>
        <section>
          <p>
            This is a placeholder for threading data parsed from RFC headers, showing flag, archive, and move
            operations. Use the event stream to refresh status on the fly.
          </p>
        </section>
        <div className="message-detail__actions">
          <button type="button">Mark read</button>
          <button type="button" className="secondary-button">
            Flag
          </button>
          <button type="button">Move</button>
        </div>
      </article>
    </FeaturePanel>
  </div>
)
