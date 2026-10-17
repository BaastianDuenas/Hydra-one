import { useEffect, useMemo, useState } from 'react'
import {
  Plus,
  Search,
  Pencil,
  Trash2,
  Package,
  TriangleAlert,
} from 'lucide-react'

import {
  obtenerRepuestos,
  crearRepuesto,
  actualizarRepuesto,
  eliminarRepuesto,
} from '../services/api'

type Repuesto = {
  id: number
  codigo: string
  nombre: string
  descripcion: string
  categoria: string
  stock_actual: number
  stock_minimo: number
  unidad_medida: string
  ubicacion: string
}

function Inventario() {
  const [repuestos, setRepuestos] = useState<Repuesto[]>([])
  const [mostrarFormulario, setMostrarFormulario] = useState(false)
  const [repuestoEditando, setRepuestoEditando] = useState<number | null>(null)

  const [busqueda, setBusqueda] = useState('')
  const [soloStockCritico, setSoloStockCritico] = useState(false)
  const [error, setError] = useState('')

  const [codigo, setCodigo] = useState('')
  const [nombre, setNombre] = useState('')
  const [descripcion, setDescripcion] = useState('')
  const [categoria, setCategoria] = useState('')
  const [stockActual, setStockActual] = useState(0)
  const [stockMinimo, setStockMinimo] = useState(0)
  const [unidadMedida, setUnidadMedida] = useState('Unidad')
  const [ubicacion, setUbicacion] = useState('')

  useEffect(() => {
    obtenerRepuestos()
      .then((data) => {
        setRepuestos(data)
        setError('')
      })
      .catch(() => {
        setError('No se pudieron cargar los repuestos.')
      })
  }, [])

  const repuestosFiltrados = useMemo(() => {
    return repuestos.filter((repuesto) => {
      const coincideBusqueda =
        repuesto.codigo.toLowerCase().includes(busqueda.toLowerCase()) ||
        repuesto.nombre.toLowerCase().includes(busqueda.toLowerCase()) ||
        repuesto.categoria.toLowerCase().includes(busqueda.toLowerCase())

      const coincideStock =
        !soloStockCritico ||
        repuesto.stock_actual <= repuesto.stock_minimo

      return coincideBusqueda && coincideStock
    })
  }, [repuestos, busqueda, soloStockCritico])

  const guardarRepuesto = async (e: React.FormEvent) => {
    e.preventDefault()

    const datos = {
      codigo,
      nombre,
      descripcion,
      categoria,
      stock_actual: stockActual,
      stock_minimo: stockMinimo,
      unidad_medida: unidadMedida,
      ubicacion,
    }

    try {
      if (repuestoEditando !== null) {
        const actualizado = await actualizarRepuesto(
          repuestoEditando,
          datos
        )

        setRepuestos(
          repuestos.map((repuesto) =>
            repuesto.id === repuestoEditando
              ? actualizado
              : repuesto
          )
        )
      } else {
        const nuevo = await crearRepuesto(datos)

        setRepuestos([...repuestos, nuevo])
      }

      limpiarFormulario()
      setError('')
    } catch (error) {
      if (error instanceof Error) {
        setError(error.message)
      }
    }
  }

  const editarRepuesto = (repuesto: Repuesto) => {
    setRepuestoEditando(repuesto.id)

    setCodigo(repuesto.codigo)
    setNombre(repuesto.nombre)
    setDescripcion(repuesto.descripcion)
    setCategoria(repuesto.categoria)
    setStockActual(repuesto.stock_actual)
    setStockMinimo(repuesto.stock_minimo)
    setUnidadMedida(repuesto.unidad_medida)
    setUbicacion(repuesto.ubicacion)

    setMostrarFormulario(true)
  }

  const borrarRepuesto = async (id: number) => {
    const confirmar = window.confirm(
      '¿Seguro que deseas eliminar este repuesto?'
    )

    if (!confirmar) return

    try {
      await eliminarRepuesto(id)

      setRepuestos(
        repuestos.filter((repuesto) => repuesto.id !== id)
      )
    } catch (error) {
      if (error instanceof Error) {
        setError(error.message)
      }
    }
  }

  const limpiarFormulario = () => {
    setCodigo('')
    setNombre('')
    setDescripcion('')
    setCategoria('')
    setStockActual(0)
    setStockMinimo(0)
    setUnidadMedida('Unidad')
    setUbicacion('')
    setRepuestoEditando(null)
    setMostrarFormulario(false)
  }

  const stockCritico = repuestos.filter(
    (repuesto) => repuesto.stock_actual <= repuesto.stock_minimo
  ).length

  return (
    <div>
      <div className="page-header page-header-row">
        <div>
          <h2>Inventario</h2>
          <p>Gestión de repuestos, stock y ubicaciones.</p>
        </div>

        <button
          className="primary-button button-with-icon"
          onClick={() => setMostrarFormulario(!mostrarFormulario)}
        >
          <Plus size={18} />
          Nuevo repuesto
        </button>
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      <section className="dashboard-cards inventory-summary">
        <div className="dashboard-card">
          <div className="card-icon">
            <Package size={22} />
          </div>

          <div>
            <span>Total de repuestos</span>
            <strong>{repuestos.length}</strong>
          </div>
        </div>

        <div className="dashboard-card">
          <div className="card-icon">
            <TriangleAlert size={22} />
          </div>

          <div>
            <span>Stock crítico</span>
            <strong>{stockCritico}</strong>
          </div>
        </div>
      </section>

      {mostrarFormulario && (
        <form className="asset-form" onSubmit={guardarRepuesto}>
          <div className="form-group">
            <label>Código</label>
            <input
              type="text"
              value={codigo}
              onChange={(e) => setCodigo(e.target.value)}
              placeholder="Ej: REP-003"
              required
            />
          </div>

          <div className="form-group">
            <label>Nombre</label>
            <input
              type="text"
              value={nombre}
              onChange={(e) => setNombre(e.target.value)}
              placeholder="Ej: Correa alternador"
              required
            />
          </div>

          <div className="form-group">
            <label>Categoría</label>
            <input
              type="text"
              value={categoria}
              onChange={(e) => setCategoria(e.target.value)}
              placeholder="Ej: Filtros"
              required
            />
          </div>

          <div className="form-group">
            <label>Unidad de medida</label>
            <select
              value={unidadMedida}
              onChange={(e) => setUnidadMedida(e.target.value)}
            >
              <option>Unidad</option>
              <option>Litro</option>
              <option>Kilogramo</option>
              <option>Metro</option>
            </select>
          </div>

          <div className="form-group">
            <label>Stock actual</label>
            <input
              type="number"
              min="0"
              value={stockActual}
              onChange={(e) => setStockActual(Number(e.target.value))}
            />
          </div>

          <div className="form-group">
            <label>Stock mínimo</label>
            <input
              type="number"
              min="0"
              value={stockMinimo}
              onChange={(e) => setStockMinimo(Number(e.target.value))}
            />
          </div>

          <div className="form-group">
            <label>Ubicación</label>
            <input
              type="text"
              value={ubicacion}
              onChange={(e) => setUbicacion(e.target.value)}
              placeholder="Ej: Bodega A - Estante 3"
              required
            />
          </div>

          <div className="form-group">
            <label>Descripción</label>
            <textarea
              value={descripcion}
              onChange={(e) => setDescripcion(e.target.value)}
              placeholder="Descripción del repuesto..."
              required
            />
          </div>

          <div className="form-actions">
            <button
              type="button"
              className="secondary-button"
              onClick={limpiarFormulario}
            >
              Cancelar
            </button>

            <button type="submit" className="primary-button">
              {repuestoEditando !== null
                ? 'Guardar cambios'
                : 'Guardar repuesto'}
            </button>
          </div>
        </form>
      )}

      <div className="toolbar">
        <div className="search-box">
          <Search size={18} />

          <input
            type="text"
            placeholder="Buscar por código, nombre o categoría..."
            value={busqueda}
            onChange={(e) => setBusqueda(e.target.value)}
          />
        </div>

        <label className="stock-filter">
          <input
            type="checkbox"
            checked={soloStockCritico}
            onChange={(e) => setSoloStockCritico(e.target.checked)}
          />

          Solo stock crítico
        </label>
      </div>

      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Código</th>
              <th>Repuesto</th>
              <th>Categoría</th>
              <th>Stock</th>
              <th>Mínimo</th>
              <th>Estado</th>
              <th>Ubicación</th>
              <th>Acciones</th>
            </tr>
          </thead>

          <tbody>
            {repuestosFiltrados.map((repuesto) => {
              const esStockBajo =
                repuesto.stock_actual <= repuesto.stock_minimo

              return (
                <tr key={repuesto.id}>
                  <td>
                    <strong>{repuesto.codigo}</strong>
                  </td>

                  <td>
                    <strong>{repuesto.nombre}</strong>
                    <span className="table-secondary">
                      {repuesto.descripcion}
                    </span>
                  </td>

                  <td>{repuesto.categoria}</td>

                  <td>
                    {repuesto.stock_actual} {repuesto.unidad_medida}
                  </td>

                  <td>{repuesto.stock_minimo}</td>

                  <td>
                    <span
                      className={
                        esStockBajo
                          ? 'status status-fuera'
                          : 'status status-operativo'
                      }
                    >
                      {esStockBajo
                        ? 'Stock bajo'
                        : 'Disponible'}
                    </span>
                  </td>

                  <td>{repuesto.ubicacion}</td>

                  <td>
                    <div className="table-actions">
                      <button
                        className="icon-button"
                        title="Editar"
                        onClick={() => editarRepuesto(repuesto)}
                      >
                        <Pencil size={17} />
                      </button>

                      <button
                        className="icon-button danger"
                        title="Eliminar"
                        onClick={() => borrarRepuesto(repuesto.id)}
                      >
                        <Trash2 size={17} />
                      </button>
                    </div>
                  </td>
                </tr>
              )
            })}

            {repuestosFiltrados.length === 0 && (
              <tr>
                <td colSpan={8} className="empty-state">
                  No se encontraron repuestos.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default Inventario