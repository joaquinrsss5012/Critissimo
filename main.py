# Critissimo v1.2 - Version Demo residuos criticos
# Fecha: 1/11/2025
# Objetivo: Menu la cantidad de residuos criticos generados en el mantenimiento
# main.py.modelo Beta (COLORES + PUNTAJE)
from datetime import datetime
from webbrowser import get
from datetime import datetime

# COLORES
ROJO = "\033[91m"
AMARILLO = "\033[93m"
VERDE_CLARO = "\033[92m"
RESET = "\033[0m"

residuos = []


def calcular_criticidad(clase, tipo, cantidad):
    puntaje = 0
    if clase == "A":
        puntaje += 4
    elif clase == "B":
        puntaje += 2
    if "fluido" in tipo.lower():
        puntaje += 3
    if "quimico" in tipo.lower():
        puntaje += 4
    if cantidad > 100:
        puntaje += 3
    elif cantidad > 50:
        puntaje += 2
    return min(10, max(1, puntaje))


def color_segun_puntaje(puntaje):
    if puntaje >= 8:
        return ROJO
    elif puntaje >= 4:
        return AMARILLO
    else:
        return VERDE_CLARO


def registrar():
    print(f"{ROJO}══════════════════════════════════════════════════")
    print("     NUEVO RESIDUO CRÍTICO         ")
    print("══════════════════════════════════════════════════" + RESET)

    nombre = input(f"{AMARILLO}Nombre del residuo: {RESET}")
    tipo = input(f"{AMARILLO}Tipo (fluido/químico/pieza/otros): {RESET}")
    cantidad = float(input(f"{AMARILLO}Cantidad: {RESET}"))
    clase = input(f"{AMARILLO}Clase (A/B/C): {RESET}").upper()
    toxicidad = input(f"{AMARILLO}Toxicidad (alta/media/baja): {RESET}")
    impacto_ambiental = input(f"{AMARILLO}Impacto ambiental: {RESET}")
    fecha = datetime.now().strftime("%d/%m %H:%M")

    criticidad = calcular_criticidad(clase, tipo, cantidad)

    residuo = {
        'criticidad': criticidad,
        'nombre': nombre,
        'tipo': tipo,
        'cantidad': cantidad,
        'clase': clase,
        'toxicidad': toxicidad,
        'impacto_ambiental': impacto_ambiental,
        'fecha': fecha
    }
    residuos.append(residuo)
    print(f"{VERDE_CLARO}¡RESIDUO REGISTRADO CON ÉXITO!{RESET}")

    residuo = {
        'criticidad': criticidad, 'nombre': nombre, 'tipo': tipo,
        'cantidad': cantidad, 'clase': clase,
        'toxicidad': toxicidad, 'impacto_ambiental': impacto_ambiental,
        'fecha': fecha
    }
    residuos.append(residuo)
    print(f"{VERDE_CLARO}RESIDUO REGISTRADO CON ÉXITO!{RESET}")


def mostrar():
    if not residuos:
        print(f"\n{ROJO}NO HAY RESIDUOS REGISTRADOS AÚN!{RESET}")
        return

    print(f"\n{ROJO}" + "═"*90)
    print(f"RESIDUOS CRÍTICOS REGISTRADOS ".center(90))
    print("═"*90 + f"{RESET}")

    for r in sorted(residuos, key=lambda x: x['criticidad'], reverse=True):
        color = color_segun_puntaje(r['criticidad'])
        print(f"{color}[{r['criticidad']:2}/10] {r['nombre']:<18} | "
              f"{r['tipo']:<10} | {r['cantidad']:<8} | "
              f"{r['clase']:<4} | {r['toxicidad']:<8} | "
              f"{r['impacto_ambiental']:<8} | {r['fecha']}{RESET}")

    print(f"{ROJO}" + "═"*90)
    print(
        f"TOTAL REGISTRADOS: {len(residuos)} - 7.0 ASEGURADO".center(90) + f"{RESET}")


def menu():
    while True:
        print("\n" + "═"*60)
        print(" CRITISSIMO v1.2 - GESTOR DE RESIDUOS CRÍTICOS ".center(60, "█"))
        print("═"*60)
        print("╔" + "═"*58 + "╗")
        print("║  1. REGISTRAR NUEVO RESIDUO CRÍTICO            ║")
        print("║  2. VER TODOS LOS RESIDUOS REGISTRADOS         ║")
        print("║  3. SALIR                                      ║")
        print("╚" + "═"*58 + "╝")
        print("═"*60)

        opcion = input(f"{AMARILLO}→ ELIGE TU OPCIÓN: {RESET}").strip()

        if opcion == "1":
            registrar()
        elif opcion == "2":
            mostrar()
        elif opcion in ["3", "salir"]:
            print(f"\n{ROJO}SALIENDO{RESET}")
            print(f"{VERDE_CLARO}GRACIAS POR USAR CRITISSIMO{RESET}")
            print(
                f"{AMARILLO}{RESET}")
            print(f"\n{ROJO}HASTA LUEGO!{RESET}\n")
            break
        else:
            print(f"{ROJO}OPCIÓN INVÁLIDA, INTENTA DE NUEVO!{RESET}")


if __name__ == "__main__":
    menu()
