# -*- coding: utf-8 -*-
"""
HU5  - Registro de medidas antropometricas
HU15 - Visualizacion grafica de la evolucion de medidas (vista coach)
HU16 - Registro de fotos de progreso de un cliente
HU17 - Comparacion de dos periodos de medicion

Estas mismas funciones se reutilizan en modo solo_lectura=True para HU24
(medidas), HU25 (grafico) y HU27 (fotos), vistas desde el rol cliente
(ver app/pantallas/mi_progreso.py), tal como se documento en la nota de
ambiguedad A9 del archivo de historias de usuario.
"""

import os
import tkinter as tk
from tkinter import filedialog, ttk

from .. import datos
from .. import navegacion as nav
from .. import utils

CAMPOS_MEDIDA = [("peso", "Peso (kg)"), ("cintura", "Cintura (cm)"), ("cadera", "Cadera (cm)"),
                 ("brazo", "Brazo (cm)"), ("pierna", "Pierna (cm)"), ("grasa", "% Grasa corporal")]


def _cliente_objetivo(cliente_id):
    return cliente_id or nav.estado["cliente_en_foco_id"]


def _volver(cliente_id):
    if nav.estado["rol"] == "cliente":
        nav.cargar_pantalla("mi_progreso")
    else:
        nav.cargar_pantalla("mediciones_listado", cliente_id=cliente_id)


def render_listado(contenedor, cliente_id=None, solo_lectura=False):
    """Lista las mediciones de un cliente y da acceso a registrar/graficar/comparar (HU5/HU24)."""
    cliente_id = _cliente_objetivo(cliente_id)
    cliente = datos.obtener_cliente_por_id(cliente_id)
    if not cliente:
        utils.mensaje_vacio(contenedor, "Cliente no encontrado.")
        return

    utils.titulo(contenedor, f"Mediciones de {cliente['nombre']}" if not solo_lectura
                 else "Mis medidas corporales")

    marco_top = ttk.Frame(contenedor)
    marco_top.pack(fill="x", pady=(0, 10))
    if not solo_lectura:
        ttk.Button(marco_top, text="+ Registrar medicion", style="Primario.TButton",
                   command=lambda: nav.cargar_pantalla("medicion_form", cliente_id=cliente_id)
                   ).pack(side="left", padx=(0, 6))
        ttk.Button(marco_top, text="Comparar dos mediciones",
                   command=lambda: nav.cargar_pantalla("medidas_comparar", cliente_id=cliente_id)
                   ).pack(side="left", padx=6)
    ttk.Button(marco_top, text="Ver grafico de evolucion",
               command=lambda: nav.cargar_pantalla(
                   "medidas_grafico", cliente_id=cliente_id, solo_lectura=solo_lectura)
               ).pack(side="left", padx=6)
    ttk.Button(marco_top, text="Fotos de progreso",
               command=lambda: nav.cargar_pantalla(
                   "fotos_progreso", cliente_id=cliente_id, solo_lectura=solo_lectura)
               ).pack(side="left", padx=6)

    lista = datos.mediciones_de_cliente(cliente_id)
    if not lista:
        texto_vacio = ("Este cliente aun no tiene mediciones registradas." if not solo_lectura
                       else "Aun no tienes mediciones registradas.")
        utils.mensaje_vacio(contenedor, texto_vacio)
        return

    columnas = [("fecha", "Fecha", 100)] + [(clave, texto, 100) for clave, texto in CAMPOS_MEDIDA]
    arbol = utils.tabla(contenedor, columnas, alturas=12)
    for medicion in lista:
        valores = [medicion["fecha"]] + [
            medicion.get(clave) if medicion.get(clave) is not None else "-"
            for clave, _ in CAMPOS_MEDIDA]
        arbol.insert("", "end", iid=medicion["id"], values=valores)


