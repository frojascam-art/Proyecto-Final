/* ============================================
   app.js
   Punto de entrada del prototipo. Por ahora solo define el
   mecanismo generico para registrar y cargar pantallas dentro
   del contenedor principal. NO contiene logica de negocio.

   Nota importante: el prototipo se abre con doble clic sobre
   index.html (protocolo file://), por lo que NO se debe usar
   fetch()/XMLHttpRequest para cargar archivos .html externos:
   los navegadores bloquean esas peticiones por CORS cuando no
   hay un servidor. Por eso cada pantalla se implementa como una
   funcion de JS (ver carpeta pantallas/) que se registra aqui.
   ============================================ */

// Registro de pantallas disponibles: { nombre: funcionRenderizado }
const pantallas = {};

// Cada archivo de pantallas/ llama a esta funcion para registrarse.
function registrarPantalla(nombre, funcionRenderizado) {
  pantallas[nombre] = funcionRenderizado;
}

// Pinta la pantalla solicitada dentro del contenedor principal.
function cargarPantalla(nombre) {
  const contenedor = document.getElementById('contenedor-principal');
  const render = pantallas[nombre];

  if (typeof render === 'function') {
    contenedor.innerHTML = '';
    // TODO: aqui es donde cada pantalla ejecuta su propia logica
    // (formularios, validaciones, datos de ejemplo, eventos, etc.)
    render(contenedor);
  } else {
    // Pantalla aun no implementada.
    contenedor.innerHTML = `<p>Pantalla "${nombre}" pendiente de implementar.</p>`;
  }
}

document.addEventListener('DOMContentLoaded', function () {
  // Conecta cada enlace de la barra de navegacion con su pantalla.
  // Esto es solo mecanica de navegacion generica; no es logica de
  // negocio de ninguna vista en particular.
  const enlaces = document.querySelectorAll('[data-pantalla]');
  enlaces.forEach(function (enlace) {
    enlace.addEventListener('click', function (evento) {
      evento.preventDefault();
      cargarPantalla(enlace.dataset.pantalla);
    });
  });

  // TODO: definir cual es la pantalla inicial real (por ejemplo,
  // "ingresar" si se requiere sesion antes de ver el resto).
  cargarPantalla('inicio');
});
