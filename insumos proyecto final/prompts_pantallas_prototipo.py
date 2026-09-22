# -*- coding: utf-8 -*-
"""
Prompts para generar las pantallas del prototipo (a partir de las Historias de
Usuario INVEST) - Sistema de Administracion de Gimnasio - Proyecto Final -
Curso IA RACSA

Cada historia de usuario de historias_usuario_invest.py se traduce aqui en un
prompt listo para pedirle a una IA (o para usar como guia propia) la
descripcion funcional completa de la(s) pantalla(s) correspondientes: que
campos tiene, que hace cada boton/accion, que estados y validaciones maneja, y
como se conecta con las demas pantallas del prototipo.

Version 2: se agrega un selector de rol al inicio (en vez de un login real) y
tres pantallas de listado que antes faltaban, para que el prototipo sea
completamente navegable desde el menu (Clientes, Rutinas, Medidas) y se pueda
cambiar de rol en cualquier momento sin recordar credenciales de ejemplo.

Los nombres de pantalla usados coinciden (donde aplica) con los de
wireframes.py, para que wireframes, prompts e historias de usuario sean
consistentes entre si:

HU1        -> Selector de rol / Inicio de sesion
HU-CLI     -> Listado de clientes (Coach/Administrador)
HU2        -> Registro de cliente (Coach/Administrador)
HU-RUT     -> Listado de rutinas de un cliente (Coach/Administrador)
HU3.1      -> Nueva rutina (Coach/Administrador)
HU3.2      -> Agregar ejercicios a la rutina (Coach/Administrador)
HU3.3      -> Agregar ejercicio: peso sugerido condicional (Coach/Administrador)
HU-MED     -> Historial de mediciones de un cliente (Coach/Administrador)
HU5        -> Registrar medicion (Coach/Administrador)
HU4        -> Mis rutinas (Vista del cliente/alumno)

Orden de dependencia tecnica:
HU1 -> HU-CLI -> HU2
HU-CLI -> HU-RUT -> HU3.1 -> HU3.2 -> HU3.3 -> HU4
HU-CLI -> HU-MED -> HU5
HU1 -> HU4 (acceso directo si el rol elegido es cliente/alumno)
"""

