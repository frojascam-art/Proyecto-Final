/* HU3.2 - Agregar ejercicios a la rutina (Coach/Administrador)
   HU3.3 - Formulario "Agregar ejercicio" (peso sugerido condicional),
   implementado como modal dentro de esta misma pantalla. */

registrarPantalla('rutina-ejercicios', function (contenedor) {
  const rutina = obtenerRutinaPorId(estado.rutinaEnFocoId);

  if (!rutina) {
    contenedor.innerHTML = '<p class="mensaje-vacio">No se encontro la rutina seleccionada.</p>';
    return;
  }

  const cliente = obtenerClientePorId(rutina.clienteId);

  contenedor.innerHTML = `
    <section class="tarjeta">
      <p class="texto-suave"><a href="#" id="enlace-volver-rutinas">&larr; Volver a rutinas de ${cliente.nombre}</a></p>
      <h1>${rutina.nombre} <span class="texto-suave">(Cliente: ${cliente.nombre})</span></h1>

      <div id="zona-tabla-ejercicios"></div>

      <div class="acciones-formulario" style="justify-content: space-between; margin-top: var(--espaciado-lg);">
        <button type="button" class="boton boton-secundario" id="boton-agregar-ejercicio">+ Agregar ejercicio</button>
        <button type="button" class="boton boton-primario" id="boton-guardar-rutina">Guardar rutina</button>
      </div>
    </section>

    <div class="fondo-modal" id="fondo-modal" style="display:none;">
      <div class="modal">
        <h2>Agregar ejercicio</h2>
        <div id="zona-mensajes-modal"></div>
        <form id="form-ejercicio" novalidate>
          <div class="campo">
            <label for="input-ejercicio">Ejercicio</label>
            <input type="text" id="input-ejercicio">
            <div class="error-campo" data-error-para="ejercicio"></div>
          </div>

          <div class="campo">
            <label>Tipo de ejercicio</label>
            <div class="opciones-radio">
              <label><input type="radio" name="tipo-ejercicio" value="con-peso" checked> Con peso</label>
              <label><input type="radio" name="tipo-ejercicio" value="sin-peso"> Sin peso</label>
            </div>
          </div>

          <div class="campo" id="campo-peso-sugerido">
            <label for="input-peso">Peso sugerido</label>
            <div class="campo-con-unidad">
              <input type="number" id="input-peso" min="0" step="0.5">
              <select id="select-unidad">
                <option value="kg">kg</option>
                <option value="lb">lb</option>
              </select>
            </div>
          </div>

          <div class="campo">
            <label for="input-series">Series</label>
            <input type="text" id="input-series">
            <div class="error-campo" data-error-para="series"></div>
          </div>

          <div class="campo">
            <label for="input-repeticiones">Repeticiones</label>
            <input type="text" id="input-repeticiones">
            <div class="error-campo" data-error-para="repeticiones"></div>
          </div>

          <div class="campo">
            <label for="input-descanso">Descanso</label>
            <input type="text" id="input-descanso" placeholder="Ej. 60 seg">
            <div class="error-campo" data-error-para="descanso"></div>
          </div>

          <div class="acciones-formulario">
            <button type="button" class="boton boton-secundario" id="boton-cancelar-modal">Cancelar</button>
            <button type="submit" class="boton boton-primario">Guardar</button>
          </div>
        </form>
      </div>
    </div>
  `;

  const zonaTabla = contenedor.querySelector('#zona-tabla-ejercicios');
  const fondoModal = contenedor.querySelector('#fondo-modal');
  const formEjercicio = contenedor.querySelector('#form-ejercicio');
  const campoPesoSugerido = contenedor.querySelector('#campo-peso-sugerido');

  function textoPeso(ejercicio) {
    if (!ejercicio.tipoConPeso) return '-';
    if (ejercicio.pesoPorDefinir) return 'Peso a definir';
    return ejercicio.peso + ' ' + ejercicio.unidad;
  }

  function pintarTabla() {
    if (!rutina.ejercicios.length) {
      zonaTabla.innerHTML = '<p class="mensaje-vacio">Esta rutina aun no tiene ejercicios. Use "+ Agregar ejercicio".</p>';
      return;
    }

    zonaTabla.innerHTML = `
      <table>
        <thead>
          <tr>
            <th>Orden</th>
            <th>Ejercicio</th>
            <th>Series</th>
            <th>Repeticiones</th>
            <th>Descanso</th>
            <th>Peso sugerido</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          ${rutina.ejercicios.map(function (ejercicio, indice) {
            return `
              <tr>
                <td>${indice + 1}</td>
                <td>${ejercicio.nombre}</td>
                <td>${ejercicio.series}</td>
                <td>${ejercicio.repeticiones}</td>
                <td>${ejercicio.descanso}</td>
                <td>${textoPeso(ejercicio)}</td>
                <td class="acciones-tabla">
                  <button type="button" class="boton boton-secundario boton-pequeno" data-mover="arriba" data-indice="${indice}" ${indice === 0 ? 'disabled' : ''}>^</button>
                  <button type="button" class="boton boton-secundario boton-pequeno" data-mover="abajo" data-indice="${indice}" ${indice === rutina.ejercicios.length - 1 ? 'disabled' : ''}>v</button>
                </td>
              </tr>
            `;
          }).join('')}
        </tbody>
      </table>
    `;

    zonaTabla.querySelectorAll('[data-mover]').forEach(function (boton) {
      boton.addEventListener('click', function () {
        const indice = Number(boton.dataset.indice);
        const destino = boton.dataset.mover === 'arriba' ? indice - 1 : indice + 1;
        const temporal = rutina.ejercicios[indice];
        rutina.ejercicios[indice] = rutina.ejercicios[destino];
        rutina.ejercicios[destino] = temporal;
        pintarTabla();
      });
    });
  }

  function actualizarVisibilidadPeso() {
    const tipo = formEjercicio.querySelector('input[name="tipo-ejercicio"]:checked').value;
    campoPesoSugerido.style.display = tipo === 'con-peso' ? '' : 'none';
  }

  formEjercicio.querySelectorAll('input[name="tipo-ejercicio"]').forEach(function (radio) {
    radio.addEventListener('change', actualizarVisibilidadPeso);
  });

  function abrirModal() {
    formEjercicio.reset();
    contenedor.querySelector('#zona-mensajes-modal').innerHTML = '';
    contenedor.querySelectorAll('#form-ejercicio .error-campo').forEach(function (el) { el.textContent = ''; });
    actualizarVisibilidadPeso();
    fondoModal.style.display = 'flex';
  }

  function cerrarModal() {
    fondoModal.style.display = 'none';
  }

  contenedor.querySelector('#boton-agregar-ejercicio').addEventListener('click', abrirModal);
  contenedor.querySelector('#boton-cancelar-modal').addEventListener('click', cerrarModal);

  formEjercicio.addEventListener('submit', function (evento) {
    evento.preventDefault();
    contenedor.querySelectorAll('#form-ejercicio .error-campo').forEach(function (el) { el.textContent = ''; });

    const nombreEjercicio = document.getElementById('input-ejercicio').value.trim();
    const tipoConPeso = formEjercicio.querySelector('input[name="tipo-ejercicio"]:checked').value === 'con-peso';
    const valorPeso = document.getElementById('input-peso').value;
    const unidad = document.getElementById('select-unidad').value;
    const series = document.getElementById('input-series').value.trim();
    const repeticiones = document.getElementById('input-repeticiones').value.trim();
    const descanso = document.getElementById('input-descanso').value.trim();

    let tieneErrores = false;
    if (!nombreEjercicio) {
      contenedor.querySelector('[data-error-para="ejercicio"]').textContent = 'El nombre del ejercicio es obligatorio.';
      tieneErrores = true;
    }
    if (!series) {
      contenedor.querySelector('[data-error-para="series"]').textContent = 'Las series son obligatorias.';
      tieneErrores = true;
    }
    if (!repeticiones) {
      contenedor.querySelector('[data-error-para="repeticiones"]').textContent = 'Las repeticiones son obligatorias.';
      tieneErrores = true;
    }
    if (!descanso) {
      contenedor.querySelector('[data-error-para="descanso"]').textContent = 'El descanso es obligatorio.';
      tieneErrores = true;
    }
    if (tieneErrores) return;

    rutina.ejercicios.push({
      id: generarId('ejercicio'),
      nombre: nombreEjercicio,
      tipoConPeso: tipoConPeso,
      peso: tipoConPeso && valorPeso ? Number(valorPeso) : null,
      unidad: tipoConPeso ? unidad : null,
      pesoPorDefinir: tipoConPeso && !valorPeso,
      series: series,
      repeticiones: repeticiones,
      descanso: descanso
    });

    cerrarModal();
    pintarTabla();
  });

  contenedor.querySelector('#enlace-volver-rutinas').addEventListener('click', function (evento) {
    evento.preventDefault();
    cargarPantalla('rutinas-listado');
  });

  contenedor.querySelector('#boton-guardar-rutina').addEventListener('click', function () {
    cargarPantalla('rutinas-listado');
  });

  pintarTabla();
});
