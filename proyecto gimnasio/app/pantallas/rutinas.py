# -*- coding: utf-8 -*-
"""
HU3.1 - Crear una rutina para un cliente
HU3.2 - Agregar ejercicios con sus parametros a una rutina
HU3.3 - Definir peso sugerido segun el tipo de ejercicio
HU10  - Organizacion de una rutina por dia o bloque
HU11  - Duplicar una rutina como base para otra
HU12  - Modificar el nombre o estado de una rutina asignada
HU13  - Adjuntar material de referencia a un ejercicio
HU14  - Historial de rutinas anteriores de un cliente (vista coach)
"""

import tkinter as tk
from tkinter import filedialog, ttk

from .. import datos
from .. import navegacion as nav
from .. import utils

DIAS_BLOQUE = ["Sin asignar", "Lunes", "Martes", "Miercoles", "Jueves", "Viernes",
               "Sabado", "Domingo", "Tren superior", "Tren inferior", "Cardio"]


def render_listado(contenedor, cliente_id):
    """Lista las rutinas activas de un cliente y sus acciones (HU3.1, HU10-HU12, HU14)."""
    cliente = datos.obtener_cliente_por_id(cliente_id)
    if not cliente:
        utils.mensaje_vacio(contenedor, "Cliente no encontrado.")
        return

    utils.titulo(contenedor, f"Rutinas de {cliente['nombre']} ({cliente['estado']})")

    marco_top = ttk.Frame(contenedor)
    marco_top.pack(fill="x", pady=(0, 10))
    ttk.Button(marco_top, text="+ Nueva rutina", style="Primario.TButton",
               command=lambda: nav.cargar_pantalla("rutina_form", cliente_id=cliente_id)
               ).pack(side="left", padx=(0, 8))
    ttk.Button(marco_top, text="Ver historial de rutinas finalizadas",
               command=lambda: nav.cargar_pantalla("rutinas_historial", cliente_id=cliente_id)
               ).pack(side="left")

    activas = datos.rutinas_activas_de_cliente(cliente_id)
    if not activas:
        utils.mensaje_vacio(contenedor, "Este cliente aun no tiene rutinas activas.")
        return

    columnas = [("nombre", "Nombre", 220), ("fecha", "Fecha de asignacion", 150),
                ("ejercicios", "Ejercicios", 90)]
    arbol = utils.tabla(contenedor, columnas, alturas=8)
    for rutina in activas:
        arbol.insert("", "end", iid=rutina["id"], values=(
            rutina["nombre"], rutina["fecha"], len(rutina["ejercicios"])))

    panel_acciones = ttk.Frame(contenedor)
    panel_acciones.pack(fill="x", pady=(8, 0))

    def _sin_seleccion():
        utils.limpiar(panel_acciones)
        ttk.Label(panel_acciones, text="Seleccione una rutina para ver acciones.",
                  style="Suave.TLabel").pack(anchor="w")

    def _on_select(_evento=None):
        seleccion = arbol.selection()
        if not seleccion:
            _sin_seleccion()
            return
        rutina_id = seleccion[0]
        utils.limpiar(panel_acciones)
        ttk.Button(panel_acciones, text="Ver / editar ejercicios", style="Primario.TButton",
                   command=lambda: nav.cargar_pantalla("rutina_ejercicios", rutina_id=rutina_id)
                   ).pack(side="left", padx=(0, 6))
        ttk.Button(panel_acciones, text="Editar nombre / estado",
                   command=lambda: _dialogo_editar_rutina(contenedor, rutina_id, cliente_id)
                   ).pack(side="left", padx=6)
        ttk.Button(panel_acciones, text="Duplicar",
                   command=lambda: _dialogo_duplicar_rutina(contenedor, rutina_id, cliente_id)
                   ).pack(side="left", padx=6)

    arbol.bind("<<TreeviewSelect>>", _on_select)
    _sin_seleccion()


