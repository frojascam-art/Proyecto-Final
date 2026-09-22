/* ============================================
   app.js
   Punto de entrada del prototipo. Define el mecanismo generico para
   registrar y cargar pantallas dentro del contenedor principal, el
   estado global de sesion (rol activo, cliente/rutina en foco) y la
   logica generica de la barra de navegacion. NO contiene logica de
   negocio de ninguna pantalla en particular.

   Nota importante: el prototipo se abre con doble clic sobre
   index.html (protocolo file://), por lo que NO se debe usar
   fetch()/XMLHttpRequest para cargar archivos .html externos. Por eso
   cada pantalla es una funcion de JS (ver carpeta pantallas/) que se
   registra aqui.
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
    render(contenedor);
  } else {
    contenedor.innerHTML = `<p>Pantalla "${nombre}" pendiente de implementar.</p>`;
  }

  window.scrollTo(0, 0);
}

// Estado global de la sesion de demostracion (sin backend real).
const estado = {
  rol: null,              // 'coach' | 'cliente'
  clienteEnFocoId: null,  // cliente sobre el que trabaja el coach, o el cliente actual si rol === 'cliente'
  rutinaEnFocoId: null,   // rutina que se esta editando (HU3.1 -> HU3.2)
  modoSeleccionCliente: null // 'rutinas' | 'mediciones' | null, usado por el listado de clientes
};

function establecerRol(rol, clienteId) {
  estado.rol = rol;
  estado.clienteEnFocoId = clienteId || null;
  estado.rutinaEnFocoId = null;
  estado.modoSeleccionCliente = null;
  actualizarNavegacion();
}

function volverAlSelectorDeRol() {
  estado.rol = null;
  estado.clienteEnFocoId = null;
  estado.rutinaEnFocoId = null;
  estado.modoSeleccionCliente = null;
  actualizarNavegacion();
  cargarPantalla('inicio');
}

// Muestra/oculta los enlaces de la barra de navegacion segun el rol activo.
function actualizarNavegacion() {
  document.querySelectorAll('[data-nav]').forEach(function (elemento) {
    const grupo = elemento.dataset.nav;
    if (grupo === 'activo') {
      elemento.style.display = estado.rol ? '' : 'none';
    } else {
      elemento.style.display = estado.rol === grupo ? '' : 'none';
    }
  });

  const insignia = document.getElementById('badge-rol');
  if (insignia) {
    insignia.textContent = estado.rol === 'coach'
      ? 'Rol: Coach/Administrador'
      : (estado.rol === 'cliente' ? 'Rol: Cliente' : '');
  }
}

document.addEventListener('DOMContentLoaded', function () {
  // Conecta cada enlace de la barra de navegacion con su pantalla.
  // Si el enlace trae data-modo, se guarda en el estado antes de
  // navegar (usado por "Rutinas"/"Medidas", que reutilizan el listado
  // de clientes en un modo distinto al de "Clientes").
  const enlaces = document.querySelectorAll('[data-pantalla]');
  enlaces.forEach(function (enlace) {
    enlace.addEventListener('click', function (evento) {
      evento.preventDefault();
      estado.modoSeleccionCliente = enlace.dataset.modo || null;
      cargarPantalla(enlace.dataset.pantalla);
    });
  });

  document.getElementById('enlace-cambiar-rol').addEventListener('click', function (evento) {
    evento.preventDefault();
    volverAlSelectorDeRol();
  });

  actualizarNavegacion();
  cargarPantalla('inicio');
});
