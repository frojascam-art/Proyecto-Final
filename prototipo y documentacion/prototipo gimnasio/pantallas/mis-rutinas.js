/* HU4 - Mis rutinas (Vista del cliente/alumno).
   Tambien accesible en modo lectura para el rol coach (revisa como la
   ve el cliente en foco), reutilizando estado.clienteEnFocoId. */

registrarPantalla('mis-rutinas', function (contenedor) {
  const cliente = obtenerClientePorId(estado.clienteEnFocoId);

  if (!cliente) {
    contenedor.innerHTML = '<p class="mensaje-vacio">No se encontro el cliente actual.</p>';
    return;
  }

  const rutinas = rutinasDeCliente(cliente.id);

  if (!rutinas.length) {
    contenedor.innerHTML = `
      <section class="tarjeta">
        <h1>Mis rutinas</h1>
        <p class="mensaje-vacio">Aun no tienes rutinas asignadas. Contacta a tu coach.</p>
      </section>
    `;
    return;
  }

  contenedor.innerHTML = `
    <section class="tarjeta">
      <h1>Mis rutinas</h1>
      <div class="fila">
        <div class="columna">
          <h2>Rutinas vigentes</h2>
          <ul class="lista-rutinas" id="lista-rutinas">
            ${rutinas.map(function (rutina, indice) {
              return `
                <li data-id="${rutina.id}" class="${indice === 0 ? 'seleccionada' : ''}">
                  ${rutina.nombre}
                  <span class="fecha-rutina">Asignada: ${rutina.fecha}</span>
                </li>
              `;
            }).join('')}
          </ul>
        </div>
        <div class="columna" id="zona-detalle-rutina"></div>
      </div>
    </section>
  `;

  const listaRutinas = contenedor.querySelector('#lista-rutinas');
  const zonaDetalle = contenedor.querySelector('#zona-detalle-rutina');

  function textoPeso(ejercicio) {
    if (!ejercicio.tipoConPeso) return '-';
    if (ejercicio.pesoPorDefinir) return 'Peso a definir';
    return ejercicio.peso + ' ' + ejercicio.unidad;
  }

  function pintarDetalle(rutina) {
    if (!rutina.ejercicios.length) {
      zonaDetalle.innerHTML = `
        <h2>Detalle: ${rutina.nombre}</h2>
        <p class="mensaje-vacio">Esta rutina todavia no tiene ejercicios.</p>
      `;
      return;
    }

    zonaDetalle.innerHTML = `
      <h2>Detalle: ${rutina.nombre}</h2>
      <table>
        <thead>
          <tr>
            <th>Ejercicio</th>
            <th>Series</th>
            <th>Repeticiones</th>
            <th>Descanso</th>
            <th>Peso sugerido</th>
          </tr>
        </thead>
        <tbody>
          ${rutina.ejercicios.map(function (ejercicio) {
            return `
              <tr>
                <td>${ejercicio.nombre}</td>
                <td>${ejercicio.series}</td>
                <td>${ejercicio.repeticiones}</td>
                <td>${ejercicio.descanso}</td>
                <td>${textoPeso(ejercicio)}</td>
              </tr>
            `;
          }).join('')}
        </tbody>
      </table>
    `;
  }

  listaRutinas.querySelectorAll('li').forEach(function (elemento) {
    elemento.addEventListener('click', function () {
      listaRutinas.querySelectorAll('li').forEach(function (li) { li.classList.remove('seleccionada'); });
      elemento.classList.add('seleccionada');
      const rutina = obtenerRutinaPorId(elemento.dataset.id);
      pintarDetalle(rutina);
    });
  });

  pintarDetalle(rutinas[0]);
});
