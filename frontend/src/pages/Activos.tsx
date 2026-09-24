import { Plus, Search } from 'lucide-react'
import { useEffect, useMemo, useState } from 'react'


import { obtenerActivos, crearActivo } from '../services/api'
type Activo = {
  id: number
  codigo: string
  nombre: string
  tipo: string
  estado: string
  horometro: number
  kilometraje: number
}

function Activos() {
  const [activos, setActivos] = useState<Activo[]>([])
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState('')
      

  const [mostrarFormulario, setMostrarFormulario] = useState(false)
  const [busqueda, setBusqueda] = useState('')
  const [filtroEstado, setFiltroEstado] = useState('Todos')

  const [codigo, setCodigo] = useState('')
  const [nombre, setNombre] = useState('')
  const [tipo, setTipo] = useState('')
  const [estado, setEstado] = useState('Operativo')
  const [horometro, setHorometro] = useState(0)
  const [kilometraje, setKilometraje] = useState(0)
 // Traer activos desde FastAPI
  useEffect(() => {
    obtenerActivos()
      .then((data) => {
        setActivos(data)
        setError('')
      })
      .catch(() => {
        setError('No se pudieron cargar los activos.')
      })
      .finally(() => {
        setCargando(false)
      })
  }, [])

  // Filtrar activos
  const activosFiltrados = useMemo(() => {
    return activos.filter((activo) => {
      const coincideBusqueda =
        activo.codigo.toLowerCase().includes(busqueda.toLowerCase()) ||
        activo.nombre.toLowerCase().includes(busqueda.toLowerCase()) ||
        activo.tipo.toLowerCase().includes(busqueda.toLowerCase())

      const coincideEstado =
        filtroEstado === 'Todos' || activo.estado === filtroEstado

      return coincideBusqueda && coincideEstado
    })
  }, [activos, busqueda, filtroEstado])



   // Crear activo en FastAPI/PostgreSQL
    const agregarActivo = async (e: React.FormEvent) => {
  e.preventDefault()

  try {
    const nuevoActivo = await crearActivo({
      codigo,
      nombre,
      tipo,
      estado,
      horometro,
      kilometraje,
    })

    setActivos([...activos, nuevoActivo])

    setCodigo('')
    setNombre('')
    setTipo('')
    setEstado('Operativo')
    setHorometro(0)
    setKilometraje(0)

    setMostrarFormulario(false)
    setError('')
  } catch (error) {
    if (error instanceof Error) {
      setError(error.message)
    } else {
      setError('Ocurrió un error al crear el activo.')
    }
  }
}

  const claseEstado = (estado: string) => {
    if (estado === 'Operativo') return 'status status-operativo'
    if (estado === 'Mantención') return 'status status-mantencion'
    return 'status status-fuera'
  }

  return (
    <div>
      <div className="page-header page-header-row">
        <div>
          <h2>Activos</h2>
          <p>Gestión de maquinaria y equipos de la empresa.</p>
        </div>

        <button
          className="primary-button button-with-icon"
          onClick={() => setMostrarFormulario(!mostrarFormulario)}
        >
          <Plus size={18} />
          Nuevo activo
        </button>
      </div>
      
         {error && (
  <div className="error-message">
    {error}
  </div>
)}
      {mostrarFormulario && (
        <form className="asset-form" onSubmit={agregarActivo}>
          <div className="form-group">
            <label>Código</label>
            <input
              type="text"
              value={codigo}
              onChange={(e) => setCodigo(e.target.value)}
              placeholder="Ej: CAM-002"
              required
            />
          </div>

          <div className="form-group">
            <label>Nombre</label>
            <input
              type="text"
              value={nombre}
              onChange={(e) => setNombre(e.target.value)}
              placeholder="Ej: Camión Komatsu"
              required
            />
          </div>

          <div className="form-group">
            <label>Tipo</label>
            <input
              type="text"
              value={tipo}
              onChange={(e) => setTipo(e.target.value)}
              placeholder="Ej: Camión minero"
              required
            />
          </div>

          <div className="form-group">
            <label>Estado</label>
            <select
              value={estado}
              onChange={(e) => setEstado(e.target.value)}
            >
              <option>Operativo</option>
              <option>Mantención</option>
              <option>Fuera de servicio</option>
            </select>
          </div>

          <div className="form-group">
            <label>Horómetro</label>
            <input
              type="number"
              min="0"
              value={horometro}
              onChange={(e) => setHorometro(Number(e.target.value))}
            />
          </div>

          <div className="form-group">
            <label>Kilometraje</label>
            <input
              type="number"
              min="0"
              value={kilometraje}
              onChange={(e) => setKilometraje(Number(e.target.value))}
            />
          </div>

          <div className="form-actions">
            <button
              type="button"
              className="secondary-button"
              onClick={() => setMostrarFormulario(false)}
            >
              Cancelar
            </button>

            <button type="submit" className="primary-button">
              Guardar activo
            </button>
          </div>
        </form>
      )}

      <div className="toolbar">
        <div className="search-box">
          <Search size={18} />
          <input
            type="text"
            placeholder="Buscar por código, nombre o tipo..."
            value={busqueda}
            onChange={(e) => setBusqueda(e.target.value)}
          />
        </div>

        <select
          className="filter-select"
          value={filtroEstado}
          onChange={(e) => setFiltroEstado(e.target.value)}
        >
          <option>Todos</option>
          <option>Operativo</option>
          <option>Mantención</option>
          <option>Fuera de servicio</option>
        </select>
      </div>

      {cargando && (
  <p>Cargando activos...</p>
)}

      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Código</th>
              <th>Nombre</th>
              <th>Tipo</th>
              <th>Estado</th>
              <th>Horómetro</th>
              <th>Kilometraje</th>
            </tr>
          </thead>

          <tbody>
            {activosFiltrados.map((activo) => (
              <tr key={activo.id}>
                <td>
                  <strong>{activo.codigo}</strong>
                </td>
                <td>{activo.nombre}</td>
                <td>{activo.tipo}</td>
                <td>
                  <span className={claseEstado(activo.estado)}>
                    {activo.estado}
                  </span>
                </td>
                <td>{activo.horometro.toLocaleString()} h</td>
                <td>
                  {activo.kilometraje > 0
                    ? `${activo.kilometraje.toLocaleString()} km`
                    : 'No aplica'}
                </td>
              </tr>
            ))}

            {activosFiltrados.length === 0 && (
              <tr>
                <td colSpan={6} className="empty-state">
                  No se encontraron activos.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default Activos