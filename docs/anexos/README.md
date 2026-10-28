# Hydra-One · Anexos técnicos visuales

Revisión: **28 de octubre de 2026**. Código de referencia: `5d449affbe4383fe5d654d1a98711b04e70c321b`.

Abre **[index.html](index.html)** para recorrer y ampliar los diagramas. Son anexos independientes, no diapositivas. Cada uno se entrega en tres representaciones:

- **draw.io**: objetos, textos y conectores editables. Abre [Hydra-One-diagramas.drawio](Hydra-One-diagramas.drawio) en un editor compatible con diagrams.net para ver las nueve pestañas. También hay archivos individuales en `drawio/`.
- **SVG**: vectorial, conserva la nitidez al ampliar; apropiado para anexos digitales e impresión.
- **PNG**: imagen a doble resolución para insertar en Word u otro editor. Carpeta `png/`.

Los archivos actuales describen lo que se observa en el código. Las propuestas están rotuladas y no son evidencia de implementación. No se consultó Neon ni se ejecutaron operaciones de negocio para elaborar estos anexos. No se atribuye a una persona la creación de la base porque el repositorio no demuestra quién la creó.

## Catálogo y uso en la defensa

| Anexo | Qué permite explicar | Pregunta que ayuda a responder |
|---|---|---|
| [01 · Contexto](svg/01-contexto.svg) | Usuario, propósito y límite del sistema | ¿Qué problema aborda Hydra-One y quién lo utiliza? |
| [02 · Contenedores](svg/02-contenedores.svg) | Navegador, API y persistencia | ¿Por qué frontend y backend se ejecutan por separado? |
| [03 · Componentes](svg/03-componentes.svg) | Páginas, cliente HTTP, routers, validación y modelos | ¿Dónde se cambia cada comportamiento? |
| [04 · ERD actual](svg/04-erd-actual.svg) | Tablas, tipos, claves y cardinalidades | ¿Cómo se relaciona un activo con su historial? |
| [05 · Secuencia de alta](svg/05-secuencia-alta.svg) | Interacciones, validación, 404 y persistencia | ¿Qué ocurre desde enviar un formulario hasta guardar? |
| [06 · Reglas de alertas](svg/06-alertas.svg) | Condiciones exactas de fecha y stock | ¿Por qué aparece esta alerta y con qué prioridad? |
| [07 · Despliegue de desarrollo](svg/07-despliegue.svg) | Dos equipos locales y una base compartida | ¿Por qué mi compañero ve datos y yo podría no verlos? |
| [08 · ERD propuesto](svg/08-erd-propuesto.svg) | Consumos y movimientos para trazabilidad | ¿Qué falta para unir mantenciones e inventario? |
| [09 · Cierre propuesto](svg/09-cierre-propuesto.svg) | Transacción, validación y prevención de duplicados | ¿Cómo evitar descuentos dobles o datos incompletos? |

Para público no técnico: empezar por 01, seguir con 02 y explicar una regla de 06 con un ejemplo. Para una revisión técnica: 04 → 05 → 03 → 07. Para discutir trabajo pendiente: comparar 04 con 08 y luego 09. No presentar los nueve a la vez: elegir el que responde a la pregunta.

## Cómo leerlos

Azul identifica aplicación o entidades existentes; verde azulado destaca datos; ámbar marca observaciones o diseño pendiente. La etiqueta de estado y el texto también expresan la diferencia, sin depender solo del color.

En el ERD, `PK` es clave primaria, `FK` referencia otra tabla y `UQ` exige unicidad. Las dos barras significan exactamente uno; círculo y pata de cuervo significan cero o muchos. La relación actual es **un activo puede tener 0..N mantenciones; cada mantención pertenece a exactamente un activo**. El ERD propuesto abrevia campos existentes y no es un script de migración aprobado.

En la secuencia, el tiempo avanza hacia abajo. Las líneas verticales son participantes, las flechas representan mensajes y las respuestas se dibujan discontinuas. `alt` separa alternativas. En las actividades, los rombos contienen decisiones y las salidas indican la condición. Los límites discontinuos en arquitectura agrupan responsabilidades; no implican microservicios.

## Fuentes verificables

Rutas relativas a la raíz del repositorio:

| Anexos | Fuentes principales |
|---|---|
| 01–03 | `frontend/src/App.tsx`, `frontend/src/pages/*.tsx`, `frontend/src/services/api.ts`, `backend/main.py`, `backend/app/routers/*.py` |
| 03–04 | `backend/app/models/*.py`, `backend/app/schemas/*.py`, `backend/app/database/connection.py` |
| 04 | `backend/alembic/versions/373c41b36d66_crear_tabla_activos.py`, `78ea66bb0d12_crear_tabla_mantenciones.py`, `a73114ad2322_crear_tabla_repuestos.py` |
| 05 | `backend/app/routers/mantenciones.py`, `backend/app/schemas/mantencion.py`, `frontend/src/services/api.ts` |
| 06 | `backend/app/routers/alertas.py` |
| 07 | `backend/main.py`, `backend/app/database/connection.py`, `frontend/src/services/api.ts`; uso de Neon informado por el equipo |
| 08–09 | Diseño propuesto a partir de la ausencia actual de consumos y movimientos; no corresponde a código implementado |

El esquema publicado es el definido en el repositorio; falta contrastarlo con la base remota y la revisión de Alembic aplicada. Los diagramas no prueban disponibilidad, rendimiento, seguridad ni aceptación de usuarios.

## Observaciones que conviene declarar en el informe

1. Inventario permite editar stock directamente; no hay un registro de entradas, salidas o ajustes.
2. Cambiar una mantención a `Completada` guarda un texto; no consume repuestos. La API no aplica una máquina de estados ni enumera los estados válidos.
3. Alertas es una consulta calculada. No existe tabla de alertas ni servicio de notificaciones.
4. El Dashboard contiene cifras estáticas. `/health` responde por la API, sin comprobar acceso a PostgreSQL.
5. No se encontró autenticación ni autorización por roles. El texto de administrador en la interfaz no demuestra esa capacidad.
6. El borrado en cascada de mantenciones se declara en SQLAlchemy; la migración no declara `ON DELETE CASCADE`. No atribuirle esa regla al servidor PostgreSQL.
7. Neon es un proveedor de PostgreSQL. Para compartir los mismos datos se debe apuntar al mismo proyecto, rama y base; tener un usuario no demuestra que el backend local esté conectado.

## Actualización y edición

Los SVG y los draw.io se generan a partir de las mismas coordenadas con `generar_diagramas.py`, usando Python estándar. Los PNG se exportan con `exportar_y_verificar.cjs` y Sharp. Ese segundo script recibe la ruta del directorio de paquetes de Node mediante `HYDRA_NODE_MODULES`; también necesita Playwright y Chrome para la comprobación visual automatizada. Los caminos locales del equipo no se incrustan en los diagramas.

```powershell
python docs/anexos/generar_diagramas.py
$env:HYDRA_NODE_MODULES = 'RUTA_AL_DIRECTORIO_NODE_MODULES'
node docs/anexos/exportar_y_verificar.cjs
```

No es necesario ejecutar estos comandos para ver o editar los archivos entregados. Si editas manualmente un `.drawio`, conserva esa versión: el generador sobrescribe los exports. Tras una edición manual, exporta SVG/PNG desde el editor para mantenerlos sincronizados. Los conectores y las etiquetas son elementos editables; al reubicar figuras, revisar sus puntos de conexión.

La revisión de calidad de estos anexos comprueba XML, exportación y límites de texto. No sustituye pruebas de la aplicación. Los resultados están en `verificacion.json`.
