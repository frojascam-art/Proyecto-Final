# Uso obligatorio del boilerplate del proyecto

Antes de crear o modificar código relacionado con pantallas, navegación, estilos, estructura HTML o carga de vistas, revise primero el boilerplate almacenado en `ejercicio clase 4/`:

* `ejercicio clase 4/index.html`
* `ejercicio clase 4/css/estilos.css`
* `ejercicio clase 4/js/app.js`
* `ejercicio clase 4/pantallas/`

Este boilerplate es la referencia principal para la estructura y las convenciones del proyecto.

## Reglas obligatorias

1. Determine si la tarea requiere crear o modificar una pantalla, componente visual, estructura HTML, estilos CSS o comportamiento JavaScript.

2. Cuando la tarea corresponda, reutilice el boilerplate existente. No cree una estructura alternativa ni duplique elementos que ya estén definidos.

3. Mantenga la estructura base establecida dentro de `ejercicio clase 4/`:

   * `ejercicio clase 4/index.html`
   * `ejercicio clase 4/css/estilos.css`
   * `ejercicio clase 4/js/app.js`
   * `ejercicio clase 4/pantallas/`

4. Toda nueva vista debe crearse dentro de `ejercicio clase 4/pantallas/`.

5. Use las clases de layout existentes, como:

   * `contenedor`
   * `fila`
   * `columna`
   * `tarjeta`

   No cree clases equivalentes con nombres diferentes salvo que exista una necesidad técnica justificada.

6. Use la función existente en `ejercicio clase 4/js/app.js` (`registrarPantalla` / `cargarPantalla`) para cargar las pantallas dentro del contenedor principal. No implemente otro mecanismo de navegación o carga de vistas sin autorización.

7. Preserve los siguientes requisitos técnicos:

   * El proyecto debe funcionar abriendo `index.html` directamente con doble clic.
   * No debe necesitar servidor local.
   * No debe necesitar un proceso de build.
   * No agregue frameworks, empaquetadores ni dependencias externas sin solicitar autorización.
   * Use HTML, CSS y JavaScript nativos, salvo indicación contraria.

8. Mantenga en cada archivo los comentarios que identifican las secciones pendientes de implementación. Agregue comentarios equivalentes cuando cree nuevas secciones incompletas.

9. Antes de escribir código nuevo, compruebe si el boilerplate ya contiene una estructura, clase, función o patrón que pueda reutilizarse.

10. No modifique el boilerplate original directamente para resolver una tarea concreta. Úselo como plantilla y realice los cambios en los archivos correspondientes del proyecto, salvo que se solicite explícitamente actualizar el boilerplate.

## Conflictos y excepciones

Si una solicitud entra en conflicto con el boilerplate:

1. No ignore el boilerplate silenciosamente.
2. Explique brevemente cuál es el conflicto.
3. Indique qué archivos o convenciones serían afectados.
4. Proponga la modificación mínima necesaria.
5. Solicite confirmación antes de cambiar la arquitectura, introducir dependencias o romper la ejecución mediante doble clic.

Si encuentra errores, código inseguro o limitaciones importantes en el boilerplate, no los copie ciegamente. Informe el problema y proponga una corrección compatible con la estructura existente.

## Verificación obligatoria

Después de realizar cambios:

1. Verifique que las rutas relativas de HTML, CSS, JavaScript y pantallas sean correctas.
2. Confirme que `index.html` siga funcionando al abrirse directamente.
3. Compruebe que no se hayan agregado dependencias o requisitos de servidor accidentalmente.
4. Ejecute las pruebas disponibles.
5. Informe qué elementos del boilerplate fueron reutilizados y cualquier desviación realizada.

Priorice siempre la reutilización y consistencia con el boilerplate sobre la creación de estructuras nuevas.
