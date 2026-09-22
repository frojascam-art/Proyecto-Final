# -*- coding: utf-8 -*-
"""
Datos de ejemplo y funciones de acceso/modificacion en memoria, con
persistencia en un archivo JSON local (datos_gimnasio.json, junto a
main.py). Equivalente en espiritu a js/datos.js del prototipo
(prototipo gimnasio/), pero a diferencia de aquel prototipo estatico,
aqui los cambios se guardan en disco despues de cada operacion que
crea o modifica informacion, para que los datos persistan entre
ejecuciones del programa.
"""

import json
from datetime import date, datetime, timedelta
from pathlib import Path

RUTA_DATOS = Path(__file__).resolve().parent.parent / "datos_gimnasio.json"

_contador_id = {"valor": 0}


def generar_id(prefijo):
    """Genera un identificador unico y legible con el prefijo indicado."""
    _contador_id["valor"] += 1
    return f"{prefijo}-{_contador_id['valor']}"


def hoy_iso():
    """Devuelve la fecha de hoy en formato AAAA-MM-DD."""
    return date.today().isoformat()


def _fecha(valor_iso):
    """Convierte una fecha en texto (AAAA-MM-DD) a un objeto date."""
    return datetime.fromisoformat(valor_iso).date()


# ---------------------------------------------------------------------
# Datos de ejemplo (valores iniciales; se sobrescriben al cargar el JSON)
# ---------------------------------------------------------------------

coaches = [
    {"id": "coach-1", "nombre": "Coach Ana Marin"},
    {"id": "coach-2", "nombre": "Coach Luis Vargas"},
]

clientes = [
    {"id": "cliente-1", "nombre": "Juan Perez", "correo": "juan.perez@example.com",
     "telefono": "8888-1111", "estado": "Activo", "coach_id": "coach-1"},
    {"id": "cliente-2", "nombre": "Maria Rojas", "correo": "maria.rojas@example.com",
     "telefono": "", "estado": "Activo", "coach_id": "coach-2"},
    {"id": "cliente-3", "nombre": "Carlos Solis", "correo": "",
     "telefono": "8888-3333", "estado": "Inactivo", "coach_id": "coach-1"},
]

rutinas = [
    {
        "id": "rutina-1", "cliente_id": "cliente-1", "nombre": "Fuerza - Fase 1",
        "fecha": "2026-08-01", "estado": "Activa",
        "ejercicios": [
            {"id": "ejercicio-1", "nombre": "Sentadilla", "dia_bloque": "Lunes",
             "tipo_con_peso": True, "peso": 40, "unidad": "kg", "peso_por_definir": False,
             "series": 4, "repeticiones": "10", "descanso": "90 seg", "material": ""},
            {"id": "ejercicio-2", "nombre": "Press banca", "dia_bloque": "Lunes",
             "tipo_con_peso": True, "peso": 30, "unidad": "kg", "peso_por_definir": False,
             "series": 3, "repeticiones": "12", "descanso": "60 seg", "material": ""},
            {"id": "ejercicio-3", "nombre": "Plancha", "dia_bloque": "Miercoles",
             "tipo_con_peso": False, "peso": None, "unidad": None, "peso_por_definir": False,
             "series": 3, "repeticiones": "30 seg", "descanso": "30 seg", "material": ""},
        ],
        "registros_cumplimiento": [],
    },
    {
        "id": "rutina-2", "cliente_id": "cliente-2", "nombre": "Cardio - Lunes",
        "fecha": "2026-09-01", "estado": "Activa", "ejercicios": [],
        "registros_cumplimiento": [],
    },
]

mediciones = [
    {"id": "medicion-1", "cliente_id": "cliente-1", "fecha": "2026-08-01",
     "peso": 78, "cintura": 88, "cadera": None, "brazo": 35, "pierna": None, "grasa": 18},
]

fotos_progreso = []   # HU16 / HU27
objetivos = []         # HU18 / HU19 / HU26
comentarios = []       # HU29 / HU30
notificaciones = []    # HU28


# ---------------------------------------------------------------------
# Persistencia en JSON
# ---------------------------------------------------------------------

def _coleccion_por_nombre():
    """Mapa {clave del JSON: lista/objeto en memoria correspondiente}."""
    return {
        "coaches": coaches, "clientes": clientes, "rutinas": rutinas,
        "mediciones": mediciones, "fotos_progreso": fotos_progreso,
        "objetivos": objetivos, "comentarios": comentarios,
        "notificaciones": notificaciones,
    }


