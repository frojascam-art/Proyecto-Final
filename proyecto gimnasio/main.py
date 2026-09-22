# -*- coding: utf-8 -*-
"""
Sistema de Gimnasio - Proyecto Final Curso IA RACSA
Version de escritorio en Python (Tkinter), construida a partir de las
historias de usuario refinadas con INVEST (ver
../insumos proyecto final/historias_usuario_invest.py) y usando como
referencia de flujo/navegacion el prototipo estatico de
../prototipo gimnasio/.

Ejecutar con:
    python main.py

Requisitos: Python 3.9 o superior con Tkinter (incluido en la instalacion
estandar de Python para Windows). No se necesitan dependencias externas
ni proceso de build. Los datos se guardan automaticamente en
datos_gimnasio.json (junto a este archivo) y persisten entre ejecuciones.
"""

import tkinter as tk

from app import datos
from app.navegacion import cargar_pantalla, construir_ventana

# Los modulos de pantallas se importan solo por su efecto secundario: cada
# uno llama a registrar_pantalla() al cargarse (equivalente a los
# <script src="pantallas/..."> del prototipo estatico), por lo que pylint
# los marca como "no usados" aunque son necesarios.
from app.pantallas import (  # pylint: disable=unused-import
    clientes,
    comunicacion,
    inicio,
    mediciones,
    mi_progreso,
    mis_rutinas,
    objetivos,
    panel_admin,
    rutinas,
)


def main():
    """Punto de entrada: carga los datos persistidos y abre la ventana principal."""
    datos.cargar_datos()
    root = tk.Tk()
    construir_ventana(root)
    cargar_pantalla("inicio")
    root.mainloop()


if __name__ == "__main__":
    main()
