# -*- coding: utf-8 -*-
"""
Nucleo de navegacion. Equivalente en Python a js/app.js del prototipo:
registro/carga de pantallas dentro de un contenedor y la barra superior
que se adapta segun el rol activo (HU1). No contiene logica de negocio
de ninguna pantalla en particular.
"""

import tkinter as tk
from tkinter import ttk

COLOR_PRIMARIO = "#2f80ed"
COLOR_PRIMARIO_OSCURO = "#1c5fb8"
COLOR_FONDO = "#f5f7fa"
COLOR_SUPERFICIE = "#ffffff"
COLOR_TEXTO = "#1f2933"
COLOR_TEXTO_SUAVE = "#616e7c"
COLOR_BORDE = "#d9e2ec"
COLOR_EXITO = "#27ae60"
COLOR_ERROR = "#eb5757"
COLOR_ADVERTENCIA = "#f2994a"

pantallas = {}

estado = {
    "rol": None,                 # 'coach' | 'cliente'
    "cliente_en_foco_id": None,  # cliente sobre el que trabaja el coach, o el propio cliente
    "rutina_en_foco_id": None,
}

# Estado interno de la ventana (se asigna una sola vez en construir_ventana);
# no son constantes, por eso van en minuscula pese a la advertencia de pylint.
_root = None  # pylint: disable=invalid-name
_contenedor = None  # pylint: disable=invalid-name
_badge_rol = None  # pylint: disable=invalid-name
_items_nav = []  # (widget, grupo, pack_kwargs)


def registrar_pantalla(nombre, funcion):
    """Asocia un nombre de pantalla con la funcion que la dibuja."""
    pantallas[nombre] = funcion


def cargar_pantalla(nombre, **kwargs):
    """Limpia el contenedor principal y dibuja en el la pantalla solicitada."""
    for widget in _contenedor.winfo_children():
        widget.destroy()
    funcion = pantallas.get(nombre)
    if funcion:
        funcion(_contenedor, **kwargs)
    else:
        ttk.Label(_contenedor, text=f'Pantalla "{nombre}" pendiente de implementar.').pack(
            padx=16, pady=16)
    _contenedor.update_idletasks()
    _root.event_generate("<<PantallaCargada>>")


def establecer_rol(rol, cliente_id=None):
    """Fija el rol activo de la sesion y el cliente en foco (HU1)."""
    estado["rol"] = rol
    estado["cliente_en_foco_id"] = cliente_id
    estado["rutina_en_foco_id"] = None
    _actualizar_navegacion()


def volver_al_selector_de_rol():
    """Cierra la sesion actual y regresa a la pantalla de seleccion de rol (HU1)."""
    estado["rol"] = None
    estado["cliente_en_foco_id"] = None
    estado["rutina_en_foco_id"] = None
    _actualizar_navegacion()
    cargar_pantalla("inicio")


def _agregar_nav(widget, grupo, **pack_kwargs):
    _items_nav.append((widget, grupo, pack_kwargs))
    return widget


def _actualizar_navegacion():
    for widget, grupo, pack_kwargs in _items_nav:
        visible = (estado["rol"] is not None) if grupo == "activo" else (estado["rol"] == grupo)
        if visible:
            widget.pack(**pack_kwargs)
        else:
            widget.pack_forget()
    if _badge_rol is not None:
        textos_rol = {"coach": "Rol: Coach/Administrador", "cliente": "Rol: Cliente"}
        _badge_rol.config(text=textos_rol.get(estado["rol"], ""))


def _configurar_estilos(root):
    """Define colores, fuentes y estilos ttk reutilizados por toda la app."""
    root.configure(bg=COLOR_FONDO)
    estilo = ttk.Style()
    try:
        estilo.theme_use("clam")
    except tk.TclError:
        pass
    estilo.configure("TFrame", background=COLOR_FONDO)
    estilo.configure("Superficie.TFrame", background=COLOR_SUPERFICIE, relief="solid",
                     borderwidth=1)
    estilo.configure("TLabel", background=COLOR_FONDO, foreground=COLOR_TEXTO,
                     font=("Segoe UI", 10))
    estilo.configure("Titulo.TLabel", font=("Segoe UI", 16, "bold"), background=COLOR_FONDO)
    estilo.configure("Subtitulo.TLabel", font=("Segoe UI", 12, "bold"), background=COLOR_FONDO)
    estilo.configure("Suave.TLabel", foreground=COLOR_TEXTO_SUAVE, background=COLOR_FONDO)
    estilo.configure("Error.TLabel", foreground=COLOR_ERROR, background=COLOR_FONDO)
    estilo.configure("Exito.TLabel", foreground=COLOR_EXITO, background=COLOR_FONDO)
    estilo.configure("TButton", font=("Segoe UI", 10), padding=6)
    estilo.configure("Primario.TButton", foreground="white", background=COLOR_PRIMARIO)
    estilo.map("Primario.TButton", background=[("active", COLOR_PRIMARIO_OSCURO)])
    estilo.configure("Treeview", rowheight=26, font=("Segoe UI", 9))
    estilo.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"))


