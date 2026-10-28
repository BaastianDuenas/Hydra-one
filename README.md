# Hydra One

Plataforma web para la gestión de maquinaria, mantenciones, inventario y alertas.

## Trabajo colaborativo con GitHub

El proyecto utiliza la rama principal `main`, donde se encuentran el código fuente, los informes y las evidencias académicas.

### 1. Clonar el repositorio (solo la primera vez)

```bash
git clone URL_DEL_REPOSITORIO
cd Hydra-One
```

### 2. Actualizar el proyecto

Antes de comenzar a trabajar:

```bash
git status
git switch main
git pull --ff-only origin main
```

Si tienes cambios locales pendientes, guárdalos antes de actualizar.

### 3. Guardar y subir modificaciones

Después de trabajar:

```bash
git status
git add .
git commit -m "Descripcion de los cambios"
git push origin main
```

Revisa siempre qué archivos vas a subir con `git status`.

### 4. Comandos útiles

| Comando | Función |
|---|---|
| `git status` | Revisar modificaciones pendientes |
| `git pull` | Descargar e integrar cambios |
| `git add .` | Preparar modificaciones |
| `git commit -m "Mensaje"` | Registrar cambios localmente |
| `git push origin main` | Publicar cambios en GitHub |
| `git branch` | Consultar la rama actual |
| `git remote -v` | Ver la conexión con GitHub |
| `git log --oneline -5` | Consultar los últimos cinco commits |

### 5. Recomendaciones

- Actualizar el repositorio antes de comenzar a trabajar.
- No sobrescribir archivos de otros integrantes sin coordinación.
- Utilizar mensajes de commit descriptivos.
- No subir contraseñas, tokens ni archivos `.env` con credenciales reales.
- Si aparece un conflicto de Git, revisarlo antes de continuar.
- Mantener las evidencias organizadas por fase.

**Flujo habitual:** actualizar → trabajar → revisar → agregar → commit → push.
