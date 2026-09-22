# -*- coding: utf-8 -*-
"""
HU2 - Registro de clientes
HU6 - Edicion de datos de un cliente
HU7 - Baja (desactivacion) de un cliente
HU8 - Busqueda y filtrado de clientes
HU9 - Reasignacion de coach a un cliente (mismo formulario que HU6)
"""

import tkinter as tk
from tkinter import ttk

from .. import datos
from .. import navegacion as nav
from .. import utils

_TITULOS_MODO = {
    None: "Listado de clientes",
    "rutinas": "Seleccione un cliente para ver sus rutinas",
    "mediciones": "Seleccione un cliente para ver sus mediciones",
    "objetivos": "Seleccione un cliente para ver sus objetivos",
}

_PANTALLA_DESTINO = {
    "rutinas": "rutinas_listado",
    "mediciones": "mediciones_listado",
    "objetivos": "objetivos_listado",
}


def _construir_filtros(contenedor, modo):
    """Crea la fila de busqueda y filtros de la tabla de clientes (HU8)."""
    filtros = ttk.Frame(contenedor)
    filtros.pack(fill="x", pady=(0, 8))

    ttk.Label(filtros, text="Buscar por nombre:").pack(side="left")
    texto_busqueda = tk.StringVar()
    ttk.Entry(filtros, textvariable=texto_busqueda, width=22).pack(side="left", padx=(4, 16))

    ttk.Label(filtros, text="Estado:").pack(side="left")
    filtro_estado = tk.StringVar(value="Todos")
    ttk.Combobox(filtros, textvariable=filtro_estado, values=["Todos", "Activo", "Inactivo"],
                 state="readonly", width=10).pack(side="left", padx=(4, 16))

    ttk.Label(filtros, text="Coach:").pack(side="left")
    filtro_coach = tk.StringVar(value="Todos")
    ttk.Combobox(filtros, textvariable=filtro_coach,
                 values=["Todos"] + [c["nombre"] for c in datos.coaches],
                 state="readonly", width=18).pack(side="left", padx=4)

    if modo is None:
        ttk.Button(filtros, text="+ Nuevo cliente", style="Primario.TButton",
                   command=lambda: nav.cargar_pantalla("cliente_form", modo_form="nuevo")
                   ).pack(side="right")

    return texto_busqueda, filtro_estado, filtro_coach


def _coach_id_por_nombre(nombre):
    """Traduce el nombre elegido en el filtro de coach a su id (o None para 'Todos')."""
    if nombre == "Todos":
        return None
    coach = next((c for c in datos.coaches if c["nombre"] == nombre), None)
    return coach["id"] if coach else None


def _cambiar_estado(cliente_id, refrescar):
    """Activa o desactiva un cliente, pidiendo confirmacion al desactivar (HU7)."""
    cliente = datos.obtener_cliente_por_id(cliente_id)
    if cliente["estado"] == "Activo":
        if not utils.confirmar(
            f"¿Desactivar a {cliente['nombre']}? Se conservara su historial, pero no se le "
            "podran crear nuevas rutinas ni mediciones mientras este inactivo."):
            return
        datos.cambiar_estado_cliente(cliente_id, "Inactivo")
    else:
        datos.cambiar_estado_cliente(cliente_id, "Activo")
    refrescar()


def _dibujar_acciones_cliente(panel_acciones, cliente, modo, refrescar):
    """Dibuja los botones de accion disponibles para el cliente seleccionado."""
    utils.limpiar(panel_acciones)
    cliente_id = cliente["id"]

    if modo is not None:
        ttk.Button(panel_acciones, text=f"Seleccionar a {cliente['nombre']}",
                   style="Primario.TButton",
                   command=lambda: nav.cargar_pantalla(_PANTALLA_DESTINO[modo],
                                                        cliente_id=cliente_id)
                   ).pack(side="left")
        return

    ttk.Button(panel_acciones, text="Editar",
               command=lambda: nav.cargar_pantalla("cliente_form", modo_form="editar",
                                                     cliente_id=cliente_id)
               ).pack(side="left", padx=(0, 6))
    ttk.Button(panel_acciones, text="Ver rutinas",
               command=lambda: nav.cargar_pantalla("rutinas_listado", cliente_id=cliente_id)
               ).pack(side="left", padx=6)
    ttk.Button(panel_acciones, text="Ver mediciones",
               command=lambda: nav.cargar_pantalla("mediciones_listado", cliente_id=cliente_id)
               ).pack(side="left", padx=6)
    ttk.Button(panel_acciones, text="Ver objetivos",
               command=lambda: nav.cargar_pantalla("objetivos_listado", cliente_id=cliente_id)
               ).pack(side="left", padx=6)
    texto_estado = "Desactivar" if cliente["estado"] == "Activo" else "Activar"
    ttk.Button(panel_acciones, text=texto_estado,
               command=lambda: _cambiar_estado(cliente_id, refrescar)).pack(side="left", padx=6)


