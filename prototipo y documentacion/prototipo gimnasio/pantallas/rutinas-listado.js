/* HU-RUT - Listado de rutinas de un cliente (Coach/Administrador) */

registrarPantalla('rutinas-listado', function (contenedor) {
  const cliente = obtenerClientePorId(estado.clienteEnFocoId);

  if (!cliente) {
    contenedor.innerHTML = '<p class="mensaje-vacio">No se encontro el cliente seleccionado.</p>';
    return;
  }

  const rutinas = rutinasDeCliente(cliente.id);
  const claseEstado = cliente.estado === 'Activo' ? 'estado-activo' : 'estado-inactivo';

  const listaRutinas = rutinas.length
    ? `
      <table>
        <thead>
          <tr>
            <th>Rutina</th>
            <th>Fecha de asignacion</th>
            <th>Ejercicios</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          ${rutinas.map(function (rutina) {
            return `
              <tr>
                <td>${rutina.nombre}</td>
                <td>${rutina.fecha}</td>
                <td>${rutina.ejercicios.length}</td>
                <td>
                  <button type="button" class="boton boton-secundario boton-pequeno" data-id="${rutina.id}">
                    Ver / editar ejercicios
                  </button>
                </td>
              </tr>
            `;
          }).join('')}
        </tbody>
      </table>
    `
    : '<p class="mensaje-vacio">Este cliente aun no tiene rutinas asignadas.</p>';

  contenedor.innerHTML = `
    <section class="tarjeta">
      <p class="texto-suave"><a href="#" id="enlace-volver-clientes">&larr; Volver al listado de clientes</a></p>
      <h1>Rutinas de ${cliente.nombre} <span class="estado-pill ${claseEstado}">${cliente.estado}</span></h1>

      ${listaRutinas}

      <div class="acciones-formulario" style="justify-content: flex-start; margin-top: var(--espaciado-lg);">
        <button type="button" class="boton boton-primario" id="boton-nueva-rutina">+ Nueva rutina</button>
      </div>
    </section>
  `;

  contenedor.querySelector('#enlace-volver-clientes').addEventListener('click', function (evento) {
    evento.preventDefault();
    estado.modoSeleccionCliente = null;
    cargarPantalla('clientes-listado');
  });

  contenedor.querySelector('#boton-nueva-rutina').addEventListener('click', function () {
    cargarPantalla('rutina-nueva');
  });

  contenedor.querySelectorAll('[data-id]').forEach(function (boton) {
    boton.addEventListener('click', function () {
      estado.rutinaEnFocoId = boton.dataset.id;
      cargarPantalla('rutina-ejercicios');
    });
  });
});