def guardar_datos():
    """Escribe todo el estado en memoria en RUTA_DATOS (datos_gimnasio.json)."""
    contenido = {"contador_id": _contador_id["valor"], **_coleccion_por_nombre()}
    try:
        with open(RUTA_DATOS, "w", encoding="utf-8") as archivo:
            json.dump(contenido, archivo, ensure_ascii=False, indent=2)
    except OSError:
        pass  # sin permisos o disco lleno: la sesion continua solo en memoria


def cargar_datos():
    """Carga RUTA_DATOS si existe; si no, crea el archivo con los datos de ejemplo."""
    if not RUTA_DATOS.exists():
        guardar_datos()
        return
    try:
        with open(RUTA_DATOS, "r", encoding="utf-8") as archivo:
            contenido = json.load(archivo)
    except (OSError, json.JSONDecodeError):
        return  # archivo corrupto o ilegible: se sigue con los datos de ejemplo en memoria

    _contador_id["valor"] = contenido.get("contador_id", _contador_id["valor"])
    for clave, coleccion in _coleccion_por_nombre().items():
        coleccion[:] = contenido.get(clave, coleccion)


# ---------------------------------------------------------------------
# Clientes - HU2, HU6, HU7, HU8, HU9
# ---------------------------------------------------------------------

def obtener_cliente_por_id(cliente_id):
    """Busca un cliente por su id; devuelve None si no existe."""
    return next((c for c in clientes if c["id"] == cliente_id), None)


def clientes_filtrados(texto="", estado="Todos", coach_id=None):
    """Filtra clientes por nombre (contiene), estado y coach asignado (HU8)."""
    texto = (texto or "").strip().lower()
    resultado = clientes
    if texto:
        resultado = [c for c in resultado if texto in c["nombre"].lower()]
    if estado and estado != "Todos":
        resultado = [c for c in resultado if c["estado"] == estado]
    if coach_id:
        resultado = [c for c in resultado if c["coach_id"] == coach_id]
    return resultado


def clientes_activos():
    """Devuelve solo los clientes con estado Activo."""
    return [c for c in clientes if c["estado"] == "Activo"]


def existe_correo_duplicado(correo, ignorar_id=None):
    """Indica si otro cliente ya usa ese correo (HU2/HU6)."""
    if not correo:
        return False
    return any(c["correo"] and c["correo"].lower() == correo.lower() and c["id"] != ignorar_id
               for c in clientes)


def nombre_coach(coach_id):
    """Devuelve el nombre del coach o 'Sin asignar' si no se encuentra."""
    coach = next((c for c in coaches if c["id"] == coach_id), None)
    return coach["nombre"] if coach else "Sin asignar"


def crear_cliente(nombre, correo, telefono, coach_id, estado="Activo"):
    """Registra un nuevo cliente (HU2)."""
    cliente = {"id": generar_id("cliente"), "nombre": nombre, "correo": correo,
               "telefono": telefono, "estado": estado, "coach_id": coach_id}
    clientes.append(cliente)
    guardar_datos()
    return cliente


def actualizar_cliente(cliente_id, **cambios):
    """Actualiza cualquier campo de un cliente existente (HU6/HU9)."""
    cliente = obtener_cliente_por_id(cliente_id)
    if cliente:
        cliente.update(cambios)
        guardar_datos()
    return cliente


def cambiar_estado_cliente(cliente_id, nuevo_estado):
    """Activa o desactiva a un cliente (HU7)."""
    return actualizar_cliente(cliente_id, estado=nuevo_estado)


# ---------------------------------------------------------------------
# Rutinas y ejercicios - HU3.1, HU3.2, HU3.3, HU10, HU11, HU12, HU13, HU14
# ---------------------------------------------------------------------

def rutinas_de_cliente(cliente_id, estado=None):
    """Rutinas de un cliente, opcionalmente filtradas por estado."""
    resultado = [r for r in rutinas if r["cliente_id"] == cliente_id]
    if estado:
        resultado = [r for r in resultado if r["estado"] == estado]
    return resultado


def rutinas_activas_de_cliente(cliente_id):
    """Rutinas vigentes (Activa) de un cliente (HU4)."""
    return rutinas_de_cliente(cliente_id, estado="Activa")


def rutinas_finalizadas_de_cliente(cliente_id):
    """Rutinas finalizadas de un cliente, para el historial (HU14)."""
    return rutinas_de_cliente(cliente_id, estado="Finalizada")


