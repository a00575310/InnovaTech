import tkinter as tk
from tkinter import ttk, messagebox
from app import profile_store as store
from storage import load_users
from session import get_user

PRIMARY = "#3B82F6"

def open_user_view(root):
    win = tk.Toplevel(root)
    win.title("Mi perfil")
    win.geometry("720x560")
    win.minsize(680, 520)

    wrapper = ttk.Frame(win, padding=24)
    wrapper.pack(fill="both", expand=True)

    # Encabezado
    title = ttk.Label(wrapper, text="Mi perfil", style="Title.TLabel")
    title.configure(font=("Segoe UI", 20, "bold"))
    title.pack(pady=(0, 6))
    tk.Frame(wrapper, bg=PRIMARY, height=3).pack(fill="x", padx=120, pady=(0, 18))

    ttk.Label(wrapper,
              text="Consulta la información guardada de tu empresa.",
              style="Hint.TLabel",
              justify="center").pack(pady=(0, 14))

    # Área scrollable
    sc = ttk.Frame(wrapper); sc.pack(fill="both", expand=True)
    canvas = tk.Canvas(sc, highlightthickness=0)
    vsb = ttk.Scrollbar(sc, orient="vertical", command=canvas.yview)
    inner = ttk.Frame(canvas, padding=0)

    inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=inner, anchor="nw")
    canvas.configure(yscrollcommand=vsb.set)

    canvas.pack(side="left", fill="both", expand=True)
    vsb.pack(side="right", fill="y")

    def section(title_txt):
        card = ttk.Frame(inner, padding=14)
        card.pack(fill="x", pady=8)
        ttk.Label(card, text=title_txt, font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 8))
        ttk.Separator(card).pack(fill="x", pady=(0, 10))
        return card

    def render():
        # limpiar
        for w in inner.winfo_children():
            w.destroy()

        # Datos guardados en profile_store
        data = store.load()
        frm  = data.get("form", {})            # estado digital (win_form)
        plan = data.get("action_plan", {})     # plan de acción (win_list)

        # Datos de la cuenta (registro)
        user_email = get_user()
        users = load_users()
        account = users.get(user_email, {}) if user_email else {}
        nombre_cuenta  = account.get("name", "—")
        empresa_cuenta = account.get("company", "—")
        correo_cuenta  = user_email or "—"

        # Perfil básico (desde la cuenta)
        s1 = section("Perfil de la empresa")
        ttk.Label(s1, text=f"Nombre: {nombre_cuenta}").pack(anchor="w")
        ttk.Label(s1, text=f"Empresa: {empresa_cuenta}").pack(anchor="w")
        ttk.Label(s1, text=f"Correo: {correo_cuenta}").pack(anchor="w")

        # Estado digital (Conoce tu empresa)
        s2 = section("Estado digital (Conoce tu empresa)")
        ttk.Label(s2, text=f"Página web: {frm.get('web', '—')}").pack(anchor="w")
        ttk.Label(s2, text=f"Vendes en línea: {frm.get('ecommerce', '—')}").pack(anchor="w")
        ttk.Label(s2, text=f"Redes sociales para marketing: {frm.get('rrss', '—')}").pack(anchor="w")
        sw = frm.get("usa_software", "—"); sw_n = frm.get("software_nombre", "")
        ttk.Label(s2, text=f"Software de gestión: {sw}{f' ({sw_n})' if sw_n else ''}").pack(anchor="w")
        ttk.Label(s2, text=f"Buscas alianzas: {frm.get('alianzas', '—')}").pack(anchor="w")

        # Plan de acción
        s3 = section("Plan de acción")
        ttk.Label(s3, text=f"Puntaje: {plan.get('score', '—')}").pack(anchor="w")
        ttk.Label(s3, text=f"Nivel: {plan.get('level', '—')}").pack(anchor="w")
        tx = tk.Text(s3, height=8, wrap="word")
        tx.pack(fill="x", pady=(6, 0))
        tx.insert("1.0", plan.get("plan_text", "Aún no generas un plan."))
        tx.configure(state="disabled")

        # Metadatos
        if data.get("updated_at") or plan.get("updated_at"):
            s4 = section("Metadatos")
            if data.get("updated_at"):
                ttk.Label(s4, text=f"Última actualización (perfil): {data['updated_at']}").pack(anchor="w")
            if plan.get("updated_at"):
                ttk.Label(s4, text=f"Última actualización (plan): {plan['updated_at']}").pack(anchor="w")

    render()

    # Refrescar automáticamente al reabrir
    win.bind("<FocusIn>", lambda e: render())

    # Botonera
    btns = ttk.Frame(wrapper); btns.pack(fill="x", pady=(12, 0))

    def editar():
        try:
            from app.win_form import open_win_form
            open_win_form(root)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el formulario:\n{e}")

    ttk.Button(btns, text="Editar (abrir formulario)", style="Primary.TButton", command=editar).pack(side="left")
    ttk.Button(btns, text="Recargar", command=render).pack(side="left", padx=8)
    ttk.Button(btns, text="Cerrar", command=win.destroy).pack(side="right")

