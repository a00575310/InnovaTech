import tkinter as tk
from tkinter import ttk

def open_win_table(root):
    """Ventana 'Contáctanos' con soporte real."""
    win = tk.Toplevel(root)
    win.title("Contáctanos")
    win.geometry("520x380")
    win.minsize(480, 360)

    frame = ttk.Frame(win, padding=20)
    frame.pack(fill="both", expand=True)

    # Título
    title = ttk.Label(frame, text="Contáctanos", style="Title.TLabel")
    title.configure(font=("Segoe UI", 16, "bold"))
    title.pack(pady=(0, 6))

    # Línea azul elegante
    tk.Frame(frame, bg="#3B82F6", height=3).pack(fill="x", padx=100, pady=(0, 20))

    # Texto guía
    ttk.Label(
        frame,
        text="Nuestro equipo está listo para apoyarte con tu seguimiento o cualquier duda las 24/7.",
        style="Hint.TLabel",
        justify="center"
    ).pack(pady=(0, 16))

    # ---- Contacto 1: Ing. Fabian Castellanos ----
    card1 = ttk.Frame(frame, padding=12)
    card1.pack(fill="x", pady=6)

    ttk.Label(card1, text="Ing. Fabian Castellanos", font=("Segoe UI", 11, "bold")).pack(anchor="w")
    ttk.Label(card1, text="Soporte Técnico").pack(anchor="w")
    ttk.Label(card1, text="📞 477 982 7051").pack(anchor="w")

    # ---- Contacto 2: Lic. Omar Salas ----
    card2 = ttk.Frame(frame, padding=12)
    card2.pack(fill="x", pady=6)

    ttk.Label(card2, text="Lic. Omar Salas", font=("Segoe UI", 11, "bold")).pack(anchor="w")
    ttk.Label(card2, text="Agente de Seguimiento Empresarial").pack(anchor="w")
    ttk.Label(card2, text="📞 479 124 6012").pack(anchor="w")

    # Botón cerrar
    ttk.Button(frame, text="Cerrar", command=win.destroy).pack(pady=20)
