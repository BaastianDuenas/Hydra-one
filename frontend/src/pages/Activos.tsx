import { Plus, Search, Pencil, Trash2, Eye } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";

import {
  obtenerActivos,
  crearActivo,
  actualizarActivo,
  eliminarActivo,
} from "../services/api";
import type { Activo } from "../services/api";

function Activos() {
  const [activos, setActivos] = useState<Activo[]>([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState("");

  const [mostrarFormulario, setMostrarFormulario] = useState(false);
  const [busqueda, setBusqueda] = useState("");
  const [filtroEstado, setFiltroEstado] = useState("Todos");

  const [codigo, setCodigo] = useState("");
  const [nombre, setNombre] = useState("");
  const [tipo, setTipo] = useState("");
  const [estado, setEstado] = useState("Operativo");
  const [horometro, setHorometro] = useState(0);
  const [kilometraje, setKilometraje] = useState(0);

  const [activoEditando, setActivoEditando] = useState<number | null>(null);

  // Traer activos desde FastAPI
  useEffect(() => {
    obtenerActivos()
      .then((data) => {
        setActivos(data);
        setError("");
      })
      .catch(() => {
        setError("No se pudieron cargar los activos.");
      })
      .finally(() => {
        setCargando(false);
      });
  }, []);

  // Filtrar activos
  const activosFiltrados = useMemo(() => {
    return activos.filter((activo) => {
      const coincideBusqueda =
        activo.codigo.toLowerCase().includes(busqueda.toLowerCase()) ||
        activo.nombre.toLowerCase().includes(busqueda.toLowerCase()) ||
        activo.tipo.toLowerCase().includes(busqueda.toLowerCase());

      const coincideEstado =
        filtroEstado === "Todos" || activo.estado === filtroEstado;

      return coincideBusqueda && coincideEstado;
    });
  }, [activos, busqueda, filtroEstado]);

  // Cargar activo en formulario para editar
  const editarActivo = (activo: Activo) => {
    setActivoEditando(activo.id);

    setCodigo(activo.codigo);
    setNombre(activo.nombre);
    setTipo(activo.tipo);
    setEstado(activo.estado);
    setHorometro(activo.horometro);
    setKilometraje(activo.kilometraje);

    setMostrarFormulario(true);
  };

  // Crear o actualizar activo
  const guardarActivo = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const datosActivo = {
        codigo,
        nombre,
        tipo,
        estado,
        horometro,
        kilometraje,
      };

      if (activoEditando !== null) {
        const actualizado = await actualizarActivo(activoEditando, datosActivo);

        setActivos(
          activos.map((activo) =>
            activo.id === activoEditando ? actualizado : activo,
          ),
        );
      } else {
        const nuevoActivo = await crearActivo(datosActivo);

        setActivos([...activos, nuevoActivo]);
      }

      setCodigo("");
      setNombre("");
      setTipo("");
      setEstado("Operativo");
      setHorometro(0);
      setKilometraje(0);

      setActivoEditando(null);
      setMostrarFormulario(false);
      setError("");
    } catch (error) {
      if (error instanceof Error) {
        setError(error.message);
      } else {
        setError("Ocurrió un error al guardar el activo.");
      }
    }
  };

  const borrarActivo = async (id: number) => {
    const confirmar = window.confirm(
      "¿Seguro que deseas eliminar este activo?",
    );

    if (!confirmar) return;

    try {
      await eliminarActivo(id);

      setActivos(activos.filter((activo) => activo.id !== id));

      setError("");
    } catch (error) {
      if (error instanceof Error) {
        setError(error.message);
      }
    }
  };

  const claseEstado = (estado: string) => {
    if (estado === "Operativo") return "status status-operativo";
    if (estado === "Mantención") return "status status-mantencion";

    return "status status-fuera";
  };

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

      {error && <div className="error-message">{error}</div>}
      {mostrarFormulario && (
        <form className="asset-form" onSubmit={guardarActivo}>
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
            <select value={estado} onChange={(e) => setEstado(e.target.value)}>
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
              {activoEditando !== null ? "Guardar cambios" : "Guardar activo"}
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

      {cargando && <p>Cargando activos...</p>}

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
              <th>Acciones</th>
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
                    : "No aplica"}
                </td>

                <td>
                  <div className="table-actions">
                    <Link
                      to={`/activos/${activo.id}`}
                      className="icon-button"
                      title="Ver detalle"
                    >
                      <Eye size={17} />
                    </Link>

                    
                    <button
                      className="icon-button"
                      title="Editar"
                      onClick={() => editarActivo(activo)}
                    >
                      <Pencil size={17} />
                    </button>

                    <button
                      className="icon-button danger"
                      title="Eliminar"
                      onClick={() => borrarActivo(activo.id)}
                    >
                      <Trash2 size={17} />
                    </button>
                  </div>
                </td>
              </tr>
            ))}

            {activosFiltrados.length === 0 && (
              <tr>
                <td colSpan={7} className="empty-state">
                  No se encontraron activos.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Activos;
