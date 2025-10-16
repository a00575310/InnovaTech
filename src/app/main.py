import tkinter as tk
from tkinter import ttk

from app.win_home import open_win_home
from app.win_form import open_win_form
from app.win_list import open_win_list
from app.win_profile import open_win_profile
from app.win_canvas import open_win_canvas

def main():
    root = tk.Tk()
    root.title("Proyecto Integrador - MVP")
    root.geometry("480x460")
    root.minsize(460, 400)

    frame = ttk.Frame(root, padding=16)
    frame.pack(fill="both", expand=True)

    # Título principal
    ttk.Label(
        frame,
        text="InnovaTech",
        font=("Segoe UI", 20, "bold")
    ).pack(pady=(0, 4))

    # Línea azul decorativa
    separator = tk.Frame(frame, height=2, bg="#1E90FF")
    separator.pack(fill="x", pady=(0, 12))

    # Botones del menú
    ttk.Button(
        frame, text="1) Home / Bienvenida",
        command=lambda: open_win_home(root)
    ).pack(pady=4, fill="x")

    ttk.Button(
        frame, text="2) Conoce más tu empresa",
        command=lambda: open_win_form(root)
    ).pack(pady=4, fill="x")

    ttk.Button(
        frame, text="3) Plan de acción",
        command=lambda: open_win_list(root)
    ).pack(pady=4, fill="x")

    ttk.Button(
        frame, text="4) Mi perfil",
        command=lambda: open_win_profile(root)
    ).pack(pady=4, fill="x")

    ttk.Button(
        frame, text="5) Instrucciones",
        command=lambda: open_win_canvas(root)
    ).pack(pady=4, fill="x")

    root.mainloop()

if __name__ == "__main__":
    main()
