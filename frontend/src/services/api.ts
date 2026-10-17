
export interface Activo {
  id: number
  codigo: string
  nombre: string
  tipo: string
  estado: string
  horometro: number
  kilometraje: number
}

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
export async function obtenerEstadoBackend() {
  const response = await fetch(`${API_URL}/health`)

  if (!response.ok) {
    throw new Error('No se pudo conectar con el backend')
  }

  return response.json()
}

export async function obtenerActivos() {
  const response = await fetch(`${API_URL}/api/activos/`)

  if (!response.ok) {
    throw new Error('No se pudieron obtener los activos')
  }

  return response.json()
}

export async function crearActivo(activo: {
  codigo: string
  nombre: string
  tipo: string
  estado: string
  horometro: number
  kilometraje: number
}) {
  const response = await fetch(`${API_URL}/api/activos/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(activo),
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'No se pudo crear el activo')
  }

  return response.json()
}
export async function obtenerActivo(id: number) {
  const response = await fetch(`${API_URL}/api/activos/${id}`)

  if (!response.ok) {
    throw new Error('No se pudo obtener el activo')
  }

  return response.json()
}

export async function actualizarActivo(
  id: number,
  activo: {
    codigo: string
    nombre: string
    tipo: string
    estado: string
    horometro: number
    kilometraje: number
  }
) {
  const response = await fetch(`${API_URL}/api/activos/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(activo),
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'No se pudo actualizar el activo')
  }

  return response.json()
}

export async function eliminarActivo(id: number) {
  const response = await fetch(`${API_URL}/api/activos/${id}`, {
    method: 'DELETE',
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'No se pudo eliminar el activo')
  }

  return response.json()
}

export async function obtenerMantenciones() {
  const response = await fetch(`${API_URL}/api/mantenciones/`)

  if (!response.ok) {
    throw new Error('No se pudieron obtener las mantenciones')
  }

  return response.json()
}

export async function crearMantencion(mantencion: {
  activo_id: number
  tipo: string
  descripcion: string
  fecha: string
  horometro: number
  estado: string
}) {
  const response = await fetch(`${API_URL}/api/mantenciones/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(mantencion),
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'No se pudo crear la mantención')
  }

  return response.json()
}


export async function actualizarMantencion(
  id: number,
  mantencion: {
    activo_id: number
    tipo: string
    descripcion: string
    fecha: string
    horometro: number
    estado: string
  }
) {
  const response = await fetch(`${API_URL}/api/mantenciones/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(mantencion),
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'No se pudo actualizar la mantención')
  }

  return response.json()
}

export async function eliminarMantencion(id: number) {
  const response = await fetch(`${API_URL}/api/mantenciones/${id}`, {
    method: 'DELETE',
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'No se pudo eliminar la mantención')
  }

  return response.json()
}

export async function obtenerMantencionesPorActivo(id: number) {
  const response = await fetch(
    `${API_URL}/api/mantenciones/activo/${id}`
  )

  if (!response.ok) {
    throw new Error('No se pudieron obtener las mantenciones del activo')
  }

  return response.json()
}

export async function obtenerRepuestos() {
  const response = await fetch(`${API_URL}/api/repuestos/`)

  if (!response.ok) {
    throw new Error('No se pudieron obtener los repuestos')
  }

  return response.json()
}

export async function crearRepuesto(repuesto: {
  codigo: string
  nombre: string
  descripcion: string
  categoria: string
  stock_actual: number
  stock_minimo: number
  unidad_medida: string
  ubicacion: string
}) {
  const response = await fetch(`${API_URL}/api/repuestos/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(repuesto),
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'No se pudo crear el repuesto')
  }

  return response.json()
}

export async function actualizarRepuesto(
  id: number,
  repuesto: {
    codigo: string
    nombre: string
    descripcion: string
    categoria: string
    stock_actual: number
    stock_minimo: number
    unidad_medida: string
    ubicacion: string
  }
) {
  const response = await fetch(`${API_URL}/api/repuestos/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(repuesto),
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'No se pudo actualizar el repuesto')
  }

  return response.json()
}

export async function eliminarRepuesto(id: number) {
  const response = await fetch(`${API_URL}/api/repuestos/${id}`, {
    method: 'DELETE',
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'No se pudo eliminar el repuesto')
  }

  return response.json()
}

export async function obtenerAlertas() {
  const response = await fetch(`${API_URL}/api/alertas/`)

  if (!response.ok) {
    throw new Error('No se pudieron obtener las alertas')
  }

  return response.json()
}