def render_form(contenedor, cliente_id):
    """Formulario para registrar una medicion, con deteccion de duplicados en la fecha (HU5)."""
    cliente = datos.obtener_cliente_por_id(cliente_id)
    utils.titulo(contenedor, f"Registrar medicion — {cliente['nombre']}")

    fecha_v = utils.campo_formulario(contenedor, "Fecha (AAAA-MM-DD):",
                                      valor_inicial=datos.hoy_iso())
    valores_v = {}
    for clave, texto in CAMPOS_MEDIDA:
        valores_v[clave] = utils.campo_formulario(contenedor, texto + ":")

    def _guardar():
        fecha = fecha_v.get().strip()
        if not utils.fecha_valida(fecha):
            utils.error("Debe indicar una fecha valida en formato AAAA-MM-DD.")
            return
        peso = utils.numero_o_none(valores_v["peso"].get())
        if peso is None:
            utils.error("El peso es obligatorio y debe ser un numero.")
            return
        otras_medidas = {clave: utils.numero_o_none(valores_v[clave].get())
                         for clave, _ in CAMPOS_MEDIDA if clave != "peso"}
        if not any(valor is not None for valor in otras_medidas.values()):
            utils.error("Debe registrar al menos una medida antropometrica ademas del peso.")
            return

        sobrescribir_id = None
        if datos.existe_medicion_en_fecha(cliente_id, fecha):
            existente = next(m for m in datos.mediciones_de_cliente(cliente_id)
                             if m["fecha"] == fecha)
            if not utils.confirmar(
                f"Ya existe una medicion para {cliente['nombre']} en {fecha}. "
                "¿Desea sobrescribirla?"):
                return
            sobrescribir_id = existente["id"]

        datos.guardar_medicion(cliente_id, fecha, sobrescribir_id=sobrescribir_id, peso=peso,
                                **otras_medidas)
        utils.informar("Medicion guardada correctamente.")
        nav.cargar_pantalla("mediciones_listado", cliente_id=cliente_id)

    utils.botones_dialogo(
        contenedor, lambda: nav.cargar_pantalla("mediciones_listado", cliente_id=cliente_id),
        _guardar, texto_guardar="Guardar medicion")


def _calcular_coordenadas(puntos, ancho, alto):
    """Calcula las coordenadas (x, y) de cada punto del grafico de lineas (HU15)."""
    margen_izq, margen_der, margen_sup, margen_inf = 60, 30, 20, 40
    valores = [valor for _, valor in puntos]
    v_min, v_max = min(valores), max(valores)
    if v_min == v_max:
        v_min -= 1
        v_max += 1
    paso_x = (ancho - margen_izq - margen_der) / (len(puntos) - 1)

    def _coord(indice, valor):
        x = margen_izq + indice * paso_x
        proporcion = (valor - v_min) / (v_max - v_min)
        y = margen_sup + (alto - margen_sup - margen_inf) * (1 - proporcion)
        return x, y

    coordenadas = [_coord(i, valor) for i, (_, valor) in enumerate(puntos)]
    return coordenadas, margen_izq, margen_der, margen_sup, margen_inf


