# -*- coding: utf-8 -*-
"""
Historias de Usuario refinadas con analisis de ambiguedad y validacion INVEST
Sistema de Administracion de Gimnasio - Proyecto Final - Curso IA RACSA

Cobertura: las 37 historias generales de historias_usuario_generales.py (8
epicas) quedan reflejadas aqui, ya sea de forma directa, fusionadas o
divididas segun el analisis de ambiguedad (ver seccion correspondiente antes
de HU1). El mapeo historia general -> HU refinada es:
  1->HU2  2->HU6   3->HU7   4->HU8   5->HU9   6->HU3.1  7->HU3.2/HU3.3
  8->HU10 9->HU11 10->HU12 11->HU13 12->HU14 13->HU5   14->HU15
 15->HU16 16->HU17 17->HU18 18->HU18 19->HU19 20->HU20 21->HU4   22->HU4
 23->HU21 24->HU22 25->HU23 26->HU24 27->HU25 28->HU26 29->HU27 30->HU1
 31->HU1  32->HU28 33->HU29 34->HU30 35->HU31 36->HU32 37->HU33

Orden de creacion del sistema (dependencias tecnicas principales):
HU1 (auth/roles) -> HU2 (clientes) -> HU6/HU7/HU8/HU9 (gestion de clientes)
HU2 -> HU3.1/3.2/3.3 (rutinas) -> HU10/HU11/HU12/HU13/HU14 (rutinas, cont.)
HU3.1..HU3.3 -> HU4 (cliente ve rutina) -> HU21/HU22/HU23 (cliente, cont.)
HU2 -> HU5 (medidas) -> HU15/HU16/HU17 (medidas, cont.) -> HU24/HU25/HU27
HU5 -> HU18/HU19 (objetivos) -> HU20 (alerta) ; HU18 -> HU26 (cliente ve meta)
HU3.1/HU12 -> HU28 (notificacion) ; HU4 -> HU29 -> HU30 (comentarios)
HU2, HU3.x, HU5, HU18 -> HU31/HU32/HU33 (panel, reportes, exportacion)

Nota: la HU3 original se dividio en tres historias mas pequenas (HU3.1, HU3.2 y
HU3.3) tras el analisis INVEST, porque mezclaba mas de una responsabilidad y
tenia una ambiguedad de negocio (el peso sugerido no aplica a todos los
ejercicios).
"""

