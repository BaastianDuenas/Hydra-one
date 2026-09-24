import { useEffect, useState } from 'react'
import {
  Truck,
  Wrench,
  TriangleAlert,
  PackageSearch,
} from 'lucide-react'

import { obtenerEstadoBackend } from '../services/api'

function Dashboard() {
  const [estadoBackend, setEstadoBackend] = useState('Comprobando...')

  useEffect(() => {
    obtenerEstadoBackend()
      .then((data) => setEstadoBackend(data.status))
      .catch(() => setEstadoBackend('Sin conexión'))
  }, [])

  return (
    <div>
      <div className="page-header">
        <div>
          <h2>Dashboard</h2>
          <p>Resumen general de la operación de Hydra One.</p>
        </div>
      </div>

      <section className="dashboard-cards">
        <div className="dashboard-card">
          <div className="card-icon">
            <Truck size={22} />
          </div>

          <div>
            <span>Total de activos</span>
            <strong>45</strong>
          </div>
        </div>

        <div className="dashboard-card">
          <div className="card-icon">
            <Truck size={22} />
          </div>

          <div>
            <span>Activos operativos</span>
            <strong>34</strong>
          </div>
        </div>

        <div className="dashboard-card">
          <div className="card-icon">
            <Wrench size={22} />
          </div>

          <div>
            <span>En mantención</span>
            <strong>7</strong>
          </div>
        </div>

        <div className="dashboard-card">
          <div className="card-icon">
            <TriangleAlert size={22} />
          </div>

          <div>
            <span>Alertas activas</span>
            <strong>4</strong>
          </div>
        </div>
      </section>

      <section className="dashboard-grid">
        <div className="dashboard-panel">
          <div className="panel-header">
            <div>
              <h3>Mantenciones próximas</h3>
              <p>Equipos que requieren atención próximamente.</p>
            </div>

            <Wrench size={20} />
          </div>

          <div className="dashboard-list">
            <div className="dashboard-list-item">
              <div>
                <strong>CAM-001</strong>
                <span>Camión Komatsu 930E</span>
              </div>

              <div className="list-right">
                <strong>12.500 h</strong>
                <span>Faltan 50 h</span>
              </div>
            </div>

            <div className="dashboard-list-item">
              <div>
                <strong>EXC-004</strong>
                <span>Excavadora CAT 320</span>
              </div>

              <div className="list-right">
                <strong>9.000 h</strong>
                <span>Faltan 120 h</span>
              </div>
            </div>

            <div className="dashboard-list-item">
              <div>
                <strong>CAR-003</strong>
                <span>Cargador frontal Volvo</span>
              </div>

              <div className="list-right">
                <strong>7.500 h</strong>
                <span>Faltan 180 h</span>
              </div>
            </div>
          </div>
        </div>

        <div className="dashboard-panel">
          <div className="panel-header">
            <div>
              <h3>Alertas recientes</h3>
              <p>Situaciones que requieren revisión.</p>
            </div>

            <TriangleAlert size={20} />
          </div>

          <div className="dashboard-list">
            <div className="dashboard-list-item">
              <div className="alert-row">
                <TriangleAlert size={18} />
                <div>
                  <strong>Stock bajo</strong>
                  <span>Filtro hidráulico CAT</span>
                </div>
              </div>

              <span className="status status-fuera">
                Crítica
              </span>
            </div>

            <div className="dashboard-list-item">
              <div className="alert-row">
                <Wrench size={18} />
                <div>
                  <strong>Mantención próxima</strong>
                  <span>CAM-001 - Komatsu 930E</span>
                </div>
              </div>

              <span className="status status-mantencion">
                Atención
              </span>
            </div>

            <div className="dashboard-list-item">
              <div className="alert-row">
                <PackageSearch size={18} />
                <div>
                  <strong>Repuesto pendiente</strong>
                  <span>Kit de frenos</span>
                </div>
              </div>

              <span className="status status-mantencion">
                Pendiente
              </span>
            </div>
          </div>
        </div>
      </section>

      <div className="backend-status">
        <span>Estado API</span>

        <strong
          className={
            estadoBackend === 'ok'
              ? 'api-online'
              : 'api-offline'
          }
        >
          {estadoBackend}
        </strong>
      </div>
    </div>
  )
}

export default Dashboard