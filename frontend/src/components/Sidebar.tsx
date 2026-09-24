import { NavLink } from 'react-router-dom'
import {
  LayoutDashboard,
  Truck,
  Wrench,
  Package,
  Bell,
} from 'lucide-react'

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <h1>HYDRA ONE</h1>
        <span>Gestión operacional</span>
      </div>

      <nav>
        <ul>
          <li>
            <NavLink
              to="/"
              end
              className={({ isActive }) =>
                isActive ? 'nav-link active' : 'nav-link'
              }
            >
              <LayoutDashboard size={18} />
              <span>Dashboard</span>
            </NavLink>
          </li>

          <li>
            <NavLink
              to="/activos"
              className={({ isActive }) =>
                isActive ? 'nav-link active' : 'nav-link'
              }
            >
              <Truck size={18} />
              <span>Activos</span>
            </NavLink>
          </li>

          <li>
            <NavLink
              to="/mantenciones"
              className={({ isActive }) =>
                isActive ? 'nav-link active' : 'nav-link'
              }
            >
              <Wrench size={18} />
              <span>Mantenciones</span>
            </NavLink>
          </li>

          <li>
            <NavLink
              to="/inventario"
              className={({ isActive }) =>
                isActive ? 'nav-link active' : 'nav-link'
              }
            >
              <Package size={18} />
              <span>Inventario</span>
            </NavLink>
          </li>

          <li>
            <NavLink
              to="/alertas"
              className={({ isActive }) =>
                isActive ? 'nav-link active' : 'nav-link'
              }
            >
              <Bell size={18} />
              <span>Alertas</span>
            </NavLink>
          </li>
        </ul>
      </nav>
    </aside>
  )
}

export default Sidebar