import tkinter as tk
from tkinter import ttk, messagebox
import re

from storage import load_users, save_users, hash_pw
from win_profile import open_win_profile
from session import set_user   # <— NUEVO

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def open_win_home(parent: tk.Tk):
    for w in parent.winfo_children():
        if isinstance(w, tk.Toplevel) and w.title() == "Inicio de sesión":
            w.deiconify(); w.lift(); w.focus_force()
            return

    win = tk.Toplevel(parent)
    win.title("Inicio de sesión")
    win.geometry("500x400")
    win.transient(parent)

    frm = ttk.Frame(win, padding=16); frm.pack(fill="both", expand=True)

    ttk.Label(frm, text="Bienvenid@, ya diste el primer paso hacia la vanguardia.",
              style="Title.TLabel").pack(anchor="w")
    ttk.Label(frm, text="Inicia sesión o crea tu perfil").pack(anchor="w", pady=(4, 12))

    container = ttk.Frame(frm); container.pack(fill="x")

    # ---------------- LOGIN ----------------
    login = ttk.Frame(container)
    ttk.Label(login, text="Correo:").grid(row=0, column=0, sticky="w", pady=4)
    ent_mail_l = ttk.Entry(login, width=32); ent_mail_l.grid(row=0, column=1, sticky="ew", pady=4)
    ttk.Label(login, text="Contraseña:").grid(row=1, column=0, sticky="w", pady=4)
    ent_pw_l = ttk.Entry(login, width=32, show="•"); ent_pw_l.grid(row=1, column=1, sticky="ew", pady=4)
    login.columnconfigure(1, weight=1)

    def do_login():
        mail = ent_mail_l.get().strip().lower()
        pw = ent_pw_l.get()
        if not EMAIL_RE.match(mail):
            messagebox.showwarning("Correo no válido", "Ingresa un correo válido."); return
        users = load_users()
        u = users.get(mail)
        if not u or u.get("password") != hash_pw(pw):
            messagebox.showerror("Acceso denegado", "Correo o contraseña incorrectos."); return
        set_user(mail)  # <— guarda usuario en sesión
        messagebox.showinfo("Bienvenido", f"Hola, {u.get('name','Usuario')} 👋")
        open_win_profile(parent, user_email=mail)
        win.destroy()

    ttk.Button(login, text="Iniciar sesión", style="Primary.TButton",
               command=do_login).grid(row=2, column=0, columnspan=2, sticky="ew", pady=(8,0))

    # --------------- REGISTRO ---------------
    register = ttk.Frame(container)
    ttk.Label(register, text="Nombre:").grid(row=0, column=0, sticky="w", pady=4)
    ent_name_r = ttk.Entry(register, width=32); ent_name_r.grid(row=0, column=1, sticky="ew", pady=4)
    ttk.Label(register, text="Correo:").grid(row=1, column=0, sticky="w", pady=4)
    ent_mail_r = ttk.Entry(register, width=32); ent_mail_r.grid(row=1, column=1, sticky="ew", pady=4)
    ttk.Label(register, text="Rol:").grid(row=2, column=0, sticky="w", pady=4)
    cmb_role_r = ttk.Combobox(register, values=["Estudiante", "Docente", "Admin"], state="readonly")
    cmb_role_r.grid(row=2, column=1, sticky="ew", pady=4); cmb_role_r.current(0)
    ttk.Label(register, text="Empresa:").grid(row=3, column=0, sticky="w", pady=4)
    ent_company_r = ttk.Entry(register, width=32); ent_company_r.grid(row=3, column=1, sticky="ew", pady=4)
    ttk.Label(register, text="Contraseña:").grid(row=4, column=0, sticky="w", pady=4)
    ent_pw_r = ttk.Entry(register, width=32, show="•"); ent_pw_r.grid(row=4, column=1, sticky="ew", pady=4)
    register.columnconfigure(1, weight=1)

    def do_register():
        name = ent_name_r.get().strip()
        mail = ent_mail_r.get().strip().lower()
        role = cmb_role_r.get()
        company = ent_company_r.get().strip()
        pw = ent_pw_r.get()
        if not name or not mail or not pw or not company:
            messagebox.showwarning("Campos faltantes", "Completa todos los datos, incluida la empresa."); return
        if not EMAIL_RE.match(mail):
            messagebox.showwarning("Correo no válido", "Ingresa un correo válido."); return
        users = load_users()
        if mail in users:
            messagebox.showerror("Ya existe", "Ese correo ya está registrado. Inicia sesión."); return

        users[mail] = {"name": name, "email": mail, "role": role, "company": company, "password": hash_pw(pw)}
        save_users(users)
        set_user(mail)  # <— guarda usuario en sesión
        messagebox.showinfo("¡Listo!", "Perfil creado correctamente.")
        open_win_profile(parent, user_email=mail)
        win.destroy()

    ttk.Button(register, text="Crear perfil", style="Primary.TButton",
               command=do_register).grid(row=5, column=0, columnspan=2, sticky="ew", pady=(8,0))

    # -------- Alternador --------
    btns = ttk.Frame(frm); btns.pack(fill="x", pady=(16,0))
    def show_login():
        register.pack_forget(); login.pack(fill="x")
    def show_register():
        login.pack_forget(); register.pack(fill="x")
    ttk.Button(btns, text="Ya tengo cuenta", command=show_login).pack(side="left", expand=True, fill="x", padx=(0,6))
    ttk.Button(btns, text="Soy nuevo/a", command=show_register).pack(side="left", expand=True, fill="x", padx=(6,0))
    show_login()
    ttk.Button(frm, text="Cerrar", command=win.destroy).pack(pady=12, fill="x")

