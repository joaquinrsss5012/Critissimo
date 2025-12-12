
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime
import pandas as pd

label_stats = None
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
app.geometry("1980x1080")

# == PANTALLA COMPLETA ===
app.state('zoomed')
app.attributes("-fullscreen", True)
app.bind("<Escape>", lambda e: app.attributes("-fullscreen", False))

ctk.set_appearance_mode("light")
app.configure(fg_color="#e8f5e9")

# ===  SCROLL PARA NO SE CORTE EL CONTENIDO EN LA PANTALLA ===
main_container = ctk.CTkScrollableFrame(app, fg_color="#e8f5e9")
main_container.pack(fill="both", expand=True, padx=30, pady=30)

ctk.CTkLabel(
    main_container,
    text="CRITISSIMO v1.4 DEMO",
    font=("Arial", 36, "bold"),
    text_color="#00C853"
).pack(pady=10)

# === TABVIEW ===
tabview = ctk.CTkTabview(
    main_container,
    segmented_button_selected_color="#00C853",
    segmented_button_selected_hover_color="#00A14A",
)

# === EXPORTAR A EXCEL ===


def exportar_excel():
    try:
        cursor = conn.execute("SELECT * FROM residuos")
        df = pd.DataFrame(cursor.fetchall(), columns=[
            desc[0] for desc in cursor.description])
        df.to_excel("residuos_criticos.xlsx", index=False)
        messagebox.showinfo(
            "Exportado", "Datos guardados en 'residuos_criticos.xlsx'")
    except Exception as e:
        messagebox.showerror(
            "Error", f"No se ha podido exportar intenté de nuevo: {str(e)}")


# === CREAR PESTAÑAS ===
tab_registro = tabview.add("Registro")
tab_historial = tabview.add("Historial")
tab_matriz = tabview.add("Matriz de Riesgo Ambiental")
tab_exportar = tabview.add("Exportar")
tab_estadisticas = tabview.add("Estadisticas")

# Frame exportar
frame_exp = ctk.CTkFrame(tab_exportar)
frame_exp.pack(fill="both", expand=True)

ctk.CTkButton(
    frame_exp,
    text="EXPORTAR A EXCEL",
    command=exportar_excel,
    font=("Arial", 18, "bold"),
    fg_color="#1dd1a1",
    hover_color="#10ac84",
    height=70,
    width=300,
    corner_radius=19
).pack(expand=True, pady=150)

# === ASIGNAR FRAMES ===
frame_reg = tab_registro
frame_hist = tab_historial
frame_matriz = tab_matriz
frame_exp = tab_exportar
frame_est = tab_estadisticas
# === REGISTRO DE RESIDUOS Segun la Normativa Legal D.S. 148/2003 ===
ctk.CTkLabel(
    frame_reg,
    text="REGISTRO DE RESIDUOS PELIGROSOS\nSEGUN NORMATIVA LEGAL D.S. 148/2003",
    font=("Arial", 24, "bold"),
    text_color="#00C853"
).grid(row=0, column=0, columnspan=2, pady=(50, 40))
# Campos de entrada visuales con placeholders
campos = [
    ("Nombre del Residuo", "ejemplo: Ácido Sulfúrico, Plomo, Mercurio"),
    ("Tipo (Sólido/Líquido/Gas)", "Ej: Liquído"),
    ("Cantidad", "EJ 1000"),
    ("Unidad (kg/litros/m3)", "EJ: litros"),
    ("Clase (I/II/III/IV)", "Ej: II"),
    ("Toxicidad (Baja/Media/Alta)", "Ej: Alta"),
    ("Impacto Ambiental (Bajo/Medio/Alto)", "Ej: Medio")
]

entries = {}
placeholder = [
    "Ejemplo: Ácido Sulfúrico, Plomo, Mercurio)",
    "Ejemplo: Liquído",
    "Ejemplo  25",
    "Ejemplo: litros",
    "Ejemplo: II",
    "Ejemplo: Alta",
    "Ejemplo: Bajo"
]


for i, (label_text, placeholder_text) in enumerate(campos):
    ctk.CTkLabel(frame_reg, text=f"{i+1}. {label_text}", font=("Arial", 14, "bold"),
                 anchor="e",).grid(row=i+1, column=0, pady=12, padx=20, sticky="e")

    entry = ctk.CTkEntry(
        frame_reg,
        width=350,
        height=42,
        placeholder_text=placeholder_text,
        font=("Arial", 14, "bold"),
        corner_radius=15,
        border_width=2,
        fg_color="#0f1a2e",
        border_color="#00d4ff",
        text_color="#ffffff",
    )
    entry.grid(row=i+1, column=1, pady=12, padx=20, sticky="w")
    entries[label_text] = entry

