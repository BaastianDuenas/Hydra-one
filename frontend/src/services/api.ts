const API_URL = 'http://localhost:8000'

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