def _dialogo_editar_rutina(padre, rutina_id, cliente_id):
    """Dialogo para renombrar una rutina o cambiar su estado activa/finalizada (HU12)."""
    rutina = datos.obtener_rutina_por_id(rutina_id)
    ventana, marco = utils.dialogo(padre, "Editar nombre / estado de la rutina",
                                    ancho=420, alto=230)

    nombre_v = utils.campo_formulario(marco, "Nombre de la rutina:",
                                       valor_inicial=rutina["nombre"])
    estado_v = utils.campo_combobox(marco, "Estado:", ["Activa", "Finalizada"],
                                     valor_inicial=rutina["estado"])

    def _guardar():
        nuevo_nombre = nombre_v.get().strip()
        if not nuevo_nombre:
            utils.error("El nombre de la rutina no puede quedar vacio.")
            return
        if estado_v.get() == "Finalizada" and rutina["estado"] == "Activa":
            otras_activas = [r for r in datos.rutinas_activas_de_cliente(cliente_id)
                             if r["id"] != rutina_id]
            if not otras_activas and not utils.confirmar(
                "Esta es la unica rutina activa de este cliente. Si la finaliza, el cliente "
                "quedara temporalmente sin rutinas vigentes. ¿Desea continuar?"):
                return
            datos.finalizar_rutina(rutina_id)
        elif estado_v.get() == "Activa" and rutina["estado"] == "Finalizada":
            datos.reactivar_rutina(rutina_id)
        datos.renombrar_rutina(rutina_id, nuevo_nombre)
        ventana.destroy()
        nav.cargar_pantalla("rutinas_listado", cliente_id=cliente_id)

    utils.botones_dialogo(marco, ventana.destroy, _guardar)


def _dialogo_duplicar_rutina(padre, rutina_id, cliente_id_origen):
    """Dialogo para duplicar una rutina existente hacia un cliente destino (HU11)."""
    rutina = datos.obtener_rutina_por_id(rutina_id)
    ventana, marco = utils.dialogo(padre, "Duplicar rutina", ancho=440, alto=260)
    ttk.Label(marco, text=f"Se copiaran los {len(rutina['ejercicios'])} ejercicio(s) de "
              f"\"{rutina['nombre']}\".", style="Suave.TLabel").pack(anchor="w", pady=(0, 8))

    nombres_clientes = [c["nombre"] for c in datos.clientes_activos()]
    cliente_actual = datos.obtener_cliente_por_id(cliente_id_origen)
    cliente_v = utils.campo_combobox(marco, "Cliente destino:", nombres_clientes,
                                      valor_inicial=cliente_actual["nombre"])
    nombre_v = utils.campo_formulario(marco, "Nombre de la nueva rutina:",
                                       valor_inicial=rutina["nombre"] + " (copia)")

    def _guardar():
        cliente_destino = next(
            (c for c in datos.clientes_activos() if c["nombre"] == cliente_v.get()), None)
        nuevo_nombre = nombre_v.get().strip()
        if not cliente_destino or not nuevo_nombre:
            utils.error("Debe indicar el cliente destino y el nombre de la nueva rutina.")
            return
        if datos.rutinas_activas_de_cliente(cliente_destino["id"]):
            respuesta = utils.preguntar_reemplazar(
                f"{cliente_destino['nombre']} ya tiene una rutina activa.")
            if respuesta is None:
                return
            if respuesta:
                for activa in datos.rutinas_activas_de_cliente(cliente_destino["id"]):
                    datos.finalizar_rutina(activa["id"])
        datos.duplicar_rutina(rutina_id, cliente_destino["id"], nuevo_nombre)
        ventana.destroy()
        utils.informar("Rutina duplicada correctamente.")
        nav.cargar_pantalla("rutinas_listado", cliente_id=cliente_destino["id"])

    utils.botones_dialogo(marco, ventana.destroy, _guardar, texto_guardar="Duplicar")


