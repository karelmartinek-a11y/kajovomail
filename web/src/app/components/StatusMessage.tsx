import clsx from 'clsx'

export type StatusMessageVariant = 'loading' | 'empty' | 'error' | 'offline'

const icons: Record<StatusMessageVariant, string> = {
  loading: '?',
  empty: '??',
  error: '??',
  offline: '??',
}

interface StatusMessageProps {
  title: string
  description?: string
  variant?: StatusMessageVariant
}

export const StatusMessage = ({
  title,
  description,
  variant = 'loading',
}: StatusMessageProps) => (
  <article className={clsx('status-message', `status-message--${variant}`)}>
    <p className="status-message__icon" aria-hidden>
      {icons[variant]}
    </p>
    <div>
      <p className="status-message__title">{title}</p>
      {description && <p className="status-message__description">{description}</p>}
    </div>
  </article>
)
