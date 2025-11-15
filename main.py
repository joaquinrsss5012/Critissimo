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

# === ASIGNAR FRAMES ===
frame_reg = tab_registro
frame_hist = tab_historial
frame_matriz = tab_matriz
frame_exp = tab_exportar

# === REGISTRO DE RESIDUOS ===
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


def registrar_db():
    datos = {k.split()[0].lower(): v.get() for k, v in entries.items()}
    criticidad = calcular_criticidad(
        datos.get("impacto", ""), datos.get("tipo", ""), datos.get("clase", ""))
    datos['criticidad'] = criticidad
    datos['fecha'] = datetime.now().strftime("%d/%m %H:%M")

    conn.execute('''
    INSERT INTO residuos (nombre,tipo,cantidad,unidad,clase,toxicidad,impacto,criticidad,fecha)
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

# === HISTORIA DE LOS RESIDUOS ===
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


# === FUNCIÓN  PAPA CARGAR  EL HISTORIAL ===
def cargar_historial():
    for i in treeview.get_children():
        treeview.delete(i)

    cursor = conn.execute(
        "SELECT id,nombre,tipo,cantidad||unidad,clase,criticidad,fecha FROM residuos ORDER BY criticidad DESC"
    )

    for row in cursor:
        criticidad = row[5]
        if criticidad >= 8:
            color = "rojo"
        elif criticidad >= 4:
            color = "naranja"
        else:
            color = "verde"
        treeview.insert("", "end", values=row, tags=(color,))

    # Colores
    treeview.tag_configure("rojo", foreground="#FF1744")
    treeview.tag_configure("naranja", foreground="#FF6B00")
    treeview.tag_configure("verde", foreground="#00C853")


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

# === MATRIZ DE RIESGO AMBIENTAL ===
matriz = [
    ["", "Leve", "Moderado", "Severo"],
    ["Baja", "Verde", "Verde", "Naranja"],
    ["Media", "Verde", "Naranja", "Rojo"],
    ["Alta", "Naranja", "Rojo", "Rojo"]
]

for i, row in enumerate(matriz):
    for j, cell in enumerate(row):
        color = "white"
        if "Verde" in cell:
            color = "#00C853"
        elif "Naranja" in cell:
            color = "#FF6B00"
        elif "Rojo" in cell:
            color = "#FF1744"

        label = ctk.CTkLabel(
            frame_matriz,
            text=cell,
            width=120, height=60,
            fg_color=color,
            text_color="white" if color != "white" else "black",
            font=("Arial", 12, "bold")
        )
        label.grid(row=i, column=j, padx=1, pady=1)

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
    width=300  # corr
).pack(pady=20)

# === INICIAR EL MENU ===
cargar_historial()  # ← AL FINAL
app.mainloop()
