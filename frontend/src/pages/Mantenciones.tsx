import { useEffect, useState } from "react";
import { Plus, Pencil, Trash2 } from "lucide-react";

import {
  obtenerActivos,
  obtenerMantenciones,
  crearMantencion,
  actualizarMantencion,
  eliminarMantencion,
} from "../services/api";

type Activo = {
  id: number;
  codigo: string;
  nombre: string;
};

type Mantencion = {
  id: number;
  activo_id: number;
  tipo: string;
  descripcion: string;
  fecha: string;
  horometro: number;
  estado: string;
};

function Mantenciones() {
  const [mantenciones, setMantenciones] = useState<Mantencion[]>([]);
  const [activos, setActivos] = useState<Activo[]>([]);
  const [mostrarFormulario, setMostrarFormulario] = useState(false);
  const [error, setError] = useState("");

  const [activoId, setActivoId] = useState(0);
  const [tipo, setTipo] = useState("Preventiva");
  const [descripcion, setDescripcion] = useState("");
  const [fecha, setFecha] = useState("");
  const [horometro, setHorometro] = useState(0);
  const [estado, setEstado] = useState("Programada");

  const [mantencionEditando, setMantencionEditando] =
  useState<number | null>(null)

  useEffect(() => {
    Promise.all([obtenerMantenciones(), obtenerActivos()])
      .then(([mantencionesData, activosData]) => {
        setMantenciones(mantencionesData);
        setActivos(activosData);

        if (activosData.length > 0) {
          setActivoId(activosData[0].id);
        }
      })
      .catch(() => {
        setError("No se pudieron cargar los datos.");
      });
  }, []);

  const guardarMantencion = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const datos = {
        activo_id: activoId,
        tipo,
        descripcion,
        fecha,
        horometro,
        estado,
      };

      if (mantencionEditando !== null) {
        const actualizada = await actualizarMantencion(
          mantencionEditando,
          datos,
        );

        setMantenciones(
          mantenciones.map((mantencion) =>
            mantencion.id === mantencionEditando ? actualizada : mantencion,
          ),
        );
      } else {
        const nueva = await crearMantencion(datos);

        setMantenciones([nueva, ...mantenciones]);
      }

      setMantencionEditando(null);
      setTipo("Preventiva");
      setDescripcion("");
      setFecha("");
      setHorometro(0);
      setEstado("Programada");
      setMostrarFormulario(false);
      setError("");
    } catch (error) {
      if (error instanceof Error) {
        setError(error.message);
      }
    }
  };

  const obtenerNombreActivo = (id: number) => {
    const activo = activos.find((activo) => activo.id === id);

    if (!activo) return `Activo ${id}`;

    return `${activo.codigo} - ${activo.nombre}`;
  };

  const editarMantencion = (mantencion: Mantencion) => {
    setMantencionEditando(mantencion.id);

    setActivoId(mantencion.activo_id);
    setTipo(mantencion.tipo);
    setDescripcion(mantencion.descripcion);
    setFecha(mantencion.fecha);
    setHorometro(mantencion.horometro);
    setEstado(mantencion.estado);

    setMostrarFormulario(true);
  };

  const borrarMantencion = async (id: number) => {
    const confirmar = window.confirm(
      "¿Seguro que deseas eliminar esta mantención?",
    );

    if (!confirmar) return;

    try {
      await eliminarMantencion(id);

      setMantenciones(
        mantenciones.filter((mantencion) => mantencion.id !== id),
      );
    } catch (error) {
      if (error instanceof Error) {
        setError(error.message);
      }
    }
  };

  return (
    <div>
      <div className="page-header page-header-row">
        <div>
          <h2>Mantenciones</h2>
          <p>Registro y seguimiento de mantenciones de los activos.</p>
        </div>

        <button
          className="primary-button button-with-icon"
          onClick={() => setMostrarFormulario(!mostrarFormulario)}
        >
          <Plus size={18} />
          Nueva mantención
        </button>
      </div>

      {error && <div className="error-message">{error}</div>}

      {mostrarFormulario && (
        <form className="asset-form" onSubmit={guardarMantencion}>
          <div className="form-group">
            <label>Activo</label>

            <select
              value={activoId}
              onChange={(e) => setActivoId(Number(e.target.value))}
              required
            >
              {activos.map((activo) => (
                <option key={activo.id} value={activo.id}>
                  {activo.codigo} - {activo.nombre}
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label>Tipo</label>

            <select value={tipo} onChange={(e) => setTipo(e.target.value)}>
              <option>Preventiva</option>
              <option>Correctiva</option>
              <option>Inspección</option>
            </select>
          </div>

          <div className="form-group">
            <label>Fecha</label>

            <input
              type="date"
              value={fecha}
              onChange={(e) => setFecha(e.target.value)}
              required
            />
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
            <label>Estado</label>

            <select value={estado} onChange={(e) => setEstado(e.target.value)}>
              <option>Programada</option>
              <option>En proceso</option>
              <option>Completada</option>
              <option>Cancelada</option>
            </select>
          </div>

          <div className="form-group">
            <label>Descripción</label>

            <textarea
              value={descripcion}
              onChange={(e) => setDescripcion(e.target.value)}
              placeholder="Detalle del trabajo a realizar..."
              required
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
              {mantencionEditando !== null
                ? "Guardar cambios"
                : "Guardar mantención"}
            </button>
          </div>
        </form>
      )}

      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>Activo</th>
              <th>Tipo</th>
              <th>Fecha</th>
              <th>Horómetro</th>
              <th>Estado</th>
              <th>Descripción</th>
              <th>Acciones</th>
            </tr>
          </thead>

          <tbody>
            {mantenciones.map((mantencion) => (
              <tr key={mantencion.id}>
                <td>
                  <strong>{obtenerNombreActivo(mantencion.activo_id)}</strong>
                </td>

                <td>{mantencion.tipo}</td>
                <td>{mantencion.fecha}</td>
                <td>{mantencion.horometro.toLocaleString()} h</td>
                <td>{mantencion.estado}</td>
                <td>{mantencion.descripcion}</td>
                <td>
                  <div className="table-actions">
                    <button
                      className="icon-button"
                      title="Editar"
                      onClick={() => editarMantencion(mantencion)}
                    >
                      <Pencil size={17} />
                    </button>

                    <button
                      className="icon-button danger"
                      title="Eliminar"
                      onClick={() => borrarMantencion(mantencion.id)}
                    >
                      <Trash2 size={17} />
                    </button>
                  </div>
                </td>
              </tr>
            ))}

            {mantenciones.length === 0 && (
              <tr>
                <td colSpan={7} className="empty-state">
                  No hay mantenciones registradas.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Mantenciones;
