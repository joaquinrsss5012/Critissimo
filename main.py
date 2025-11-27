import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import pandas as pd

# === BASE DE DATOS ===
conn = sqlite3.connect('critissimo.db')
conn.execute('''
CREATE TABLE IF NOT EXISTS residuos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT, tipo TEXT, cantidad REAL, unidad TEXT,
    clase TEXT, toxicidad TEXT, impacto TEXT,
    criticidad INTEGER, fecha TEXT
)
''')
conn.commit()

# === VENTANA PRINCIPAL DE CRITISSIMO ===
app = ctk.CTk()
app.title("Critissimo v1.4 DEMO")
app.geometry("1200x700")
app.resizable(False, False)

ctk.CTkLabel(
    app,
    text="CRITISSIMO v1.4 DEMO",
    font=("Arial", 36, "bold"),
    text_color="#00C853"
).pack(pady=10)

# === TABVIEW ===
tabview = ctk.CTkTabview(app)
tabview.pack(pady=10, padx=20, fill="both", expand=True)

# === CREAR PESTAÑAS ===
tab_registro = tabview.add("Registro")
tab_historial = tabview.add("Historial")
tab_matriz = tabview.add("Matriz de Riesgo Ambiental")
tab_exportar = tabview.add("Exportar")
tab_estadisticas = tabview.add("Estadisticas")

# === ASIGNAR FRAMES ===
frame_reg = tab_registro
frame_hist = tab_historial
frame_matriz = tab_matriz
frame_exp = tab_exportar
frame_est = tab_estadisticas

# === REGISTRO DE RESIDUOS  ===
entries = {}
campos = ["Nombre", "Tipo", "Cantidad", "Unidad",
          "Clase (A/B/C)", "Toxicidad", "Impacto"]

for i, campo in enumerate(campos):
    ctk.CTkLabel(frame_reg, text=campo + ":").grid(row=i,
                                                   column=0, padx=10, pady=5, sticky="w")
    entry = ctk.CTkEntry(frame_reg, width=300)
    entry.grid(row=i, column=1, padx=10, pady=5)
    entries[campo] = entry


def calcular_criticidad(impacto, tipo, origen):
    score = 0
    if "alto" in impacto.lower():
        score += 3
    if "corrosivo" in tipo.lower():
        score += 3
    if "roto" in origen.lower():
        score += 2
    return score

# ALERTAS PREDICTIVAS AMBIENTALES


def alertas_predictiva_ambientales():
    alertas_ambientales = []

    # 1.Los Residuos más criticos
    cursor = conn.execute("""
        SELECT nombre, tipo, criticidad, fecha
        FROM residuos
        WHERE criticidad >= 8
        ORDER BY criticidad DESC, fecha DESC
        LIMIT 5
 """)

    for row in cursor:
        alertas.ambientales.append(
            f"CRITICO PRÓXIMO ¡{row[0]} ({row[1]}) \nCriticidad: {row[2]}/10 \nRegistrado el: {row[3]}")

    # 2.Residuos que se repiten y suben de criticidad
    cursor2 = conn.execute("""
       SELECT nombre, COUNT(*) as veces, AVG(criticidad) as prom
       FROM residuos
       WHERE criticidad >= 5
       GROUP BY nombre
       HAVING veces >= 2 AND prom >= 5.5
""")

    for row in cursor2:
        alertas.ambientales.append(
            F"¡SUBE DE CRITICIDAD! {row[0]} \nVeces registrado: {row[1]} \nCriticidad Promedio: {row[2]:.1f}/10")
    return alertas.ambientales
# === FUNCIÓN PARA REGISTRAR EN LA BASE DE DATOS ===


def registrar_db():
    datos = {k.split()[0].lower(): v.get() for k, v in entries.items()}
    criticidad = calcular_criticidad(
        datos.get("impacto", ""), datos.get("tipo", ""), datos.get("clase", ""))
    datos['criticidad'] = criticidad
    datos['fecha'] = datetime.now().strftime("%d/%m %H:%M")

    conn.execute('''
    INSERT INTO residuos
    (nombre,tipo,cantidad,unidad,clase,toxicidad,impacto,criticidad,fecha)
    VALUES (?,?,?,?,?,?,?,?,?)
    ''', (
        datos['nombre'], datos['tipo'], datos['cantidad'], datos['unidad'],
        datos['clase'], datos['toxicidad'], datos['impacto'], criticidad, datos['fecha']
    ))

    conn.commit()
    messagebox.showinfo(
        "Éxito", f"Residuo registrado. Criticidad: {criticidad}/10")
    for entry in entries.values():
        entry.delete(0, "end")