def render_form(contenedor, cliente_id):
    """Formulario para crear una rutina vacia y pasar a agregarle ejercicios (HU3.1)."""
    cliente = datos.obtener_cliente_por_id(cliente_id)
    utils.titulo(contenedor, f"Nueva rutina para {cliente['nombre']}")

    nombre_v = utils.campo_formulario(contenedor, "Nombre de la rutina:")

    def _crear():
        nombre = nombre_v.get().strip()
        if not nombre:
            utils.error("Debe indicar un nombre para la rutina.")
            return
        activas = datos.rutinas_activas_de_cliente(cliente_id)
        if activas:
            respuesta = utils.preguntar_reemplazar(
                f"{cliente['nombre']} ya tiene la rutina activa \"{activas[0]['nombre']}\".")
            if respuesta is None:
                return
            if respuesta:
                for activa in activas:
                    datos.finalizar_rutina(activa["id"])
        rutina = datos.crear_rutina(cliente_id, nombre)
        nav.cargar_pantalla("rutina_ejercicios", rutina_id=rutina["id"])

    botones = ttk.Frame(contenedor)
    botones.pack(anchor="w", pady=16)
    ttk.Button(botones, text="Cancelar",
               command=lambda: nav.cargar_pantalla("rutinas_listado", cliente_id=cliente_id)
               ).pack(side="left", padx=(0, 8))
    ttk.Button(botones, text="Crear rutina", style="Primario.TButton",
               command=_crear).pack(side="left")


def _texto_peso(ejercicio):
    if not ejercicio["tipo_con_peso"]:
        return "-"
    if ejercicio["peso_por_definir"] or ejercicio["peso"] is None:
        return "Peso a definir"
    return f"{ejercicio['peso']} {ejercicio['unidad']}"


def render_ejercicios(contenedor, rutina_id):
    """Muestra y permite editar la tabla de ejercicios de una rutina (HU3.2/HU3.3/HU10/HU13)."""
    rutina = datos.obtener_rutina_por_id(rutina_id)
    if not rutina:
        utils.mensaje_vacio(contenedor, "Rutina no encontrada.")
        return
    cliente = datos.obtener_cliente_por_id(rutina["cliente_id"])

    utils.titulo(contenedor, f"{rutina['nombre']} — {cliente['nombre']}")
    ttk.Label(contenedor, text=f"Estado: {rutina['estado']}",
              style="Suave.TLabel").pack(anchor="w", pady=(0, 8))

    columnas = [("orden", "Orden", 50), ("dia", "Dia/Bloque", 110), ("nombre", "Ejercicio", 160),
                ("series", "Series", 60), ("rep", "Repeticiones", 90), ("descanso", "Descanso", 90),
                ("peso", "Peso sugerido", 110), ("material", "Material", 90)]
    arbol = utils.tabla(contenedor, columnas, alturas=10)

    def _refrescar():
        arbol.delete(*arbol.get_children())
        for indice, ejercicio in enumerate(rutina["ejercicios"], start=1):
            arbol.insert("", "end", iid=ejercicio["id"], values=(
                indice, ejercicio.get("dia_bloque") or "Sin asignar", ejercicio["nombre"],
                ejercicio["series"], ejercicio["repeticiones"], ejercicio["descanso"],
                _texto_peso(ejercicio), "Si" if ejercicio.get("material") else "-"))

    _refrescar()

    marco_botones = ttk.Frame(contenedor)
    marco_botones.pack(fill="x", pady=8)
    ttk.Button(marco_botones, text="+ Agregar ejercicio", style="Primario.TButton",
               command=lambda: _abrir_form_ejercicio(contenedor, rutina, None, _refrescar)
               ).pack(side="left", padx=(0, 6))

    def _con_seleccion(accion):
        seleccion = arbol.selection()
        if not seleccion:
            utils.error("Seleccione primero un ejercicio de la tabla.")
            return
        accion(seleccion[0])

    def _editar_seleccionado(eid):
        ejercicio = next(e for e in rutina["ejercicios"] if e["id"] == eid)
        _abrir_form_ejercicio(contenedor, rutina, ejercicio, _refrescar)

    ttk.Button(marco_botones, text="Editar seleccionado",
               command=lambda: _con_seleccion(_editar_seleccionado)).pack(side="left", padx=6)
    ttk.Button(marco_botones, text="Subir",
               command=lambda: _con_seleccion(
                   lambda eid: (datos.mover_ejercicio(rutina_id, eid, "arriba"), _refrescar()))
               ).pack(side="left", padx=6)
    ttk.Button(marco_botones, text="Bajar",
               command=lambda: _con_seleccion(
                   lambda eid: (datos.mover_ejercicio(rutina_id, eid, "abajo"), _refrescar()))
               ).pack(side="left", padx=6)
    ttk.Button(marco_botones, text="Adjuntar material (HU13)",
               command=lambda: _con_seleccion(
                   lambda eid: _adjuntar_material(rutina_id, eid, _refrescar))
               ).pack(side="left", padx=6)

    ttk.Button(contenedor, text="Guardar y volver al listado de rutinas", style="Primario.TButton",
               command=lambda: nav.cargar_pantalla(
                   "rutinas_listado", cliente_id=rutina["cliente_id"])
               ).pack(anchor="w", pady=(16, 0))