# === BOTON VERDE GRANDE PARA REGISTRAR ===
button_registrar = ctk.CTkButton(
    frame_reg,
    text="REGISTRAR RESIDUO",
    command=lambda: registrar_db(),
    font=("Arial", 18, "bold"),
    fg_color="#1dd1a1",
    hover_color="#10ac84",
    height=50,
    width=300,
    corner_radius=15,
)
button_registrar.grid(row=len(campos) + 1, column=0, columnspan=2, pady=80)
# Tooltips para ayudar al usuario
info_label = ctk.CTkLabel(
    frame_reg,
    text=" Clse I: Muy Peligroso(ej: residuos infecciosos, mercurio)\n "
    "Clase II: Peligroso (ej: residuos químicos, baterias, aceites)\n "
    "Clase III: Moderado (ej: residuos con menor riesgo)\n "
    "Clase IV: Poco Peligroso",
    font=("Arial", 19),
    text_color="#888888",
    justify="left",
)
info_label.grid(row=len(campos)+2, column=0, columnspan=2, pady=(20, 10))
# === FUNCIÓN PARA CALCULAR LA CRITICIDAD SEGUN LA NORMATIVA LEGAL D.S. 148/2003 ===


def calcular_criticidad(impacto, tipo, clase, toxicidad):
    """ Criticidad 1 a 10 segun Normativa Legal D.S. 148/2003
    Del Ministerio del Medio Ambiente de Chile.
    Reglamiento Sanitario para la gestion de residuos peligrosos
    """
    # Onderaciones oficales bsadas en D.S. 148/2003
    impacto_val = {"Bajo": 1, "Medio": 3, "Alto": 5}.get(impacto.strip(), 1)
    tipo_val = {"Sólido": 1, "Líquido": 4, "Gas": 6}.get(tipo.strip(), 1)
    clase_val = {"I": 7, "II": 4, "III": 2,
                 "IV": 0}.get(clase.strip().upper(), 0)
    toxicidad_val = {"Baja": 1, "Media": 3,
                     "Alta": 5}.get(toxicidad.strip(), 1)
    # Fórmula de criticidad oficial
    puntaje_bruto = (impacto_val * 1.0) * (tipo_val * 1.2) + \
        (clase_val * 1.4) + (toxicidad_val * 1.1)

    # Normalizar a escala de 1 a 10
    criticidad = int((puntaje_bruto / 27.0) * 10)
    criticidad = max(1, min(10, (criticidad)))
    return criticidad

# === FUNCIÓN DE ALERTAS PREDICTIVAS AMBIENTALES ===


def alertas_predictiva_ambientales():
    alertas = []

    # 1.Los Residuos más criticos
    cursor = conn.execute("""
        SELECT nombre, tipo, criticidad, fecha
        FROM residuos
        WHERE criticidad >= 8
        ORDER BY criticidad DESC, fecha DESC
        LIMIT 5
        """)
    for row in cursor:
        alertas.append(
            f"CRITICO {row[0]} ({row[1]}) - {row[2]} - {row[3]}")

    # 2.Residuos que se repiten y suben de criticidad
    cursor2 = conn.execute("""
        SELECT nombre, COUNT(*) as veces, AVG(criticidad) as prom
        FROM residuos
        WHERE criticidad >= 5
        GROUP BY nombre
        HAVING veces >= 2 AND prom >= 5.5
""")
    for row in cursor2:
        alertas.append(
            f"¡SUBE DE CRITICIDAD! {row[0]} \nVeces registrado: {row[1]} \nCriticidad Promedio: {row[2]:.1f}/10")

    return alertas
# === FUNCIÓN PARA REGISTRAR EN LA BASE DE DATOS ===


