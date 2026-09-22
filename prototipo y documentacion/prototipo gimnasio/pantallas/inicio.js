/* HU1 - Selector de rol / Inicio */

registrarPantalla('inicio', function (contenedor) {
  contenedor.innerHTML = `
    <section class="selector-rol">
      <h1>Sistema de Gimnasio</h1>
      <p class="texto-suave">
        Prototipo de demostracion. Elija con que rol quiere explorarlo;
        podra cambiar de rol en cualquier momento desde la barra superior.
      </p>
      <div class="fila opciones-rol">
        <article class="tarjeta tarjeta-rol" id="tarjeta-rol-coach">
          <h2>Coach / Administrador</h2>
          <p class="texto-suave">Gestione clientes, rutinas y mediciones.</p>
          <button type="button" class="boton boton-primario" id="boton-rol-coach">
            Entrar como Coach/Administrador
          </button>
        </article>
        <article class="tarjeta tarjeta-rol" id="tarjeta-rol-cliente">
          <h2>Cliente</h2>
          <p class="texto-suave">Consulte sus rutinas asignadas.</p>
          <button type="button" class="boton boton-primario" id="boton-rol-cliente">
            Entrar como Cliente
          </button>
        </article>
      </div>
    </section>
  `;

  contenedor.querySelector('#boton-rol-coach').addEventListener('click', function () {
    establecerRol('coach', null);
    cargarPantalla('clientes-listado');
  });

  contenedor.querySelector('#boton-rol-cliente').addEventListener('click', function () {
    // Cliente de ejemplo fijo para la demostracion.
    establecerRol('cliente', 'cliente-1');
    cargarPantalla('mis-rutinas');
  });
});