def _adjuntar_material(rutina_id, ejercicio_id, refrescar):
    ruta = filedialog.askopenfilename(
        title="Seleccionar video o imagen de referencia",
        filetypes=[("Videos e imagenes", "*.mp4 *.mov *.avi *.png *.jpg *.jpeg *.gif"),
                   ("Todos los archivos", "*.*")])
    if not ruta:
        return
    datos.actualizar_ejercicio(rutina_id, ejercicio_id, material=ruta)
    refrescar()
    utils.informar("Material adjuntado al ejercicio.")


def _construir_campo_peso(marco, ejercicio, es_edicion):
    """Crea el tipo de ejercicio y el peso sugerido condicional; devuelve sus variables (HU3.3)."""
    marco_peso = ttk.Frame(marco)
    entrada_peso = tk.StringVar()
    unidad_v = tk.StringVar(value="kg")

    def _refrescar_peso(*_):
        utils.limpiar(marco_peso)
        if tipo_v.get() != "Con peso":
            marco_peso.pack_forget()
            return
        marco_peso.pack(fill="x", pady=4)
        fila = ttk.Frame(marco_peso)
        fila.pack(fill="x")
        ttk.Label(fila, text="Peso sugerido:", width=24).pack(side="left")
        tiene_peso = es_edicion and ejercicio.get("peso")
        entrada_peso.set(str(ejercicio["peso"]) if tiene_peso else "")
        ttk.Entry(fila, textvariable=entrada_peso, width=10).pack(side="left")
        unidad_v.set((ejercicio.get("unidad") if es_edicion else "kg") or "kg")
        ttk.Combobox(fila, textvariable=unidad_v, values=["kg", "lb"], width=6,
                     state="readonly").pack(side="left", padx=6)

    tipo_inicial = "Con peso" if (not es_edicion or ejercicio["tipo_con_peso"]) else "Sin peso"
    tipo_v = utils.campo_radiobuttons(marco, "Tipo de ejercicio:", ["Con peso", "Sin peso"],
                                       valor_inicial=tipo_inicial, callback=_refrescar_peso)
    _refrescar_peso()
    return tipo_v, entrada_peso, unidad_v


def _construir_campos_ejercicio(marco, ejercicio, es_edicion):
    """Crea todos los campos del formulario de ejercicio; devuelve sus StringVar en un dict."""
    campos_v = {
        "nombre": utils.campo_formulario(
            marco, "Ejercicio:", valor_inicial=ejercicio["nombre"] if es_edicion else ""),
    }
    dia_inicial = (ejercicio.get("dia_bloque") if es_edicion else "Sin asignar") or "Sin asignar"
    campos_v["dia"] = utils.campo_combobox(marco, "Dia / bloque:", DIAS_BLOQUE,
                                            valor_inicial=dia_inicial)
    campos_v["tipo"], campos_v["peso"], campos_v["unidad"] = _construir_campo_peso(
        marco, ejercicio, es_edicion)
    campos_v["series"] = utils.campo_formulario(
        marco, "Series:", valor_inicial=str(ejercicio["series"]) if es_edicion else "")
    rep_inicial = str(ejercicio["repeticiones"]) if es_edicion else ""
    campos_v["repeticiones"] = utils.campo_formulario(marco, "Repeticiones:",
                                                        valor_inicial=rep_inicial)
    campos_v["descanso"] = utils.campo_formulario(
        marco, "Descanso:", valor_inicial=ejercicio["descanso"] if es_edicion else "")
    return campos_v