historias_usuario_invest = """
HISTORIAS DE USUARIO REFINADAS (ANALISIS DE AMBIGUEDAD + INVEST)

--------------------------------------------------------------------
ANALISIS DE AMBIGUEDADES ENTRE LAS HISTORIAS GENERALES (antes de refinar)
--------------------------------------------------------------------
Antes de redactar las historias refinadas se revisaron las 37 historias
generales en conjunto (no una por una) para detectar contradicciones,
solapamientos o terminos ambiguos entre ellas. Los hallazgos y la decision
tomada para cada uno son:

A1. Las historias generales #30 (login cliente) y #31 (login administrador)
    describen la misma funcionalidad de autenticacion para dos roles ->
    se unificaron en una sola historia con distinto resultado segun el rol
    (HU1).
A2. La historia general #7 mezclaba series/repeticiones/descanso (aplican a
    todo ejercicio) con el peso sugerido (no aplica a ejercicios de cardio o
    isometricos) -> se dividio en HU3.2 (datos comunes) y HU3.3 (peso
    condicional).
A3. Las historias generales #6 (crear rutina) y #7 (agregar ejercicios) son
    en realidad dos pasos de un mismo flujo con responsabilidades distintas
    (contenedor vs. contenido) -> separadas en HU3.1 y HU3.2.
A4. La historia general #5 ("asignar coach a cada cliente") se solapa con el
    dato "coach asignado" que ya se captura al registrar el cliente (#1) ->
    se interpreto #5 como la reasignacion de coach de un cliente YA
    existente (HU9), distinta de la asignacion inicial (HU2).
A5. La historia general #10 ("modificar una rutina asignada") es ambigua:
    puede referirse a agregar/quitar ejercicios (ya cubierto por HU3.2) o a
    otros atributos de la rutina -> se acoto HU12 a nombre y estado de la
    rutina, dejando los ejercicios a HU3.2/HU10.
A6. La historia general #9 usa dos terminos para lo que parece una sola
    accion: "duplicar" y "usar como plantilla" -> se definio como una unica
    funcionalidad (duplicar una rutina existente), sin biblioteca de
    plantillas separada (HU11).
A7. La historia general #13 (coach registra "peso corporal") y la #24
    (cliente registra "el peso que utilice en cada ejercicio") usan la
    palabra "peso" para dos conceptos distintos -> se renombro explicitamente
    como "peso utilizado en el ejercicio" en HU22 para no confundirlo con el
    peso corporal de HU5.
A8. La historia general #20 ("alerta si el cliente lleva semanas sin
    registrar avances") no aclara si "avance" es una medicion del coach
    (#13) o el cumplimiento marcado por el cliente (#23) -> se definio
    "avance" como cualquiera de los dos eventos (HU20).
A9. Las historias generales #14 y #27 (grafico de evolucion, visto por coach
    y por cliente) son la misma funcionalidad para dos roles -> se mantienen
    como dos historias (aportan valor a audiencias distintas) pero
    documentadas como una unica fuente de datos y reglas (HU15 y HU25).
A10. La historia general #36 ("generar un reporte de progreso") se solapa
    conceptualmente con los graficos (#14/#27) -> se diferencio el reporte
    (documento exportable con rango de fechas, HU32) del grafico en pantalla
    (vista interactiva sin exportar, HU15/HU25).
A11. La historia general #37 ("exportar informacion de clientes y progreso")
    no especifica formato ni alcance -> se acoto en HU33 a un archivo CSV de
    todos los clientes activos con su progreso resumido.
A12. La historia general #32 (notificacion de rutina asignada/modificada) no
    especifica el canal -> se acoto en HU28 a notificacion dentro del
    sistema, ya que ninguna historia general describe integraciones
    externas (correo, push).
A13. La historia general #33 ("comentario o duda sobre un ejercicio") no
    aclara si el comentario es sobre el ejercicio dentro de una rutina
    especifica o sobre un catalogo general de ejercicios -> se acoto en
    HU29 a que el comentario siempre pertenece a un ejercicio dentro de una
    rutina asignada concreta (no existe catalogo general en el alcance
    actual).

--------------------------------------------------------------------
HU1 - Autenticacion y control de roles
--------------------------------------------------------------------
Como usuario del sistema quiero iniciar sesion con mi usuario y contrasena, y que
el sistema me reconozca como administrador/coach o como cliente, para acceder
unicamente a las funciones y datos que correspondan a mi rol.

Criterios de aceptacion:
- Dado un usuario registrado con rol "coach" o "cliente", cuando inicia sesion con
  credenciales validas, entonces el sistema lo redirige a la vista correspondiente
  a su rol.
- Dado que un usuario ingresa credenciales invalidas, cuando intenta iniciar
  sesion, entonces el sistema muestra un mensaje de error generico (sin indicar si
  fallo el usuario o la contrasena).
- Dado que un cliente intenta acceder a una funcion exclusiva de administrador,
  entonces el sistema le niega el acceso.

--------------------------------------------------------------------
HU2 - Registro de clientes
--------------------------------------------------------------------
Como administrador quiero registrar un nuevo cliente con sus datos personales, de
contacto, su estado (activo/inactivo) y el coach asignado, para tener el
expediente base sobre el cual se construiran sus rutinas y su seguimiento.

Criterios de aceptacion:
- Dado que estoy autenticado como administrador, cuando registro un cliente, debo
  ingresar como minimo: nombre completo, un dato de contacto (correo o telefono) y
  el coach asignado.
- Dado que falta un campo obligatorio, cuando intento guardar, el sistema debe
  impedirlo y senalar que falta.
- Dado que ya existe un cliente con el mismo correo, cuando intento registrarlo de
  nuevo, el sistema debe advertir la duplicidad.
- Todo cliente nuevo queda con estado "activo" por defecto.

--------------------------------------------------------------------
HU3.1 - Crear una rutina para un cliente
--------------------------------------------------------------------
Como coach quiero crear una rutina de entrenamiento vacia y asociarla a un cliente
especifico para tener el contenedor donde luego se agregaran los ejercicios del
plan.

Criterios de aceptacion:
- Dado que soy coach autenticado y tengo un cliente activo, cuando creo una
  rutina, entonces debo indicar un nombre para la rutina y seleccionar el cliente
  al que pertenece.
- Dado que un cliente ya tiene una rutina activa, cuando intento crear una nueva
  rutina para el, entonces el sistema debe indicarme que ya existe una activa y
  preguntarme si deseo reemplazarla o mantener ambas.
- Dado que intento guardar una rutina sin seleccionar un cliente, cuando confirmo
  la creacion, entonces el sistema debe impedirlo y mostrar un mensaje de error.

--------------------------------------------------------------------
HU3.2 - Agregar ejercicios con sus parametros a una rutina
--------------------------------------------------------------------
Como coach quiero agregar ejercicios a una rutina existente, definiendo para cada
uno las series, repeticiones y tiempo de descanso, para especificar el trabajo
concreto que el cliente debe realizar en cada sesion.

Criterios de aceptacion:
- Dado que tengo una rutina creada, cuando agrego un ejercicio, entonces debo
  indicar su nombre, numero de series, numero de repeticiones y tiempo de
  descanso.
- Dado que intento guardar un ejercicio sin indicar series o repeticiones,
  entonces el sistema debe impedirlo y solicitar los datos obligatorios.
- Dado que una rutina ya tiene ejercicios agregados, cuando agrego uno nuevo,
  entonces debo poder definir el orden en que aparece dentro de la rutina.

--------------------------------------------------------------------
HU3.3 - Definir peso sugerido segun el tipo de ejercicio
--------------------------------------------------------------------
Como coach quiero indicar un peso sugerido unicamente en los ejercicios que lo
requieran, para orientar al cliente sobre la carga a utilizar sin forzar ese dato
en ejercicios donde no aplica (cardio, isometricos, estiramientos, etc.).

Criterios de aceptacion:
- Dado que agrego un ejercicio marcado como "con peso" (pesas libres, maquinas),
  cuando lo configuro, entonces el sistema debe permitirme ingresar un peso
  sugerido en la unidad definida (kg o lb).
- Dado que agrego un ejercicio marcado como "sin peso" (cardio, isometricos),
  cuando lo configuro, entonces el sistema no debe mostrar ni solicitar el campo
  de peso sugerido.
- Dado que un ejercicio requiere peso, cuando lo guardo sin especificar el valor,
  entonces el sistema debe permitirlo pero marcarlo como "peso a definir".

--------------------------------------------------------------------
HU4 - Cliente visualiza sus rutinas vigentes
--------------------------------------------------------------------
Como cliente quiero ver todas las rutinas de entrenamiento vigentes que me asigno
mi coach, con el detalle de series y repeticiones de cada ejercicio, para saber
que debo realizar en cada sesion.

Criterios de aceptacion:
- Dado que tengo una o mas rutinas activas, cuando entro a "Mis rutinas", veo cada
  una identificada por nombre y fecha de asignacion.
- Dado que aun no tengo ninguna rutina asignada, el sistema muestra un mensaje
  indicando que no hay rutinas todavia.
- Dado que selecciono una rutina, veo el detalle de cada ejercicio con series,
  repeticiones, descanso y, si aplica, peso sugerido.

Nota: se asume que un cliente puede tener varias rutinas vigentes en paralelo,
siguiendo la regla definida en HU3.1. Si se decide limitar a una sola rutina
activa por cliente, esta historia y la HU3.1 deben ajustarse.

--------------------------------------------------------------------
HU5 - Registro de medidas antropometricas
--------------------------------------------------------------------
Como coach quiero registrar el peso corporal y las medidas antropometricas de un
cliente (cintura, cadera, brazo, pierna, porcentaje de grasa) en una fecha
determinada, para tener el punto de partida sobre el cual se medira su progreso.

Criterios de aceptacion:
- Dado que estoy autenticado como coach, cuando registro una medicion, debo
  indicar la fecha, el peso (kg) y al menos una medida antropometrica.
- Dado que falta la fecha o el peso, el sistema debe impedir guardar.
- Dado que ya existe una medicion para ese cliente en esa misma fecha, el sistema
  debe advertir la duplicidad y preguntar si deseo sobrescribirla.

--------------------------------------------------------------------
HU6 - Edicion de datos de un cliente
--------------------------------------------------------------------
Como administrador quiero editar la informacion personal y de contacto de un
cliente ya registrado para mantener su expediente actualizado sin perder su
historial de rutinas y mediciones.

Criterios de aceptacion:
- Dado un cliente existente, cuando el administrador modifica su nombre,
  contacto o coach asignado y guarda, el sistema actualiza el expediente
  conservando el historial de rutinas y mediciones asociado.
- Dado que el administrador deja vacio el nombre o ambos datos de contacto
  (correo y telefono), cuando intenta guardar, el sistema lo impide y senala
  el campo faltante (misma regla que HU2).
- Dado que el nuevo correo ingresado ya pertenece a otro cliente, el sistema
  advierte la duplicidad antes de guardar.

--------------------------------------------------------------------
HU7 - Baja (desactivacion) de un cliente
--------------------------------------------------------------------
Como administrador quiero desactivar a un cliente para reflejar que ya no
esta activo en el gimnasio, sin eliminar su historial.

Criterios de aceptacion:
- Dado un cliente activo, cuando el administrador lo desactiva, el sistema
  cambia su estado a "inactivo" y conserva intactos sus rutinas y mediciones
  previas.
- Dado un cliente inactivo, cuando el administrador intenta crear una nueva
  rutina o registrar una medicion para el, el sistema lo impide y le indica
  que primero debe reactivarlo.
- Dado un cliente inactivo, el administrador puede reactivarlo desde la misma
  pantalla, devolviendolo a estado "activo".

--------------------------------------------------------------------
HU8 - Busqueda y filtrado de clientes
--------------------------------------------------------------------
Como administrador quiero buscar y filtrar clientes por nombre, estado o
coach asignado para encontrar rapidamente el expediente que necesito.

Criterios de aceptacion:
- Dado un texto ingresado en el buscador, el sistema filtra la lista de
  clientes cuyo nombre lo contenga, sin distinguir mayusculas/minusculas.
- Dado un filtro de estado (activo/inactivo) o de coach asignado, el sistema
  muestra unicamente los clientes que cumplen ese criterio, y ambos filtros
  pueden combinarse con la busqueda por nombre.
- Dado que ningun cliente cumple los criterios combinados, el sistema muestra
  un mensaje "No se encontraron clientes." en lugar de una tabla vacia.

--------------------------------------------------------------------
HU9 - Reasignacion de coach a un cliente
--------------------------------------------------------------------
Como administrador quiero cambiar el coach responsable de un cliente ya
registrado para redistribuir la carga de trabajo entre coaches.

Nota (ambiguedad A4): esta historia cubre la reasignacion posterior; la
asignacion inicial de coach ocurre al registrar el cliente (HU2).

Criterios de aceptacion:
- Dado un cliente con un coach ya asignado, cuando el administrador selecciona
  un nuevo coach y guarda, el sistema actualiza el coach responsable sin
  afectar las rutinas ya creadas.
- Dado que el administrador no selecciona ningun coach, el sistema impide
  guardar el cambio.
- Dado un cambio de coach, el sistema conserva el historial de que coach creo
  cada rutina previa (no se reescribe retroactivamente).

--------------------------------------------------------------------
HU10 - Organizacion de una rutina por dia o bloque
--------------------------------------------------------------------
Como coach quiero agrupar los ejercicios de una rutina por dia de la semana o
por bloque (tren superior, tren inferior, cardio) para estructurar el plan de
entrenamiento completo.

Depende de HU3.2.

Criterios de aceptacion:
- Dado que agrego un ejercicio a una rutina, debo indicar a que dia o bloque
  pertenece, eligiendo de una lista predefinida (Lunes...Domingo, o un bloque
  libre con nombre).
- Dado una rutina con ejercicios en varios dias/bloques, cuando la visualizo,
  los ejercicios se agrupan y muestran bajo el encabezado de su dia/bloque
  correspondiente.
- Dado que un ejercicio no tiene dia/bloque asignado, el sistema lo agrupa
  bajo un encabezado "Sin asignar" en vez de impedir guardarlo.

--------------------------------------------------------------------
HU11 - Duplicar una rutina como base para otra
--------------------------------------------------------------------
Como coach quiero duplicar una rutina existente (propia o de otro cliente)
para usarla como punto de partida de una nueva rutina y ahorrar tiempo al
armar planes similares.

Nota (ambiguedad A6): "duplicar" y "usar como plantilla" se tratan como una
sola funcionalidad; no existe una biblioteca de plantillas separada.

Criterios de aceptacion:
- Dado una rutina existente, cuando el coach elige "duplicar", el sistema
  crea una copia con todos sus ejercicios, series, repeticiones, descansos y
  pesos sugeridos, sin fecha de asignacion ni cliente definidos.
- Dado la copia recien creada, el coach debe indicar un cliente y un nombre
  antes de guardarla (aplican las mismas reglas de HU3.1, incluida la
  advertencia de rutina activa existente).
- Dado que se duplica una rutina, los cambios posteriores a la copia no
  afectan a la rutina original.

--------------------------------------------------------------------
HU12 - Modificar el nombre o estado de una rutina asignada
--------------------------------------------------------------------
Como coach quiero cambiar el nombre o el estado (activa/finalizada) de una
rutina ya asignada a un cliente para mantenerla alineada con su situacion
actual.

Nota (ambiguedad A5): agregar, quitar o reordenar ejercicios ya esta cubierto
por HU3.2/HU10; esta historia se limita a nombre y estado de la rutina.

Criterios de aceptacion:
- Dado una rutina existente, cuando el coach edita su nombre y guarda, el
  sistema lo actualiza sin alterar los ejercicios ya definidos.
- Dado una rutina activa, cuando el coach la marca como "finalizada", el
  sistema deja de mostrarla en "rutinas vigentes" del cliente (HU4) pero la
  conserva en el historial (HU14/HU23).
- Dado que se intenta finalizar la unica rutina activa de un cliente, el
  sistema pide confirmacion antes de aplicar el cambio, ya que el cliente
  quedara temporalmente sin rutinas vigentes.

--------------------------------------------------------------------
HU13 - Adjuntar material de referencia a un ejercicio
--------------------------------------------------------------------
Como coach quiero adjuntar un video o una imagen de referencia a un ejercicio
de una rutina para que el cliente entienda la tecnica correcta.

Criterios de aceptacion:
- Dado un ejercicio dentro de una rutina, cuando el coach adjunta un enlace
  de video o una imagen, el sistema lo guarda asociado a ese ejercicio
  especifico (no a un catalogo general).
- Dado un ejercicio sin material adjunto, el sistema no muestra ningun
  enlace ni imagen en su detalle (el campo es opcional).
- Dado que el coach reemplaza el material adjunto de un ejercicio, el sistema
  conserva unicamente el mas reciente.

--------------------------------------------------------------------
HU14 - Historial de rutinas anteriores de un cliente (vista coach)
--------------------------------------------------------------------
Como coach quiero ver el historial de rutinas finalizadas de un cliente para
evaluar la progresion de sus cargas de entrenamiento.

Criterios de aceptacion:
- Dado un cliente con rutinas finalizadas (HU12), el coach puede consultar la
  lista ordenada de mas reciente a mas antigua, cada una con su rango de
  fechas de vigencia.
- Dado que selecciona una rutina del historial, el coach ve el detalle
  completo de sus ejercicios tal como quedo al finalizar (sin poder
  editarlo).
- Dado un cliente sin rutinas finalizadas, el sistema muestra un mensaje
  indicando que aun no hay historial.

--------------------------------------------------------------------
HU15 - Visualizacion grafica de la evolucion de medidas (vista coach)
--------------------------------------------------------------------
Como coach quiero visualizar en un grafico la evolucion de las medidas de un
cliente a lo largo del tiempo para identificar tendencias y ajustar el plan
si es necesario.

Criterios de aceptacion:
- Dado un cliente con dos o mas mediciones registradas (HU5), el coach puede
  ver un grafico de lineas con el peso y, opcionalmente, otra medida
  antropometrica seleccionable, en el eje del tiempo.
- Dado un cliente con una sola medicion o ninguna, el sistema muestra un
  mensaje indicando que se necesitan al menos dos mediciones para graficar
  una tendencia.
- Dado el grafico visible, el coach puede pasar el cursor sobre un punto para
  ver la fecha y el valor exacto de esa medicion.

--------------------------------------------------------------------
HU16 - Registro de fotos de progreso de un cliente
--------------------------------------------------------------------
Como coach quiero registrar fotos de progreso de un cliente asociadas a una
fecha para tener un respaldo visual ademas de los datos numericos.

Criterios de aceptacion:
- Dado un cliente, cuando el coach sube una o mas fotos indicando la fecha,
  el sistema las guarda asociadas a esa fecha (independiente de si existe
  una medicion numerica ese mismo dia).
- Dado que no se indica una fecha, el sistema impide guardar la foto.
- Dado un cliente con fotos registradas, el coach puede eliminarlas
  individualmente.

--------------------------------------------------------------------
HU17 - Comparacion de dos periodos de medicion
--------------------------------------------------------------------
Como coach quiero comparar dos mediciones de un cliente para mostrarle de
forma clara los avances obtenidos.

Criterios de aceptacion:
- Dado un cliente con dos o mas mediciones, el coach puede elegir una
  medicion de "inicio" y una de "fin" y ver, lado a lado, cada medida junto
  con la diferencia (absoluta y porcentual).
- Dado que alguna medida no esta registrada en una de las dos fechas
  elegidas, el sistema muestra "-" en esa fila en lugar de calcular una
  diferencia.
- Dado que el coach elige la misma medicion como inicio y fin, el sistema lo
  impide y solicita elegir fechas distintas.

--------------------------------------------------------------------
HU18 - Definicion de objetivo y meta medible con fecha limite
--------------------------------------------------------------------
Como coach quiero definir para un cliente un objetivo (perder peso, ganar
masa muscular, mejorar resistencia, etc.) junto con una meta medible y una
fecha limite, para orientar el diseno de su rutina y poder evaluar si el plan
esta funcionando.

Nota: fusiona las historias generales #17 y #18; un objetivo sin una meta
medible con fecha no es evaluable, por lo que se definen juntos.

Criterios de aceptacion:
- Dado un cliente, cuando el coach define un objetivo, debe indicar el tipo
  de objetivo, un valor meta medible (por ejemplo, peso objetivo en kg) y una
  fecha limite.
- Dado que falta el valor meta o la fecha limite, el sistema impide guardar
  el objetivo.
- Dado un cliente con un objetivo activo, cuando el coach define uno nuevo,
  el sistema pregunta si desea reemplazar el objetivo activo o mantener
  ambos (misma logica que rutinas activas, HU3.1).

--------------------------------------------------------------------
HU19 - Actualizacion o cierre de un objetivo
--------------------------------------------------------------------
Como coach quiero marcar un objetivo como cumplido o actualizarlo cuando
cambien las circunstancias del cliente para mantener el plan alineado con
sus necesidades actuales.

Criterios de aceptacion:
- Dado un objetivo activo, cuando el coach lo marca como "cumplido", el
  sistema registra la fecha de cumplimiento y deja de mostrarlo como
  objetivo vigente del cliente.
- Dado un objetivo activo, cuando el coach edita su meta o fecha limite, el
  sistema actualiza esos valores conservando el objetivo original en el
  historial de cambios.
- Dado un objetivo cumplido, el coach puede consultarlo en el historial del
  cliente, pero no puede reabrirlo (debe crear uno nuevo).

--------------------------------------------------------------------
HU20 - Alerta de inactividad de un cliente
--------------------------------------------------------------------
Como coach quiero recibir una alerta cuando un cliente lleve varias semanas
sin registrar avances para poder contactarlo y ajustar su seguimiento.

Nota (ambiguedad A8): "avance" se define como al menos uno de estos dos
eventos: una medicion registrada por el coach (HU5) o una rutina/ejercicio
marcado como realizado por el cliente (HU21).

Criterios de aceptacion:
- Dado un cliente activo sin ninguno de los dos eventos de avance durante 3
  semanas o mas, el sistema lo marca en el panel del coach con una senal de
  alerta.
- Dado que el cliente registra un avance (medicion o marca de cumplimiento),
  el sistema reinicia el conteo de semanas de inactividad para ese cliente.
- Dado un cliente inactivo (HU7, dado de baja), el sistema no genera alertas
  de inactividad para el.

--------------------------------------------------------------------
HU21 - Cliente marca ejercicios o rutina como realizada
--------------------------------------------------------------------
Como cliente quiero marcar un ejercicio o una rutina completa como realizada
para llevar un registro de mi cumplimiento.

Criterios de aceptacion:
- Dado el detalle de una rutina vigente (HU4), el cliente puede marcar cada
  ejercicio como realizado de forma individual.
- Dado que todos los ejercicios de una sesion quedan marcados, el sistema
  ofrece marcar la rutina completa de ese dia como realizada en un solo
  paso.
- Dado un ejercicio ya marcado como realizado, el cliente puede desmarcarlo
  el mismo dia si se equivoco.

--------------------------------------------------------------------
HU22 - Cliente registra su desempeno real por ejercicio
--------------------------------------------------------------------
Como cliente quiero registrar el peso que utilice o las repeticiones que
logre en cada ejercicio para que mi coach pueda ver si estoy progresando
segun lo planeado.

Nota (ambiguedad A7): este "peso utilizado en el ejercicio" es un dato
distinto del "peso corporal" registrado en HU5; se nombran de forma
diferenciada para evitar confusion.

Criterios de aceptacion:
- Dado un ejercicio marcado como "con peso" (HU3.3), el cliente puede indicar
  el peso que utilizo (en la misma unidad definida por el coach) ademas de
  marcarlo como realizado.
- Dado un ejercicio "sin peso", el sistema no solicita el peso utilizado,
  unicamente permite indicar las repeticiones logradas si difieren de las
  planeadas.
- Dado un registro de desempeno ya guardado para una fecha, el cliente puede
  corregirlo el mismo dia en que lo registro.

--------------------------------------------------------------------
HU23 - Cliente consulta su historial de rutinas completadas
--------------------------------------------------------------------
Como cliente quiero consultar el historial de rutinas que ya complete para
revisar como ha evolucionado mi entrenamiento.

Criterios de aceptacion:
- Dado que tengo rutinas finalizadas o sesiones marcadas como realizadas
  (HU21), puedo verlas listadas de mas reciente a mas antigua.
- Dado que selecciono una sesion del historial, veo el detalle de lo
  planeado junto con lo que realmente registre (HU22) en esa fecha.
- Dado que aun no he completado ninguna rutina, el sistema muestra un
  mensaje indicandolo en vez de una lista vacia.

--------------------------------------------------------------------
HU24 - Cliente visualiza sus medidas corporales
--------------------------------------------------------------------
Como cliente quiero ver mis medidas corporales registradas por mi coach para
conocer mi evolucion fisica.

Criterios de aceptacion:
- Dado que tengo mediciones registradas por mi coach (HU5), puedo verlas en
  una tabla ordenada de mas reciente a mas antigua, en modo de solo lectura.
- Dado que no tengo ninguna medicion registrada, el sistema muestra un
  mensaje indicandolo.
- El cliente no puede editar ni eliminar sus propias mediciones; solo el
  coach puede hacerlo (HU5).

--------------------------------------------------------------------
HU25 - Cliente visualiza grafico de su progreso
--------------------------------------------------------------------
Como cliente quiero visualizar un grafico de mi progreso (peso, medidas,
porcentaje de grasa) a lo largo del tiempo para mantenerme motivado al ver
resultados.

Nota (ambiguedad A9): usa la misma fuente de datos y reglas de HU15, mostrado
en modo de solo lectura para el rol cliente.

Criterios de aceptacion:
- Dado que tengo dos o mas mediciones registradas, puedo ver el mismo tipo de
  grafico de lineas definido en HU15, limitado a mis propios datos.
- Dado que tengo menos de dos mediciones, el sistema muestra el mismo mensaje
  de HU15 indicando que se necesitan al menos dos para graficar una
  tendencia.
- El cliente puede elegir que medida ver en el grafico (peso, alguna medida
  antropometrica o porcentaje de grasa), igual que el coach, pero limitado a
  sus propios datos.

--------------------------------------------------------------------
HU26 - Cliente visualiza su objetivo y avance
--------------------------------------------------------------------
Como cliente quiero ver el objetivo que tengo definido y cuanto me falta para
alcanzarlo para saber en que debo enfocarme.

Criterios de aceptacion:
- Dado un objetivo activo definido por mi coach (HU18), puedo ver su meta, la
  fecha limite y mi valor mas reciente registrado, junto con la diferencia
  restante hasta la meta.
- Dado que no tengo ningun objetivo activo, el sistema muestra un mensaje
  indicando que mi coach aun no ha definido uno.
- El cliente no puede editar su propio objetivo; solo el coach puede hacerlo
  (HU18/HU19).

--------------------------------------------------------------------
HU27 - Cliente visualiza sus fotos de progreso
--------------------------------------------------------------------
Como cliente quiero ver mis fotos de progreso ordenadas cronologicamente para
comparar visualmente mi transformacion.

Criterios de aceptacion:
- Dado que tengo fotos registradas por mi coach (HU16), puedo verlas
  ordenadas de la mas antigua a la mas reciente.
- Dado dos fotos seleccionadas, el sistema las muestra lado a lado para
  facilitar la comparacion visual.
- Dado que no tengo fotos registradas, el sistema muestra un mensaje
  indicandolo.

--------------------------------------------------------------------
HU28 - Notificacion de asignacion o modificacion de rutina
--------------------------------------------------------------------
Como cliente quiero recibir una notificacion dentro del sistema cuando mi
coach me asigne o modifique una rutina para enterarme de inmediato de los
cambios.

Nota (ambiguedad A12): se acota a notificacion interna (dentro del sistema);
no incluye correo ni notificaciones push, por ser un alcance no definido en
las historias generales.

Criterios de aceptacion:
- Dado que mi coach crea una rutina para mi (HU3.1) o cambia su estado
  (HU12), el sistema me muestra una notificacion no leida al ingresar a
  "Mis rutinas".
- Dado que abro la notificacion, el sistema me lleva directamente al detalle
  de la rutina correspondiente y la marca como leida.
- Dado varias notificaciones sin leer, el sistema las lista ordenadas de mas
  reciente a mas antigua.

--------------------------------------------------------------------
HU29 - Cliente deja comentario o duda sobre un ejercicio
--------------------------------------------------------------------
Como cliente quiero dejar un comentario o duda sobre un ejercicio de mi
rutina para que mi coach me responda antes de la siguiente sesion.

Nota (ambiguedad A13): el comentario siempre pertenece a un ejercicio dentro
de una rutina asignada concreta, no a un catalogo general de ejercicios (que
no existe en el alcance actual).

Criterios de aceptacion:
- Dado un ejercicio dentro de una rutina vigente, el cliente puede escribir
  un comentario asociado a ese ejercicio especifico.
- Dado un comentario enviado, el sistema lo marca como "pendiente de
  respuesta" hasta que el coach responda.
- Dado que el coach responde (HU30), el cliente ve la respuesta junto a su
  comentario original en el mismo ejercicio.

--------------------------------------------------------------------
HU30 - Coach recibe y responde comentarios de clientes
--------------------------------------------------------------------
Como coach quiero recibir las dudas o comentarios que dejan mis clientes en
sus rutinas para poder resolverlas de manera oportuna.

Criterios de aceptacion:
- Dado uno o mas comentarios pendientes de mis clientes, el sistema me los
  muestra agrupados en un listado, indicando cliente, rutina y ejercicio de
  origen.
- Dado que respondo un comentario, el sistema lo marca como "resuelto" y deja
  de aparecer en la lista de pendientes.
- Dado que un cliente inactivo (HU7) tiene comentarios previos sin responder,
  el sistema los conserva visibles en el historial pero fuera del listado de
  pendientes.

--------------------------------------------------------------------
HU31 - Panel general del administrador
--------------------------------------------------------------------
Como administrador quiero ver un panel general con el numero de clientes
activos, rutinas asignadas y objetivos proximos a vencer para tener una
vision rapida del estado del gimnasio.

Criterios de aceptacion:
- Dado el ingreso al panel, el administrador ve tres indicadores: total de
  clientes activos, total de rutinas vigentes y total de objetivos con fecha
  limite dentro de los proximos 14 dias.
- Dado que hace clic en cualquiera de los indicadores, el sistema lo lleva al
  listado filtrado correspondiente (clientes activos, rutinas vigentes u
  objetivos proximos a vencer).
- Dado que no hay datos para alguno de los indicadores, el sistema muestra
  "0" en vez de omitir el indicador.

--------------------------------------------------------------------
HU32 - Reporte de progreso de un cliente
--------------------------------------------------------------------
Como administrador quiero generar un reporte del progreso de un cliente en un
rango de fechas para compartirlo con el o usarlo en una evaluacion.

Nota (ambiguedad A10): se diferencia del grafico en pantalla (HU15/HU25, solo
lectura interactiva) en que el reporte es un documento exportable con un
rango de fechas explicito definido por el administrador.

Criterios de aceptacion:
- Dado un cliente y un rango de fechas, el administrador puede generar un
  reporte que incluya sus mediciones, objetivo vigente y cumplimiento de
  rutinas en ese rango.
- Dado un rango de fechas sin ningun dato registrado, el sistema genera el
  reporte indicando que no hay informacion disponible en ese periodo, en
  lugar de fallar.
- El reporte generado puede descargarse como archivo (PDF), independiente de
  los datos que se mantienen en pantalla.

--------------------------------------------------------------------
HU33 - Exportacion de informacion de clientes y progreso
--------------------------------------------------------------------
Como administrador quiero exportar la informacion de los clientes activos y
su progreso para respaldar los datos o analizarlos externamente.

Nota (ambiguedad A11): se acota el alcance a un archivo CSV con todos los
clientes activos y su resumen de progreso (ultima medicion y objetivo
vigente); otros formatos u otros alcances (por ejemplo, un solo cliente, o
incluir inactivos) quedan fuera del alcance actual y deberan solicitarse como
una historia adicional si se necesitan.

Criterios de aceptacion:
- Dado que el administrador solicita la exportacion, el sistema genera un
  archivo CSV con una fila por cliente activo: nombre, contacto, coach
  asignado, ultima medicion registrada y objetivo vigente.
- Dado que un cliente activo no tiene mediciones u objetivo registrado, el
  sistema deja esas columnas vacias en vez de omitir la fila.
- Dado que la exportacion se completa, el sistema ofrece la descarga
  inmediata del archivo generado.
"""

if __name__ == "__main__":
    print(historias_usuario_invest)
