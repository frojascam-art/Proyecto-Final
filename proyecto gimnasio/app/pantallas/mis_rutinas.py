# -*- coding: utf-8 -*-
"""
HU4  - Cliente visualiza sus rutinas vigentes
HU21 - Cliente marca ejercicios o rutina como realizada
HU22 - Cliente registra su desempeno real por ejercicio
HU23 - Cliente consulta su historial de rutinas completadas
"""

import tkinter as tk
from tkinter import ttk

from .. import datos
from .. import navegacion as nav
from .. import utils
from . import comunicacion


def render(contenedor):
    """Pantalla 'Mis rutinas': rutinas vigentes del cliente y su detalle (HU4/HU21/HU22)."""
    cliente_id = nav.estado["cliente_en_foco_id"]
    cliente = datos.obtener_cliente_por_id(cliente_id)
    if not cliente:
        utils.mensaje_vacio(contenedor, "No hay un cliente activo en esta sesion.")
        return

    utils.titulo(contenedor, "Mis rutinas vigentes")
    ttk.Button(contenedor, text="Ver mi historial de rutinas completadas",
               command=lambda: nav.cargar_pantalla("mi_historial")).pack(anchor="w", pady=(0, 10))

    activas = datos.rutinas_activas_de_cliente(cliente_id)
    if not activas:
        utils.mensaje_vacio(contenedor, "Aun no tienes rutinas asignadas. Contacta a tu coach.")
        return

    marco_principal = ttk.Frame(contenedor)
    marco_principal.pack(fill="both", expand=True)

    marco_izq = ttk.Frame(marco_principal)
    marco_izq.pack(side="left", fill="y", padx=(0, 16))
    ttk.Label(marco_izq, text="Rutinas vigentes", style="Subtitulo.TLabel").pack(anchor="w")
    lista_rutinas = tk.Listbox(marco_izq, height=10, width=28, exportselection=False)
    for rutina in activas:
        lista_rutinas.insert("end", f"{rutina['nombre']} ({rutina['fecha']})")
    lista_rutinas.pack()
    lista_rutinas.selection_set(0)

    marco_der = ttk.Frame(marco_principal)
    marco_der.pack(side="left", fill="both", expand=True)

    def _rutina_seleccionada():
        indice = lista_rutinas.curselection()
        if not indice:
            return None
        return activas[indice[0]]

    def _dibujar_detalle(*_):
        utils.limpiar(marco_der)
        rutina = _rutina_seleccionada()
        if rutina:
            _dibujar_detalle_rutina(contenedor, marco_der, cliente_id, rutina, _dibujar_detalle)

    lista_rutinas.bind("<<ListboxSelect>>", _dibujar_detalle)
    _dibujar_detalle()


def _dibujar_detalle_rutina(contenedor, marco_der, cliente_id, rutina, refrescar):
    """Dibuja el detalle de una rutina (tabla de ejercicios + acciones del dia) (HU21/HU22/HU29)."""
    ttk.Label(marco_der, text=rutina["nombre"], style="Subtitulo.TLabel").pack(anchor="w")

    columnas = [("nombre", "Ejercicio", 160), ("dia", "Dia/Bloque", 100), ("series", "Series", 60),
                ("rep", "Repeticiones", 90), ("descanso", "Descanso", 80),
                ("peso", "Peso sugerido", 100), ("hoy", "Hoy", 90)]
    arbol = utils.tabla(marco_der, columnas, alturas=8)

    registro_hoy = datos.registro_de_hoy(rutina["id"])
    for ejercicio in rutina["ejercicios"]:
        estado_hoy = registro_hoy["ejercicios"].get(ejercicio["id"])
        texto_hoy = "Realizado" if estado_hoy and estado_hoy["realizado"] else "Pendiente"
        peso = "-" if not ejercicio["tipo_con_peso"] else (
            "Por definir" if ejercicio["peso_por_definir"] or ejercicio["peso"] is None
            else f"{ejercicio['peso']} {ejercicio['unidad']}")
        arbol.insert("", "end", iid=ejercicio["id"], values=(
            ejercicio["nombre"], ejercicio.get("dia_bloque") or "Sin asignar",
            ejercicio["series"], ejercicio["repeticiones"], ejercicio["descanso"], peso,
            texto_hoy))

    panel_acciones = ttk.Frame(marco_der)
    panel_acciones.pack(fill="x", pady=(8, 0))

    def _con_seleccion(accion):
        seleccion = arbol.selection()
        if not seleccion:
            utils.error("Seleccione primero un ejercicio de la tabla.")
            return
        ejercicio = next(e for e in rutina["ejercicios"] if e["id"] == seleccion[0])
        accion(ejercicio)

    ttk.Button(panel_acciones, text="Marcar ejercicio como realizado", style="Primario.TButton",
               command=lambda: _con_seleccion(
                   lambda ej: _abrir_marcar(contenedor, rutina, ej, refrescar))
               ).pack(side="left", padx=(0, 6))
    ttk.Button(panel_acciones, text="Dejar comentario / duda",
               command=lambda: _con_seleccion(
                   lambda ej: comunicacion.abrir_dialogo_comentario(
                       contenedor, cliente_id, rutina["id"], ej))).pack(side="left", padx=6)
    ttk.Button(panel_acciones, text="Marcar rutina completa de hoy como realizada",
               command=lambda: _marcar_rutina_completa(rutina, refrescar)
               ).pack(side="left", padx=6)


