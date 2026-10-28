# Evidencias complementarias que conviene reunir

Este archivo es una guía de captura, no un registro de pruebas aprobadas. Los diagramas entregados documentan diseño y lectura del código. Para demostrar funcionamiento, acompañarlos con evidencia reproducible.

| Evidencia | Representación visual sugerida | Qué registrar para que sea útil |
|---|---|---|
| Recorrido de un activo | Tríptico de capturas: alta → ficha → historial | Fecha, versión, código de prueba y resultado esperado/obtenido |
| Persistencia real | Captura de interfaz junto a consulta SELECT del mismo registro | ID coincidente, entorno, consulta y resultado; ocultar datos personales y secretos |
| Conexión a Neon | Captura acotada del proyecto/rama/base y revisión Alembic | Identificación del entorno sin contraseñas; confirmar que ambos equipos usan el mismo destino |
| Alertas | Tabla de casos acompañada de tres capturas | Stock cero, stock en mínimo y mantención vencida; probar también condiciones sin alerta |
| Validación | Formulario inválido + respuesta HTTP + ausencia de nuevo registro | Entrada, 422 o 404 esperado, resultado observado y explicación breve |
| Cambios de fase | Comparación de diagramas versionados y tabla de decisiones | Estado anterior, cambio, motivo, impacto y evidencia enlazada |
| Integración pendiente | ERD propuesto + actividad de cierre | Aprobación de reglas, tareas y pruebas futuras; rotularlo como diseño |
| Aceptación de usuarios | Matriz de tareas y comentarios anonimizados | Quién valida en términos de rol, tarea, dificultad observada y mejora acordada |

## Casos sugeridos para alertas

| Condición | Resultado que indica el código actual |
|---|---|
| stock_actual = 0, stock_minimo ≥ 0 | Crítica: repuesto sin stock |
| 0 < stock_actual ≤ stock_minimo | Alta: stock bajo |
| stock_actual > stock_minimo | Sin alerta de inventario |
| Programada y fecha < hoy | Crítica: mantención vencida |
| Programada y hoy ≤ fecha ≤ hoy + 7 | Media: mantención próxima |
| Programada y fecha > hoy + 7 | Sin alerta de mantención |
| Estado distinto de Programada | No se incluye en alertas de mantenciones |

Ejecutar en datos de prueba acordados. No modificar la base compartida solo para fabricar capturas. Guardar una ficha por caso: ID, objetivo, precondiciones, pasos, resultado esperado, resultado real, fecha, versión y archivo de evidencia. No dar por aprobado un caso sin ejecutarlo.

## Decisiones que pueden explicar, pendientes de confirmar con el equipo

- **Monolito modular:** el código reúne routers en una API. Beneficio razonable: menor complejidad de operación para el MVP; límite: la lógica vive directamente en los routers. Confirmar si fue una elección explícita del equipo.
- **React / FastAPI:** separación de interfaz y API que se observa en el proyecto. Facilita trabajar por capas; exige coordinar contratos y errores. Evitar afirmar mejoras de rendimiento que no se hayan medido.
- **PostgreSQL en Neon:** puede facilitar compartir persistencia sin mantener un servidor local para cada integrante. Requiere gestionar el destino, conectividad, permisos y migraciones. No se ha verificado aquí la configuración remota, plan, backups ni costos.
- **SQLAlchemy / Alembic:** modelos y migraciones están versionados en el repositorio. La presencia de archivos no demuestra que todos los entornos estén actualizados.
- **Consumos y movimientos propuestos:** permitirían justificar cada descuento y reconstruir cambios. Requieren transacciones, restricciones y política de reversión; no afirmar que ya están implementados.

La justificación final debe distinguir «razón documentada por el equipo» de «beneficio técnico posible». Para cada decisión: problema → alternativas consideradas → criterio → elección → costo o límite → evidencia.

## Acceso necesario para completar evidencias reales

Para capturas funcionales se requiere la aplicación ejecutándose con datos de prueba. Para contrastar el ERD con Neon basta una conexión autorizada de lectura al esquema y a los registros de prueba. Identificar al creador o verificar permisos, ramas y backups requiere acceso autorizado a la consola del proyecto o información del responsable. Nada de esto es necesario para abrir los anexos entregados. No se incorporan credenciales en imágenes ni archivos de documentación.
