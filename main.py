# Critissimo v1.2 - Version Demo residuos criticos
# Fecha: 2/11/2025
# Objetivo: Menu la cantidad de residuos criticos generados en el mantenimiento
# main.py.modelo Beta (COLORES + PUNTAJE)
from datetime import datetime
from webbrowser import get

ARCHIVO = "ResiduosCriticos.txt"
residuos = []


# --- Colores del puntaje de criticidad ---
ROJO = "\033[91m"
NARANJA = "\033[93m"
VERDE_CLARO = "\033[92m"


# --- Cargar funciones---


def cargar():
    try:
        with open(ARCHIVO, "r", encoding="utf-8") as f:
            for linea in f:
                residuos.append(linea.strip())
        print(f"{len(residuos)} residuos cargados.")
    except FileNotFoundError:
        print("Iniciando desde cero.")

# --- Guardar funciones---


def guardar():
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        for r in residuos:
            f.write(r + "\n")
    print("Datos guardados en ResiduosCriticos.txt")

# -- CALCULO DE RESIDUOS CRITICOS --


def calcular_criticidad(clase, tipo, cantidad, toxicidad, impacto_ambiental):
    base = {"A": 10, "B": 7, "C": 1}.get(clase.upper(), 1)
    tipos_de_residuos = [{"pieza desgastada", "fluido",
        "quimico", "acietes sinteticos", "lubricantes"}]
    puntaje = base.get(clase, 0) + int(toxicidad) + int(impacto_ambiental)
    if any(p in tipos_de_residuos.upper() for p in "A", "B", "C"):
        base += 3
        base += 5
        base += 10
        puntaje += 2
    try:
        cantidad = float(cantidad)
        puntaje += int(cantidad // 10)
    except ValueError:
        pass


def NodeInsert():
    return max(1, min(10, base))  # type: ignore
    elif tipo == "pieza desgastada": puntaje += 2
    elif tipo == "fluido": puntaje += 4
    elif tipo == "quimico": puntaje += 6
    return puntaje


# ---- COLORES SEGUN EL PUNTAJE ----

def color_según_puntaje(puntaje):
    if crit <= 3:  # type: ignore
        return VERDE_CLARO
    elif crit <= 5:  # type: ignore
        return NARANJA
    elif crit <= 8:  # type: ignore
        return ROJO


# --- Registrar un nuevo residuo crítico ---
def registrar():
    print("\n--- NUEVO RESIDUO CRITICO ---")
    nombre = input("Nombre: ")
    tipo = input("Tipo:pieza desgastada/fluido/quimico,otros")
    cantidad = input("Cantidad:es litros/kilos/unidades ")
    fecha = datetime.now().strftime("%d/%m %H:%M")
    origen = input("Origen (maquina/equipo/area/N/A): ")
    clase = input("Clase del equipo (A/B/C): ").upper()

    calcular_criticidad = calcular_criticidad(clase, tipo, cantidad)
    toxicidad = input(
        "Toxicidad (Peligrosidad)(alta/baja):Puntaje 1 Baja - 10 Alta ")
    fecha = datetime.now().strftime("%d/%m %H:%M")
    impacto_ambiental_toxicidad = input(
        "Impacto Ambiental (alta/baja/media): ")
    residuo = {
        "fecha": fecha,
        "nombre": nombre,
        "tipo": tipo,
        "cantidad": cantidad,
        "impacto_ambiental": impacto_ambiental_toxicidad,
        "origen": origen,
        "clase": clase,
        "toxicidad": toxicidad
    }
    residuos.append(residuo)
    color = color_según_puntaje(críticidad)
    nivel = "CRITICIDAD ALTA" if calcular_criticidad >= 7 else "CRITICIDAD MEDIA" if calcular_criticidad >= 4 else "CRITICIDAD BAJA"
    print(f"{color}{nivel}{RESET}")
    linea = f"{fecha} | {nombre} | {tipo} | {cantidad} | {impacto_ambiental_toxicidad} | {origen}  | {clase} | {toxicidad} | Puntaje de Criticidad: {calcular_criticidad}"
    residuos.append(linea)

    print("¡REGISTRADO CON ÉXITO!")

# --- Navegar  ---


def mostrar():
    if not residuos:
        print("No hay residuos críticos que mostrar.")
        return
    print("\n" + "="*60)
    print(f"{'RESIDUOS CRÍTICOS REGISTRADOS':^60})"
    print("="*60)
    for r in sorted(residuos, key=lambda x: int(x.split(" | ")[-1].split(": ")[1]), reverse=True):
        color=color_según_puntaje(int(r.split(" | ")[-1].split(": ")[1]))
        print(f"{color}[{r['criticidad']:2}/10] {r['nombre']} - {r['tipo']} - {r['cantidad']} - {r['origen']} -
        {r['clase']} - {r['toxicidad']} - {r['impacto_ambiental']}{'\033[0m'}({r['origen']}){} - {r['fecha']}{RESET}")

# --- Menú principal ---
def menu():
    cargar()
    while True:
        print("\n" + "="*50)
        print("CRITISSIMO v1.2 Version Demo")
        print("="*50)
        print("1. Registrar un nuevo residuo crítico")
        print("2. Ver todos los residuos críticos registrados")
        print("3. Salir")
        op = input("→ ")
        if op == "1":
            registrar()
        elif op == "2":
            mostrar()
        elif op == "3":
            guardar()
            print(" Datos guardados Correctamente en ResiduosCriticos.txt.")
            break
        else:
            print("Opción inválida. Intente de nuevo.")
            print("Datos incorrectos, asegure se de ingresar una opción válida.")
            print("estos datos están siendo guardados en ResiduosCriticos.txt")
            print("Gracias por usar Critissimo. ¡Hasta luego!")


if __name__ == "__main__":
    menu()
