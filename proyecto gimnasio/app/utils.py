# -*- coding: utf-8 -*-
"""Widgets y validaciones reutilizados por las pantallas de app/pantallas/."""

import re
import tkinter as tk
from datetime import date
from tkinter import messagebox, ttk

PATRON_FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def titulo(contenedor, texto):
    """Dibuja el titulo principal de una pantalla."""
    ttk.Label(contenedor, text=texto, style="Titulo.TLabel").pack(anchor="w", pady=(0, 12))


def subtitulo(contenedor, texto):
    """Dibuja un subtitulo de seccion dentro de una pantalla."""
    ttk.Label(contenedor, text=texto, style="Subtitulo.TLabel").pack(anchor="w", pady=(16, 6))


def mensaje_vacio(contenedor, texto):
    """Muestra un mensaje de 'sin datos' con estilo atenuado."""
    ttk.Label(contenedor, text=texto, style="Suave.TLabel").pack(anchor="w", pady=12)


def limpiar(contenedor):
    """Destruye todos los widgets hijos de un contenedor, para volver a dibujarlo."""
    for widget in contenedor.winfo_children():
        widget.destroy()


def campo_formulario(contenedor, etiqueta, ancho=32, valor_inicial=""):
    """Crea una fila de formulario con etiqueta + campo de texto; devuelve su variable."""
    fila = ttk.Frame(contenedor)
    fila.pack(fill="x", pady=4)
    ttk.Label(fila, text=etiqueta, width=24).pack(side="left")
    variable = tk.StringVar(value=valor_inicial)
    ttk.Entry(fila, textvariable=variable, width=ancho).pack(side="left", fill="x", expand=True)
    return variable


# Un selector de formulario necesita legitimamente contenedor, etiqueta, valores,
# valor inicial, ancho y un callback opcional; dividirlo perjudicaria la legibilidad.
def campo_combobox(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        contenedor, etiqueta, valores, valor_inicial=None, ancho=29, callback=None):
    """Crea una fila de formulario con etiqueta + combobox; devuelve su variable."""
    fila = ttk.Frame(contenedor)
    fila.pack(fill="x", pady=4)
    ttk.Label(fila, text=etiqueta, width=24).pack(side="left")
    inicial = valor_inicial if valor_inicial is not None else (valores[0] if valores else "")
    variable = tk.StringVar(value=inicial)
    combo = ttk.Combobox(fila, textvariable=variable, values=valores, width=ancho,
                         state="readonly")
    combo.pack(side="left", fill="x", expand=True)
    if callback:
        combo.bind("<<ComboboxSelected>>", callback)
    return variable


def campo_radiobuttons(contenedor, etiqueta, opciones, valor_inicial=None, callback=None):
    """Crea una fila de formulario con etiqueta + radiobuttons; devuelve su variable."""
    fila = ttk.Frame(contenedor)
    fila.pack(fill="x", pady=4)
    ttk.Label(fila, text=etiqueta, width=24).pack(side="left")
    variable = tk.StringVar(value=valor_inicial if valor_inicial is not None else opciones[0])
    for opcion in opciones:
        ttk.Radiobutton(fila, text=opcion, value=opcion, variable=variable,
                        command=callback).pack(side="left", padx=(0, 10))
    return variable


def tabla(contenedor, columnas, alturas=12):
    """Crea un Treeview con scrollbar. columnas: lista de tuplas (clave, texto, ancho)."""
    marco = ttk.Frame(contenedor)
    marco.pack(fill="both", expand=True, pady=8)
    arbol = ttk.Treeview(marco, columns=[c[0] for c in columnas], show="headings", height=alturas)
    for clave, texto, ancho in columnas:
        arbol.heading(clave, text=texto)
        arbol.column(clave, width=ancho, anchor="w")
    scroll = ttk.Scrollbar(marco, orient="vertical", command=arbol.yview)
    arbol.configure(yscrollcommand=scroll.set)
    arbol.pack(side="left", fill="both", expand=True)
    scroll.pack(side="right", fill="y")
    return arbol


def fecha_valida(texto):
    """Valida que el texto tenga formato AAAA-MM-DD y sea una fecha real."""
    if not texto or not PATRON_FECHA.match(texto):
        return False
    try:
        date.fromisoformat(texto)
        return True
    except ValueError:
        return False


def numero_o_none(texto):
    """Convierte un texto a int/float, o None si esta vacio o no es numerico."""
    texto = (texto or "").strip()
    if not texto:
        return None
    try:
        return float(texto) if "." in texto else int(texto)
    except ValueError:
        return None


def error(texto):
    """Muestra un cuadro de dialogo de error de validacion."""
    messagebox.showerror("Datos incompletos", texto)


def confirmar(texto):
    """Pregunta si/no; devuelve True o False."""
    return messagebox.askyesno("Confirmar", texto)


def preguntar_reemplazar(texto):
    """Devuelve True=reemplazar, False=mantener ambas, None=cancelar."""
    return messagebox.askyesnocancel(
        "Ya existe un elemento activo",
        texto + "\n\nSi = reemplazarlo\nNo = mantener ambos\nCancelar = no hacer nada")


def informar(texto):
    """Muestra un cuadro de dialogo informativo."""
    messagebox.showinfo("Sistema de Gimnasio", texto)


def botones_dialogo(contenedor, on_cancelar, on_guardar, texto_guardar="Guardar"):
    """Fila estandar de botones Cancelar/Guardar usada por los dialogos modales."""
    botones = ttk.Frame(contenedor)
    botones.pack(pady=16)
    ttk.Button(botones, text="Cancelar", command=on_cancelar).pack(side="left", padx=(0, 8))
    ttk.Button(botones, text=texto_guardar, style="Primario.TButton",
               command=on_guardar).pack(side="left")


def dialogo(padre, titulo_texto, ancho=440, alto=380):
    """Crea una ventana Toplevel modal con un contenedor interno; devuelve ambos."""
    ventana = tk.Toplevel(padre)
    ventana.title(titulo_texto)
    ventana.geometry(f"{ancho}x{alto}")
    ventana.transient(padre.winfo_toplevel())
    ventana.grab_set()
    contenedor = ttk.Frame(ventana, padding=16)
    contenedor.pack(fill="both", expand=True)
    return ventana, contenedor
