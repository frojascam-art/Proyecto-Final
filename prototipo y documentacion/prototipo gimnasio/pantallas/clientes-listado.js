/* HU-CLI - Listado de clientes (Coach/Administrador)
   Reutilizada por los enlaces de menu "Clientes" (modo normal),
   "Rutinas" y "Medidas" (modo seleccion, ver estado.modoSeleccionCliente). */

registrarPantalla('clientes-listado', function (contenedor) {
  const modo = estado.modoSeleccionCliente; // 'rutinas' | 'mediciones' | null

  const titulos = {
    rutinas: 'Selecciona un cliente para ver sus rutinas',
    mediciones: 'Selecciona un cliente para ver sus mediciones'
  };
  const titulo = titulos[modo] || 'Listado de clientes';

  contenedor.innerHTML = `
    <section class="tarjeta">
      <div class="fila" style="justify-content: space-between; align-items: center;">
        <h1>${titulo}</h1>
        ${modo ? '' : '<button type="button" class="boton boton-primario" id="boton-nuevo-cliente">+ Nuevo cliente</button>'}
      </div>

      <div class="campo campo-busqueda">
        <label for="input-busqueda-cliente">Buscar por nombre</label>
        <input type="text" id="input-busqueda-cliente" placeholder="Ej. Juan Perez">
      </div>

      <div id="zona-tabla-clientes"></div>
    </section>
  `;

  if (!modo) {
    contenedor.querySelector('#boton-nuevo-cliente').addEventListener('click', function () {
      cargarPantalla('cliente-nuevo');
    });
  }

  const zonaTabla = contenedor.querySelector('#zona-tabla-clientes');
  const inputBusqueda = contenedor.querySelector('#input-busqueda-cliente');

  function pintarTabla() {
    const clientes = clientesFiltrados(inputBusqueda.value);

    if (!clientes.length) {
      zonaTabla.innerHTML = '<p class="mensaje-vacio">No se encontraron clientes.</p>';
      return;
    }

    const filas = clientes.map(function (cliente) {
      const claseEstado = cliente.estado === 'Activo' ? 'estado-activo' : 'estado-inactivo';
      let acciones;

      if (modo === 'rutinas') {
        acciones = `<button type="button" class="boton boton-secundario boton-pequeno" data-accion="ver-rutinas" data-id="${cliente.id}">Ver rutinas</button>`;
      } else if (modo === 'mediciones') {
        acciones = `<button type="button" class="boton boton-secundario boton-pequeno" data-accion="ver-mediciones" data-id="${cliente.id}">Ver mediciones</button>`;
      } else {
        acciones = `
          <div class="acciones-tabla">
            <button type="button" class="boton boton-secundario boton-pequeno" data-accion="ver-rutinas" data-id="${cliente.id}">Ver rutinas</button>
            <button type="button" class="boton boton-secundario boton-pequeno" data-accion="ver-mediciones" data-id="${cliente.id}">Ver mediciones</button>
            <button type="button" class="boton boton-secundario boton-pequeno" data-accion="registrar-medicion" data-id="${cliente.id}">Registrar medicion</button>
          </div>
        `;
      }

      return `
        <tr>
          <td>${cliente.nombre}</td>
          <td>${cliente.correo || cliente.telefono || '-'}</td>
          <td><span class="estado-pill ${claseEstado}">${cliente.estado}</span></td>
          <td>${nombreCoach(cliente.coachId)}</td>
          <td>${acciones}</td>
        </tr>
      `;
    }).join('');

    zonaTabla.innerHTML = `
      <table>
        <thead>
          <tr>
            <th>Nombre completo</th>
            <th>Contacto</th>
            <th>Estado</th>
            <th>Coach asignado</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>${filas}</tbody>
      </table>
    `;

    zonaTabla.querySelectorAll('[data-accion]').forEach(function (boton) {
      boton.addEventListener('click', function () {
        const clienteId = boton.dataset.id;
        estado.clienteEnFocoId = clienteId;
        if (boton.dataset.accion === 'ver-rutinas') {
          cargarPantalla('rutinas-listado');
        } else if (boton.dataset.accion === 'ver-mediciones') {
          cargarPantalla('mediciones-listado');
        } else if (boton.dataset.accion === 'registrar-medicion') {
          cargarPantalla('medicion-nueva');
        }
      });
    });
  }

  inputBusqueda.addEventListener('input', pintarTabla);
  pintarTabla();
});