ctk.CTkButton(
    frame_reg,
    text="REGISTRAR RESIDUO",
    command=registrar_db,
    fg_color="#1dd1a1",
    hover_color="#10ac84",
    height=50,
    width=300  # ← CORREGIDO: SIN PUNTO
).grid(row=len(campos), column=0, columnspan=2, pady=20)

# === HISTORIAL DE LOS RESIDUOS ===
tree_frame = ctk.CTkFrame(tab_historial)
tree_frame.pack(pady=10, padx=20, fill="both", expand=True)

treeview = ttk.Treeview(
    tree_frame,
    columns=("id", "nombre", "tipo", "cantidad",
             "clase", "criticidad", "fecha"),
    show="headings",
    height=15
)

# Encabezados
for col, text in [
    ("id", "ID"), ("nombre", "Nombre"), ("tipo", "Tipo"), ("cantidad", "Cantidad"),
    ("clase", "Clase"), ("criticidad", "Criticidad"), ("fecha", "Fecha")
]:
    treeview.heading(col, text=text)

# Anchos
treeview.column("id", width=50)
treeview.column("nombre", width=200)
treeview.column("tipo", width=100)
treeview.column("cantidad", width=100)
treeview.column("clase", width=80)
treeview.column("criticidad", width=100)
treeview.column("fecha", width=120)
treeview.pack(fill="both", expand=True)

label_criticos = ctk.CTkLabel(tab_historial, text="RESIDUOS CRÍTICOS: 0", font=(
    "Arial", 18, "bold"), text_color="#00C853")
label_criticos.pack(pady=10)
# Conteo de críticos
label_criticos = ctk.CTkLabel(
    tab_historial, text="", font=("Arial", 18, "bold"))
label_criticos.pack(pady=10)

# === FUNCIÓN  PAPA CARGAR  EL HISTORIAL ===


def cargar_historial():
  # Limpiar la tabla
    for row in treeview.get_children():
        treeview.delete(i)

   # cargar datos desde la base de datos
cursor = conn.execute(
    "SELECT id, nombre, tipo, cantidad, clase, criticidad, fecha FROM residuos")

criticos = 0
for row in cursor:
    criticidad = row[5]
    if criticidad >= 8:
        color = "#FF1744", "rojo"
        criticos += 1
    elif criticidad >= 4:
        color = "#FF6B00", "naranja"
    else:
        color = "#00C853", "verde"
    treeview.insert("", "end", values=row, tags=(color[1],))

    # Configurarcion de colores
treeview.tag_configure("rojo", background="#FFCDD2")
treeview.tag_configure("naranja", background="#FFE0B2")
treeview.tag_configure("verde", background="#C8E6C9")

# Acuatializar los contadores en vivo
label_criticos.configure(
    text=f"RESIDUOS CRÍTICOS: {criticos}",
    text_color="#FF1744" if criticos > 0 else "#00C853",
)

# Alertas Predictivas Ambientales
alertas = alertas_predictiva_ambientales():
if alertas:
    mensaje = "IMPACTO AMBIENTAL CRITICO DETECTADO:\n\n" + "\n\n".join(alertas)
    messagebox.showwarning("ALERTAS PREDICTIVAS AMBIENTALES", mensaje)

    # Actualizar Estadisticas
actualizar_estadisticas()

# === BOTÓN ACTUALIZAR ===
frame_hist_btn = ctk.CTkFrame(tab_historial)
frame_hist_btn.pack(pady=10, fill="x")

ctk.CTkButton(
    frame_hist_btn,
    text="ACTUALIZAR HISTORIAL",
    command=cargar_historial,
    fg_color="#1dd1a1",
    hover_color="#10ac84"
).pack(pady=5)

ctk.CTkButton(
    frame_hist_btn,
    text="ELIMINAR SELECCIONADO",
    command=eliminar_residuo,
    fg_color="#e74c3c",
    hover_color="#c0392b"
).pack(side="left", padx=20)