def render_listado(contenedor, modo=None):
    """Pantalla de listado de clientes: busqueda, filtros y acciones (HU2/HU6/HU7/HU8/HU9)."""
    utils.titulo(contenedor, _TITULOS_MODO.get(modo, "Listado de clientes"))
    texto_busqueda, filtro_estado, filtro_coach = _construir_filtros(contenedor, modo)

    columnas = [("nombre", "Nombre", 200), ("contacto", "Contacto", 180),
                ("estado", "Estado", 90), ("coach", "Coach asignado", 180)]
    arbol = utils.tabla(contenedor, columnas, alturas=12)

    panel_acciones = ttk.Frame(contenedor)
    panel_acciones.pack(fill="x", pady=(8, 0))

    def _sin_seleccion(texto="Seleccione un cliente de la tabla para ver acciones disponibles."):
        utils.limpiar(panel_acciones)
        ttk.Label(panel_acciones, text=texto, style="Suave.TLabel").pack(anchor="w")

    def _refrescar(*_):
        arbol.delete(*arbol.get_children())
        lista = datos.clientes_filtrados(texto_busqueda.get(), filtro_estado.get(),
                                          _coach_id_por_nombre(filtro_coach.get()))
        if not lista:
            _sin_seleccion("No se encontraron clientes.")
            return
        for cliente in lista:
            contacto = cliente["correo"] or cliente["telefono"] or "-"
            arbol.insert("", "end", iid=cliente["id"], values=(
                cliente["nombre"], contacto, cliente["estado"],
                datos.nombre_coach(cliente["coach_id"])))
        _sin_seleccion()

    def _on_select(_evento=None):
        seleccion = arbol.selection()
        cliente = datos.obtener_cliente_por_id(seleccion[0]) if seleccion else None
        if not cliente:
            _sin_seleccion()
            return
        _dibujar_acciones_cliente(panel_acciones, cliente, modo, _refrescar)

    arbol.bind("<<TreeviewSelect>>", _on_select)
    texto_busqueda.trace_add("write", _refrescar)
    filtro_estado.trace_add("write", _refrescar)
    filtro_coach.trace_add("write", _refrescar)
    _refrescar()


def render_form(contenedor, modo_form="nuevo", cliente_id=None):
    """Formulario de alta/edicion de un cliente (HU2/HU6/HU9)."""
    cliente = datos.obtener_cliente_por_id(cliente_id) if cliente_id else None
    utils.titulo(contenedor, "Editar cliente" if modo_form == "editar" else "Nuevo cliente")

    nombre_v = utils.campo_formulario(contenedor, "Nombre completo:",
                                       valor_inicial=cliente["nombre"] if cliente else "")
    correo_v = utils.campo_formulario(contenedor, "Correo electronico:",
                                       valor_inicial=cliente["correo"] if cliente else "")
    telefono_v = utils.campo_formulario(contenedor, "Telefono:",
                                         valor_inicial=cliente["telefono"] if cliente else "")
    estado_v = utils.campo_combobox(contenedor, "Estado:", ["Activo", "Inactivo"],
                                     valor_inicial=cliente["estado"] if cliente else "Activo")

    nombres_coach = [c["nombre"] for c in datos.coaches]
    coach_inicial = datos.nombre_coach(cliente["coach_id"]) if cliente else (
        nombres_coach[0] if nombres_coach else "")
    coach_v = utils.campo_combobox(contenedor, "Coach asignado:", nombres_coach,
                                    valor_inicial=coach_inicial)
    if modo_form == "editar":
        ttk.Label(contenedor, text="Cambiar este campo reasigna el coach responsable (HU9); "
                  "no afecta las rutinas ya creadas.",
                  style="Suave.TLabel").pack(anchor="w", pady=(0, 4))

    def _guardar():
        nombre = nombre_v.get().strip()
        correo = correo_v.get().strip()
        telefono = telefono_v.get().strip()
        if not nombre or not (correo or telefono):
            utils.error("Debe indicar el nombre completo y al menos un dato de contacto "
                        "(correo o telefono).")
            return
        coach = next((c for c in datos.coaches if c["nombre"] == coach_v.get()), None)
        if not coach:
            utils.error("Debe seleccionar un coach asignado.")
            return
        ignorar_id = cliente_id if modo_form == "editar" else None
        if datos.existe_correo_duplicado(correo, ignorar_id):
            if not utils.confirmar("Ya existe un cliente con este correo. ¿Desea continuar de "
                                   "todas formas?"):
                return
        if modo_form == "editar":
            datos.actualizar_cliente(cliente_id, nombre=nombre, correo=correo, telefono=telefono,
                                      estado=estado_v.get(), coach_id=coach["id"])
            utils.informar("Cliente actualizado correctamente.")
        else:
            datos.crear_cliente(nombre, correo, telefono, coach["id"], estado_v.get())
            utils.informar("Cliente registrado correctamente.")
        nav.cargar_pantalla("clientes_listado")

    botones = ttk.Frame(contenedor)
    botones.pack(anchor="w", pady=16)
    ttk.Button(botones, text="Cancelar",
               command=lambda: nav.cargar_pantalla("clientes_listado")
               ).pack(side="left", padx=(0, 8))
    ttk.Button(botones, text="Guardar cliente", style="Primario.TButton",
               command=_guardar).pack(side="left")


nav.registrar_pantalla("clientes_listado", render_listado)
nav.registrar_pantalla("cliente_form", render_form)
