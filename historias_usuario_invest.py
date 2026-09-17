# -*- coding: utf-8 -*-
"""
Historias de Usuario refinadas con analisis de ambiguedad y validacion INVEST
Sistema de Administracion de Gimnasio - Proyecto Final - Curso IA RACSA

Orden de creacion del sistema (dependencias tecnicas):
HU1 (auth/roles) -> HU2 (clientes) -> HU3.1/3.2/3.3 (rutinas) -> HU4 (cliente ve
rutina) ; HU2 -> HU5 (medidas)

Nota: la HU3 original se dividio en tres historias mas pequenas (HU3.1, HU3.2 y
HU3.3) tras el analisis INVEST, porque mezclaba mas de una responsabilidad y
tenia una ambiguedad de negocio (el peso sugerido no aplica a todos los
ejercicios).
"""

historias_usuario_invest = """
HISTORIAS DE USUARIO REFINADAS (ANALISIS DE AMBIGUEDAD + INVEST)

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
"""

if __name__ == "__main__":
    print(historias_usuario_invest)