# Botón de eliminar Residuos


def eliminar_residuo():
    seleccionado = treeview.focus()
    if not seleccionado:
        messagebox.showwarning(
            "Advertencia", "Elige un residuo para eliminar.")
        return

    valores = treeview.item(seleccionado, "values")
    if messagebox.askyesno("Confirmar eliminación", f"¿Esta seguro de eliminar el residuo ID ?{valores[0]}?\n{valores[1]}"):
        conn.execute("DELETE FROM residuos WHERE id = ?", (valores[0],))
        conn.commit()
        cargar_historial()
        messagebox.showinfo("Éxito", "Residuo eliminado correctamente.")


# === MATRIZ DE RIESGO AMBIENTAL ===
def mostrar_matriz():
    ventana_matriz = ctk.CTkToplevel(app)
    ventana_matriz.title("Matriz de Riesgo Ambiental")
    ventana_matriz.geometry("900x600")

    matriz_texto = """
                                                        MATRIZ DE RIESGO AMBIENTAL

    | Impacto / Probabilidad | Baja (1) | Media (2) | Alta (3) |
    |-----------------------|----------|-----------|----------|
    | Bajo (1)              | \033[92m1 (Baja)\033[0m         | \033[92m1 (Baja)\033[0m      | \033[92m1 (Baja)\033[0m       |
    | Medio (2)             | \033[92m1 (Baja)\033[0m         | \033[93m3 (Moderado)\033[0m  | \033[93m5 (Moderado)\033[0m   |
    | Alto (3)              | \033[91m3 (Alto)\033[0m         | \033[91m6 (Alto)\033[0m      | \033[91m9 (Alto)\033[0m       |

    Escalas de puntuación de Riesgo:
    - 1-3: Bajo
    - 4-6: Moderado
    - 7-10: Alto
    """

    etiqueta_matriz = ctk.CTkLabel(
        ventana_matriz,
        text=matriz_texto,
        font=("Courier", 14),
        justify="left"
    )
    etiqueta_matriz.pack(pady=20, padx=20)
    etiqueta_matriz.configure(
        font=("Courier", 16, "bold"),
        text_color="#00C853",
        justify="left"
    )

    titulo = ctk.CTkLabel(
        ventana_matriz,
        text="Matriz de Riesgo Ambiental",
        font=("Courier", 18, "bold"),
        text_color="#FF1744",
        justify="center"
    )
    titulo.pack(pady=10)

# === EXPORTAR A EXCEL ===


def exportar_excel():
    cursor = conn.execute("SELECT * FROM residuos")
    df = pd.DataFrame(cursor.fetchall(), columns=[
                      desc[0] for desc in cursor.description])
    df.to_excel("residuos_criticos.xlsx", index=False)
    messagebox.showinfo(
        "Exportado", "Datos guardados en 'residuos_criticos.xlsx'")


ctk.CTkButton(
    frame_exp,
    text="EXPORTAR A EXCEL",
    command=exportar_excel,
    fg_color="#1dd1a1",
    hover_color="#10ac84",
    height=50,
    width=300
).pack(pady=20)

# === INICIAR EL MENU ===
cargar_historial()
# Estadisticas Simples que se acualizan solas a mediada que se registran residuos
label_stats = None


def actualizar_estadisticas():
    global label_stats
    total = conn.execute("SELECT COUNT(*) FROM residuos").fetchone()[0]
    criticos = conn.execute(
        "SELECT COUNT(*) FROM residuos WHERE criticidad >= 8").fetchone()[0]
    promedio = conn.execute(
        "SELECT AVG(criticidad) FROM residuos").fetchone()[0] or 0

    stats_text = f"Total Residuos: {total}\nResiduos Críticos: {criticos}\nCriticidad Promedio: {promedio:.2f}/10"

    if label_stats is None:
        label_stats = ctk.CTkLabel(frame_est, text=stats_text, font=(
            "Arial", 26, "bold"), text_color="#00C853")
        label_stats.pack(pady=20)
    else:
        label_stats.configure(text=stats_text)
        if criticos > 0:
            label_stats.configure(text_color="#FF1744")
        else:
            label_stats.configure(text_color="#00C853")


actualizar_estadisticas()
app.mainloop()
