# -*- coding: utf-8 -*-
"""
HU20 - Alerta de inactividad de un cliente (mostrada en el panel)
HU31 - Panel general del administrador
HU32 - Reporte de progreso de un cliente
HU33 - Exportacion de informacion de clientes y progreso
"""

import csv
import tkinter as tk
from tkinter import filedialog, ttk

from .. import datos
from .. import navegacion as nav
from .. import utils


def _tarjeta_kpi(padre, texto, valor, pantalla):
    """Crea una tarjeta de indicador (KPI) del panel general (HU31)."""
    tarjeta = ttk.Frame(padre, style="Superficie.TFrame", padding=16)
    tarjeta.pack(side="left", padx=(0, 12))
    ttk.Label(tarjeta, text=str(valor), font=("Segoe UI", 22, "bold"),
              background=nav.COLOR_SUPERFICIE).pack()
    ttk.Label(tarjeta, text=texto, style="Suave.TLabel",
              background=nav.COLOR_SUPERFICIE).pack()
    ttk.Button(tarjeta, text="Ver clientes",
               command=lambda: nav.cargar_pantalla(pantalla)).pack(pady=(8, 0))


def _seccion_alertas(contenedor):
    """Dibuja la lista de clientes activos sin avances en 3+ semanas (HU20)."""
    inactivos = datos.clientes_inactivos()
    if not inactivos:
        ttk.Label(contenedor, text="Ningun cliente activo lleva 3 semanas o mas sin registrar "
                  "avances.", style="Exito.TLabel").pack(anchor="w")
        return

    columnas = [("nombre", "Cliente", 200), ("coach", "Coach", 160),
                ("ultimo", "Ultimo avance", 140)]
    arbol = utils.tabla(contenedor, columnas, alturas=min(8, len(inactivos)))
    for cliente, ultima in inactivos:
        arbol.insert("", "end", iid=cliente["id"], values=(
            cliente["nombre"], datos.nombre_coach(cliente["coach_id"]), ultima or "Sin registros"))

    def _on_select(_evento=None):
        seleccion = arbol.selection()
        if seleccion:
            nav.cargar_pantalla("mediciones_listado", cliente_id=seleccion[0])

    arbol.bind("<Double-1>", _on_select)
    ttk.Label(contenedor, text="Doble clic sobre un cliente para revisar sus mediciones.",
              style="Suave.TLabel").pack(anchor="w", pady=(4, 0))


def render_panel(contenedor):
    """Panel general del administrador: KPIs, alertas de inactividad y accesos (HU20/HU31)."""
    utils.titulo(contenedor, "Panel general")

    total_rutinas_activas = sum(len(datos.rutinas_activas_de_cliente(c["id"]))
                                for c in datos.clientes_activos())
    indicadores = [
        ("Clientes activos", len(datos.clientes_activos()), "clientes_listado"),
        ("Rutinas vigentes", total_rutinas_activas, "clientes_listado"),
        ("Objetivos por vencer (14 dias)", len(datos.objetivos_proximos_a_vencer()),
         "clientes_listado"),
    ]
    marco_kpi = ttk.Frame(contenedor)
    marco_kpi.pack(fill="x", pady=(0, 16))
    for texto, valor, pantalla in indicadores:
        _tarjeta_kpi(marco_kpi, texto, valor, pantalla)

    utils.subtitulo(contenedor, "Alertas de inactividad (3+ semanas sin avances) — HU20")
    _seccion_alertas(contenedor)

    marco_acciones = ttk.Frame(contenedor)
    marco_acciones.pack(fill="x", pady=(20, 0))
    ttk.Button(marco_acciones, text="Generar reporte de progreso de un cliente (HU32)",
               command=lambda: nav.cargar_pantalla("reporte_cliente")
               ).pack(side="left", padx=(0, 8))
    ttk.Button(marco_acciones, text="Exportar clientes activos a CSV (HU33)",
               command=_exportar_csv).pack(side="left")


def _exportar_csv():
    ruta = filedialog.asksaveasfilename(defaultextension=".csv",
                                        filetypes=[("Archivo CSV", "*.csv")],
                                        initialfile="clientes_progreso.csv")
    if not ruta:
        return
    with open(ruta, "w", newline="", encoding="utf-8-sig") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["Nombre", "Contacto", "Coach asignado", "Ultima medicion",
                            "Objetivo vigente"])
        for cliente in datos.clientes_activos():
            escritor.writerow(_fila_exportacion(cliente))
    utils.informar(f"Archivo exportado correctamente en:\n{ruta}")


def _fila_exportacion(cliente):
    """Arma la fila del CSV de exportacion para un cliente activo (HU33)."""
    contacto = cliente["correo"] or cliente["telefono"] or ""
    mediciones = datos.mediciones_de_cliente(cliente["id"])
    ultima = mediciones[0]["fecha"] if mediciones else ""
    objetivo = datos.objetivo_activo_de_cliente(cliente["id"])
    texto_objetivo = (f"{objetivo['tipo']} ({objetivo['valor_meta']} {objetivo['unidad']})"
                      if objetivo else "")
    return [cliente["nombre"], contacto, datos.nombre_coach(cliente["coach_id"]), ultima,
            texto_objetivo]


