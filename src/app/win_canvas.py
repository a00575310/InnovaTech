# app/win_canvas.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

PRIMARY = "#3B82F6"

def open_win_canvas(root):
    """Ventana de 'Instrucciones' con guía de uso de toda la app."""
    win = tk.Toplevel(root)
    win.title("Instrucciones de uso")
    win.geometry("760x560")
    win.minsize(700, 520)

    wrapper = ttk.Frame(win, padding=24)
    wrapper.pack(fill="both", expand=True)

    # Encabezado elegante
    title = ttk.Label(wrapper, text="Instrucciones de uso", style="Title.TLabel")
    title.configure(font=("Segoe UI", 20, "bold"))
    title.pack(pady=(0, 6))
    tk.Frame(wrapper, bg=PRIMARY, height=3).pack(fill="x", padx=120, pady=(0, 18))

    ttk.Label(
        wrapper,
        text="Aquí encontrarás una guía rápida para comprender cada ventana y cómo usar la plataforma.",
        style="Hint.TLabel",
        justify="center"
    ).pack(pady=(0, 14))

    # Área scrollable (para no mezclar pack y grid)
    sc = ttk.Frame(wrapper); sc.pack(fill="both", expand=True)
    canvas = tk.Canvas(sc, highlightthickness=0)
    vsb = ttk.Scrollbar(sc, orient="vertical", command=canvas.yview)
    inner = ttk.Frame(canvas, padding=0)
    inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=inner, anchor="nw")
    canvas.configure(yscrollcommand=vsb.set)
    canvas.pack(side="left", fill="both", expand=True)
    vsb.pack(side="right", fill="y")

    # Helper de sección tipo “tarjeta”
    def section(title_txt):
        card = ttk.Frame(inner, padding=14)
        card.pack(fill="x", pady=8)
        ttk.Label(card, text=title_txt, font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 8))
        ttk.Separator(card).pack(fill="x", pady=(0, 10))
        return card

    # ---------------- Secciones de ayuda ----------------
    # Inicio / Menú principal
    s0 = section("Inicio (menú principal)")
    ttk.Label(s0, text=(
        "Desde aquí accedes a todas las secciones. Recomendación de uso:\n"
        "1) Inicia sesión o regístrate\n"
        "2) Conoce más tu empresa\n"
        "3) Plan de acción\n"
        "4) Contáctanos\n"
        "5) Instrucciones (esta ventana)\n"
        "6) Mi perfil"
    )).pack(anchor="w")

    # 1) Home / Registro y acceso
    s1 = section("1) Inicia sesión o regístrate")
    ttk.Label(s1, text=(
        "• Crea tu cuenta con nombre, correo y empresa.\n"
        "• Si ya tienes cuenta, inicia sesión para que tus datos se asocien y se guarden correctamente.\n"
        "• La sesión activa permite mostrar tu Nombre, Empresa y Correo en 'Mi perfil'."
    )).pack(anchor="w")

    # 2) Conoce tu empresa (Formulario diagnóstico)
    s2 = section("2) Conoce más tu empresa")
    ttk.Label(s2, text=(
        "• Completa el formulario de diagnóstico y, si lo deseas, los datos básicos de la empresa.\n"
        "• Responde sobre presencia web, ventas en línea, redes sociales, uso de software y alianzas.\n"
        "• Al guardar, las respuestas se almacenan y se calcula un puntaje estimado (0 a 9) que verás en la parte superior."
    )).pack(anchor="w")

    # 3) Plan de acción
    s3 = section("3) Plan de acción")
    ttk.Label(s3, text=(
        "• Ingresa el puntaje (0 a 9) que obtuviste en el formulario.\n"
        "• Presiona 'Generar plan' para recibir recomendaciones claras y accionables según tu nivel.\n"
        "• Puedes guardar el plan como .txt o en tu historial.\n"
        "• Además, el plan se actualiza automáticamente en 'Mi perfil' (puntaje, nivel y detalle)."
    )).pack(anchor="w")

    # 4) Contáctanos
    s4 = section("4) Contáctanos")
    ttk.Label(s4, text=(
        "• Encuentra los contactos de soporte y seguimiento.\n"
        "• Ejemplo: Ing. Fabian Castellanos (Soporte Técnico) y Lic. Omar Salas (Seguimiento), con sus teléfonos.\n"
        "• Úsalo para resolver dudas técnicas o solicitar acompañamiento."
    )).pack(anchor="w")

    # 5) Instrucciones
    s5 = section("5) Instrucciones")
    ttk.Label(s5, text=(
        "• Es la guía general de uso de la plataforma.\n"
        "• Aquí se describe para qué sirve cada sección y el flujo recomendado."
    )).pack(anchor="w")

    # 6) Mi perfil
    s6 = section("6) Mi perfil")
    ttk.Label(s6, text=(
        "• Visualiza toda tu información consolidada:\n"
        "  - Nombre, Empresa y Correo (desde tu cuenta).\n"
        "  - Estado digital (respuestas guardadas en 'Conoce tu empresa').\n"
        "  - Plan de acción actual (puntaje, nivel y texto) generado en 'Plan de acción'.\n"
        "• La información se actualiza al volver a esta ventana o con el botón 'Recargar'."
    )).pack(anchor="w")

    # Sección: Buenas prácticas y tips
    tips = section("Buenas prácticas")
    ttk.Label(tips, text=(
        "• No mezcles 'pack' y 'grid' dentro del mismo contenedor (frame) para evitar errores de layout.\n"
        "• Mantén tu sesión iniciada para que los datos se guarden correctamente en tu perfil.\n"
        "• Si cambias información en el formulario, recuerda volver a generar el plan para actualizarlo en 'Mi perfil'.\n"
        "• Ante cualquier duda, utiliza la sección 'Contáctanos'."
    )).pack(anchor="w")

    # ---- Botonera inferior ----
    btns = ttk.Frame(wrapper)
    btns.pack(fill="x", pady=(12, 0))

    def export_txt():
        # Exportar el contenido de las instrucciones a .txt
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivo de texto", "*.txt")],
            title="Guardar instrucciones"
        )
        if not path:
            return
        try:
            # Recolectar texto de todas las secciones (simple)
            secciones = []
            for frame in inner.winfo_children():
                # Primer label (título) + resto de labels
                children = frame.winfo_children()
                title_lbls = [w for w in children if isinstance(w, ttk.Label)]
                # Construye una salida simple
                bloque = []
                for w in title_lbls:
                    # Obtener texto si existe 'cget'
                    try:
                        bloque.append(str(w.cget("text")))
                    except Exception:
                        pass
                if bloque:
                    secciones.append("\n".join(bloque))
            content = "\n\n".join(secciones)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("Instrucciones", "Instrucciones guardadas correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")

    ttk.Button(btns, text="Guardar instrucciones (.txt)", command=export_txt).pack(side="left")
    ttk.Button(btns, text="Cerrar", command=win.destroy).pack(side="right")
