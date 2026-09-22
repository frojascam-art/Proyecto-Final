# -*- coding: utf-8 -*-
"""
HU18 - Definicion de objetivo y meta medible con fecha limite
HU19 - Actualizacion o cierre de un objetivo

render_listado se reutiliza con solo_lectura=True para HU26 (el cliente ve
su objetivo y cuanto le falta), llamado desde app/pantallas/mi_progreso.py.
"""

from tkinter import ttk

from .. import datos
from .. import navegacion as nav
from .. import utils

TIPOS_OBJETIVO = ["Perder peso", "Ganar masa muscular", "Mejorar resistencia", "Otro"]


def _cliente_objetivo(cliente_id):
    return cliente_id or nav.estado["cliente_en_foco_id"]


def _volver(cliente_id):
    if nav.estado["rol"] == "cliente":
        nav.cargar_pantalla("mi_progreso")
    else:
        nav.cargar_pantalla("objetivos_listado", cliente_id=cliente_id)


def _diferencia_a_meta(cliente_id, objetivo):
    mediciones = datos.mediciones_de_cliente(cliente_id)
    if not mediciones or objetivo["unidad"].strip().lower() not in ("kg", "kg."):
        return None
    ultimo_peso = mediciones[0].get("peso")
    if ultimo_peso is None:
        return None
    return ultimo_peso - objetivo["valor_meta"]


def render_listado(contenedor, cliente_id=None, solo_lectura=False):
    """Muestra el objetivo activo y el historial de un cliente (HU18/HU19/HU26)."""
    cliente_id = _cliente_objetivo(cliente_id)
    cliente = datos.obtener_cliente_por_id(cliente_id)
    utils.titulo(contenedor, f"Objetivos de {cliente['nombre']}" if not solo_lectura
                 else "Mi objetivo")

    activo = datos.objetivo_activo_de_cliente(cliente_id)
    tarjeta = ttk.Frame(contenedor, style="Superficie.TFrame", padding=14)
    tarjeta.pack(fill="x", pady=(0, 12))

    if not activo:
        texto = ("Este cliente no tiene un objetivo activo." if not solo_lectura
                 else "Tu coach aun no ha definido un objetivo para ti.")
        ttk.Label(tarjeta, text=texto, style="Suave.TLabel").pack(anchor="w")
    else:
        ttk.Label(tarjeta, text=activo["tipo"], style="Subtitulo.TLabel").pack(anchor="w")
        ttk.Label(tarjeta, text=f"Meta: {activo['valor_meta']} {activo['unidad']}   |   "
                  f"Fecha limite: {activo['fecha_limite']}").pack(anchor="w", pady=(4, 0))
        diferencia = _diferencia_a_meta(cliente_id, activo)
        if diferencia is not None:
            ttk.Label(tarjeta, text=f"Ultimo peso registrado vs. meta: diferencia de "
                      f"{diferencia:+g} kg.", style="Suave.TLabel").pack(anchor="w", pady=(4, 0))
        else:
            ttk.Label(tarjeta, text="Aun no hay suficientes mediciones para calcular el avance.",
                      style="Suave.TLabel").pack(anchor="w", pady=(4, 0))

        if not solo_lectura:
            marco_acciones = ttk.Frame(tarjeta)
            marco_acciones.pack(anchor="w", pady=(10, 0))
            ttk.Button(marco_acciones, text="Editar meta / fecha",
                       command=lambda: _abrir_editar_objetivo(contenedor, activo, cliente_id)
                       ).pack(side="left", padx=(0, 6))
            ttk.Button(marco_acciones, text="Marcar como cumplido",
                       command=lambda: _marcar_cumplido(activo["id"], cliente_id)
                       ).pack(side="left")

    if not solo_lectura:
        ttk.Button(contenedor, text="+ Definir nuevo objetivo", style="Primario.TButton",
                   command=lambda: nav.cargar_pantalla("objetivo_form", cliente_id=cliente_id)
                   ).pack(anchor="w", pady=(0, 12))

    historial = [o for o in datos.objetivos_de_cliente(cliente_id) if o["estado"] != "Activo"]
    if historial:
        utils.subtitulo(contenedor, "Historial de objetivos")
        columnas = [("tipo", "Tipo", 160), ("meta", "Meta", 120), ("limite", "Fecha limite", 110),
                    ("estado", "Estado", 100), ("cumplido", "Cumplido el", 110)]
        arbol = utils.tabla(contenedor, columnas, alturas=6)
        for objetivo in historial:
            arbol.insert("", "end", values=(
                objetivo["tipo"], f"{objetivo['valor_meta']} {objetivo['unidad']}",
                objetivo["fecha_limite"], objetivo["estado"], objetivo["fecha_cumplido"] or "-"))

    ttk.Button(contenedor, text="Volver", command=lambda: _volver(cliente_id)).pack(anchor="w",
                                                                                     pady=(16, 0))


