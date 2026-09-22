# -*- coding: utf-8 -*-
"""
HU24 - Cliente visualiza sus medidas corporales
HU25 - Cliente visualiza grafico de su progreso
HU26 - Cliente visualiza su objetivo y avance
HU27 - Cliente visualiza sus fotos de progreso

Pantalla de acceso (hub) que reutiliza en modo solo_lectura=True las
funciones ya construidas para el rol coach en mediciones.py y objetivos.py
(ver nota de ambiguedad A9 en el archivo de historias de usuario INVEST).
"""

from tkinter import ttk

from .. import navegacion as nav
from .. import utils


def render(contenedor):
    """Pantalla hub con accesos a medidas, grafico, objetivo y fotos del cliente."""
    utils.titulo(contenedor, "Mi progreso")
    ttk.Label(contenedor, text="Consulta tus medidas, tu grafico de evolucion, tu objetivo y tus "
              "fotos de progreso.", style="Suave.TLabel").pack(anchor="w", pady=(0, 16))

    opciones = [
        ("Mis medidas corporales (HU24)", "mediciones_listado"),
        ("Mi grafico de progreso (HU25)", "medidas_grafico"),
        ("Mi objetivo (HU26)", "objetivos_listado"),
        ("Mis fotos de progreso (HU27)", "fotos_progreso"),
    ]
    for texto, pantalla in opciones:
        ttk.Button(contenedor, text=texto, style="Primario.TButton",
                   command=lambda p=pantalla: nav.cargar_pantalla(p, solo_lectura=True)
                   ).pack(anchor="w", pady=4)


nav.registrar_pantalla("mi_progreso", render)
