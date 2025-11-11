import type { PropsWithChildren } from 'react'

export const AppLayout = ({ children }: PropsWithChildren): JSX.Element => (
  <div className="app-shell">
    <header className="app-header">
      <div className="brand">
        <span className="brand-mark">SE</span>
        <div>
          <p className="brand-title">Sports Events</p>
          <p className="brand-subtitle">Live calendar</p>
        </div>
      </div>
    </header>
    <main className="app-main">{children}</main>
  </div>
)

export default AppLayout