def _construir_menu(barra):
    """Crea los enlaces de navegacion que se muestran u ocultan segun el rol (HU1)."""
    menu = tk.Frame(barra, bg=COLOR_PRIMARIO)
    menu.pack(side="left")

    def enlace(texto, pantalla, grupo, **kwargs):
        boton = tk.Button(menu, text=texto, relief="flat", bg=COLOR_PRIMARIO, fg="white",
                           activebackground=COLOR_PRIMARIO_OSCURO, activeforeground="white",
                           font=("Segoe UI", 10), bd=0, padx=8,
                           command=lambda: cargar_pantalla(pantalla, **kwargs))
        _agregar_nav(boton, grupo, side="left", padx=2)

    enlace("Clientes", "clientes_listado", "coach")
    enlace("Rutinas", "clientes_listado", "coach", modo="rutinas")
    enlace("Medidas", "clientes_listado", "coach", modo="mediciones")
    enlace("Objetivos", "clientes_listado", "coach", modo="objetivos")
    enlace("Comentarios", "comentarios_coach", "coach")
    enlace("Panel", "panel_admin", "coach")
    enlace("Mis rutinas", "mis_rutinas", "cliente")
    enlace("Mi progreso", "mi_progreso", "cliente")
    enlace("Notificaciones", "notificaciones", "cliente")


def _construir_info_rol(barra):
    """Crea el indicador de rol activo y el boton 'Cambiar rol' (HU1); devuelve el badge."""
    info_rol = tk.Frame(barra, bg=COLOR_PRIMARIO)
    _agregar_nav(info_rol, "activo", side="right", padx=16)

    badge = tk.Label(info_rol, text="", bg=COLOR_PRIMARIO, fg="white",
                     font=("Segoe UI", 9, "italic"))
    badge.pack(side="left", padx=8)

    tk.Button(info_rol, text="Cambiar rol", relief="flat", bg=COLOR_PRIMARIO_OSCURO, fg="white",
              bd=0, padx=8, command=volver_al_selector_de_rol).pack(side="left")
    return badge


def _construir_barra_superior(root):
    """Crea la barra superior (logo, menu y badge de rol); devuelve el badge de rol."""
    barra = tk.Frame(root, bg=COLOR_PRIMARIO, height=48)
    barra.pack(side="top", fill="x")
    tk.Label(barra, text="Sistema de Gimnasio", bg=COLOR_PRIMARIO, fg="white",
             font=("Segoe UI", 12, "bold")).pack(side="left", padx=16, pady=10)
    _construir_menu(barra)
    return _construir_info_rol(barra)


def _construir_area_scroll(root):
    """Crea el area central con scroll vertical; devuelve el contenedor de pantallas."""
    marco_scroll = tk.Frame(root, bg=COLOR_FONDO)
    marco_scroll.pack(side="top", fill="both", expand=True)

    canvas = tk.Canvas(marco_scroll, bg=COLOR_FONDO, highlightthickness=0)
    scroll_y = ttk.Scrollbar(marco_scroll, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scroll_y.set)
    canvas.pack(side="left", fill="both", expand=True)
    scroll_y.pack(side="right", fill="y")

    contenedor = ttk.Frame(canvas, padding=20)
    ventana_id = canvas.create_window((0, 0), window=contenedor, anchor="nw")

    def _ajustar_scroll(_evento=None):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def _ajustar_ancho(evento):
        canvas.itemconfig(ventana_id, width=evento.width)

    contenedor.bind("<Configure>", _ajustar_scroll)
    canvas.bind("<Configure>", _ajustar_ancho)
    canvas.bind_all("<MouseWheel>", lambda evento: canvas.yview_scroll(
        int(-1 * (evento.delta / 120)), "units"))
    return contenedor


def construir_ventana(root):
    """Construye la barra de navegacion y el contenedor principal (HU1)."""
    global _root, _contenedor, _badge_rol  # pylint: disable=global-statement
    _root = root

    root.title("Sistema de Gimnasio - Proyecto Final")
    root.geometry("1100x700")
    root.minsize(900, 560)

    _configurar_estilos(root)
    _badge_rol = _construir_barra_superior(root)
    _contenedor = _construir_area_scroll(root)

    tk.Label(root, text="Sistema de Gimnasio - Proyecto Final Curso IA RACSA", bg=COLOR_FONDO,
             fg=COLOR_TEXTO_SUAVE, font=("Segoe UI", 8)).pack(side="bottom", pady=6)

    _actualizar_navegacion()