def registrar_db():
    try:
        nombre = entries["Nombre del Residuo"].get().strip()
        tipo = entries["Tipo (Sólido/Líquido/Gas)"].get().strip()
        cantidad = float(entries["Cantidad"].get().strip())
        unidad = entries["Unidad (kg/litros/m3)"].get().strip()
        clase = entries["Clase (I/II/III/IV)"].get().strip()
        toxicidad = entries["Toxicidad (Baja/Media/Alta)"].get().strip()
        impacto = entries["Impacto Ambiental (Bajo/Medio/Alto)"].get().strip()

        if not all([nombre, tipo, cantidad, unidad, clase, toxicidad, impacto]):
            messagebox.showwarning(
                "Advertencia", "Por favor completa todos los campos.")
            return

        criticidad = calcular_criticidad(impacto, tipo, clase, toxicidad)
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn.execute('''
            INSERT INTO residuos (nombre, tipo, cantidad, unidad, clase, toxicidad, impacto, criticidad, fecha)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (nombre, tipo, cantidad, unidad,
              clase, toxicidad, impacto, criticidad, fecha))
        conn.commit()

        messagebox.showinfo(
            "Éxito", f"Residuo registrado con criticidad {criticidad}/10")
        for entry in entries.values():
            entry.delete(0, tk.END)

        cargar_historial()
    except ValueError:
        messagebox.showerror(
            "Error", "Cantidad debe ser un número válido.")


# === HISTORIAL DE LOS RESIDUOS ===
tree_frame = ctk.CTkFrame(tab_historial)
tree_frame.pack(pady=10, padx=20, fill="both", expand=True)

treeview = ttk.Treeview(
    tree_frame,
    columns=("id", "nombre", "tipo", "cantidad",
             "clase", "criticidad", "fecha"),
    show="headings",
    height=19
)
# Encabezados
for col, text in [
    ("id", "ID"),
    ("nombre", "Nombre del Residuo"),
    ("tipo", "Tipo"),
    ("cantidad", "Cantidad"),
    ("clase", "Clase"),
    ("criticidad", "Criticidad"),
    ("fecha", "Fecha de Registro")
]:
    treeview.heading(col, text=text)
# Anchos
treeview.column("id", width=50, anchor="center")
treeview.column("nombre", width=300, anchor="w")
treeview.column("tipo", width=100, anchor="center")
treeview.column("cantidad", width=120, anchor="center")
treeview.column("clase", width=80, anchor="center")
treeview.column("criticidad", width=100, anchor="center")
treeview.column("fecha", width=150, anchor="center")
treeview.pack(fill="both", expand=True, padx=20, pady=10)
# Conteo de críticos
label_criticos = ctk.CTkLabel(
    tab_historial, text="", font=("Arial", 18, "bold"))
label_criticos.pack(pady=10)

# === FUNCIÓN  PAPA CARGAR  EL HISTORIAL ===
tabview.pack(fill="both", expand=True, padx=20, pady=20)


def cargar_historial():
    if tabview.get() == "Historial":
        cargar_historial()


for item in treeview.get_children():
    treeview.delete(item)

   # Configurarcion de colores
treeview.tag_configure("rojo", foreground="#FF1744",
                       font=("Arial", 12, "bold"))
treeview.tag_configure("naranja", foreground="#FF6B00")
treeview.tag_configure("verde", foreground="#00C853")


# cargar datos desde la base de datos
cursor = conn.execute("""
    SELECT id, nombre, tipo, cantidad || ' ' || unidad, clase, criticidad, fecha
    FROM residuos
    ORDER BY fecha DESC
""")


criticos = 0

for row in cursor:
    criticidad = row[5]

    # Definir tag antes de su uso
    if criticidad >= 8:
        tag = "rojo"
        criticos += 1
    elif criticidad >= 5:
        tag = "naranja"
    else:
        tag = "verde"

    # Inserta el tag definido
    treeview.insert("", "end", values=row, tags=(tag,))

# Acuatializar los contadores en vivo
label_criticos.configure(
    text=f"RESIDUOS CRÍTICOS>8: {criticos}",
    text_color="#FF1744" if criticos > 0 else "#00C853",
)

# Alertas Predictivas Ambientales
alertas = alertas_predictiva_ambientales()
if alertas:
    mensaje = "IMPACTO AMBIENTAL CRITICO DETECTADO:\n\n" + "\n\n".join(alertas)
    messagebox.showwarning("ALERTAS PREDICTIVAS AMBIENTALES", mensaje)
    # Actualizar Estadisticas
    actualizar_estadisticas()

# === BOTÓN ACTUALIZAR ===
frame_hist_btn = ctk.CTkFrame(tab_historial)
frame_hist_btn.pack(pady=10, fill="x")


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

# === MATRIZ DE RIESGO AMBIENTAL ===


def mostrar_matriz():

    if hasattr(mostrar_matriz, "abierta") and mostrar_matriz.abierta:
        return  # Evitar abrir múltiples ventanas
    mostrar_matriz.abierta = True

    ventana_matriz = ctk.CTkToplevel(app)
    ventana_matriz.title(
        "Matriz de Riesgo Ambiental - Critissimoo D.S. 148/2003")
    ventana_matriz.geometry("800x600")
    ventana_matriz.configure(bg="#f0f0f0")

    # titulo
    ctk.CTkLabel(
        ventana_matriz,
        text="MATRIZ DE RIESGO AMBIENTAL\nSEGUN NORMATIVA LEGAL D.S. 148/2003",
        font=("Arial", 20, "bold"),
        text_color="#00C853"
    ).pack(pady=10)

    # Frame para la matriz
    frame_matriz = ctk.CTkFrame(ventana_matriz, fg_color="white")
    frame_matriz.pack(pady=20, padx=20, fill="both", expand=True)

    # Colores para la matriz
    colores = {
        1: "#00E676", 2: "#00E676", 3: "#00E676",
        4: "#FFEB3B", 5: "#FFEB3B", 6: "#FFEB3B",
        7: "#FF3D00", 8: "#FF3D00", 9: "#FF3D00", 10: "#FF3D00"
    }
    # DATOS DE LA MATRIZ
    filas = ["Improbable", "Posible", "Ocasiona",
             "Frecuente", "Casi Seguro", "Siempre"]
    columnas = ["Muy Bajo", "Bajo", "Moderado", "Alto", "Muy Alto", "Extremo"]

    # Encabezados filas
    for j, col in enumerate(columnas):
        ctk.CTkLabel(frame_matriz, text=col, font=("Arial", 12, "bold"), width=12,
                     fg_color="#404040", text_color="white").grid(row=0, column=j+1, padx=1, pady=1)

    # Encabezados filas
    for i,  fila in enumerate(filas):
        ctk.CTkLabel(frame_matriz, text=fila, font=("Arial", 12, "bold"), width=15,
                     fg_color="#404040", text_color="white").grid(row=i+1, column=0, padx=1, pady=1)

    # Colores Matriz Ambiemtal
    for i in range(6):
        for j in range(6):
            criticidad = i + j + 1
            color = colores[criticidad]
            text_color = "#000000" if criticidad <= 6 else "#FFFFFF"
            celda = ctk.CTkLabel(
                frame_matriz,
                text=str(criticidad),
                font=("Arial", 30, "bold"),
                width=140,
                height=8,
                fg_color=color,
                text_color=text_color,
                corner_radius=10,
            )
            celda.grid(row=i+1, column=j+1, padx=3, pady=5)

    def cerrar_ventana():
        mostrar_matriz.abierta = False
        ventana_matriz.destroy()

    ventana_matriz.protocol("WM_DELETE_WINDOW", cerrar_ventana)

# Estadisticas Simples que se acualizan solas a medida que se registran residuos}}


def actualizar_estadisticas():
    global label_stats

    total = conn.execute("SELECT COUNT(*) FROM residuos").fetchone()[0]
    criticos = conn.execute(
        "SELECT COUNT(*) FROM residuos WHERE criticidad >= 8").fetchone()[0]
    promedio_query = conn.execute(
        "SELECT AVG(criticidad) FROM residuos").fetchone()[0]
    promedio = round(promedio_query, 2) if promedio_query else 0.0

    stats_text = f"Total Residuos: {total}\nResiduos Críticos: {criticos}\nCriticidad Promedio: {promedio}/10"

    if label_stats is None:
        label_stats = ctk.CTkLabel(
            frame_est,
            text=stats_text,
            font=("Arial", 18, "bold"),
            text_color="#00C853",
            fg_color="#202020",
            corner_radius=10,
            padx=20,
            pady=20
        )
        label_stats.pack(expand=True, pady=85)
    else:
        label_stats.configure(text=stats_text)
        label_stats.configure(
            text_color="#FF1744" if criticos > 0 else "#00C853")


# === INICIAR LA APLICACIÓN ===
tabview.set("Registro")
cargar_historial()
actualizar_estadisticas()
# BOTON ABRIR MATRIZ DE RIESGO AMBIENTAL
ctk.CTkButton(
    frame_matriz,
    text="ABRIR MATRIZ DE RIESGO AMBIENTAL",
    command=lambda: mostrar_matriz(),
    font=("Arial", 20, "bold"),
    fg_color="#1dd1a1",
    hover_color="#10ac84",
    height=50,
    width=500,
    corner_radius=19,
).pack(expand=True, pady=200)

app.mainloop()
