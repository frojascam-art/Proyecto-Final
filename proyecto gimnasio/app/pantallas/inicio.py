# -*- coding: utf-8 -*-
"""HU1 - Autenticacion y control de roles (selector de rol)."""

import tkinter as tk
from tkinter import ttk

from .. import datos
from .. import navegacion as nav
from .. import utils


def render(contenedor):
    """Pantalla inicial: selector de rol (coach/administrador o cliente)."""
    utils.titulo(contenedor, "Bienvenido al Sistema de Gimnasio")
    ttk.Label(contenedor, text="Seleccione con que rol desea ingresar al sistema.",
              style="Suave.TLabel").pack(anchor="w", pady=(0, 20))

    tarjeta_coach = ttk.Frame(contenedor, style="Superficie.TFrame", padding=16)
    tarjeta_coach.pack(fill="x", pady=(0, 16))
    ttk.Label(tarjeta_coach, text="Coach / Administrador",
              style="Subtitulo.TLabel").pack(anchor="w")
    ttk.Label(tarjeta_coach, text="Gestiona clientes, rutinas, mediciones, objetivos y reportes.",
              style="Suave.TLabel").pack(anchor="w", pady=(2, 10))
    ttk.Button(tarjeta_coach, text="Entrar como Coach/Administrador", style="Primario.TButton",
               command=_entrar_como_coach).pack(anchor="w")

    tarjeta_cliente = ttk.Frame(contenedor, style="Superficie.TFrame", padding=16)
    tarjeta_cliente.pack(fill="x")
    ttk.Label(tarjeta_cliente, text="Cliente", style="Subtitulo.TLabel").pack(anchor="w")
    ttk.Label(tarjeta_cliente, text="Consulta tus rutinas, tu progreso y tus objetivos.",
              style="Suave.TLabel").pack(anchor="w", pady=(2, 10))

    lista_clientes = datos.clientes_activos()
    if not lista_clientes:
        utils.mensaje_vacio(tarjeta_cliente, "No hay clientes activos registrados todavia.")
        return

    marco = ttk.Frame(tarjeta_cliente)
    marco.pack(anchor="w")
    variable = tk.StringVar(value=lista_clientes[0]["nombre"])
    combo = ttk.Combobox(marco, textvariable=variable, state="readonly", width=28,
                          values=[c["nombre"] for c in lista_clientes])
    combo.current(0)
    combo.pack(side="left", padx=(0, 12))

    def _entrar_como_cliente():
        cliente = lista_clientes[combo.current()]
        nav.establecer_rol("cliente", cliente["id"])
        nav.cargar_pantalla("mis_rutinas")

    ttk.Button(marco, text="Entrar como Cliente", style="Primario.TButton",
               command=_entrar_como_cliente).pack(side="left")


def _entrar_como_coach():
    nav.establecer_rol("coach")
    nav.cargar_pantalla("clientes_listado")


nav.registrar_pantalla("inicio", render)
