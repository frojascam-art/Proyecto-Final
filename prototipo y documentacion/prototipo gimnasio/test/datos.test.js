// Pruebas unitarias para js/datos.js usando el runner integrado de Node
// (node:test + node:assert), sin dependencias externas ni frameworks, para
// respetar la restriccion del proyecto de "cero dependencias sin build".
//
// js/datos.js se carga con vm.createContext() en cada prueba (en vez de
// require()) porque el archivo original define variables globales sueltas
// (const datos, function generarId, etc.) pensadas para un <script> de
// navegador, no un modulo de Node. Esto evita modificar el archivo fuente.

const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const RUTA_DATOS = path.join(__dirname, '..', 'js', 'datos.js');
const CODIGO_DATOS = fs.readFileSync(RUTA_DATOS, 'utf8');

function cargarDatos() {
  const sandbox = {};
  vm.createContext(sandbox);
  vm.runInContext(CODIGO_DATOS, sandbox, { filename: RUTA_DATOS });
  return sandbox;
}

test('obtenerClientePorId retorna el cliente cuando existe', () => {
  const ctx = cargarDatos();
  const cliente = ctx.obtenerClientePorId('cliente-2');
  assert.equal(cliente.nombre, 'Maria Rojas');
});

test('obtenerClientePorId retorna null cuando el id no existe', () => {
  const ctx = cargarDatos();
  assert.equal(ctx.obtenerClientePorId('no-existe'), null);
});

test('clientesFiltrados sin texto retorna todos los clientes', () => {
  const ctx = cargarDatos();
  assert.equal(ctx.clientesFiltrados('').length, ctx.datos.clientes.length);
  assert.equal(ctx.clientesFiltrados(undefined).length, ctx.datos.clientes.length);
});

test('clientesFiltrados busca por nombre sin importar mayusculas/minusculas', () => {
  const ctx = cargarDatos();
  const resultado = ctx.clientesFiltrados('MARIA');
  assert.equal(resultado.length, 1);
  assert.equal(resultado[0].id, 'cliente-2');
});

test('clientesFiltrados retorna vacio si no hay coincidencias', () => {
  const ctx = cargarDatos();
  assert.deepEqual(ctx.clientesFiltrados('xyz-inexistente'), []);
});

test('clientesActivos solo retorna clientes con estado Activo', () => {
  const ctx = cargarDatos();
  const activos = ctx.clientesActivos();
  assert.ok(activos.every((c) => c.estado === 'Activo'));
  assert.ok(!activos.some((c) => c.id === 'cliente-3'));
});

test('existeCorreoDuplicado detecta coincidencia sin importar mayusculas/minusculas', () => {
  const ctx = cargarDatos();
  assert.equal(ctx.existeCorreoDuplicado('JUAN.PEREZ@example.com'), true);
});

test('existeCorreoDuplicado retorna false para correo vacio o no registrado', () => {
  const ctx = cargarDatos();
  assert.equal(ctx.existeCorreoDuplicado(''), false);
  assert.equal(ctx.existeCorreoDuplicado(null), false);
  assert.equal(ctx.existeCorreoDuplicado('nadie@example.com'), false);
});

test('nombreCoach retorna el nombre del coach asignado', () => {
  const ctx = cargarDatos();
  assert.equal(ctx.nombreCoach('coach-1'), 'Coach Ana Marin');
});

test('nombreCoach retorna "Sin asignar" para un id desconocido', () => {
  const ctx = cargarDatos();
  assert.equal(ctx.nombreCoach('coach-inexistente'), 'Sin asignar');
});

test('rutinasDeCliente retorna solo las rutinas del cliente indicado', () => {
  const ctx = cargarDatos();
  const rutinas = ctx.rutinasDeCliente('cliente-1');
  assert.equal(rutinas.length, 1);
  assert.equal(rutinas[0].id, 'rutina-1');
});

test('rutinaActivaDeCliente retorna null si el cliente no tiene rutinas', () => {
  const ctx = cargarDatos();
  assert.equal(ctx.rutinaActivaDeCliente('cliente-3'), null);
});

test('obtenerRutinaPorId encuentra y no encuentra correctamente', () => {
  const ctx = cargarDatos();
  assert.equal(ctx.obtenerRutinaPorId('rutina-2').nombre, 'Cardio - Lunes');
  assert.equal(ctx.obtenerRutinaPorId('rutina-inexistente'), null);
});

test('eliminarRutina quita la rutina del arreglo de datos', () => {
  const ctx = cargarDatos();
  const totalAntes = ctx.datos.rutinas.length;
  ctx.eliminarRutina('rutina-1');
  assert.equal(ctx.datos.rutinas.length, totalAntes - 1);
  assert.equal(ctx.obtenerRutinaPorId('rutina-1'), null);
});

test('eliminarRutina no falla si el id no existe', () => {
  const ctx = cargarDatos();
  const totalAntes = ctx.datos.rutinas.length;
  assert.doesNotThrow(() => ctx.eliminarRutina('no-existe'));
  assert.equal(ctx.datos.rutinas.length, totalAntes);
});

test('medicionesDeCliente filtra por cliente y ordena por fecha descendente', () => {
  const ctx = cargarDatos();
  ctx.datos.mediciones.push({
    id: 'medicion-2',
    clienteId: 'cliente-1',
    fecha: '2026-09-01',
    peso: 76,
    cintura: 85,
    cadera: null,
    brazo: 36,
    pierna: null,
    grasa: 17
  });

  const mediciones = ctx.medicionesDeCliente('cliente-1');
  assert.equal(mediciones.length, 2);
  assert.equal(mediciones[0].id, 'medicion-2');
  assert.equal(mediciones[1].id, 'medicion-1');
});

test('existeMedicionEnFecha detecta duplicados e ignora el id excluido', () => {
  const ctx = cargarDatos();
  assert.equal(ctx.existeMedicionEnFecha('cliente-1', '2026-08-01'), true);
  assert.equal(ctx.existeMedicionEnFecha('cliente-1', '2026-08-01', 'medicion-1'), false);
  assert.equal(ctx.existeMedicionEnFecha('cliente-1', '2099-01-01'), false);
});

test('generarId produce ids unicos e incrementales con el prefijo dado', () => {
  const ctx = cargarDatos();
  const id1 = ctx.generarId('cliente');
  const id2 = ctx.generarId('cliente');
  assert.notEqual(id1, id2);
  assert.ok(id1.startsWith('cliente-'));
  assert.ok(id2.startsWith('cliente-'));
});
