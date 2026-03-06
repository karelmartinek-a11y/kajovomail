import { NavLink, Outlet } from 'react-router-dom'
import clsx from 'clsx'

import brandMeta from '@brand/brand/brand.json'
import signace from '@brand/signace/signace.svg?url'

import { useViewport } from '@hooks/useViewport'
import { useSession } from '@app/providers/SessionProvider'

const navItems = [
  { to: '/', label: 'Mailbox', helper: 'Folders · Threads · Virtual views' },
  { to: '/accounts', label: 'Accounts', helper: 'Providers · Capabilities' },
  { to: '/compose', label: 'Compose', helper: 'Drafts · Send · Templates' },
  { to: '/drafts', label: 'Drafts', helper: 'Autosave · Versions' },
  { to: '/search', label: 'Search', helper: 'Global · Providers' },
  { to: '/ai', label: 'AI Console', helper: 'Responses · Previews' },
  { to: '/offers', label: 'Offers', helper: 'Threads · Audit' },
  { to: '/settings', label: 'Settings', helper: 'Security & Sessions' },
]

export const CoreLayout = () => {
  const { isDesktop } = useViewport()
  const { status, user, logout } = useSession()

  const sessionLabel =
    status === 'authenticated'
      ? `Signed in as ${user?.email ?? 'unknown user'}`
      : status === 'loading'
      ? 'Syncing session'
      : 'Guest access'

  const handleLogout = () => {
    logout()
  }

  return (
    <div className="core-layout">
      <header className="core-layout__header">
        <div className="brand-mark">
          <img src={signace} alt={`${brandMeta.appName} signace`} className="brand-mark__image" />
          <div>
            <p className="brand-mark__name">{brandMeta.appName}</p>
            <p className="brand-mark__tagline">mail.hcasc.cz</p>
          </div>
        </div>
        <div className="core-layout__status">
          <p className="core-layout__status-label">{sessionLabel}</p>
          <button
            className="core-layout__status-action"
            type="button"
            onClick={handleLogout}
            disabled={status === 'loading'}
          >
            Secure logout
          </button>
        </div>
      </header>
      <div className="core-layout__shell">
        <nav
          className={clsx('core-layout__nav', {
            'core-layout__nav--collapsed': !isDesktop,
          })}
        >
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                clsx('core-layout__nav-item', {
                  'core-layout__nav-item--active': isActive,
                })
              }
              aria-label={item.label}
            >
              <span className="core-layout__nav-label">{item.label}</span>
              <span className="core-layout__nav-helper">{item.helper}</span>
            </NavLink>
          ))}
        </nav>
        <main className="core-layout__content">
          <Outlet />
        </main>
      </div>
    </div>
  )
}
