/* HU2 - Registro de cliente (Coach/Administrador) */

registrarPantalla('cliente-nuevo', function (contenedor) {
  const opcionesCoach = datos.coaches.map(function (coach) {
    return `<option value="${coach.id}">${coach.nombre}</option>`;
  }).join('');

  contenedor.innerHTML = `
    <section class="tarjeta formulario">
      <h1>Nuevo cliente</h1>
      <div id="zona-mensajes"></div>

      <form id="form-cliente-nuevo" novalidate>
        <div class="campo">
          <label for="input-nombre">Nombre completo</label>
          <input type="text" id="input-nombre">
          <div class="error-campo" data-error-para="nombre"></div>
        </div>

        <div class="campo">
          <label for="input-correo">Correo electronico</label>
          <input type="email" id="input-correo">
          <div class="error-campo" data-error-para="correo"></div>
        </div>

        <div class="campo">
          <label for="input-telefono">Telefono</label>
          <input type="text" id="input-telefono">
          <div class="error-campo" data-error-para="contacto"></div>
        </div>

        <div class="campo">
          <label>Estado</label>
          <div class="opciones-radio">
            <label><input type="radio" name="estado" value="Activo" checked> Activo</label>
            <label><input type="radio" name="estado" value="Inactivo"> Inactivo</label>
          </div>
        </div>

        <div class="campo">
          <label for="select-coach">Coach asignado</label>
          <select id="select-coach">
            <option value="">Seleccionar coach</option>
            ${opcionesCoach}
          </select>
          <div class="error-campo" data-error-para="coach"></div>
        </div>

        <div class="acciones-formulario">
          <button type="button" class="boton boton-secundario" id="boton-cancelar">Cancelar</button>
          <button type="submit" class="boton boton-primario">Guardar cliente</button>
        </div>
      </form>
    </section>
  `;

  const zonaMensajes = contenedor.querySelector('#zona-mensajes');

  function limpiarErrores() {
    zonaMensajes.innerHTML = '';
    contenedor.querySelectorAll('.error-campo').forEach(function (el) { el.textContent = ''; });
    contenedor.querySelectorAll('.campo-invalido').forEach(function (el) { el.classList.remove('campo-invalido'); });
  }

  function marcarError(idCampo, claveError, texto) {
    document.getElementById(idCampo).classList.add('campo-invalido');
    contenedor.querySelector('[data-error-para="' + claveError + '"]').textContent = texto;
  }

  contenedor.querySelector('#boton-cancelar').addEventListener('click', function () {
    cargarPantalla('clientes-listado');
  });

  contenedor.querySelector('#form-cliente-nuevo').addEventListener('submit', function (evento) {
    evento.preventDefault();
    limpiarErrores();

    const nombre = document.getElementById('input-nombre').value.trim();
    const correo = document.getElementById('input-correo').value.trim();
    const telefono = document.getElementById('input-telefono').value.trim();
    const estadoCliente = contenedor.querySelector('input[name="estado"]:checked').value;
    const coachId = document.getElementById('select-coach').value;

    let tieneErrores = false;

    if (!nombre) {
      marcarError('input-nombre', 'nombre', 'El nombre completo es obligatorio.');
      tieneErrores = true;
    }
    if (!correo && !telefono) {
      marcarError('input-correo', 'contacto', 'Ingrese al menos un correo o un telefono.');
      tieneErrores = true;
    }
    if (!coachId) {
      marcarError('select-coach', 'coach', 'Debe seleccionar un coach asignado.');
      tieneErrores = true;
    }

    if (tieneErrores) return;

    if (existeCorreoDuplicado(correo)) {
      zonaMensajes.innerHTML = `
        <div class="mensaje mensaje-advertencia">
          Ya existe un cliente registrado con ese correo. Verifique antes de continuar.
        </div>
      `;
      return;
    }

    datos.clientes.push({
      id: generarId('cliente'),
      nombre: nombre,
      correo: correo,
      telefono: telefono,
      estado: estadoCliente,
      coachId: coachId
    });

    cargarPantalla('clientes-listado');
  });
});