def render_grafico(contenedor, cliente_id=None, solo_lectura=False):
    """Grafico de lineas de la evolucion de una medida, con valor al pasar el cursor (HU15/HU25)."""
    cliente_id = _cliente_objetivo(cliente_id)
    cliente = datos.obtener_cliente_por_id(cliente_id)
    utils.titulo(contenedor, f"Evolucion de medidas — {cliente['nombre']}" if not solo_lectura
                 else "Mi progreso en grafico")

    fila_medida = ttk.Frame(contenedor)
    fila_medida.pack(fill="x", pady=(0, 8))
    ttk.Label(fila_medida, text="Medida a graficar:").pack(side="left")
    combo = ttk.Combobox(fila_medida, state="readonly", width=22,
                          values=[texto for _, texto in CAMPOS_MEDIDA])
    combo.current(0)
    combo.pack(side="left", padx=6)

    etiqueta_punto = ttk.Label(contenedor, text="Mueva el cursor sobre el grafico para ver el "
                                "valor exacto de cada medicion.", style="Suave.TLabel")
    etiqueta_punto.pack(anchor="w", pady=(4, 4))

    canvas = tk.Canvas(contenedor, bg="white", height=340, highlightthickness=1,
                       highlightbackground=nav.COLOR_BORDE)
    canvas.pack(fill="x", pady=6)

    def _dibujar(*_):
        if not canvas.winfo_exists():
            return
        canvas.delete("all")
        clave = CAMPOS_MEDIDA[combo.current()][0]
        puntos = [(m["fecha"], m[clave]) for m in reversed(datos.mediciones_de_cliente(cliente_id))
                 if m.get(clave) is not None]
        if len(puntos) < 2:
            canvas.create_text(20, 20, anchor="nw",
                                text="Se necesitan al menos dos mediciones con esta medida para "
                                     "graficar una tendencia.", fill=nav.COLOR_TEXTO_SUAVE)
            return

        ancho = canvas.winfo_width() or 800
        alto = 340
        coordenadas, margen_izq, margen_der, margen_sup, margen_inf = _calcular_coordenadas(
            puntos, ancho, alto)

        canvas.create_line(margen_izq, margen_sup, margen_izq, alto - margen_inf,
                            fill=nav.COLOR_BORDE)
        canvas.create_line(margen_izq, alto - margen_inf, ancho - margen_der, alto - margen_inf,
                            fill=nav.COLOR_BORDE)

        for i in range(len(coordenadas) - 1):
            canvas.create_line(*coordenadas[i], *coordenadas[i + 1], fill=nav.COLOR_PRIMARIO,
                               width=2)
        for (fecha, _valor), (x, y) in zip(puntos, coordenadas):
            canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill=nav.COLOR_PRIMARIO, outline="")
            canvas.create_text(x, alto - margen_inf + 14, text=fecha[5:], font=("Segoe UI", 7))

        def _mover(evento):
            mas_cercano = min(range(len(coordenadas)),
                              key=lambda i: abs(coordenadas[i][0] - evento.x))
            fecha, valor = puntos[mas_cercano]
            etiqueta_punto.config(text=f"Fecha: {fecha}  —  Valor: {valor}")

        canvas.bind("<Motion>", _mover)

    combo.bind("<<ComboboxSelected>>", _dibujar)
    contenedor.after(50, _dibujar)

    ttk.Button(contenedor, text="Volver",
               command=lambda: _volver(cliente_id)).pack(anchor="w", pady=(12, 0))


