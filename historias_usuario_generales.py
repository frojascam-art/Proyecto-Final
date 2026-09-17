# -*- coding: utf-8 -*-
"""
Historias de Usuario Generales - Sistema de Administracion de Gimnasio
Proyecto Final - Curso IA RACSA

Roles considerados:
- Administrador/Coach: gestiona clientes, rutinas, mediciones y objetivos.
- Cliente: consulta y sigue las rutinas asignadas y su propio progreso.
"""

historias_usuario_generales = """
HISTORIAS DE USUARIO GENERALES - SISTEMA DE ADMINISTRACION DE GIMNASIO

Epica 1: Gestion de Clientes (Administrador)

1. Como administrador quiero registrar nuevos clientes con sus datos personales y de
   contacto para tener un expediente centralizado de cada miembro del gimnasio.
2. Como administrador quiero editar la informacion de un cliente existente para
   mantener sus datos actualizados.
3. Como administrador quiero desactivar o dar de baja a un cliente para reflejar que
   ya no esta activo sin perder su historial.
4. Como administrador quiero buscar y filtrar clientes por nombre, estado o coach
   asignado para encontrar rapidamente el expediente que necesito.
5. Como administrador quiero asignar un coach responsable a cada cliente para
   distribuir la carga de trabajo y definir quien da seguimiento.

Epica 2: Rutinas de Entrenamiento (Administrador/Coach)

6. Como coach quiero crear rutinas de ejercicios personalizadas para cada cliente
   para adaptarlas a sus objetivos y nivel fisico.
7. Como coach quiero definir para cada ejercicio series, repeticiones, peso sugerido
   y tiempo de descanso para que el cliente sepa exactamente como ejecutarlo.
8. Como coach quiero organizar las rutinas por dia de la semana o por bloque (por
   ejemplo, tren superior, tren inferior, cardio) para estructurar el plan de
   entrenamiento completo.
9. Como coach quiero duplicar o usar como plantilla una rutina ya creada para ahorrar
   tiempo al armar rutinas similares para otros clientes.
10. Como coach quiero modificar una rutina asignada a un cliente para ajustarla segun
    su evolucion o disponibilidad.
11. Como coach quiero adjuntar videos o imagenes de referencia a un ejercicio para
    que el cliente entienda la tecnica correcta.
12. Como coach quiero ver el historial de rutinas anteriores de un cliente para
    evaluar la progresion de sus cargas de entrenamiento.

Epica 3: Medidas y Progreso Fisico (Administrador/Coach)

13. Como coach quiero registrar el peso corporal y medidas antropometricas (cintura,
    cadera, brazo, pierna, porcentaje de grasa, etc.) de un cliente para llevar un
    control periodico de su composicion corporal.
14. Como coach quiero visualizar la evolucion de las medidas de un cliente en un
    grafico a lo largo del tiempo para identificar tendencias y ajustar el plan si
    es necesario.
15. Como coach quiero registrar fotos de progreso del cliente para tener un respaldo
    visual ademas de los datos numericos.
16. Como coach quiero comparar dos periodos de medicion de un cliente para mostrarle
    de forma clara los avances obtenidos.

Epica 4: Objetivos (Administrador/Coach)

17. Como coach quiero definir un objetivo especifico para cada cliente (perder peso,
    ganar masa muscular, mejorar resistencia, etc.) para orientar el diseno de su
    rutina.
18. Como coach quiero establecer metas medibles con fecha limite para un cliente
    para poder evaluar si el plan esta funcionando.
19. Como coach quiero marcar un objetivo como cumplido o actualizarlo cuando cambie
    para mantener el plan alineado con las necesidades actuales del cliente.
20. Como coach quiero recibir una alerta cuando un cliente lleve varias semanas sin
    registrar avances para poder contactarlo y ajustar su seguimiento.

Epica 5: Vista del Cliente - Mis Rutinas

21. Como cliente quiero ver la rutina de entrenamiento que me asigno mi coach para
    saber que ejercicios debo realizar en cada sesion.
22. Como cliente quiero ver el detalle de cada ejercicio (series, repeticiones, peso
    sugerido y video demostrativo) para ejecutarlo correctamente.
23. Como cliente quiero marcar un ejercicio o una rutina completa como realizada
    para llevar un registro de mi cumplimiento.
24. Como cliente quiero registrar el peso real que utilice o las repeticiones que
    logre en cada ejercicio para que mi coach pueda ver si estoy progresando segun
    lo planeado.
25. Como cliente quiero consultar el historial de rutinas que ya complete para
    revisar como ha evolucionado mi entrenamiento.

Epica 6: Vista del Cliente - Mi Progreso y Objetivos

26. Como cliente quiero ver mis medidas corporales registradas por mi coach para
    conocer mi evolucion fisica.
27. Como cliente quiero visualizar un grafico de mi progreso (peso, medidas,
    porcentaje de grasa) a lo largo del tiempo para mantenerme motivado al ver
    resultados.
28. Como cliente quiero ver el objetivo que tengo definido y cuanto me falta para
    alcanzarlo para saber en que debo enfocarme.
29. Como cliente quiero ver mis fotos de progreso ordenadas cronologicamente para
    comparar visualmente mi transformacion.

Epica 7: Cuenta, Acceso y Comunicacion

30. Como cliente quiero iniciar sesion con mi usuario y contrasena para acceder
    unicamente a mi informacion personal y mis rutinas.
31. Como administrador quiero iniciar sesion con un rol de administrador/coach para
    acceder a las funciones de gestion de todos los clientes.
32. Como cliente quiero recibir una notificacion cuando mi coach me asigne o
    modifique una rutina para enterarme de inmediato de los cambios.
33. Como cliente quiero poder dejar un comentario o duda sobre un ejercicio de mi
    rutina para que mi coach me responda antes de la siguiente sesion.
34. Como coach quiero recibir las dudas o comentarios que dejan mis clientes en sus
    rutinas para poder resolverlas de manera oportuna.

Epica 8: Reportes y Panel General (Administrador)

35. Como administrador quiero ver un panel general con el numero de clientes
    activos, rutinas asignadas y objetivos proximos a vencer para tener una vision
    rapida del estado del gimnasio.
36. Como administrador quiero generar un reporte del progreso de un cliente en un
    rango de fechas para compartirlo con el o usarlo en una evaluacion.
37. Como administrador quiero exportar la informacion de clientes y su progreso
    para respaldar los datos o analizarlos externamente.
"""

if __name__ == "__main__":
    print(historias_usuario_generales)
