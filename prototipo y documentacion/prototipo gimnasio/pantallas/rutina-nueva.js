/* HU3.1 - Nueva rutina (Coach/Administrador) */

registrarPantalla('rutina-nueva', function (contenedor) {
  const clientePreseleccionado = obtenerClientePorId(estado.clienteEnFocoId);

  const campoCliente = clientePreseleccionado
    ? `
      <div class="campo">
        <label>Cliente</label>
        <input type="text" value="${clientePreseleccionado.nombre}" disabled>
      </div>
    `
    : `
      <div class="campo">
        <label for="select-cliente">Cliente</label>
        <select id="select-cliente">
          <option value="">Seleccionar cliente</option>
          ${clientesActivos().map(function (c) {
            return `<option value="${c.id}">${c.nombre}</option>`;
          }).join('')}
        </select>
        <div class="error-campo" data-error-para="cliente"></div>
      </div>
    `;

  contenedor.innerHTML = `
    <section class="tarjeta formulario">
      <h1>Nueva rutina</h1>
      <div id="zona-mensajes"></div>

      <form id="form-rutina-nueva" novalidate>
        ${campoCliente}

        <div class="campo">
          <label for="input-nombre-rutina">Nombre de la rutina</label>
          <input type="text" id="input-nombre-rutina">
          <div class="error-campo" data-error-para="nombre"></div>
        </div>

        <div class="acciones-formulario">
          <button type="button" class="boton boton-secundario" id="boton-cancelar">Cancelar</button>
          <button type="submit" class="boton boton-primario">Crear rutina</button>
        </div>
      </form>
    </section>
  `;

  const zonaMensajes = contenedor.querySelector('#zona-mensajes');

  contenedor.querySelector('#boton-cancelar').addEventListener('click', function () {
    cargarPantalla(clientePreseleccionado ? 'rutinas-listado' : 'clientes-listado');
  });

  function crearRutina(clienteId, nombreRutina) {
    const rutina = {
      id: generarId('rutina'),
      clienteId: clienteId,
      nombre: nombreRutina,
      fecha: new Date().toISOString().slice(0, 10),
      ejercicios: []
    };
    datos.rutinas.push(rutina);
    estado.clienteEnFocoId = clienteId;
    estado.rutinaEnFocoId = rutina.id;
    cargarPantalla('rutina-ejercicios');
  }

  contenedor.querySelector('#form-rutina-nueva').addEventListener('submit', function (evento) {
    evento.preventDefault();
    zonaMensajes.innerHTML = '';
    contenedor.querySelectorAll('.error-campo').forEach(function (el) { el.textContent = ''; });

    const clienteId = clientePreseleccionado
      ? clientePreseleccionado.id
      : document.getElementById('select-cliente').value;
    const nombreRutina = document.getElementById('input-nombre-rutina').value.trim();

    let tieneErrores = false;

    if (!clienteId) {
      contenedor.querySelector('[data-error-para="cliente"]').textContent = 'Debe seleccionar un cliente.';
      tieneErrores = true;
    }
    if (!nombreRutina) {
      contenedor.querySelector('[data-error-para="nombre"]').textContent = 'El nombre de la rutina es obligatorio.';
      tieneErrores = true;
    }

    if (tieneErrores) return;

    const rutinaActiva = rutinaActivaDeCliente(clienteId);

    if (rutinaActiva) {
      zonaMensajes.innerHTML = `
        <div class="mensaje mensaje-advertencia">
          Este cliente ya tiene una rutina activa: "${rutinaActiva.nombre}". Desea reemplazarla o mantener ambas?
          <div class="acciones-mensaje">
            <button type="button" class="boton boton-secundario boton-pequeno" id="boton-reemplazar">Reemplazar</button>
            <button type="button" class="boton boton-secundario boton-pequeno" id="boton-mantener-ambas">Mantener ambas</button>
          </div>
        </div>
      `;

      zonaMensajes.querySelector('#boton-reemplazar').addEventListener('click', function () {
        eliminarRutina(rutinaActiva.id);
        crearRutina(clienteId, nombreRutina);
      });

      zonaMensajes.querySelector('#boton-mantener-ambas').addEventListener('click', function () {
        crearRutina(clienteId, nombreRutina);
      });

      return;
    }

    crearRutina(clienteId, nombreRutina);
  });
});