def render_comparar(contenedor, cliente_id):
    """Compara dos mediciones de un cliente, mostrando la diferencia por medida (HU17)."""
    cliente = datos.obtener_cliente_por_id(cliente_id)
    utils.titulo(contenedor, f"Comparar mediciones — {cliente['nombre']}")

    lista = datos.mediciones_de_cliente(cliente_id)
    if len(lista) < 2:
        utils.mensaje_vacio(contenedor, "Se necesitan al menos dos mediciones para comparar.")
        ttk.Button(contenedor, text="Volver",
                   command=lambda: nav.cargar_pantalla("mediciones_listado", cliente_id=cliente_id)
                   ).pack(anchor="w", pady=(16, 0))
        return

    fechas = [m["fecha"] for m in lista]
    fila = ttk.Frame(contenedor)
    fila.pack(fill="x", pady=8)
    ttk.Label(fila, text="Inicio:").pack(side="left")
    inicio_v = tk.StringVar(value=fechas[-1])
    ttk.Combobox(fila, textvariable=inicio_v, values=fechas, state="readonly", width=14
                 ).pack(side="left", padx=(4, 16))
    ttk.Label(fila, text="Fin:").pack(side="left")
    fin_v = tk.StringVar(value=fechas[0])
    ttk.Combobox(fila, textvariable=fin_v, values=fechas, state="readonly", width=14
                 ).pack(side="left", padx=4)

    marco_resultado = ttk.Frame(contenedor)
    marco_resultado.pack(fill="both", expand=True, pady=8)

    def _comparar():
        if inicio_v.get() == fin_v.get():
            utils.error("Elija dos fechas distintas para comparar.")
            return
        m_inicio = next(m for m in lista if m["fecha"] == inicio_v.get())
        m_fin = next(m for m in lista if m["fecha"] == fin_v.get())
        utils.limpiar(marco_resultado)
        columnas = [("medida", "Medida", 160), ("inicio", f"Inicio ({m_inicio['fecha']})", 130),
                    ("fin", f"Fin ({m_fin['fecha']})", 130), ("dif", "Diferencia", 160)]
        arbol = utils.tabla(marco_resultado, columnas, alturas=len(CAMPOS_MEDIDA))
        for clave, texto in CAMPOS_MEDIDA:
            v_inicio = m_inicio.get(clave)
            v_fin = m_fin.get(clave)
            if v_inicio is None or v_fin is None:
                diferencia = "-"
            else:
                absoluta = v_fin - v_inicio
                porcentual = (absoluta / v_inicio * 100) if v_inicio else 0
                diferencia = f"{absoluta:+g} ({porcentual:+.1f}%)"
            arbol.insert("", "end", values=(texto, v_inicio if v_inicio is not None else "-",
                                             v_fin if v_fin is not None else "-", diferencia))

    ttk.Button(contenedor, text="Comparar", style="Primario.TButton",
               command=_comparar).pack(anchor="w")
    _comparar()

    ttk.Button(contenedor, text="Volver",
               command=lambda: nav.cargar_pantalla("mediciones_listado", cliente_id=cliente_id)
               ).pack(anchor="w", pady=(16, 0))


def render_fotos(contenedor, cliente_id=None, solo_lectura=False):
    """Galeria de fotos de progreso de un cliente, con comparacion de dos fotos (HU16/HU27)."""
    cliente_id = _cliente_objetivo(cliente_id)
    cliente = datos.obtener_cliente_por_id(cliente_id)
    utils.titulo(contenedor, f"Fotos de progreso — {cliente['nombre']}" if not solo_lectura
                 else "Mis fotos de progreso")

    if not solo_lectura:
        marco_top = ttk.Frame(contenedor)
        marco_top.pack(fill="x", pady=(0, 8))
        ttk.Button(marco_top, text="+ Agregar foto", style="Primario.TButton",
                   command=lambda: _abrir_form_foto(contenedor, cliente_id, _refrescar)
                   ).pack(side="left")

    fotos = datos.fotos_de_cliente(cliente_id)
    if not fotos:
        texto_vacio = ("Este cliente aun no tiene fotos registradas." if not solo_lectura
                       else "Aun no tienes fotos registradas.")
        utils.mensaje_vacio(contenedor, texto_vacio)
        ttk.Button(contenedor, text="Volver",
                   command=lambda: _volver(cliente_id)).pack(anchor="w", pady=(16, 0))
        return

    columnas = [("fecha", "Fecha", 100), ("archivo", "Archivo", 260)]
    arbol = utils.tabla(contenedor, columnas, alturas=8)
    arbol.configure(selectmode="extended")

    def _refrescar():
        arbol.delete(*arbol.get_children())
        for foto in datos.fotos_de_cliente(cliente_id):
            arbol.insert("", "end", iid=foto["id"],
                         values=(foto["fecha"], os.path.basename(foto["ruta"])))

    _refrescar()

    vista_previa = ttk.Frame(contenedor)
    vista_previa.pack(fill="x", pady=8)

    def _mostrar_previa(*_):
        utils.limpiar(vista_previa)
        seleccion = arbol.selection()
        fotos_sel = [f for f in datos.fotos_de_cliente(cliente_id) if f["id"] in seleccion]
        if not fotos_sel:
            return
        for foto in fotos_sel[:2]:
            _dibujar_previa_foto(vista_previa, foto)
        if len(fotos_sel) == 2:
            ttk.Label(vista_previa, text="Comparando dos fotos seleccionadas (Ctrl+clic para "
                      "elegir dos filas).", style="Suave.TLabel").pack(side="left", padx=8)

    arbol.bind("<<TreeviewSelect>>", _mostrar_previa)

    if not solo_lectura:
        def _eliminar():
            seleccion = arbol.selection()
            if not seleccion:
                utils.error("Seleccione una foto para eliminar.")
                return
            for foto_id in seleccion:
                datos.eliminar_foto(foto_id)
            _refrescar()
            utils.limpiar(vista_previa)

        ttk.Button(contenedor, text="Eliminar foto(s) seleccionada(s)",
                   command=_eliminar).pack(anchor="w", pady=(4, 0))

    ttk.Button(contenedor, text="Volver",
               command=lambda: _volver(cliente_id)).pack(anchor="w", pady=(16, 0))


