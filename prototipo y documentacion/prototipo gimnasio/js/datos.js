/* ============================================
   datos.js
   Datos de ejemplo y funciones de acceso/modificacion en memoria.
   No hay backend: todo vive aqui durante la sesion del navegador y se
   reinicia al recargar la pagina.
   ============================================ */

let contadorId = 0;
function generarId(prefijo) {
  contadorId += 1;
  return prefijo + '-' + contadorId;
}

const datos = {
  coaches: [
    { id: 'coach-1', nombre: 'Coach Ana Marin' },
    { id: 'coach-2', nombre: 'Coach Luis Vargas' }
  ],

  clientes: [
    {
      id: 'cliente-1',
      nombre: 'Juan Perez',
      correo: 'juan.perez@example.com',
      telefono: '8888-1111',
      estado: 'Activo',
      coachId: 'coach-1'
    },
    {
      id: 'cliente-2',
      nombre: 'Maria Rojas',
      correo: 'maria.rojas@example.com',
      telefono: '',
      estado: 'Activo',
      coachId: 'coach-2'
    },
    {
      id: 'cliente-3',
      nombre: 'Carlos Solis',
      correo: '',
      telefono: '8888-3333',
      estado: 'Inactivo',
      coachId: 'coach-1'
    }
  ],

  rutinas: [
    {
      id: 'rutina-1',
      clienteId: 'cliente-1',
      nombre: 'Fuerza - Fase 1',
      fecha: '2026-08-01',
      ejercicios: [
        {
          id: 'ejercicio-1',
          nombre: 'Sentadilla',
          tipoConPeso: true,
          peso: 40,
          unidad: 'kg',
          pesoPorDefinir: false,
          series: 4,
          repeticiones: 10,
          descanso: '90 seg'
        },
        {
          id: 'ejercicio-2',
          nombre: 'Press banca',
          tipoConPeso: true,
          peso: 30,
          unidad: 'kg',
          pesoPorDefinir: false,
          series: 3,
          repeticiones: 12,
          descanso: '60 seg'
        },
        {
          id: 'ejercicio-3',
          nombre: 'Plancha',
          tipoConPeso: false,
          peso: null,
          unidad: null,
          pesoPorDefinir: false,
          series: 3,
          repeticiones: '30 seg',
          descanso: '30 seg'
        }
      ]
    },
    {
      id: 'rutina-2',
      clienteId: 'cliente-2',
      nombre: 'Cardio - Lunes',
      fecha: '2026-09-01',
      ejercicios: []
    }
  ],

  mediciones: [
    {
      id: 'medicion-1',
      clienteId: 'cliente-1',
      fecha: '2026-08-01',
      peso: 78,
      cintura: 88,
      cadera: null,
      brazo: 35,
      pierna: null,
      grasa: 18
    }
  ]
};

function obtenerClientePorId(clienteId) {
  return datos.clientes.find(function (c) { return c.id === clienteId; }) || null;
}

function clientesFiltrados(textoBusqueda) {
  const texto = (textoBusqueda || '').trim().toLowerCase();
  if (!texto) return datos.clientes;
  return datos.clientes.filter(function (c) {
    return c.nombre.toLowerCase().indexOf(texto) !== -1;
  });
}

function clientesActivos() {
  return datos.clientes.filter(function (c) { return c.estado === 'Activo'; });
}

function existeCorreoDuplicado(correo) {
  if (!correo) return false;
  return datos.clientes.some(function (c) {
    return c.correo && c.correo.toLowerCase() === correo.toLowerCase();
  });
}

function nombreCoach(coachId) {
  const coach = datos.coaches.find(function (c) { return c.id === coachId; });
  return coach ? coach.nombre : 'Sin asignar';
}

function rutinasDeCliente(clienteId) {
  return datos.rutinas.filter(function (r) { return r.clienteId === clienteId; });
}

function rutinaActivaDeCliente(clienteId) {
  const rutinas = rutinasDeCliente(clienteId);
  return rutinas.length ? rutinas[0] : null;
}

function obtenerRutinaPorId(rutinaId) {
  return datos.rutinas.find(function (r) { return r.id === rutinaId; }) || null;
}

function eliminarRutina(rutinaId) {
  const indice = datos.rutinas.findIndex(function (r) { return r.id === rutinaId; });
  if (indice !== -1) datos.rutinas.splice(indice, 1);
}

function medicionesDeCliente(clienteId) {
  return datos.mediciones
    .filter(function (m) { return m.clienteId === clienteId; })
    .slice()
    .sort(function (a, b) { return b.fecha.localeCompare(a.fecha); });
}

function existeMedicionEnFecha(clienteId, fecha, ignorarId) {
  return datos.mediciones.some(function (m) {
    return m.clienteId === clienteId && m.fecha === fecha && m.id !== ignorarId;
  });
}