def _marcar_cumplido(objetivo_id, cliente_id):
    if utils.confirmar("¿Confirma que este objetivo se cumplio? No podra reabrirse."):
        datos.marcar_objetivo_cumplido(objetivo_id)
        nav.cargar_pantalla("objetivos_listado", cliente_id=cliente_id)


def _abrir_editar_objetivo(padre, objetivo, cliente_id):
    ventana, marco = utils.dialogo(padre, "Editar meta y fecha limite", ancho=420, alto=230)
    meta_v = utils.campo_formulario(marco, "Nuevo valor meta:",
                                     valor_inicial=str(objetivo["valor_meta"]))
    fecha_v = utils.campo_formulario(marco, "Nueva fecha limite (AAAA-MM-DD):",
                                      valor_inicial=objetivo["fecha_limite"])

    def _guardar():
        valor_meta = utils.numero_o_none(meta_v.get())
        fecha_limite = fecha_v.get().strip()
        if valor_meta is None or not utils.fecha_valida(fecha_limite):
            utils.error("Debe indicar un valor meta numerico y una fecha limite valida.")
            return
        datos.actualizar_objetivo(objetivo["id"], valor_meta=valor_meta, fecha_limite=fecha_limite)
        ventana.destroy()
        nav.cargar_pantalla("objetivos_listado", cliente_id=cliente_id)

    utils.botones_dialogo(marco, ventana.destroy, _guardar)


def render_form(contenedor, cliente_id):
    """Formulario para definir un nuevo objetivo activo (HU18)."""
    cliente = datos.obtener_cliente_por_id(cliente_id)
    utils.titulo(contenedor, f"Definir objetivo — {cliente['nombre']}")

    tipo_v = utils.campo_combobox(contenedor, "Tipo de objetivo:", TIPOS_OBJETIVO)
    meta_v = utils.campo_formulario(contenedor, "Valor meta:")
    unidad_v = utils.campo_formulario(contenedor, "Unidad (kg, %, min, etc.):", valor_inicial="kg")
    fecha_v = utils.campo_formulario(contenedor, "Fecha limite (AAAA-MM-DD):")

    def _guardar():
        valor_meta = utils.numero_o_none(meta_v.get())
        unidad = unidad_v.get().strip()
        fecha_limite = fecha_v.get().strip()
        if valor_meta is None or not unidad or not utils.fecha_valida(fecha_limite):
            utils.error("Debe indicar un valor meta numerico, una unidad y una fecha "
                        "limite valida.")
            return
        activo = datos.objetivo_activo_de_cliente(cliente_id)
        if activo:
            respuesta = utils.preguntar_reemplazar(
                f"{cliente['nombre']} ya tiene el objetivo activo \"{activo['tipo']}\".")
            if respuesta is None:
                return
            if respuesta:
                datos.marcar_objetivo_cumplido(activo["id"])
                datos.actualizar_objetivo(activo["id"], estado="Reemplazado")
        datos.crear_objetivo(cliente_id, tipo_v.get(), valor_meta, unidad, fecha_limite)
        utils.informar("Objetivo definido correctamente.")
        nav.cargar_pantalla("objetivos_listado", cliente_id=cliente_id)

    botones = ttk.Frame(contenedor)
    botones.pack(anchor="w", pady=16)
    ttk.Button(botones, text="Cancelar",
               command=lambda: nav.cargar_pantalla("objetivos_listado", cliente_id=cliente_id)
               ).pack(side="left", padx=(0, 8))
    ttk.Button(botones, text="Guardar objetivo", style="Primario.TButton",
               command=_guardar).pack(side="left")


nav.registrar_pantalla("objetivos_listado", render_listado)
nav.registrar_pantalla("objetivo_form", render_form)