def _dibujar_previa_foto(vista_previa, foto):
    """Muestra la vista previa de una foto (imagen si es posible, o un enlace para abrirla)."""
    marco = ttk.Frame(vista_previa)
    marco.pack(side="left", padx=8)
    ttk.Label(marco, text=foto["fecha"], style="Subtitulo.TLabel").pack()
    try:
        imagen = tk.PhotoImage(file=foto["ruta"])
        etiqueta_img = ttk.Label(marco, image=imagen)
        etiqueta_img.image = imagen
        etiqueta_img.pack()
    except tk.TclError:
        ttk.Label(marco, text=os.path.basename(foto["ruta"]), style="Suave.TLabel").pack()
        # La ruta la eligio el propio usuario en un filedialog (ver _abrir_form_foto),
        # nunca proviene de una fuente externa no confiable.
        ttk.Button(marco, text="Abrir archivo",
                   command=lambda r=foto["ruta"]: os.startfile(r)  # nosec B606
                   ).pack(pady=4)


def _abrir_form_foto(padre, cliente_id, refrescar):
    """Dialogo para registrar una foto de progreso a partir de un archivo local (HU16)."""
    ventana, marco = utils.dialogo(padre, "Agregar foto de progreso", ancho=460, alto=220)
    fecha_v = utils.campo_formulario(marco, "Fecha (AAAA-MM-DD):", valor_inicial=datos.hoy_iso())
    ruta_v = tk.StringVar()

    fila_ruta = ttk.Frame(marco)
    fila_ruta.pack(fill="x", pady=4)
    ttk.Label(fila_ruta, text="Archivo:", width=24).pack(side="left")
    ttk.Entry(fila_ruta, textvariable=ruta_v, width=28, state="readonly").pack(side="left")

    def _elegir_archivo():
        ruta = filedialog.askopenfilename(
            title="Seleccionar foto de progreso",
            filetypes=[("Imagenes", "*.png *.jpg *.jpeg *.gif"), ("Todos los archivos", "*.*")])
        if ruta:
            ruta_v.set(ruta)

    ttk.Button(fila_ruta, text="Examinar...", command=_elegir_archivo).pack(side="left", padx=6)

    def _guardar():
        fecha = fecha_v.get().strip()
        if not utils.fecha_valida(fecha):
            utils.error("Debe indicar una fecha valida en formato AAAA-MM-DD.")
            return
        if not ruta_v.get():
            utils.error("Debe seleccionar un archivo de imagen.")
            return
        datos.agregar_foto(cliente_id, fecha, ruta_v.get())
        ventana.destroy()
        refrescar()

    utils.botones_dialogo(marco, ventana.destroy, _guardar, texto_guardar="Guardar foto")


nav.registrar_pantalla("mediciones_listado", render_listado)
nav.registrar_pantalla("medicion_form", render_form)
nav.registrar_pantalla("medidas_grafico", render_grafico)
nav.registrar_pantalla("medidas_comparar", render_comparar)
nav.registrar_pantalla("fotos_progreso", render_fotos)
