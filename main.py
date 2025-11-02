# Critissimo v1.0 - Version Primitiva residuos criticos
# Fecha: 1/11/2025
# Objetivo: Menur la cantidad de residuos criticos generados en el mantenimiento
# main.py.modelo Primitivo de Critissimo
from datetime import datetime

ARCHIVO = "ResiduosCriticos.txt"
residuos = []


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
    nombre = input("Nombre: ")
    tipo = input("Tipo: ")
    cantidad = input("Cantidad: ")
    fecha = datetime.now().strftime("%d/%m %H:%M")
    toxicidad = input("Toxicidad (alta/baja):Puntaje 1 Bajo - 10 Alto ")
    linea = f"{fecha} | {nombre} | {tipo} | {cantidad} | {toxicidad}"
    residuos.append(linea)
    print("¡REGISTRADO CON ÉXITO!")


def mostrar():
    if not residuos:
        print("No hay residuos críticos que mostrar.")
        return
    print("\n--- TUS RESIDUOS CRÍTICOS ---")
    for i, r in enumerate(residuos, 1):
        print(f"{i}. {r}")


def menu():
    cargar()
    while True:
        print("\n" + "="*40)
        print("CRITISSIMO v1.0 Version Primitiva")
        print("="*40)
        print("1. Registrar")
        print("2. Ver todos")
        print("3. Salir")
        op = input("→ ")
        if op == "1":
            registrar()
        elif op == "2":
            mostrar()
        elif op == "3":
            guardar()
            print("¡CHAO! Datos guardados.")
            break
        else:
            print("Opción inválida. Intente de nuevo.")


if __name__ == "__main__":
    menu()
