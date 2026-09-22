# -*- coding: utf-8 -*-
"""
HU28 - Notificacion de asignacion o modificacion de rutina
HU29 - Cliente deja comentario o duda sobre un ejercicio
HU30 - Coach recibe y responde comentarios de clientes
"""

import tkinter as tk
from tkinter import ttk

from .. import datos
from .. import navegacion as nav
from .. import utils


def render_notificaciones(contenedor):
    """Pantalla de notificaciones del cliente, con acceso directo a la rutina (HU28)."""
    cliente_id = nav.estado["cliente_en_foco_id"]
    utils.titulo(contenedor, "Mis notificaciones")

    lista = datos.notificaciones_de_cliente(cliente_id)
    if not lista:
        utils.mensaje_vacio(contenedor, "No tienes notificaciones por el momento.")
        return

    for notificacion in lista:
        marco = ttk.Frame(contenedor, style="Superficie.TFrame", padding=10)
        marco.pack(fill="x", pady=4)
        prefijo = "🔵 " if not notificacion["leida"] else ""
        estilo_texto = "Subtitulo.TLabel" if not notificacion["leida"] else "TLabel"
        ttk.Label(marco, text=f"{prefijo}{notificacion['fecha']} — {notificacion['mensaje']}",
                  style=estilo_texto).pack(side="left", anchor="w")
        if notificacion["rutina_id"]:
            ttk.Button(marco, text="Ver rutina",
                       command=lambda n=notificacion: _abrir_rutina(n)).pack(side="right")
        elif not notificacion["leida"]:
            ttk.Button(marco, text="Marcar como leida",
                       command=lambda n=notificacion: (datos.marcar_notificacion_leida(n["id"]),
                                                        nav.cargar_pantalla("notificaciones"))
                       ).pack(side="right")


def _abrir_rutina(notificacion):
    datos.marcar_notificacion_leida(notificacion["id"])
    nav.cargar_pantalla("rutina_ejercicios", rutina_id=notificacion["rutina_id"])


def abrir_dialogo_comentario(padre, cliente_id, rutina_id, ejercicio):
    """Abre el dialogo para ver y dejar comentarios sobre un ejercicio (HU29)."""
    ventana, marco = utils.dialogo(padre, f'Comentario sobre "{ejercicio["nombre"]}"',
                                    ancho=460, alto=380)

    existentes = datos.comentarios_de_ejercicio(rutina_id, ejercicio["id"])
    if existentes:
        ttk.Label(marco, text="Comentarios anteriores:", style="Subtitulo.TLabel").pack(anchor="w")
        for comentario in existentes:
            ttk.Label(marco, text=f'[{comentario["fecha"]}] Tu: {comentario["texto_cliente"]}',
                      wraplength=400, justify="left").pack(anchor="w", pady=(6, 0))
            if comentario["respuesta_coach"]:
                ttk.Label(marco, text=f'[{comentario["fecha_respuesta"]}] Coach: '
                          f'{comentario["respuesta_coach"]}', wraplength=400, justify="left",
                          style="Exito.TLabel").pack(anchor="w")
            else:
                ttk.Label(marco, text="(Pendiente de respuesta del coach)",
                          style="Suave.TLabel").pack(anchor="w")

    ttk.Label(marco, text="Nuevo comentario o duda:", style="Subtitulo.TLabel").pack(anchor="w",
                                                                                      pady=(12, 4))
    texto = tk.Text(marco, height=4, width=48)
    texto.pack()

    def _enviar():
        contenido = texto.get("1.0", "end").strip()
        if not contenido:
            utils.error("Escriba el comentario antes de enviarlo.")
            return
        datos.crear_comentario(cliente_id, rutina_id, ejercicio["id"], contenido)
        utils.informar("Comentario enviado a tu coach.")
        ventana.destroy()

    ttk.Button(marco, text="Enviar comentario", style="Primario.TButton", command=_enviar
               ).pack(anchor="w", pady=12)
    ttk.Button(marco, text="Cerrar", command=ventana.destroy).pack(anchor="w")


def _ejercicio_del_comentario(rutina, comentario):
    if not rutina:
        return None
    return next((e for e in rutina["ejercicios"] if e["id"] == comentario["ejercicio_id"]), None)


def render_comentarios_coach(contenedor):
    """Pantalla del coach con los comentarios pendientes y ya resueltos (HU30)."""
    utils.titulo(contenedor, "Comentarios y dudas de clientes")

    pendientes = datos.comentarios_pendientes()
    if not pendientes:
        utils.mensaje_vacio(contenedor, "No hay comentarios pendientes por responder.")
    else:
        for comentario in pendientes:
            cliente = datos.obtener_cliente_por_id(comentario["cliente_id"])
            rutina = datos.obtener_rutina_por_id(comentario["rutina_id"])
            ejercicio = _ejercicio_del_comentario(rutina, comentario)
            marco = ttk.Frame(contenedor, style="Superficie.TFrame", padding=10)
            marco.pack(fill="x", pady=6)
            nombre_ej = ejercicio["nombre"] if ejercicio else "(ejercicio eliminado)"
            nombre_rut = rutina["nombre"] if rutina else "(rutina eliminada)"
            ttk.Label(marco, text=f"{cliente['nombre']} — {nombre_rut} / {nombre_ej}",
                      style="Subtitulo.TLabel").pack(anchor="w")
            ttk.Label(marco, text=f'[{comentario["fecha"]}] {comentario["texto_cliente"]}',
                      wraplength=700, justify="left").pack(anchor="w", pady=(4, 8))
            respuesta = tk.Text(marco, height=2, width=70)
            respuesta.pack(anchor="w")
            ttk.Button(marco, text="Responder y marcar resuelto",
                       command=lambda c=comentario, r=respuesta: _responder(c, r)
                       ).pack(anchor="w", pady=(6, 0))

    resueltos = [c for c in datos.comentarios if c["estado"] == "Resuelto"]
    if resueltos:
        utils.subtitulo(contenedor, "Comentarios resueltos")
        columnas = [("cliente", "Cliente", 160), ("comentario", "Comentario", 260),
                    ("respuesta", "Respuesta", 260)]
        arbol = utils.tabla(contenedor, columnas, alturas=6)
        for comentario in resueltos:
            cliente = datos.obtener_cliente_por_id(comentario["cliente_id"])
            arbol.insert("", "end", values=(cliente["nombre"], comentario["texto_cliente"],
                                             comentario["respuesta_coach"]))


def _responder(comentario, campo_texto):
    respuesta = campo_texto.get("1.0", "end").strip()
    if not respuesta:
        utils.error("Escriba una respuesta antes de enviarla.")
        return
    datos.responder_comentario(comentario["id"], respuesta)
    utils.informar("Respuesta enviada al cliente.")
    nav.cargar_pantalla("comentarios_coach")


nav.registrar_pantalla("notificaciones", render_notificaciones)
nav.registrar_pantalla("comentarios_coach", render_comentarios_coach)
