# Mapas ilustrados de Hydra-One

Estas tres imágenes explican el proyecto mediante iconos y recorridos. Generadas con la herramienta de imágenes y revisadas contra los hechos del código descritos en los anexos. Son PNG ilustrados, no objetos editables de draw.io ni capturas de la aplicación. Los dibujos de interfaces, equipos y servidores son representaciones conceptuales.

## 1. Arquitectura — ¿quién hace cada trabajo?

Abre `01-arquitectura.png`. Lee los números de izquierda a derecha:

1. **Usuario:** persona que registra y consulta información.
2. **React:** la pantalla que utiliza esa persona. TypeScript ayuda a desarrollar esta interfaz. La pantalla envía solicitudes al backend y muestra sus respuestas.
3. **FastAPI:** recibe las solicitudes, valida datos y ejecuta las operaciones. Los cuatro iconos inferiores son módulos del mismo backend: activos, mantenciones, inventario y alertas. No son cuatro servidores independientes.
4. **PostgreSQL en Neon:** almacena los registros. PostgreSQL es el motor de base de datos; Neon es el servicio donde el equipo indica que lo aloja.

Las flechas de ida y vuelta indican solicitudes y respuestas, no cuatro canales independientes. HTTP/JSON conecta interfaz y API; SQL representa las operaciones de datos y TLS el cifrado de la conexión indicada para Neon. El navegador no se conecta directamente a la base de datos. El servidor dibujado representa el proceso backend, no una máquina física contratada.

Frase para explicarlo: **«La pantalla pide, el backend procesa y la base de datos conserva».** La conexión remota no se verificó durante la creación de estas ilustraciones.

## 2. Datos — ¿qué información se relaciona?

Abre `02-datos.png`:

- **Activos:** los equipos registrados, representados por una excavadora.
- **Mantenciones:** intervenciones o trabajos asociados a esos equipos. Las tarjetas representan varios registros, no una cantidad fija de tres.
- **Repuestos:** piezas y existencias del inventario.

`id` identifica un registro. En mantenciones, `activo_id` señala a qué activo pertenece. **1 → 0..N** significa que un activo puede tener ninguna, una o muchas mantenciones; cada mantención corresponde a un activo. La llave junto a `activo_id` representa una referencia, no otra clave primaria.

La cadena rota indica una limitación real del esquema actual: **no hay relación de consumo entre mantenciones y repuestos**. Estar dentro de la misma base de datos no crea esa relación automáticamente. La nube identifica el destino previsto por el equipo; el esquema se deduce del código, no de una inspección remota.

Frase para explicarlo: **«Podemos consultar las mantenciones de un equipo, pero aún no registrar qué repuestos consumió cada trabajo».** El ERD técnico anterior conserva los campos y tipos completos; esta imagen muestra solo la idea central.

## 3. Proceso — ¿qué pasa al registrar una mantención?

Abre `03-proceso.png`:

1. Se elige un activo.
2. Se completa el formulario de mantención; “completar” aquí significa rellenarlo, no cambiar su estado a Completada.
3. El backend valida los datos: una entrada inválida puede devolver HTTP 422.
4. Se comprueba que el activo exista. Si no existe, se devuelve HTTP 404.
5. Si las comprobaciones pasan y la escritura tiene éxito, se guarda la mantención.
6. La API devuelve la confirmación y los datos guardados (HTTP 201).

El icono de inventario en pausa significa **stock sin cambios**: crear una mantención no descuenta piezas. Es un recorrido resumido del caso normal con dos errores importantes; no enumera todos los posibles fallos de red o de base de datos. La pantalla de confirmación es ilustrativa.

Frase para explicarlo: **«Primero validamos el trabajo y el equipo; después guardamos. El descuento de inventario es una integración pendiente».**

## Uso

Insertar cada PNG como imagen independiente en el anexo correspondiente. Mantener la explicación en el texto del informe o usar las frases como ayuda memoria. No presentar las ilustraciones como prueba de ejecución: para eso se necesitan capturas o resultados reales con fecha y versión.

Los diagramas técnicos anteriores siguen disponibles en `../drawio/`; estas imágenes son una alternativa visual para explicar arquitectura, relaciones y recorrido, no una sustitución del detalle técnico de los nueve modelos.