prompts_pantallas_prototipo = """
PROMPTS PARA CONSTRUIR LAS PANTALLAS DEL PROTOTIPO (POR HISTORIA DE USUARIO)

Nota tecnica valida para todas las pantallas: el prototipo es estatico
(HTML/CSS/JS nativos, sin backend, sin build, abre con doble clic sobre
index.html). Todos los datos (clientes, rutinas, ejercicios, mediciones) viven
en memoria (arreglos/objetos JS) durante la sesion del navegador; se
inicializan con datos de ejemplo al cargar la pagina y se pierden al recargar.

--------------------------------------------------------------------
HU1 - Autenticacion y control de roles -> Pantalla "Selector de rol / Inicio"
--------------------------------------------------------------------
PROMPT:
Describa y construya la pantalla inicial de un prototipo estatico
(HTML/CSS/JS, sin backend real) para un sistema de gestion de gimnasio, en la
que la persona elige con que rol quiere explorar el prototipo (no hay
autenticacion real, es un selector de rol para fines de demostracion).

Campos:
- Ninguno (no es un formulario de usuario/contrasena).

Acciones:
- Boton [ Entrar como Coach/Administrador ].
- Boton [ Entrar como Cliente ].

Comportamiento:
- Al presionar [ Entrar como Coach/Administrador ], guardar el rol activo como
  "coach" y llevar a la pantalla "Listado de clientes" (HU-CLI).
- Al presionar [ Entrar como Cliente ], guardar el rol activo como "cliente",
  fijar un cliente de ejemplo como "cliente actual" (de los datos de
  ejemplo) y llevar a la pantalla "Mis rutinas" (HU4).
- El rol activo debe quedar visible en todo momento en una barra superior
  persistente (fuera de esta pantalla), junto con un control [ Cambiar rol ]
  que en cualquier momento regresa a esta pantalla sin pedir confirmacion (al
  ser un prototipo de demostracion, cambiar de rol no requiere "cerrar
  sesion" con validacion de credenciales).
- Si alguien con rol "cliente" intenta entrar directamente (via URL/estado
  interno) a una pantalla exclusiva de coach/administrador, mostrar un aviso
  de acceso denegado y devolverlo a "Mis rutinas"; de forma simetrica, si el
  rol "coach" intenta entrar a "Mis rutinas", debe poder verla igual (util
  para que el coach revise como la ve el cliente), pero sin que aparezca
  "Mis rutinas" en su menu de navegacion.

Relacion con otras pantallas:
- Es la puerta de entrada del prototipo completo: ninguna otra pantalla debe
  quedar accesible desde la barra de navegacion antes de elegir un rol aqui.
- El rol elegido determina que opciones de la barra de navegacion se
  habilitan despues: coach/administrador ve "Clientes", "Rutinas" y
  "Medidas"; cliente ve unicamente "Mis rutinas". Ambos roles ven siempre el
  control [ Cambiar rol ].

--------------------------------------------------------------------
HU-CLI - Listado de clientes (Coach/Administrador) [pantalla nueva]
--------------------------------------------------------------------
PROMPT:
Describa y construya la pantalla "Listado de clientes", accesible solo con
rol coach/administrador. Es la pantalla de aterrizaje al elegir ese rol en
HU1 y el destino del enlace "Clientes" de la barra de navegacion.

Estructura:
- Barra superior "Panel Coach/Administrador" con el rol activo y
  [ Cambiar rol ] (ver HU1).
- Campo de busqueda por nombre (filtra la tabla en vivo, sin recargar).
- Tabla de clientes con columnas: Nombre completo, Contacto (correo o
  telefono), Estado (Activo/Inactivo), Coach asignado, y una columna de
  Acciones con tres enlaces por fila: [ Ver rutinas ], [ Ver mediciones ],
  [ Registrar medicion ].
- Boton [ + Nuevo cliente ] en la parte superior de la tabla.

Comportamiento:
- El filtro de busqueda compara contra el nombre completo, sin distinguir
  mayusculas/minusculas.
- [ Ver rutinas ] navega a "Listado de rutinas de un cliente" (HU-RUT) con
  ese cliente preseleccionado.
- [ Ver mediciones ] navega a "Historial de mediciones de un cliente"
  (HU-MED) con ese cliente preseleccionado.
- [ Registrar medicion ] navega directo a "Registrar medicion" (HU5) con ese
  cliente preseleccionado.
- [ + Nuevo cliente ] navega a "Registro de cliente" (HU2).
- Si no hay clientes que coincidan con la busqueda, mostrar un mensaje
  "No se encontraron clientes." en lugar de una tabla vacia.

Relacion con otras pantallas:
- Es el punto de entrada a HU2, HU-RUT, HU-MED y HU5: ninguna de esas
  pantallas debe ser accesible desde el menu principal sin pasar primero por
  este listado (excepto volviendo atras dentro de su propio flujo).
- Los enlaces "Rutinas" y "Medidas" de la barra de navegacion reutilizan esta
  misma pantalla, mostrando el mismo listado de clientes pero con foco en la
  accion correspondiente (el usuario igual debe elegir un cliente antes de
  ver rutinas o mediciones).

--------------------------------------------------------------------
HU2 - Registro de clientes -> Pantalla "Registro de cliente
(Coach/Administrador)"
--------------------------------------------------------------------
PROMPT:
Describa y construya la pantalla "Nuevo cliente", accesible solo con rol
coach/administrador (ver HU1), abierta desde el boton [ + Nuevo cliente ] del
"Listado de clientes" (HU-CLI).

Campos:
- Nombre completo (texto, obligatorio).
- Correo electronico (texto/email, obligatorio si no se llena telefono).
- Telefono (texto, obligatorio si no se llena correo).
- Estado (radio: "Activo" / "Inactivo"; "Activo" viene marcado por defecto).
- Coach asignado (selector; se llena con la lista de coaches disponibles del
  sistema).

Acciones:
- Boton [ Cancelar ] (regresa a "Listado de clientes" sin guardar).
- Boton [ Guardar cliente ].

Comportamiento:
- Al guardar, validar que existan nombre completo, al menos un dato de
  contacto (correo o telefono) y coach asignado; si falta alguno, impedir el
  guardado y senalar el campo faltante.
- Si el correo ingresado ya existe en la lista de clientes de ejemplo,
  mostrar una advertencia de duplicado antes de permitir continuar.
- Al guardar con exito, el cliente debe quedar disponible de inmediato (en
  los datos de ejemplo en memoria) en: (a) el "Listado de clientes" (HU-CLI),
  (b) el selector de "Cliente" en "Nueva rutina" (HU3.1), y (c) el selector
  de cliente en "Registrar medicion" (HU5); y debe regresar automaticamente
  al "Listado de clientes" tras guardar.

Relacion con otras pantallas:
- Forma parte del "Panel Coach/Administrador"; su barra superior usa el mismo
  patron descrito en HU-CLI (rol activo + [ Cambiar rol ]) usado en el resto
  de pantallas de este rol (HU-CLI, HU-RUT, HU3.1, HU3.2, HU3.3, HU-MED,
  HU5).
- El coach asignado aqui es el mismo dato que decide, en el prototipo, que
  coach ve a este cliente al crear una rutina (HU3.1).

--------------------------------------------------------------------
HU-RUT - Listado de rutinas de un cliente (Coach/Administrador) [pantalla
nueva]
--------------------------------------------------------------------
PROMPT:
Describa y construya la pantalla "Rutinas de [nombre del cliente]", accesible
solo con rol coach/administrador, abierta desde [ Ver rutinas ] en el
"Listado de clientes" (HU-CLI) o desde el enlace "Rutinas" de la barra de
navegacion (que primero pide elegir un cliente en HU-CLI).

Estructura:
- Titulo con el nombre del cliente y su estado (Activo/Inactivo).
- Lista de rutinas activas del cliente (nombre, fecha de asignacion), cada
  una con un enlace [ Ver / editar ejercicios ].
- Boton [ + Nueva rutina ] para ese cliente.

Comportamiento:
- Si el cliente no tiene ninguna rutina, mostrar el mensaje "Este cliente aun
  no tiene rutinas asignadas." en lugar de la lista, junto con el boton
  [ + Nueva rutina ].
- [ Ver / editar ejercicios ] navega a "Agregar ejercicios a la rutina"
  (HU3.2) con esa rutina cargada (incluyendo los ejercicios ya guardados).
- [ + Nueva rutina ] navega a "Nueva rutina" (HU3.1) con el cliente ya
  preseleccionado (el campo Cliente de HU3.1 aparece bloqueado/fijo en este
  flujo, ya que se sabe de antemano para quien es la rutina).

Relacion con otras pantallas:
- Recibe el cliente elegido en "Listado de clientes" (HU-CLI).
- Es el punto de entrada de HU3.1 (nueva rutina) y HU3.2 (ver/editar
  ejercicios de una rutina existente) para ese cliente especifico.
- El listado que aqui se muestra debe coincidir exactamente con lo que ese
  mismo cliente ve en "Mis rutinas" (HU4) cuando entra con rol cliente.

--------------------------------------------------------------------
HU3.1 - Crear una rutina para un cliente -> Pantalla "Nueva rutina
(Coach/Administrador)"
--------------------------------------------------------------------
PROMPT:
Describa y construya la pantalla "Nueva rutina", accesible solo con rol
coach/administrador, dentro del "Panel Coach/Administrador".

Campos:
- Cliente (selector, obligatorio; se llena con los clientes activos
  registrados en HU2). Si se llega desde "Listado de rutinas de un cliente"
  (HU-RUT), este campo viene preseleccionado y bloqueado para edicion.
- Nombre de la rutina (texto, obligatorio).

Acciones:
- Boton [ Cancelar ] (regresa a HU-RUT si el cliente venia preseleccionado,
  o a HU-CLI en caso contrario; en ambos casos sin guardar).
- Boton [ Crear rutina ].

Comportamiento:
- Si se intenta crear la rutina sin seleccionar cliente, impedirlo y mostrar
  un mensaje de error.
- Si el cliente seleccionado ya tiene, en los datos de ejemplo, una rutina
  activa, mostrar un aviso indicando el nombre de esa rutina y preguntar si
  desea reemplazarla o mantener ambas en paralelo; "reemplazar" elimina la
  rutina anterior junto con todos sus ejercicios, "mantener ambas" conserva
  la rutina anterior intacta y agrega la nueva por separado.
- Al crear la rutina con exito, pasar automaticamente a la pantalla "Agregar
  ejercicios a la rutina" (HU3.2) para esa misma rutina recien creada, que
  inicia vacia (sin ejercicios).

Relacion con otras pantallas:
- Usa como fuente de datos los clientes creados en HU2 (pantalla "Registro de
  cliente").
- Se llega aqui desde "Listado de rutinas de un cliente" (HU-RUT, cliente
  preseleccionado) o, en un flujo alterno, desde el "Listado de clientes"
  (HU-CLI) si se decide exponer un acceso directo.
- Es el punto de entrada de HU3.2: la rutina que se crea aqui es la misma que
  se completa con ejercicios en la siguiente pantalla.
- La rutina resultante, una vez tenga ejercicios (HU3.2/HU3.3), es la que el
  cliente vera en "Mis rutinas" (HU4) y la que aparece en HU-RUT.

--------------------------------------------------------------------
HU3.2 - Agregar ejercicios a una rutina -> Pantalla "Agregar ejercicios a la
rutina (Coach/Administrador)"
--------------------------------------------------------------------
PROMPT:
Describa y construya la pantalla donde el coach/administrador agrega
ejercicios a la rutina creada en HU3.1 (o abierta desde HU-RUT). Mostrar en
la parte superior el nombre de la rutina y el cliente al que pertenece (dato
heredado de HU3.1/HU-RUT).

Estructura:
- Tabla de ejercicios con columnas: Orden, Ejercicio, Series, Repeticiones,
  Descanso, Peso sugerido (esta ultima con el valor, "peso a definir" o "-"
  cuando el ejercicio es "sin peso", segun HU3.3), y una columna de Acciones
  con botones [ ^ ] y [ v ] para mover la fila un puesto hacia arriba/abajo.
- Boton [ + Agregar ejercicio ], que abre el formulario de HU3.3 para
  capturar un ejercicio nuevo.
- Boton [ Guardar rutina ], alineado al final, y enlace [ Volver ] hacia
  "Listado de rutinas de un cliente" (HU-RUT).

Comportamiento:
- Cada ejercicio agregado debe incluir obligatoriamente nombre, series,
  repeticiones y descanso; si falta series o repeticiones, impedir agregarlo
  y solicitar los datos obligatorios (esta validacion vive en el formulario
  de HU3.3).
- El "Orden" de cada ejercicio se asigna segun la posicion en que se agrega;
  los botones [ ^ ]/[ v ] permiten reordenar la tabla intercambiando la
  posicion de la fila con la inmediata superior/inferior y renumerando la
  columna "Orden" automaticamente.
- [ Guardar rutina ] confirma el listado completo de ejercicios como el
  contenido final de la rutina y regresa a "Listado de rutinas de un
  cliente" (HU-RUT).

Relacion con otras pantallas:
- Recibe la rutina (nombre, cliente y, si ya existian, sus ejercicios) desde
  "Nueva rutina" (HU3.1) o desde "Listado de rutinas de un cliente" (HU-RUT).
- El boton [ + Agregar ejercicio ] abre el formulario descrito en HU3.3,
  donde se define si el ejercicio muestra o no el campo de peso.
- El resultado final (tabla de ejercicios con sus datos) es exactamente lo
  que el cliente vera en el detalle de su rutina en "Mis rutinas" (HU4) y lo
  que se muestra al reabrir la rutina desde HU-RUT.

--------------------------------------------------------------------
HU3.3 - Peso sugerido segun tipo de ejercicio -> Formulario "Agregar
ejercicio" (Coach/Administrador)
--------------------------------------------------------------------
PROMPT:
Describa y construya el formulario "Agregar ejercicio" que se abre desde la
pantalla de HU3.2, con dos comportamientos posibles segun el "Tipo de
ejercicio" elegido.

Campos:
- Ejercicio (texto, obligatorio).
- Tipo de ejercicio (radio: "Con peso" / "Sin peso"; "Con peso" viene
  marcado por defecto).
- Peso sugerido - campo condicional: solo visible/habilitado si el tipo es
  "Con peso". Incluye un valor numerico y un selector de unidad (kg / lb),
  con "kg" por defecto.
- Series, Repeticiones, Descanso (obligatorios, igual que en HU3.2).

Comportamiento:
- Si se elige "Con peso", mostrar el campo "Peso sugerido" (valor + unidad);
  si se guarda sin indicar un valor numerico, permitir guardarlo pero
  marcarlo como "peso a definir" en la tabla de HU3.2.
- Si se elige "Sin peso" (por ejemplo cardio, isometricos, estiramientos), el
  campo "Peso sugerido" no debe mostrarse ni solicitarse en absoluto, y la
  tabla de HU3.2 debe mostrar "-" en esa columna para ese ejercicio.
- Si falta series o repeticiones, impedir guardar y senalar los campos
  obligatorios.
- Al guardar, el ejercicio (con o sin peso) se agrega como una fila nueva al
  final de la tabla de la pantalla "Agregar ejercicios a la rutina" (HU3.2).

Relacion con otras pantallas:
- Es un sub-paso de HU3.2: no es una pantalla independiente, sino el
  formulario (modal o seccion desplegable) que alimenta su tabla de
  ejercicios.
- El dato "peso sugerido" (si existe) es el mismo que luego se muestra en el
  detalle de la rutina que ve el cliente en "Mis rutinas" (HU4).

--------------------------------------------------------------------
HU-MED - Historial de mediciones de un cliente (Coach/Administrador)
[pantalla nueva]
--------------------------------------------------------------------
PROMPT:
Describa y construya la pantalla "Mediciones de [nombre del cliente]",
accesible solo con rol coach/administrador, abierta desde [ Ver mediciones ]
en el "Listado de clientes" (HU-CLI) o desde el enlace "Medidas" de la barra
de navegacion (que primero pide elegir un cliente en HU-CLI).

Estructura:
- Titulo con el nombre del cliente.
- Tabla con el historial de mediciones ordenado de mas reciente a mas
  antigua: columnas Fecha, Peso (kg), Cintura, Cadera, Brazo, Pierna (cm) y
  % de grasa corporal (mostrar "-" en las celdas de medidas no registradas
  en esa fecha).
- Boton [ + Registrar medicion ].

Comportamiento:
- Si el cliente no tiene mediciones registradas, mostrar el mensaje "Este
  cliente aun no tiene mediciones registradas." en lugar de la tabla, junto
  con el boton [ + Registrar medicion ].
- [ + Registrar medicion ] navega a "Registrar medicion" (HU5) con el
  cliente ya preseleccionado.

Relacion con otras pantallas:
- Recibe el cliente elegido en "Listado de clientes" (HU-CLI).
- Es el punto de entrada de HU5 para ese cliente especifico, y el lugar
  donde se reflejan de inmediato las mediciones que HU5 vaya guardando.

--------------------------------------------------------------------
HU5 - Registro de medidas antropometricas -> Pantalla "Registrar medicion
(Coach/Administrador)"
--------------------------------------------------------------------
PROMPT:
Describa y construya la pantalla "Registrar medicion", accesible solo con
rol coach/administrador, mostrando en el titulo el nombre del cliente sobre
el que se registra la medicion (cliente ya existente, ver HU2), llegado
desde "Listado de clientes" (HU-CLI) o "Historial de mediciones de un
cliente" (HU-MED).

Campos:
- Fecha (obligatorio).
- Peso en kg (obligatorio).
- Cintura, Cadera, Brazo, Pierna (cm) y % de grasa corporal (opcionales, pero
  se debe registrar al menos una medida antropometrica ademas del peso).

Acciones:
- Boton [ Cancelar ] (regresa a "Historial de mediciones de un cliente"
  (HU-MED) sin guardar).
- Boton [ Guardar medicion ].

Comportamiento:
- Si falta la fecha o el peso, impedir guardar y senalar los campos
  obligatorios.
- Si no se completa ninguna medida antropometrica ademas del peso, impedir
  guardar y senalar que se requiere al menos una.
- Si ya existe, en los datos de ejemplo, una medicion para ese mismo cliente
  en la misma fecha, mostrar una advertencia de duplicado y preguntar si se
  desea sobrescribirla.
- Al guardar con exito, regresar a "Historial de mediciones de un cliente"
  (HU-MED), donde la nueva medicion debe aparecer de inmediato.

Relacion con otras pantallas:
- El cliente sobre el que se registra la medicion es el mismo creado en HU2
  ("Registro de cliente"); esta pantalla se abre desde el listado/expediente
  de ese cliente (HU-CLI o HU-MED).
- Forma parte del "Panel Coach/Administrador", junto con HU-CLI, HU2, HU-RUT,
  HU3.1, HU3.2, HU3.3 y HU-MED, y comparte con ellas la misma barra superior
  con el rol activo y [ Cambiar rol ].

--------------------------------------------------------------------
HU4 - Cliente visualiza sus rutinas vigentes -> Pantalla "Mis rutinas (Vista
del cliente/alumno)"
--------------------------------------------------------------------
PROMPT:
Describa y construya la pantalla "Mis rutinas", accesible con rol
cliente/alumno (destino automatico al elegir "Entrar como Cliente" en HU1) y
tambien accesible en modo lectura por el rol coach/administrador (para
revisar como la ve el cliente), con dos secciones lado a lado.

Estructura:
- Barra superior "Mis rutinas" con el rol activo y [ Cambiar rol ] (ver HU1).
- Columna izquierda "Rutinas vigentes": lista de las rutinas activas del
  cliente actual (nombre y fecha de asignacion), una de ellas seleccionada
  por defecto.
- Columna derecha "Detalle": tabla con los ejercicios de la rutina
  seleccionada (Ejercicio, Series, Repeticiones, Descanso y Peso sugerido
  cuando aplique).

Comportamiento:
- Al hacer clic en una rutina de la lista izquierda, actualizar la columna
  derecha con el detalle de esa rutina.
- Si el cliente no tiene ninguna rutina asignada, mostrar en lugar de las dos
  columnas un mensaje: "Aun no tienes rutinas asignadas. Contacta a tu
  coach.".

Relacion con otras pantallas:
- Consume directamente los datos generados por el coach/administrador en
  HU3.1 (rutina), HU3.2 (ejercicios) y HU3.3 (peso sugerido cuando aplica), y
  debe coincidir exactamente con lo que se ve en "Listado de rutinas de un
  cliente" (HU-RUT) para ese mismo cliente.
- Es la unica pantalla a la que un usuario con rol cliente puede navegar
  desde la barra de navegacion, segun lo definido en HU1 (ademas del control
  [ Cambiar rol ], comun a ambos roles).
"""

if __name__ == "__main__":
    print(prompts_pantallas_prototipo)
