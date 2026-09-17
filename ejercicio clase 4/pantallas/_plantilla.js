/* ============================================
   _plantilla.js
   Plantilla de referencia para crear una pantalla nueva.
   Este archivo NO se incluye en index.html: es solo un ejemplo.

   Pasos para crear una pantalla real:
   1. Copiar este archivo y renombrarlo (ej. agendar-cita.js).
   2. Cambiar 'nombre-de-la-pantalla' por el mismo valor usado
      en el atributo data-pantalla del enlace de navegacion.
   3. Completar el HTML y, si aplica, la logica especifica.
   4. Incluir el script nuevo en index.html, ANTES de js/app.js.
   ============================================ */

registrarPantalla('nombre-de-la-pantalla', function (contenedor) {
  contenedor.innerHTML = `
    <section class="tarjeta">
      <h1>Titulo de la pantalla</h1>
      <p>Contenido de ejemplo. Reemplazar por el HTML real de la vista.</p>
    </section>
  `;

  // TODO: logica especifica de esta pantalla (eventos, validaciones,
  // datos de ejemplo, llamadas futuras a datos reales, etc.)
});
