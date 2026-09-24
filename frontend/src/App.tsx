import { BrowserRouter, Routes, Route } from 'react-router-dom'
import './App.css'

import Sidebar from './components/Sidebar'
import Topbar from './components/Topbar'

import Dashboard from './pages/Dashboard'
import Activos from './pages/Activos'
import Mantenciones from './pages/Mantenciones'
import Inventario from './pages/Inventario'
import Alertas from './pages/Alertas'

function App() {
  return (
    <BrowserRouter>
      <div className="app-layout">
        <Sidebar />

        <div className="app-main">
          <Topbar />

          <main className="main-content">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/activos" element={<Activos />} />
              <Route path="/mantenciones" element={<Mantenciones />} />
              <Route path="/inventario" element={<Inventario />} />
              <Route path="/alertas" element={<Alertas />} />
            </Routes>
          </main>
        </div>
      </div>
    </BrowserRouter>
  )
}

export default App