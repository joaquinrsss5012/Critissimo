# Critissimo v1.0 - Version Primitiva residuos criticos
# Fecha: 1/11/2025
# Objetivo: Menu la cantidad de residuos criticos generados en el mantenimiento
# main.py.modelo Primitivo de Critissimo


import datetime
from datetime import datetime


ARCHIVO = "ResiduosCriticos.txt"
residuos = []
print("Critissimo v1.0")


def cargar():
    try:
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            for linea in f:
                residuos.append(linea.strip())
        print(f"{len(residuos)} residuos cargados.")
    except FileNotFoundError:
        print("Iniciando desde cero.")


def guardar():
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        for r in residuos:
            f.write(r + "\n")
    print("Datos guardados en ResiduosCriticos.txt")


def registrar():
    print("\n--- NUEVO RESIDUO Critico ---")


Nombre = input("Nombre")
Tipo = input("Tipo ")
Cantidad = input("Cantidad ")
