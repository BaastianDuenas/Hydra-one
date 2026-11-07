Hydra One
Plataforma web orientada a la gestión de maquinaria, mantenciones, inventario y alertas, desarrollada como parte de un proyecto académico de Ingeniería en Informática.

Descripción

Este repositorio contiene la documentación, informes y evidencias del desarrollo de Hydra One, organizados según las fases del proyecto.

Su propósito es mantener un respaldo personal y ordenado de las entregas académicas, facilitar su consulta y su posterior revisión.

Trabajo colaborativo
El proyecto utiliza la rama principal main, donde se encuentran el código fuente, los informes y las evidencias académicas.

1. Clonar el repositorio
git clone URL_DEL_REPOSITORIO
cd Hydra-One
2. Actualizar el proyecto
Antes de comenzar a trabajar:

git status
git switch main
git pull --ff-only origin main
Si tienes cambios locales pendientes, guárdalos antes de actualizar.

3. Guardar y subir modificaciones
Después de trabajar:

git status
git add .
git commit -m "Descripcion de los cambios"
git push origin main
Revisar siempre antes de subir archivos con git status.

4. Comandos útiles
Comando	Función
git status	Revisar modificaciones pendientes
git pull	Descargar e integrar cambios
git add .	Preparar modificaciones
git commit -m "Mensaje"	Registrar cambios localmente
git push origin main	Publicar cambios en GitHub
git branch	Consultar la rama actual
git remote -v	Ver la conexión con GitHub
git log --oneline -5	Consultar los últimos cinco commits