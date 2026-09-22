// Pruebas unitarias para el mecanismo generico de pantallas de js/app.js
// (registrarPantalla / cargarPantalla / estado), que es el patron que el
// boilerplate exige reutilizar para toda la navegacion del proyecto.
//
// js/app.js espera un entorno de navegador (document, window). Como aqui
// corremos en Node sin jsdom (para no agregar dependencias), se crea un DOM
// minimo simulado suficiente para ejercitar la logica, sin tocar el archivo
// fuente original.

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const RUTA_APP = path.join(__dirname, '..', 'js', 'app.js');
const CODIGO_APP = fs.readFileSync(RUTA_APP, 'utf8');

function cargarApp() {
  const contenedorPrincipal = { innerHTML: '' };
  const elementosPorId = {
    'contenedor-principal': contenedorPrincipal,
    'enlace-cambiar-rol': { addEventListener() {} }
  };

  const documentoFalso = {
    getElementById(id) {
      return elementosPorId[id] || null;
    },
    querySelectorAll() {
      return [];
    },
    addEventListener() {
      // El listener de DOMContentLoaded nunca se dispara en las pruebas;
      // aqui solo interesa la logica de registrarPantalla/cargarPantalla.
    }
  };

  const sandbox = {
    document: documentoFalso,
    window: { scrollTo() {} }
  };

  vm.createContext(sandbox);
  vm.runInContext(CODIGO_APP, sandbox, { filename: RUTA_APP });

  return { ctx: sandbox, contenedorPrincipal };
}

test('registrarPantalla agrega la funcion al registro de pantallas', () => {
  const { ctx } = cargarApp();
  const render = () => {};
  ctx.registrarPantalla('demo', render);
  assert.equal(ctx.pantallas.demo, render);
});

test('cargarPantalla ejecuta la funcion registrada con el contenedor principal', () => {
  const { ctx, contenedorPrincipal } = cargarApp();
  let contenedorRecibido = null;
  ctx.registrarPantalla('demo', (contenedor) => {
    contenedorRecibido = contenedor;
  });

  ctx.cargarPantalla('demo');
  assert.equal(contenedorRecibido, contenedorPrincipal);
});

test('cargarPantalla muestra mensaje pendiente si la pantalla no existe', () => {
  const { ctx, contenedorPrincipal } = cargarApp();
  ctx.cargarPantalla('pantalla-no-registrada');
  assert.match(contenedorPrincipal.innerHTML, /pendiente de implementar/);
});

test('establecerRol actualiza el estado global y limpia foco previo', () => {
  const { ctx } = cargarApp();
  ctx.estado.rutinaEnFocoId = 'rutina-1';
  ctx.estado.modoSeleccionCliente = 'rutinas';

  ctx.establecerRol('coach', 'cliente-1');

  assert.equal(ctx.estado.rol, 'coach');
  assert.equal(ctx.estado.clienteEnFocoId, 'cliente-1');
  assert.equal(ctx.estado.rutinaEnFocoId, null);
  assert.equal(ctx.estado.modoSeleccionCliente, null);
});

test('volverAlSelectorDeRol limpia el estado y navega a "inicio"', () => {
  const { ctx } = cargarApp();
  let pantallaCargada = null;
  ctx.registrarPantalla('inicio', () => {
    pantallaCargada = 'inicio';
  });

  ctx.establecerRol('cliente', 'cliente-2');
  ctx.volverAlSelectorDeRol();

  assert.equal(ctx.estado.rol, null);
  assert.equal(ctx.estado.clienteEnFocoId, null);
  assert.equal(pantallaCargada, 'inicio');
});