def render_reporte(contenedor):
    """Formulario para generar y exportar el reporte de progreso de un cliente (HU32)."""
    utils.titulo(contenedor, "Reporte de progreso de un cliente")

    nombres_clientes = [c["nombre"] for c in datos.clientes]
    cliente_v = utils.campo_combobox(contenedor, "Cliente:", nombres_clientes)
    inicio_v = utils.campo_formulario(contenedor, "Desde (AAAA-MM-DD):",
                                       valor_inicial="2000-01-01")
    fin_v = utils.campo_formulario(contenedor, "Hasta (AAAA-MM-DD):", valor_inicial=datos.hoy_iso())

    texto_reporte = tk.Text(contenedor, height=16, width=90)

    def _generar():
        if not utils.fecha_valida(inicio_v.get()) or not utils.fecha_valida(fin_v.get()):
            utils.error("Debe indicar un rango de fechas valido (AAAA-MM-DD).")
            return
        cliente = next(c for c in datos.clientes if c["nombre"] == cliente_v.get())
        contenido = _construir_reporte(cliente, inicio_v.get(), fin_v.get())
        texto_reporte.delete("1.0", "end")
        texto_reporte.insert("1.0", contenido)
        texto_reporte.pack(fill="both", expand=True, pady=12)

    def _guardar_archivo():
        contenido = texto_reporte.get("1.0", "end").strip()
        if not contenido:
            utils.error("Genere el reporte antes de guardarlo.")
            return
        ruta = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Archivo de texto", "*.txt")],
                                            initialfile="reporte_progreso.txt")
        if not ruta:
            return
        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write(contenido)
        utils.informar(f"Reporte guardado en:\n{ruta}")

    marco_botones = ttk.Frame(contenedor)
    marco_botones.pack(anchor="w", pady=12)
    ttk.Button(marco_botones, text="Generar reporte", style="Primario.TButton",
               command=_generar).pack(side="left", padx=(0, 8))
    ttk.Button(marco_botones, text="Guardar como archivo .txt",
               command=_guardar_archivo).pack(side="left", padx=8)
    ttk.Button(marco_botones, text="Volver al panel",
               command=lambda: nav.cargar_pantalla("panel_admin")).pack(side="left", padx=8)


def _lineas_mediciones(cliente, inicio, fin):
    mediciones_rango = [m for m in datos.mediciones_de_cliente(cliente["id"])
                        if inicio <= m["fecha"] <= fin]
    lineas = ["Mediciones en el periodo:"]
    if not mediciones_rango:
        lineas.append("  No hay informacion disponible en ese periodo.")
        return lineas
    for medicion in sorted(mediciones_rango, key=lambda m: m["fecha"]):
        lineas.append(
            f"  {medicion['fecha']}: peso {medicion.get('peso', '-')} kg, "
            f"cintura {medicion.get('cintura', '-')}, cadera {medicion.get('cadera', '-')}, "
            f"brazo {medicion.get('brazo', '-')}, pierna {medicion.get('pierna', '-')}, "
            f"grasa {medicion.get('grasa', '-')}%")
    return lineas


def _lineas_objetivo(cliente):
    objetivo = datos.objetivo_activo_de_cliente(cliente["id"])
    if not objetivo:
        return ["Objetivo vigente:", "  Sin objetivo activo."]
    return ["Objetivo vigente:",
            f"  {objetivo['tipo']} — meta {objetivo['valor_meta']} {objetivo['unidad']} "
            f"antes de {objetivo['fecha_limite']}"]


def _lineas_cumplimiento(cliente, inicio, fin):
    registros_rango = [(r, reg) for r, reg in datos.registros_de_cliente(cliente["id"])
                       if inicio <= reg["fecha"] <= fin]
    lineas = ["Cumplimiento de rutinas en el periodo:"]
    if not registros_rango:
        lineas.append("  No hay informacion disponible en ese periodo.")
        return lineas
    for rutina, registro in sorted(registros_rango, key=lambda par: par[1]["fecha"]):
        total = len(rutina["ejercicios"])
        realizados = sum(1 for v in registro["ejercicios"].values() if v["realizado"])
        lineas.append(f"  {registro['fecha']}: {rutina['nombre']} — {realizados}/{total} "
                      "ejercicios realizados")
    return lineas


def _construir_reporte(cliente, inicio, fin):
    """Arma el texto completo del reporte de progreso de un cliente (HU32)."""
    lineas = [f"REPORTE DE PROGRESO — {cliente['nombre']}", f"Periodo: {inicio} a {fin}", ""]
    lineas += _lineas_mediciones(cliente, inicio, fin)
    lineas.append("")
    lineas += _lineas_objetivo(cliente)
    lineas.append("")
    lineas += _lineas_cumplimiento(cliente, inicio, fin)
    return "\n".join(lineas)


nav.registrar_pantalla("panel_admin", render_panel)
nav.registrar_pantalla("reporte_cliente", render_reporte)
