# -*- coding: utf-8 -*-
"""
Wireframes en texto (ASCII) para las pantallas del Sistema de Administracion de
Gimnasio - Proyecto Final - Curso IA RACSA

Cada pantalla incluye el prompt utilizado para generarla y el wireframe
resultante en arte ASCII con caracteres de caja.
"""

wireframes = r"""
================================================================
PANTALLA 1 - HU1: Inicio de sesion
================================================================

PROMPT:
Dibuje un wireframe en modo texto (arte ASCII con caracteres de caja) de la
pantalla de inicio de sesion de un sistema de gestion de gimnasio. Use una sola
caja externa que enmarque toda la pantalla. Dentro, centrado: un titulo "Sistema
de Gimnasio" arriba, separado por una linea horizontal; debajo una caja "Iniciar
sesion" con dos campos en lineas separadas (Usuario, Contrasena) cada uno con
linea de entrada [__________]; debajo un boton [ Ingresar ] centrado; debajo un
enlace "Olvido su contrasena?"; y en la parte inferior de la pantalla, fuera de
la caja, un mensaje de error de ejemplo entre parentesis. Devuelva unicamente el
wireframe dentro de un bloque de texto monoespaciado, sin explicacion.

WIREFRAME:
+----------------------------------------------------------+
|                  Sistema de Gimnasio                      |
+----------------------------------------------------------+
|                                                            |
|          +------------------------------+                 |
|          |         Iniciar sesion         |                |
|          |                                |                |
|          |  Usuario:                      |                |
|          |  [__________________________]  |                |
|          |                                |                |
|          |  Contrasena:                   |                |
|          |  [__________________________]  |                |
|          |                                |                |
|          |          [ Ingresar ]          |                |
|          |                                |                |
|          |     Olvido su contrasena?      |                |
|          +------------------------------+                 |
|                                                            |
|         (Usuario o contrasena incorrectos)                |
+----------------------------------------------------------+


================================================================
PANTALLA 2 - HU2: Registro de cliente (Administrador)
================================================================

PROMPT:
Dibuje un wireframe en modo texto (arte ASCII con caracteres de caja) de la
pantalla de registro de un nuevo cliente para un administrador de gimnasio. Use
una sola caja externa. Arriba, una barra con "Panel Administrador" a la izquierda
y [ Cerrar sesion ] a la derecha, separada por linea horizontal. Debajo, titulo
"Nuevo cliente" y un formulario con: Nombre completo, Correo electronico,
Telefono (cada uno con linea de entrada), Estado con opciones tipo radio (*)
Activo ( ) Inactivo, y Coach asignado con un selector [ Seleccionar coach v ]. Al
final, dos botones alineados a la derecha: [ Cancelar ] y [ Guardar cliente ].
Devuelva unicamente el wireframe dentro de un bloque de texto monoespaciado, sin
explicacion.

WIREFRAME:
+----------------------------------------------------------+
| Panel Administrador                    [ Cerrar sesion ] |
+----------------------------------------------------------+
|  Nuevo cliente                                            |
|                                                            |
|  Nombre completo:                                         |
|  [______________________________________________]        |
|                                                            |
|  Correo electronico:                                      |
|  [______________________________________________]        |
|                                                            |
|  Telefono:                                                |
|  [______________________________________________]        |
|                                                            |
|  Estado:      (*) Activo      ( ) Inactivo                |
|                                                            |
|  Coach asignado:  [ Seleccionar coach            v ]      |
|                                                            |
|                                                            |
|                          [ Cancelar ] [ Guardar cliente ] |
+----------------------------------------------------------+


================================================================
PANTALLA 3 - HU3.1: Crear nueva rutina (Coach)
================================================================

PROMPT:
Dibuje un wireframe en modo texto (arte ASCII con caracteres de caja) de la
pantalla donde un coach crea una nueva rutina vacia. Use una sola caja externa.
Arriba, barra con "Panel Coach" a la izquierda y [ Cerrar sesion ] a la derecha.
Debajo, titulo "Nueva rutina" con dos campos: Cliente (selector [ Seleccionar
cliente v ]) y Nombre de la rutina (linea de entrada). Debajo, un aviso entre
parentesis indicando que el cliente ya tiene una rutina activa. Al final,
botones [ Cancelar ] y [ Crear rutina ] alineados a la derecha. Devuelva
unicamente el wireframe dentro de un bloque de texto monoespaciado, sin
explicacion.

WIREFRAME:
+----------------------------------------------------------+
| Panel Coach                            [ Cerrar sesion ] |
+----------------------------------------------------------+
|  Nueva rutina                                             |
|                                                            |
|  Cliente:      [ Seleccionar cliente             v ]      |
|                                                            |
|  Nombre de la rutina:                                     |
|  [______________________________________________]        |
|                                                            |
|  (Este cliente ya tiene una rutina activa:                |
|   "Fuerza - Fase 1". Desea crear otra en paralelo?)       |
|                                                            |
|                            [ Cancelar ] [ Crear rutina ] |
+----------------------------------------------------------+


================================================================
PANTALLA 4 - HU3.2: Agregar ejercicios a la rutina (Coach)
================================================================

PROMPT:
Dibuje un wireframe en modo texto (arte ASCII con caracteres de caja) de la
pantalla donde un coach agrega ejercicios a una rutina ya creada. Use una sola
caja externa con el titulo de la rutina arriba. Debajo, una tabla con columnas
Orden, Ejercicio, Series, Repeticiones, Descanso, mostrando 2 filas de ejemplo.
Debajo de la tabla, un boton [ + Agregar ejercicio ]. Al final, boton [ Guardar
rutina ] alineado a la derecha. Devuelva unicamente el wireframe dentro de un
bloque de texto monoespaciado, sin explicacion.

WIREFRAME:
+----------------------------------------------------------+
|  Rutina: Fuerza - Fase 1         (Cliente: J. Perez)      |
+----------------------------------------------------------+
| Ord | Ejercicio           | Series | Reps | Descanso      |
|-----|----------------------|--------|------|---------------|
|  1  | Sentadilla           |   4    |  10  |  90 seg       |
|  2  | Press banca          |   3    |  12  |  60 seg       |
|                                                            |
|                [ + Agregar ejercicio ]                    |
|                                                            |
|                                      [ Guardar rutina ]  |
+----------------------------------------------------------+


================================================================
PANTALLA 5 - HU3.3: Peso sugerido condicional segun tipo de
ejercicio (Coach)
================================================================

PROMPT:
Dibuje un wireframe en modo texto (arte ASCII con caracteres de caja) del
formulario "Agregar ejercicio" mostrando dos estados posibles lado a lado dentro
de una misma caja externa: Estado A y Estado B. En ambos, un selector "Tipo de
ejercicio" con opciones (*) Con peso / ( ) Sin peso. En el Estado A ("Con peso"
seleccionado), debe aparecer un campo adicional "Peso sugerido (kg): [____]". En
el Estado B ("Sin peso" seleccionado), ese campo no debe aparecer, y en su lugar
debe indicarse entre parentesis "(sin campo de peso)". Devuelva unicamente el
wireframe dentro de un bloque de texto monoespaciado, sin explicacion.

WIREFRAME:
+----------------------------------------------------------+
|  Agregar ejercicio                                        |
+-----------------------------+------------------------------+
|  Estado A: "Con peso"        |  Estado B: "Sin peso"        |
|                               |                              |
|  Ejercicio:                  |  Ejercicio:                  |
|  [Press militar___________]  |  [Plancha (cardio)________]  |
|                               |                              |
|  Tipo de ejercicio:          |  Tipo de ejercicio:          |
|  (*) Con peso  ( ) Sin peso  |  ( ) Con peso  (*) Sin peso  |
|                               |                              |
|  Peso sugerido (kg):         |  (sin campo de peso)         |
|  [_______]                   |                              |
|                               |                              |
|          [ Guardar ]         |          [ Guardar ]         |
+-----------------------------+------------------------------+


================================================================
PANTALLA 6 - HU4: Mis rutinas (Vista del cliente)
================================================================

PROMPT:
Dibuje un wireframe en modo texto (arte ASCII con caracteres de caja) de la
pantalla "Mis rutinas" vista por un cliente. Use una sola caja externa. Arriba,
barra con "Mis rutinas" a la izquierda y [ Cerrar sesion ] a la derecha. Debajo,
dos cajas lado a lado: a la izquierda una lista "Rutinas vigentes" con 2 rutinas
de ejemplo, una de ellas seleccionada (marcada entre corchetes); a la derecha una
caja "Detalle" con una tabla de ejercicios (Ejercicio, Series, Reps, Descanso,
Peso sugerido) de la rutina seleccionada. Debajo, fuera de ambas cajas, un
estado alternativo entre parentesis para cuando no hay rutinas asignadas.
Devuelva unicamente el wireframe dentro de un bloque de texto monoespaciado, sin
explicacion.

WIREFRAME:
+----------------------------------------------------------+
| Mis rutinas                            [ Cerrar sesion ] |
+------------------------+-----------------------------------+
| Rutinas vigentes        | Detalle: Fuerza - Fase 1          |
|                         |                                   |
| [Fuerza - Fase 1]       | Ejercicio    | Series | Reps | Peso |
|  Cardio - Lunes         |--------------|--------|------|------|
|                         | Sentadilla   |   4    |  10  | 40kg |
|                         | Press banca  |   3    |  12  | 30kg |
|                         | Plancha      |   3    |  30s |  -   |
|                         |                                   |
+------------------------+-----------------------------------+

  (Si el cliente no tiene rutinas: "Aun no tienes rutinas
   asignadas. Contacta a tu coach.")


================================================================
PANTALLA 7 - HU5: Registrar medidas antropometricas (Coach)
================================================================

PROMPT:
Dibuje un wireframe en modo texto (arte ASCII con caracteres de caja) de la
pantalla donde un coach registra las medidas antropometricas de un cliente. Use
una sola caja externa. Arriba, titulo "Registrar medicion" con el nombre del
cliente entre parentesis. Debajo, un formulario con: Fecha, Peso (kg), Cintura
(cm), Cadera (cm), Brazo (cm), Pierna (cm) y % de grasa corporal, cada uno con
linea de entrada. Debajo, un aviso entre parentesis indicando que ya existe una
medicion en esa fecha. Al final, botones [ Cancelar ] y [ Guardar medicion ]
alineados a la derecha. Devuelva unicamente el wireframe dentro de un bloque de
texto monoespaciado, sin explicacion.

WIREFRAME:
+----------------------------------------------------------+
|  Registrar medicion            (Cliente: J. Perez)        |
+----------------------------------------------------------+
|  Fecha:              [__________]                         |
|  Peso (kg):          [______]                              |
|  Cintura (cm):       [______]                              |
|  Cadera (cm):        [______]                              |
|  Brazo (cm):         [______]                              |
|  Pierna (cm):        [______]                              |
|  % grasa corporal:   [______]                              |
|                                                            |
|  (Ya existe una medicion para esta fecha.                 |
|   Desea sobrescribirla?)                                  |
|                                                            |
|                        [ Cancelar ] [ Guardar medicion ] |
+----------------------------------------------------------+
"""

if __name__ == "__main__":
    print(wireframes)