def obtener_rutina_por_id(rutina_id):
    """Busca una rutina por su id; devuelve None si no existe."""
    return next((r for r in rutinas if r["id"] == rutina_id), None)


def crear_rutina(cliente_id, nombre):
    """Crea una rutina vacia para un cliente (HU3.1)."""
    rutina = {"id": generar_id("rutina"), "cliente_id": cliente_id, "nombre": nombre,
              "fecha": hoy_iso(), "estado": "Activa", "ejercicios": [],
              "registros_cumplimiento": []}
    rutinas.append(rutina)
    guardar_datos()
    return rutina


def duplicar_rutina(rutina_id, cliente_id, nombre_nuevo):
    """Copia una rutina existente (con sus ejercicios) para otro cliente (HU11)."""
    original = obtener_rutina_por_id(rutina_id)
    if not original:
        return None
    copia = {
        "id": generar_id("rutina"), "cliente_id": cliente_id, "nombre": nombre_nuevo,
        "fecha": hoy_iso(), "estado": "Activa",
        "ejercicios": [dict(e, id=generar_id("ejercicio")) for e in original["ejercicios"]],
        "registros_cumplimiento": [],
    }
    rutinas.append(copia)
    guardar_datos()
    return copia


def renombrar_rutina(rutina_id, nuevo_nombre):
    """Cambia el nombre de una rutina (HU12)."""
    rutina = obtener_rutina_por_id(rutina_id)
    if rutina:
        rutina["nombre"] = nuevo_nombre
        guardar_datos()
    return rutina


def finalizar_rutina(rutina_id):
    """Marca una rutina como Finalizada (HU12)."""
    rutina = obtener_rutina_por_id(rutina_id)
    if rutina:
        rutina["estado"] = "Finalizada"
        guardar_datos()
    return rutina


def reactivar_rutina(rutina_id):
    """Vuelve a marcar una rutina como Activa (HU12)."""
    rutina = obtener_rutina_por_id(rutina_id)
    if rutina:
        rutina["estado"] = "Activa"
        guardar_datos()
    return rutina


def agregar_ejercicio(rutina_id, **campos):
    """Agrega un ejercicio al final de una rutina (HU3.2/HU3.3)."""
    rutina = obtener_rutina_por_id(rutina_id)
    if not rutina:
        return None
    ejercicio = {"id": generar_id("ejercicio"), **campos}
    rutina["ejercicios"].append(ejercicio)
    guardar_datos()
    return ejercicio


def actualizar_ejercicio(rutina_id, ejercicio_id, **campos):
    """Actualiza los campos de un ejercicio existente (HU3.2/HU3.3/HU13)."""
    rutina = obtener_rutina_por_id(rutina_id)
    if not rutina:
        return None
    ejercicio = next((e for e in rutina["ejercicios"] if e["id"] == ejercicio_id), None)
    if ejercicio:
        ejercicio.update(campos)
        guardar_datos()
    return ejercicio


def mover_ejercicio(rutina_id, ejercicio_id, direccion):
    """Intercambia un ejercicio con el anterior/siguiente en el orden (HU3.2)."""
    rutina = obtener_rutina_por_id(rutina_id)
    ejercicios = rutina["ejercicios"]
    indice = next((i for i, e in enumerate(ejercicios) if e["id"] == ejercicio_id), None)
    if indice is None:
        return
    nuevo_indice = indice - 1 if direccion == "arriba" else indice + 1
    if 0 <= nuevo_indice < len(ejercicios):
        ejercicios[indice], ejercicios[nuevo_indice] = ejercicios[nuevo_indice], ejercicios[indice]
        guardar_datos()


def registro_de_hoy(rutina_id):
    """Devuelve (creandolo si no existe) el registro de cumplimiento de hoy (HU21/HU22)."""
    rutina = obtener_rutina_por_id(rutina_id)
    hoy = hoy_iso()
    registro = next((r for r in rutina["registros_cumplimiento"] if r["fecha"] == hoy), None)
    if not registro:
        registro = {"fecha": hoy, "ejercicios": {}}
        rutina["registros_cumplimiento"].append(registro)
        guardar_datos()
    return registro


