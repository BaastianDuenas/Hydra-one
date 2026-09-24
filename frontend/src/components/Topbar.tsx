import { User } from 'lucide-react'

function Topbar() {
  return (
    <header className="topbar">
      <div>
        <span className="topbar-title">Panel de administración</span>
      </div>

      <div className="topbar-user">
        <div className="user-icon">
          <User size={18} />
        </div>

        <div>
          <strong>Administrador</strong>
          <span>Hydra One</span>
        </div>
      </div>
    </header>
  )
}

export default Topbar