def _abrir_marcar(padre, rutina, ejercicio, refrescar):
    """Dialogo para marcar un ejercicio como realizado hoy y registrar su desempeno (HU21/HU22)."""
    ventana, marco = utils.dialogo(padre, f'Registrar "{ejercicio["nombre"]}" de hoy', ancho=420,
                                    alto=260)

    peso_v = tk.StringVar()
    rep_v = tk.StringVar()
    if ejercicio["tipo_con_peso"]:
        fila = ttk.Frame(marco)
        fila.pack(fill="x", pady=6)
        ttk.Label(fila, text=f"Peso utilizado en el ejercicio ({ejercicio['unidad'] or 'kg'}):",
                  width=30).pack(side="left")
        ttk.Entry(fila, textvariable=peso_v, width=10).pack(side="left")
    fila_rep = ttk.Frame(marco)
    fila_rep.pack(fill="x", pady=6)
    ttk.Label(fila_rep, text="Repeticiones logradas (si difieren de lo planeado):",
              width=30).pack(side="left")
    ttk.Entry(fila_rep, textvariable=rep_v, width=10).pack(side="left")

    def _guardar():
        peso_usado = utils.numero_o_none(peso_v.get()) if ejercicio["tipo_con_peso"] else None
        repeticiones = rep_v.get().strip() or None
        datos.marcar_ejercicio_realizado(rutina["id"], ejercicio["id"], True, peso_usado,
                                          repeticiones)
        ventana.destroy()
        refrescar()

    utils.botones_dialogo(marco, ventana.destroy, _guardar)


def _marcar_rutina_completa(rutina, refrescar):
    if not utils.confirmar(f'¿Marcar todos los ejercicios de "{rutina["nombre"]}" como realizados '
                           "hoy?"):
        return
    for ejercicio in rutina["ejercicios"]:
        datos.marcar_ejercicio_realizado(rutina["id"], ejercicio["id"], True)
    refrescar()


def render_historial(contenedor):
    """Historial de rutinas/sesiones completadas por el cliente actual (HU23)."""
    cliente_id = nav.estado["cliente_en_foco_id"]
    utils.titulo(contenedor, "Mi historial de rutinas completadas")

    registros = datos.registros_de_cliente(cliente_id)
    if not registros:
        utils.mensaje_vacio(contenedor, "Aun no has completado ninguna rutina.")
        return

    columnas = [("fecha", "Fecha", 100), ("rutina", "Rutina", 200),
                ("realizados", "Ejercicios realizados", 140)]
    arbol = utils.tabla(contenedor, columnas, alturas=12)
    for rutina, registro in registros:
        total = len(rutina["ejercicios"])
        realizados = sum(1 for v in registro["ejercicios"].values() if v["realizado"])
        arbol.insert("", "end", values=(registro["fecha"], rutina["nombre"],
                                         f"{realizados} / {total}"))

    ttk.Button(contenedor, text="Volver a mis rutinas",
               command=lambda: nav.cargar_pantalla("mis_rutinas")).pack(anchor="w", pady=(16, 0))


nav.registrar_pantalla("mis_rutinas", render)
nav.registrar_pantalla("mi_historial", render_historial)
