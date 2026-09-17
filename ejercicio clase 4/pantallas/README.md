# Carpeta de pantallas

Cada vista del sistema (inicio de sesion, agendar cita, mis citas,
gestion de pacientes, etc.) se implementara como un archivo `.js` en
esta carpeta, siguiendo el patron de `_plantilla.js`.

## Por que .js y no .html

El prototipo se abre con doble clic sobre `index.html` (protocolo
`file://`), sin servidor. Bajo ese protocolo los navegadores bloquean
`fetch()`/`XMLHttpRequest` hacia archivos locales por CORS, asi que no
se pueden cargar fragmentos `.html` externos de forma dinamica.

En su lugar, cada pantalla es un archivo `.js` que registra una
funcion de renderizado mediante `registrarPantalla(nombre, funcion)`
(definida en `js/app.js`). Esa funcion recibe el contenedor principal
y construye su HTML con JavaScript.

## Pasos para agregar una pantalla nueva

1. Copiar `_plantilla.js` y renombrarlo, por ejemplo `agendar-cita.js`.
2. Dentro, llamar a `registrarPantalla('agendar-cita', function (contenedor) { ... })`.
3. Incluir el script en `index.html`, en la seccion "SCRIPTS DE
   PANTALLAS", ANTES de `js/app.js`:
   `<script src="pantallas/agendar-cita.js"></script>`
4. Verificar que el enlace correspondiente en la barra de navegacion
   tenga el mismo valor en `data-pantalla="agendar-cita"`.
