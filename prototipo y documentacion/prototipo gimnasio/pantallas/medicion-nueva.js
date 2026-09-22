/* HU5 - Registrar medicion (Coach/Administrador) */

registrarPantalla('medicion-nueva', function (contenedor) {
  const cliente = obtenerClientePorId(estado.clienteEnFocoId);

  if (!cliente) {
    contenedor.innerHTML = '<p class="mensaje-vacio">No se encontro el cliente seleccionado.</p>';
    return;
  }

  contenedor.innerHTML = `
    <section class="tarjeta formulario">
      <h1>Registrar medicion <span class="texto-suave">(Cliente: ${cliente.nombre})</span></h1>
      <div id="zona-mensajes"></div>

      <form id="form-medicion" novalidate>
        <div class="campo">
          <label for="input-fecha">Fecha</label>
          <input type="date" id="input-fecha">
          <div class="error-campo" data-error-para="fecha"></div>
        </div>

        <div class="campo">
          <label for="input-peso">Peso (kg)</label>
          <input type="number" id="input-peso" min="0" step="0.1">
          <div class="error-campo" data-error-para="peso"></div>
        </div>

        <div class="campo">
          <label for="input-cintura">Cintura (cm)</label>
          <input type="number" id="input-cintura" min="0" step="0.1">
        </div>

        <div class="campo">
          <label for="input-cadera">Cadera (cm)</label>
          <input type="number" id="input-cadera" min="0" step="0.1">
        </div>

        <div class="campo">
          <label for="input-brazo">Brazo (cm)</label>
          <input type="number" id="input-brazo" min="0" step="0.1">
        </div>

        <div class="campo">
          <label for="input-pierna">Pierna (cm)</label>
          <input type="number" id="input-pierna" min="0" step="0.1">
        </div>

        <div class="campo">
          <label for="input-grasa">% de grasa corporal</label>
          <input type="number" id="input-grasa" min="0" max="100" step="0.1">
          <div class="error-campo" data-error-para="antropometrica"></div>
        </div>

        <div class="acciones-formulario">
          <button type="button" class="boton boton-secundario" id="boton-cancelar">Cancelar</button>
          <button type="submit" class="boton boton-primario">Guardar medicion</button>
        </div>
      </form>
    </section>
  `;

  const zonaMensajes = contenedor.querySelector('#zona-mensajes');

  contenedor.querySelector('#boton-cancelar').addEventListener('click', function () {
    cargarPantalla('mediciones-listado');
  });

  function guardarMedicion(fecha, peso, medidas, sobrescribirId) {
    if (sobrescribirId) {
      const indice = datos.mediciones.findIndex(function (m) { return m.id === sobrescribirId; });
      datos.mediciones[indice] = Object.assign({ id: sobrescribirId, clienteId: cliente.id, fecha: fecha, peso: peso }, medidas);
    } else {
      datos.mediciones.push(Object.assign({ id: generarId('medicion'), clienteId: cliente.id, fecha: fecha, peso: peso }, medidas));
    }
    cargarPantalla('mediciones-listado');
  }

  contenedor.querySelector('#form-medicion').addEventListener('submit', function (evento) {
    evento.preventDefault();
    zonaMensajes.innerHTML = '';
    contenedor.querySelectorAll('.error-campo').forEach(function (el) { el.textContent = ''; });

    const fecha = document.getElementById('input-fecha').value;
    const peso = document.getElementById('input-peso').value;
    const camposOpcionales = {
      cintura: document.getElementById('input-cintura').value,
      cadera: document.getElementById('input-cadera').value,
      brazo: document.getElementById('input-brazo').value,
      pierna: document.getElementById('input-pierna').value,
      grasa: document.getElementById('input-grasa').value
    };

    let tieneErrores = false;
    if (!fecha) {
      contenedor.querySelector('[data-error-para="fecha"]').textContent = 'La fecha es obligatoria.';
      tieneErrores = true;
    }
    if (!peso) {
      contenedor.querySelector('[data-error-para="peso"]').textContent = 'El peso es obligatorio.';
      tieneErrores = true;
    }
    const hayAlMenosUnaMedida = Object.keys(camposOpcionales).some(function (clave) { return camposOpcionales[clave] !== ''; });
    if (!hayAlMenosUnaMedida) {
      contenedor.querySelector('[data-error-para="antropometrica"]').textContent = 'Registre al menos una medida antropometrica ademas del peso.';
      tieneErrores = true;
    }

    if (tieneErrores) return;

    const medidas = {
      cintura: camposOpcionales.cintura ? Number(camposOpcionales.cintura) : null,
      cadera: camposOpcionales.cadera ? Number(camposOpcionales.cadera) : null,
      brazo: camposOpcionales.brazo ? Number(camposOpcionales.brazo) : null,
      pierna: camposOpcionales.pierna ? Number(camposOpcionales.pierna) : null,
      grasa: camposOpcionales.grasa ? Number(camposOpcionales.grasa) : null
    };

    const medicionExistente = datos.mediciones.find(function (m) {
      return m.clienteId === cliente.id && m.fecha === fecha;
    });

    if (medicionExistente) {
      zonaMensajes.innerHTML = `
        <div class="mensaje mensaje-advertencia">
          Ya existe una medicion para este cliente en esa fecha. Desea sobrescribirla?
          <div class="acciones-mensaje">
            <button type="button" class="boton boton-secundario boton-pequeno" id="boton-sobrescribir">Sobrescribir</button>
            <button type="button" class="boton boton-secundario boton-pequeno" id="boton-cancelar-sobrescritura">Cancelar</button>
          </div>
        </div>
      `;
      zonaMensajes.querySelector('#boton-sobrescribir').addEventListener('click', function () {
        guardarMedicion(fecha, Number(peso), medidas, medicionExistente.id);
      });
      zonaMensajes.querySelector('#boton-cancelar-sobrescritura').addEventListener('click', function () {
        zonaMensajes.innerHTML = '';
      });
      return;
    }

    guardarMedicion(fecha, Number(peso), medidas, null);
  });
});