def _leer_campos_ejercicio(campos_v):
    """Valida el formulario de ejercicio y arma el diccionario a guardar, o None si falta algo."""
    nombre = campos_v["nombre"].get().strip()
    series = campos_v["series"].get().strip()
    repeticiones = campos_v["repeticiones"].get().strip()
    descanso = campos_v["descanso"].get().strip()
    if not nombre or not series or not repeticiones:
        return None

    con_peso = campos_v["tipo"].get() == "Con peso"
    peso = None
    unidad = None
    peso_por_definir = False
    if con_peso:
        unidad = campos_v["unidad"].get()
        valor_peso = utils.numero_o_none(campos_v["peso"].get())
        if valor_peso is None:
            peso_por_definir = True
        else:
            peso = valor_peso

    return {"nombre": nombre, "dia_bloque": campos_v["dia"].get(), "tipo_con_peso": con_peso,
            "peso": peso, "unidad": unidad, "peso_por_definir": peso_por_definir,
            "series": series, "repeticiones": repeticiones, "descanso": descanso}


def _abrir_form_ejercicio(padre, rutina, ejercicio, refrescar):
    """Dialogo para agregar o editar un ejercicio de una rutina (HU3.2/HU3.3/HU10)."""
    es_edicion = ejercicio is not None
    ventana, marco = utils.dialogo(
        padre, "Editar ejercicio" if es_edicion else "Agregar ejercicio", ancho=440, alto=420)
    campos_v = _construir_campos_ejercicio(marco, ejercicio, es_edicion)

    def _guardar():
        campos = _leer_campos_ejercicio(campos_v)
        if campos is None:
            utils.error("Debe indicar nombre del ejercicio, series y repeticiones.")
            return
        if es_edicion:
            datos.actualizar_ejercicio(rutina["id"], ejercicio["id"], **campos)
        else:
            campos["material"] = ""
            datos.agregar_ejercicio(rutina["id"], **campos)
        ventana.destroy()
        refrescar()

    utils.botones_dialogo(marco, ventana.destroy, _guardar, texto_guardar="Guardar ejercicio")


def render_historial(contenedor, cliente_id):
    """Historial de rutinas finalizadas de un cliente, en modo solo lectura (HU14)."""
    cliente = datos.obtener_cliente_por_id(cliente_id)
    utils.titulo(contenedor, f"Historial de rutinas finalizadas — {cliente['nombre']}")

    finalizadas = datos.rutinas_finalizadas_de_cliente(cliente_id)
    if not finalizadas:
        utils.mensaje_vacio(contenedor, "Este cliente aun no tiene rutinas finalizadas.")
    else:
        columnas = [("nombre", "Nombre", 220), ("fecha", "Fecha de asignacion", 150),
                    ("ejercicios", "Ejercicios", 90)]
        arbol = utils.tabla(contenedor, columnas, alturas=10)
        for rutina in sorted(finalizadas, key=lambda r: r["fecha"], reverse=True):
            arbol.insert("", "end", iid=rutina["id"], values=(
                rutina["nombre"], rutina["fecha"], len(rutina["ejercicios"])))

        def _on_select(_evento=None):
            seleccion = arbol.selection()
            if seleccion:
                nav.cargar_pantalla("rutina_ejercicios", rutina_id=seleccion[0])

        arbol.bind("<Double-1>", _on_select)
        ttk.Label(contenedor, text="Doble clic sobre una rutina para ver su detalle.",
                  style="Suave.TLabel").pack(anchor="w", pady=(4, 0))

    ttk.Button(contenedor, text="Volver a rutinas activas",
               command=lambda: nav.cargar_pantalla("rutinas_listado", cliente_id=cliente_id)
               ).pack(anchor="w", pady=(16, 0))


nav.registrar_pantalla("rutinas_listado", render_listado)
nav.registrar_pantalla("rutina_form", render_form)
nav.registrar_pantalla("rutina_ejercicios", render_ejercicios)
nav.registrar_pantalla("rutinas_historial", render_historial)
