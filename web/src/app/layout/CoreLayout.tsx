import { NavLink, Outlet } from 'react-router-dom'
import clsx from 'clsx'

import brandMeta from '@brand/brand/brand.json'
import signace from '@brand/signace/signace.svg?url'
import mark from '@brand/logo/exports/mark/svg/kajovo-mail_mark.svg?url'

import { useViewport } from '@hooks/useViewport'
import { useSession } from '@app/providers/SessionProvider'

const navItems = [
  { to: '/', label: 'Pošta', helper: 'Složky · Vlákna · Virtuální pohledy' },
  { to: '/accounts', label: 'Účty', helper: 'Poskytovatelé · Schopnosti' },
  { to: '/compose', label: 'Napsat', helper: 'Koncepty · Odeslání · Šablony' },
  { to: '/drafts', label: 'Koncepty', helper: 'Automatické ukládání · Verze' },
  { to: '/search', label: 'Hledání', helper: 'Globální · Poskytovatelé' },
  { to: '/ai', label: 'AI panel', helper: 'Odpovědi · Náhledy' },
  { to: '/offers', label: 'Nabídky', helper: 'Vlákna · Audit' },
  { to: '/settings', label: 'Nastavení', helper: 'Bezpečnost a relace' },
]

export const CoreLayout = () => {
  const { isDesktop } = useViewport()
  const { status, user, logout } = useSession()

  const sessionLabel =
    status === 'authenticated'
      ? `Přihlášen: ${user?.email ?? 'neznámý uživatel'}`
      : status === 'loading'
      ? 'Synchronizuji relaci'
      : 'Nepřihlášený přístup'

  const handleLogout = () => {
    logout()
  }

  return (
    <div className="core-layout">
      <header className="core-layout__header">
        <div className="brand-mark">
          <div className="brand-compact" aria-label={`${brandMeta.appName} značka`}>
            <img src={signace} alt={`${brandMeta.appName} signace`} className="brand-compact__signace" />
            <img src={mark} alt={`${brandMeta.appName} mark`} className="brand-compact__mark" />
          </div>
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
            Bezpečné odhlášení
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
