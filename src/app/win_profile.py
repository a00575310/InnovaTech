import tkinter as tk
from tkinter import ttk, messagebox

from storage import load_users, save_users

def open_win_profile(parent: tk.Tk, user_email: str = None):
    users = load_users()
    user = users.get(user_email, {}) if user_email else {}

    win = tk.Toplevel(parent)
    win.title("Perfil")
    win.geometry("520x380")
    win.transient(parent)

    frm = ttk.Frame(win, padding=16); frm.pack(fill="both", expand=True)
    ttk.Label(frm, text="Perfil de Usuario", style="Title.TLabel").pack(pady=(0, 12))

    form = ttk.Frame(frm); form.pack(fill="x", pady=6)

    ttk.Label(form, text="Nombre:").grid(row=0, column=0, sticky="w", pady=4)
    ent_name = ttk.Entry(form, width=36); ent_name.grid(row=0, column=1, sticky="ew", pady=4)

    ttk.Label(form, text="Correo:").grid(row=1, column=0, sticky="w", pady=4)
    ent_mail = ttk.Entry(form, width=36); ent_mail.grid(row=1, column=1, sticky="ew", pady=4)

    ttk.Label(form, text="Rol:").grid(row=2, column=0, sticky="w", pady=4)
    cmb_role = ttk.Combobox(form, values=["Estudiante", "Docente", "Admin"], state="readonly")
    cmb_role.grid(row=2, column=1, sticky="ew", pady=4)

    ttk.Label(form, text="Empresa:").grid(row=3, column=0, sticky="w", pady=4)
    ent_company = ttk.Entry(form, width=36); ent_company.grid(row=3, column=1, sticky="ew", pady=4)

    form.columnconfigure(1, weight=1)

    # Prefill
    ent_name.insert(0, user.get("name", ""))
    ent_mail.insert(0, user.get("email", ""))
    ent_company.insert(0, user.get("company", ""))
    if user.get("role") in ["Estudiante", "Docente", "Admin"]:
        cmb_role.set(user["role"])
    else:
        cmb_role.current(0)

    ttk.Separator(frm).pack(fill="x", pady=12)

    def save_profile():
        name = ent_name.get().strip()
        mail = ent_mail.get().strip().lower()
        role = cmb_role.get()
        company = ent_company.get().strip()

        if not name or not mail:
            messagebox.showwarning("Campos faltantes", "Nombre y correo son obligatorios.")
            return

        users = load_users()
        old_mail = user.get("email", mail)
        account = users.get(old_mail, {"password": user.get("password", "")})
        account.update({"name": name, "email": mail, "role": role, "company": company})

        if old_mail != mail:
            users.pop(old_mail, None)
        users[mail] = account

        save_users(users)
        messagebox.showinfo("Guardado", "Tu perfil fue actualizado.")

    btns = ttk.Frame(frm); btns.pack(fill="x")
    ttk.Button(btns, text="Guardar", style="Primary.TButton", command=save_profile).pack(side="left", padx=(0,8))
    ttk.Button(btns, text="Cerrar", command=win.destroy).pack(side="left")