def marcar_ejercicio_realizado(rutina_id, ejercicio_id, realizado, peso_usado=None,
                                repeticiones_logradas=None):
    """Registra el cumplimiento y desempeno de hoy para un ejercicio (HU21/HU22)."""
    registro = registro_de_hoy(rutina_id)
    registro["ejercicios"][ejercicio_id] = {
        "realizado": realizado, "peso_usado": peso_usado,
        "repeticiones_logradas": repeticiones_logradas,
    }
    guardar_datos()


def registros_de_cliente(cliente_id):
    """Historial de cumplimiento (HU23) de todas las rutinas del cliente."""
    resultado = []
    for rutina in rutinas_de_cliente(cliente_id):
        for registro in rutina["registros_cumplimiento"]:
            resultado.append((rutina, registro))
    resultado.sort(key=lambda par: par[1]["fecha"], reverse=True)
    return resultado


# ---------------------------------------------------------------------
# Mediciones - HU5, HU15, HU17
# ---------------------------------------------------------------------

def mediciones_de_cliente(cliente_id):
    """Mediciones de un cliente, de la mas reciente a la mas antigua."""
    return sorted([m for m in mediciones if m["cliente_id"] == cliente_id],
                  key=lambda m: m["fecha"], reverse=True)


def existe_medicion_en_fecha(cliente_id, fecha, ignorar_id=None):
    """Indica si ya hay una medicion de ese cliente en esa fecha (HU5)."""
    return any(m["cliente_id"] == cliente_id and m["fecha"] == fecha and m["id"] != ignorar_id
               for m in mediciones)


def guardar_medicion(cliente_id, fecha, sobrescribir_id=None, **valores):
    """Crea una medicion nueva o sobrescribe una existente en la misma fecha (HU5)."""
    if sobrescribir_id:
        medicion = next((m for m in mediciones if m["id"] == sobrescribir_id), None)
        if medicion:
            medicion.update(valores)
            guardar_datos()
            return medicion
    medicion = {"id": generar_id("medicion"), "cliente_id": cliente_id, "fecha": fecha, **valores}
    mediciones.append(medicion)
    guardar_datos()
    return medicion


# ---------------------------------------------------------------------
# Fotos de progreso - HU16, HU27
# ---------------------------------------------------------------------

def fotos_de_cliente(cliente_id):
    """Fotos de progreso de un cliente, ordenadas cronologicamente."""
    return sorted([f for f in fotos_progreso if f["cliente_id"] == cliente_id],
                  key=lambda f: f["fecha"])


def agregar_foto(cliente_id, fecha, ruta, descripcion=""):
    """Registra una foto de progreso para un cliente en una fecha (HU16)."""
    foto = {"id": generar_id("foto"), "cliente_id": cliente_id, "fecha": fecha,
            "ruta": ruta, "descripcion": descripcion}
    fotos_progreso.append(foto)
    guardar_datos()
    return foto


def eliminar_foto(foto_id):
    """Elimina una foto de progreso por su id (HU16)."""
    fotos_progreso[:] = [f for f in fotos_progreso if f["id"] != foto_id]
    guardar_datos()


# ---------------------------------------------------------------------
# Objetivos - HU18, HU19, HU20, HU26
# ---------------------------------------------------------------------

def objetivo_activo_de_cliente(cliente_id):
    """Objetivo actualmente activo de un cliente, o None."""
    return next((o for o in objetivos if o["cliente_id"] == cliente_id and o["estado"] == "Activo"),
                None)


def objetivos_de_cliente(cliente_id):
    """Todos los objetivos de un cliente, del mas reciente al mas antiguo."""
    return sorted([o for o in objetivos if o["cliente_id"] == cliente_id],
                  key=lambda o: o["fecha_limite"], reverse=True)


def crear_objetivo(cliente_id, tipo, valor_meta, unidad, fecha_limite):
    """Define un nuevo objetivo activo para un cliente (HU18)."""
    objetivo = {"id": generar_id("objetivo"), "cliente_id": cliente_id, "tipo": tipo,
                "valor_meta": valor_meta, "unidad": unidad, "fecha_limite": fecha_limite,
                "estado": "Activo", "fecha_cumplido": None, "historial": []}
    objetivos.append(objetivo)
    guardar_datos()
    return objetivo


def actualizar_objetivo(objetivo_id, **cambios):
    """Actualiza la meta o fecha limite de un objetivo, guardando el valor previo (HU19)."""
    objetivo = next((o for o in objetivos if o["id"] == objetivo_id), None)
    if objetivo:
        objetivo["historial"].append({
            "valor_meta": objetivo["valor_meta"], "fecha_limite": objetivo["fecha_limite"],
            "cambiado_el": hoy_iso(),
        })
        objetivo.update(cambios)
        guardar_datos()
    return objetivo


