/* HU-MED - Historial de mediciones de un cliente (Coach/Administrador) */

registrarPantalla('mediciones-listado', function (contenedor) {
  const cliente = obtenerClientePorId(estado.clienteEnFocoId);

  if (!cliente) {
    contenedor.innerHTML = '<p class="mensaje-vacio">No se encontro el cliente seleccionado.</p>';
    return;
  }

  const mediciones = medicionesDeCliente(cliente.id);

  const valor = function (numero) { return numero === null || numero === undefined ? '-' : numero; };

  const tabla = mediciones.length
    ? `
      <table>
        <thead>
          <tr>
            <th>Fecha</th>
            <th>Peso (kg)</th>
            <th>Cintura (cm)</th>
            <th>Cadera (cm)</th>
            <th>Brazo (cm)</th>
            <th>Pierna (cm)</th>
            <th>% grasa</th>
          </tr>
        </thead>
        <tbody>
          ${mediciones.map(function (m) {
            return `
              <tr>
                <td>${m.fecha}</td>
                <td>${valor(m.peso)}</td>
                <td>${valor(m.cintura)}</td>
                <td>${valor(m.cadera)}</td>
                <td>${valor(m.brazo)}</td>
                <td>${valor(m.pierna)}</td>
                <td>${valor(m.grasa)}</td>
              </tr>
            `;
          }).join('')}
        </tbody>
      </table>
    `
    : '<p class="mensaje-vacio">Este cliente aun no tiene mediciones registradas.</p>';

  contenedor.innerHTML = `
    <section class="tarjeta">
      <p class="texto-suave"><a href="#" id="enlace-volver-clientes">&larr; Volver al listado de clientes</a></p>
      <h1>Mediciones de ${cliente.nombre}</h1>

      ${tabla}

      <div class="acciones-formulario" style="justify-content: flex-start; margin-top: var(--espaciado-lg);">
        <button type="button" class="boton boton-primario" id="boton-nueva-medicion">+ Registrar medicion</button>
      </div>
    </section>
  `;

  contenedor.querySelector('#enlace-volver-clientes').addEventListener('click', function (evento) {
    evento.preventDefault();
    estado.modoSeleccionCliente = null;
    cargarPantalla('clientes-listado');
  });

  contenedor.querySelector('#boton-nueva-medicion').addEventListener('click', function () {
    cargarPantalla('medicion-nueva');
  });
});
