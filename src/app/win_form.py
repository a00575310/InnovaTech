# app/win_form.py
import tkinter as tk
from tkinter import ttk, messagebox
from app import profile_store as store

PRIMARY = "#3B82F6"

def open_win_form(root):
    win = tk.Toplevel(root)
    win.title("Conoce tu Empresa")
    win.geometry("720x640")
    win.minsize(680, 600)

    # ===== Contenedor principal =====
    wrapper = ttk.Frame(win, padding=24)
    wrapper.pack(fill="both", expand=True)

    # ---- Encabezado ----
    title = ttk.Label(wrapper, text="Conoce tu Empresa", style="Title.TLabel")
    title.configure(font=("Segoe UI", 20, "bold"))
    title.pack(pady=(0, 6))

    tk.Frame(wrapper, bg=PRIMARY, height=3).pack(fill="x", padx=120, pady=(0, 18))

    ttk.Label(
        wrapper,
        text="Completa tus datos y responde para evaluar el estado digital de tu negocio.",
        style="Hint.TLabel",
        justify="center"
    ).pack(pady=(0, 14))

    # ===== Scroll area =====
    scroll_container = ttk.Frame(wrapper)
    scroll_container.pack(fill="both", expand=True)

    canvas = tk.Canvas(scroll_container, highlightthickness=0)
    vsb = ttk.Scrollbar(scroll_container, orient="vertical", command=canvas.yview)
    inner = ttk.Frame(canvas, padding=0)

    inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=inner, anchor="nw")
    canvas.configure(yscrollcommand=vsb.set)

    canvas.pack(side="left", fill="both", expand=True)
    vsb.pack(side="right", fill="y")

    # ===== Helpers =====
    def card(title_text):
        c = ttk.Frame(inner, padding=14)
        c.pack(fill="x", pady=8)
        header = ttk.Label(c, text=title_text, font=("Segoe UI", 11, "bold"))
        header.pack(anchor="w", pady=(0, 8))
        ttk.Separator(c).pack(fill="x", pady=(0, 10))
        return c

    # ====== Sección: Perfil básico ======
    c_perfil = card("Perfil de la empresa")

    row_p1 = ttk.Frame(c_perfil); row_p1.pack(fill="x", pady=4)
    ttk.Label(row_p1, text="Nombre de la empresa:").pack(side="left")
    entry_nombre = ttk.Entry(row_p1)
    entry_nombre.pack(side="left", fill="x", expand=True, padx=(8, 0))

    row_p2 = ttk.Frame(c_perfil); row_p2.pack(fill="x", pady=4)
    ttk.Label(row_p2, text="Sector o giro:").pack(side="left")
    entry_sector = ttk.Entry(row_p2)
    entry_sector.pack(side="left", fill="x", expand=True, padx=(8, 0))

    row_p3 = ttk.Frame(c_perfil); row_p3.pack(fill="x", pady=4)
    ttk.Label(row_p3, text="Tiempo en operación (años):").pack(side="left")
    entry_tiempo = ttk.Entry(row_p3, width=10)
    entry_tiempo.pack(side="left", padx=(8, 0))

    # ===== Variables del cuestionario =====
    v_web = tk.StringVar(value="no")          # 1) Página web
    v_ecommerce = tk.StringVar(value="nunca") # 2) Vendes en línea
    v_rrss = tk.StringVar(value="nada")       # 3) Redes sociales
    v_sw = tk.StringVar(value="no")           # 4) Usa software
    v_sw_nombre = tk.StringVar(value="")      # 4b) ¿Cuál?
    v_alianzas = tk.StringVar(value="no")     # 5) Buscas alianzas

    # ===== 1) ¿Tu empresa tiene página web? =====
    c1 = card("1) ¿Tu empresa tiene página web?")
    row1 = ttk.Frame(c1); row1.pack(fill="x")
    ttk.Radiobutton(row1, text="Sí",  value="si", variable=v_web).pack(side="left", padx=(0, 12))
    ttk.Radiobutton(row1, text="No",  value="no", variable=v_web).pack(side="left")

    # ===== 2) ¿Vendes en línea? =====
    c2 = card("2) ¿Vendes en línea?")
    row2 = ttk.Frame(c2); row2.pack(fill="x")
    ttk.Radiobutton(row2, text="Nunca",   value="nunca",  variable=v_ecommerce).pack(side="left", padx=(0, 12))
    ttk.Radiobutton(row2, text="A veces", value="aveces", variable=v_ecommerce).pack(side="left", padx=(0, 12))
    ttk.Radiobutton(row2, text="Siempre", value="siempre",variable=v_ecommerce).pack(side="left")

    # ===== 3) ¿Usas redes sociales para marketing? =====
    c3 = card("3) ¿Usas redes sociales para marketing?")
    row3 = ttk.Frame(c3); row3.pack(fill="x")
    ttk.Radiobutton(row3, text="Nada", value="nada",  variable=v_rrss).pack(side="left", padx=(0, 12))
    ttk.Radiobutton(row3, text="Poco", value="poco",  variable=v_rrss).pack(side="left", padx=(0, 12))
    ttk.Radiobutton(row3, text="Mucho",value="mucho", variable=v_rrss).pack(side="left")

    # ===== 4) ¿Utilizas software de gestión? (+ ¿Cuál?) =====
    c4 = card("4) ¿Utilizas software de gestión?")
    row4 = ttk.Frame(c4); row4.pack(fill="x")
    def _enable_sw():
        sw_entry.configure(state="normal")
        if not v_sw_nombre.get().strip():
            sw_entry.delete(0, "end")
    def _disable_sw():
        v_sw_nombre.set("")
        sw_entry.configure(state="disabled")

    ttk.Radiobutton(row4, text="Sí", value="si", variable=v_sw, command=_enable_sw).pack(side="left", padx=(0, 12))
    ttk.Radiobutton(row4, text="No", value="no", variable=v_sw, command=_disable_sw).pack(side="left")

    sw_entry = ttk.Entry(c4, textvariable=v_sw_nombre, width=60, state="disabled")
    sw_entry.insert(0, "¿Cuál?")
    sw_entry.pack(fill="x", pady=(10, 0))

    # ===== 5) ¿Buscas alianzas? =====
    c5 = card("5) ¿Buscas alianzas?")
    row5 = ttk.Frame(c5); row5.pack(fill="x")
    ttk.Radiobutton(row5, text="Sí", value="si", variable=v_alianzas).pack(side="left", padx=(0, 12))
    ttk.Radiobutton(row5, text="No", value="no", variable=v_alianzas).pack(side="left")

    # ===== Puntaje visible (nuevo) =====
    score_frame = ttk.Frame(wrapper); score_frame.pack(fill="x", pady=(12, 0))
    lbl_score = ttk.Label(score_frame, text="Puntaje estimado: 0.0 / 9", font=("Segoe UI", 11, "bold"))
    lbl_score.pack(anchor="w")

    # ----- Cálculo del puntaje -----
    # Escala máxima = 9
    # web: si=2, no=0
    # ecommerce: nunca=0, aveces=2, siempre=3
    # rrss: nada=0, poco=1, mucho=2
    # software: si=1, no=0
    # alianzas: si=1, no=0
    def compute_score() -> float:
        score = 0.0
        score += 2.0 if v_web.get() == "si" else 0.0
        score += {"nunca": 0.0, "aveces": 2.0, "siempre": 3.0}.get(v_ecommerce.get(), 0.0)
        score += {"nada": 0.0, "poco": 1.0, "mucho": 2.0}.get(v_rrss.get(), 0.0)
        score += 1.0 if v_sw.get() == "si" else 0.0
        score += 1.0 if v_alianzas.get() == "si" else 0.0
        return round(score, 1)

    def refresh_score_label():
        lbl_score.configure(text=f"Puntaje estimado: {compute_score()} / 9")

    # Actualizar puntaje cuando cambian respuestas
    for var in (v_web, v_ecommerce, v_rrss, v_sw, v_alianzas):
        var.trace_add("write", lambda *_: refresh_score_label())

    # ===== Botonera =====
    btns = ttk.Frame(wrapper); btns.pack(fill="x", pady=(12, 0))

    def limpiar():
        entry_nombre.delete(0, "end")
        entry_sector.delete(0, "end")
        entry_tiempo.delete(0, "end")

        v_web.set("no")
        v_ecommerce.set("nunca")
        v_rrss.set("nada")
        v_sw.set("no")
        v_sw_nombre.set("")
        sw_entry.configure(state="disabled")

        refresh_score_label()
        messagebox.showinfo("Formulario", "Se limpió el formulario.")

    def guardar():
        # Perfil básico
        nombre = entry_nombre.get().strip()
        sector = entry_sector.get().strip()
        tiempo = entry_tiempo.get().strip()

        if nombre or sector or tiempo:
            store.update_profile_basic(nombre or None, sector or None, tiempo or None)

        # Cuestionario
        store.update_form_answers(
            web=v_web.get(),
            ecommerce=v_ecommerce.get(),
            rrss=v_rrss.get(),
            usa_software=v_sw.get(),
            software_nombre=v_sw_nombre.get().strip(),
            alianzas=v_alianzas.get()
        )

        # Mostrar puntaje al guardar
        messagebox.showinfo("Guardado",
                            f"¡Listo! Tus datos fueron guardados.\n\n"
                            f"Puntaje estimado: {compute_score()} / 9")

    ttk.Button(btns, text="Guardar", style="Primary.TButton", command=guardar).pack(side="left")
    ttk.Button(btns, text="Limpiar", command=limpiar).pack(side="left", padx=8)
    ttk.Button(btns, text="Volver", command=win.destroy).pack(side="right")

    # Inicializar puntaje en pantalla
    refresh_score_label()