def marcar_objetivo_cumplido(objetivo_id):
    """Cierra un objetivo como Cumplido, con la fecha de hoy (HU19)."""
    objetivo = next((o for o in objetivos if o["id"] == objetivo_id), None)
    if objetivo:
        objetivo["estado"] = "Cumplido"
        objetivo["fecha_cumplido"] = hoy_iso()
        guardar_datos()
    return objetivo


def objetivos_proximos_a_vencer(dias=14):
    """Objetivos activos cuya fecha limite esta dentro de los proximos N dias (HU31)."""
    limite = date.today() + timedelta(days=dias)
    return [o for o in objetivos if o["estado"] == "Activo" and _fecha(o["fecha_limite"]) <= limite]


# ---------------------------------------------------------------------
# Alertas de inactividad - HU20
# ---------------------------------------------------------------------

def ultima_fecha_avance(cliente_id):
    """Fecha del ultimo avance (medicion o cumplimiento) de un cliente, o None."""
    fechas = [m["fecha"] for m in mediciones_de_cliente(cliente_id)]
    for rutina in rutinas_de_cliente(cliente_id):
        fechas += [r["fecha"] for r in rutina["registros_cumplimiento"]]
    return max(fechas) if fechas else None


def clientes_inactivos(semanas=3):
    """Clientes activos sin avances en las ultimas N semanas, con su ultima fecha (HU20)."""
    limite = date.today() - timedelta(weeks=semanas)
    resultado = []
    for cliente in clientes_activos():
        ultima = ultima_fecha_avance(cliente["id"])
        if ultima is None or _fecha(ultima) < limite:
            resultado.append((cliente, ultima))
    return resultado


# ---------------------------------------------------------------------
# Comentarios - HU29, HU30
# ---------------------------------------------------------------------

def crear_comentario(cliente_id, rutina_id, ejercicio_id, texto):
    """Registra un comentario/duda del cliente sobre un ejercicio (HU29)."""
    comentario = {"id": generar_id("comentario"), "cliente_id": cliente_id, "rutina_id": rutina_id,
                  "ejercicio_id": ejercicio_id, "texto_cliente": texto, "fecha": hoy_iso(),
                  "estado": "Pendiente", "respuesta_coach": None, "fecha_respuesta": None}
    comentarios.append(comentario)
    guardar_datos()
    return comentario


def comentarios_pendientes():
    """Comentarios de clientes que aun no tienen respuesta del coach (HU30)."""
    return [c for c in comentarios if c["estado"] == "Pendiente"]


def comentarios_de_ejercicio(rutina_id, ejercicio_id):
    """Comentarios existentes sobre un ejercicio puntual de una rutina."""
    return [c for c in comentarios
            if c["rutina_id"] == rutina_id and c["ejercicio_id"] == ejercicio_id]


def responder_comentario(comentario_id, respuesta):
    """Responde un comentario pendiente y lo marca como Resuelto (HU30)."""
    comentario = next((c for c in comentarios if c["id"] == comentario_id), None)
    if comentario:
        comentario["respuesta_coach"] = respuesta
        comentario["fecha_respuesta"] = hoy_iso()
        comentario["estado"] = "Resuelto"
        guardar_datos()
    return comentario


# ---------------------------------------------------------------------
# Notificaciones - HU28
# ---------------------------------------------------------------------

def crear_notificacion(cliente_id, mensaje, rutina_id=None):
    """Crea una notificacion no leida para un cliente (HU28)."""
    notificacion = {"id": generar_id("notificacion"), "cliente_id": cliente_id,
                    "mensaje": mensaje, "rutina_id": rutina_id, "leida": False,
                    "fecha": hoy_iso()}
    notificaciones.append(notificacion)
    guardar_datos()
    return notificacion


def notificaciones_de_cliente(cliente_id):
    """Notificaciones de un cliente, de la mas reciente a la mas antigua."""
    return sorted([n for n in notificaciones if n["cliente_id"] == cliente_id],
                  key=lambda n: n["fecha"], reverse=True)


def marcar_notificacion_leida(notificacion_id):
    """Marca una notificacion como leida (HU28)."""
    notificacion = next((n for n in notificaciones if n["id"] == notificacion_id), None)
    if notificacion:
        notificacion["leida"] = True
        guardar_datos()
