import { useEffect, useMemo, useState } from 'react'
import {
  Bell,
  Package,
  Search,
  TriangleAlert,
  Wrench,
} from 'lucide-react'

import { obtenerAlertas } from '../services/api'


type Alerta = {
  id: string
  tipo: string
  prioridad: string
  titulo: string
  descripcion: string
  origen_id: number
}


function Alertas() {
  const [alertas, setAlertas] = useState<Alerta[]>([])
  const [busqueda, setBusqueda] = useState('')
  const [filtroTipo, setFiltroTipo] = useState('Todas')
  const [error, setError] = useState('')

  useEffect(() => {
    obtenerAlertas()
      .then((data) => {
        setAlertas(data)
        setError('')
      })
      .catch(() => {
        setError('No se pudieron cargar las alertas.')
      })
  }, [])

  const alertasFiltradas = useMemo(() => {
    return alertas.filter((alerta) => {
      const coincideBusqueda =
        alerta.titulo.toLowerCase().includes(busqueda.toLowerCase()) ||
        alerta.descripcion.toLowerCase().includes(busqueda.toLowerCase())

      const coincideTipo =
        filtroTipo === 'Todas' ||
        alerta.tipo === filtroTipo

      return coincideBusqueda && coincideTipo
    })
  }, [alertas, busqueda, filtroTipo])

  const criticas = alertas.filter(
    (alerta) => alerta.prioridad === 'Critica'
  ).length

  const inventario = alertas.filter(
    (alerta) => alerta.tipo === 'Inventario'
  ).length

  const mantenciones = alertas.filter(
    (alerta) => alerta.tipo === 'Mantencion'
  ).length

  const clasePrioridad = (prioridad: string) => {
    if (prioridad === 'Critica') {
      return 'status status-fuera'
    }

    if (prioridad === 'Alta') {
      return 'status status-mantencion'
    }

    return 'status status-operativo'
  }

  return (
    <div>
      <div className="page-header">
        <h2>Alertas</h2>
        <p>
          Situaciones detectadas automáticamente por Hydra One.
        </p>
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      <section className="dashboard-cards alerts-summary">
        <div className="dashboard-card">
          <div className="card-icon">
            <Bell size={22} />
          </div>

          <div>
            <span>Alertas activas</span>
            <strong>{alertas.length}</strong>
          </div>
        </div>

        <div className="dashboard-card">
          <div className="card-icon">
            <TriangleAlert size={22} />
          </div>

          <div>
            <span>Críticas</span>
            <strong>{criticas}</strong>
          </div>
        </div>

        <div className="dashboard-card">
          <div className="card-icon">
            <Package size={22} />
          </div>

          <div>
            <span>Inventario</span>
            <strong>{inventario}</strong>
          </div>
        </div>

        <div className="dashboard-card">
          <div className="card-icon">
            <Wrench size={22} />
          </div>

          <div>
            <span>Mantenciones</span>
            <strong>{mantenciones}</strong>
          </div>
        </div>
      </section>

      <div className="toolbar">
        <div className="search-box">
          <Search size={18} />

          <input
            type="text"
            placeholder="Buscar alerta..."
            value={busqueda}
            onChange={(e) => setBusqueda(e.target.value)}
          />
        </div>

        <select
          className="filter-select"
          value={filtroTipo}
          onChange={(e) => setFiltroTipo(e.target.value)}
        >
          <option>Todas</option>
          <option>Inventario</option>
          <option>Mantencion</option>
        </select>
      </div>

      <div className="alerts-list">
        {alertasFiltradas.map((alerta) => (
          <div className="alert-card" key={alerta.id}>
            <div className="alert-icon">
              {alerta.tipo === 'Inventario'
                ? <Package size={20} />
                : <Wrench size={20} />}
            </div>

            <div className="alert-content">
              <div className="alert-title-row">
                <strong>{alerta.titulo}</strong>

                <span className={clasePrioridad(alerta.prioridad)}>
                  {alerta.prioridad}
                </span>
              </div>

              <p>{alerta.descripcion}</p>

              <span className="alert-type">
                {alerta.tipo}
              </span>
            </div>
          </div>
        ))}

        {alertasFiltradas.length === 0 && (
          <div className="empty-alerts">
            <Bell size={30} />

            <strong>No hay alertas</strong>

            <span>
              No existen situaciones que requieran atención.
            </span>
          </div>
        )}
      </div>
    </div>
  )
}

export default Alertas