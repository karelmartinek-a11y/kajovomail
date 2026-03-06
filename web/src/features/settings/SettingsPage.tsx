
import { FeaturePanel } from '@app/components/FeaturePanel'
import { StatusMessage } from '@app/components/StatusMessage'

export const SettingsPage = () => (
  <div className="page-container">
    <FeaturePanel title="Security & sessions" lead="Role, password, reset, logout-all">
      <div className="settings-grid">
        <div className="settings-card">
          <p className="settings-card__title">Sessions</p>
          <button type="button" className="secondary-button">
            Logout from all devices
          </button>
        </div>
        <div className="settings-card">
          <p className="settings-card__title">Password</p>
          <button type="button">Change password</button>
        </div>
        <div className="settings-card">
          <p className="settings-card__title">Roles</p>
          <p className="settings-card__meta">User · Admin · Auditor</p>
        </div>
      </div>
    </FeaturePanel>
    <FeaturePanel title="Audit" lead="Log sensitive transitions without secrets">
      <StatusMessage
        variant="offline"
        title="Audit stream pending"
        description="Changes are recorded without exposing credentials." 
      />
    </FeaturePanel>
  </div>
)
