import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { ArrowLeft, Wrench } from 'lucide-react'

import {
  obtenerActivo,
  obtenerMantencionesPorActivo,
} from '../services/api'

type Activo = {
  id: number
  codigo: string
  nombre: string
  tipo: string
  estado: string
  horometro: number
  kilometraje: number
}

type Mantencion = {
  id: number
  activo_id: number
  tipo: string
  descripcion: string
  fecha: string
  horometro: number
  estado: string
}

function ActivoDetalle() {
  const { id } = useParams()

  const [activo, setActivo] = useState<Activo | null>(null)
  const [mantenciones, setMantenciones] = useState<Mantencion[]>([])
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!id) return

    const activoId = Number(id)

    Promise.all([
      obtenerActivo(activoId),
      obtenerMantencionesPorActivo(activoId),
    ])
      .then(([activoData, mantencionesData]) => {
        setActivo(activoData)
        setMantenciones(mantencionesData)
      })
      .catch(() => {
        setError('No se pudo cargar la información del activo.')
      })
      .finally(() => {
        setCargando(false)
      })
  }, [id])

  if (cargando) {
    return <p>Cargando activo...</p>
  }

  if (error) {
    return <div className="error-message">{error}</div>
  }

  if (!activo) {
    return <p>Activo no encontrado.</p>
  }

  return (
    <div>
      <Link to="/activos" className="back-link">
        <ArrowLeft size={18} />
        Volver a activos
      </Link>

      <div className="page-header">
        <h2>{activo.nombre}</h2>
        <p>
          {activo.codigo} · {activo.tipo}
        </p>
      </div>

      <section className="asset-detail-grid">
        <div className="detail-card">
          <span>Estado</span>
          <strong>{activo.estado}</strong>
        </div>

        <div className="detail-card">
          <span>Horómetro</span>
          <strong>
            {activo.horometro.toLocaleString()} h
          </strong>
        </div>

        <div className="detail-card">
          <span>Kilometraje</span>
          <strong>
            {activo.kilometraje > 0
              ? `${activo.kilometraje.toLocaleString()} km`
              : 'No aplica'}
          </strong>
        </div>

        <div className="detail-card">
          <span>Mantenciones registradas</span>
          <strong>{mantenciones.length}</strong>
        </div>
      </section>

      <section className="dashboard-panel maintenance-history">
        <div className="panel-header">
          <div>
            <h3>Historial de mantenciones</h3>
            <p>
              Mantenciones asociadas a este activo.
            </p>
          </div>

          <Wrench size={20} />
        </div>

        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Fecha</th>
                <th>Tipo</th>
                <th>Horómetro</th>
                <th>Estado</th>
                <th>Descripción</th>
              </tr>
            </thead>

            <tbody>
              {mantenciones.map((mantencion) => (
                <tr key={mantencion.id}>
                  <td>{mantencion.fecha}</td>
                  <td>{mantencion.tipo}</td>
                  <td>
                    {mantencion.horometro.toLocaleString()} h
                  </td>
                  <td>{mantencion.estado}</td>
                  <td>{mantencion.descripcion}</td>
                </tr>
              ))}

              {mantenciones.length === 0 && (
                <tr>
                  <td colSpan={5} className="empty-state">
                    Este activo todavía no tiene mantenciones registradas.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  )
}

export default ActivoDetalle