# app/win_api.py
import os
import tkinter as tk
from tkinter import ttk, messagebox
from newsapi import NewsApiClient
import pandas as pd
import webbrowser

NEWS_API_KEY = os.getenv("NEWS_API_KEY", "d57e670f20204cf188acd22bec866b8e")

def open_win_api(root: tk.Tk):
    # Evitar ventanas duplicadas
    for w in root.winfo_children():
        if isinstance(w, tk.Toplevel) and w.title().startswith("Noticias"):
            w.lift()
            w.focus_force()
            return

    win = tk.Toplevel(root)
    win.title("Noticias en tiempo real (NewsAPI Demo)")
    win.geometry("720x560")
    win.minsize(680, 520)
    win.transient(root)
    win.grab_set()

    try:
        newsapi = NewsApiClient(api_key=NEWS_API_KEY)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo inicializar NewsAPI:\n{e}", parent=win)
        win.destroy()
        return

    container = ttk.Frame(win, padding=12)
    container.pack(fill="both", expand=True)

    lbl_title = ttk.Label(container, text="Consulta titulares de noticias", font=("Segoe UI", 14, "bold"))
    lbl_title.pack(pady=(0, 10))

    opts = ttk.Frame(container)
    opts.pack(fill="x", pady=(0, 8))

    ttk.Label(opts, text="Categoría:").grid(row=0, column=0, padx=6, pady=4, sticky="w")
    combo_categoria = ttk.Combobox(
        opts,
        values=["Business", "Technology", "Science", "Health", "Sports", "Entertainment", "General"],
        state="readonly", width=16
    )
    combo_categoria.current(0)
    combo_categoria.grid(row=0, column=1, padx=6, pady=4, sticky="w")

    ttk.Label(opts, text="País:").grid(row=0, column=2, padx=6, pady=4, sticky="w")
    combo_pais = ttk.Combobox(
        opts,
        values=["us", "mx", "gb", "ca", "br", "fr", "de", "in"],
        state="readonly", width=8
    )
    combo_pais.current(0)
    combo_pais.grid(row=0, column=3, padx=6, pady=4, sticky="w")

    btn_buscar = ttk.Button(container, text="Obtener titulares")
    btn_buscar.pack(pady=6)

    text_frame = ttk.Frame(container)
    text_frame.pack(fill="both", expand=True, pady=(6, 6))

    text_result = tk.Text(text_frame, wrap="word", height=20)
    text_result.pack(side="left", fill="both", expand=True)

    scroll_y = ttk.Scrollbar(text_frame, orient="vertical", command=text_result.yview)
    scroll_y.pack(side="right", fill="y")
    text_result.configure(yscrollcommand=scroll_y.set)

    lbl_footer = ttk.Label(container, text="Fuente: https://newsapi.org  |  Demo educativa", font=("Segoe UI", 8))
    lbl_footer.pack(side="bottom", pady=4)

    def pintar_articulos(articulos_df: pd.DataFrame):
        text_result.config(state="normal")
        text_result.delete("1.0", tk.END)
        text_result.tag_configure("titulo", font=("Segoe UI", 10, "bold"))
        text_result.tag_configure("link", underline=True)
        text_result.tag_bind("link", "<Button-1>", lambda e: click_enlace(e))
        text_result.tag_bind("link", "<Enter>", lambda e: text_result.config(cursor="hand2"))
        text_result.tag_bind("link", "<Leave>", lambda e: text_result.config(cursor=""))

        for _, art in articulos_df.iterrows():
            text_result.insert(tk.END, "📰 ", ())
            text_result.insert(tk.END, f"{art['Title']}\n", ("titulo",))
            text_result.insert(tk.END, f"   Fuente: {art['Source']} | Fecha: {art['Published']}\n", ())
            start = text_result.index(tk.INSERT)
            text_result.insert(tk.END, f"   Enlace: {art['URL']}\n\n", ("link",))
            end = text_result.index(tk.INSERT)
            text_result.tag_add(art['URL'], start, end)

        text_result.config(state="disabled")

    def click_enlace(event):
        index = text_result.index(f"@{event.x},{event.y}")
        tags = text_result.tag_names(index)
        for t in tags:
            if t.startswith("http://") or t.startswith("https://"):
                webbrowser.open(t)
                break

    def abrir_enlace_desde_seleccion():
        try:
            seleccion = text_result.get(tk.SEL_FIRST, tk.SEL_LAST)
            for palabra in seleccion.split():
                if palabra.startswith("http://") or palabra.startswith("https://"):
                    webbrowser.open(palabra)
                    return
            messagebox.showinfo("Aviso", "Selecciona una línea con enlace válido.", parent=win)
        except tk.TclError:
            messagebox.showinfo("Aviso", "Selecciona una URL.", parent=win)

    def obtener_noticias():
        try:
            categoria = combo_categoria.get().strip().lower()
            pais = combo_pais.get().strip().lower()

            top_headlines = newsapi.get_top_headlines(
                category=categoria,
                country=pais,
                language="en"
            )

            if top_headlines.get("status") == "ok" and top_headlines.get("totalResults", 0) > 0:
                articulos = pd.DataFrame([
                    {
                        "Title": art.get("title", "(sin título)") or "(sin título)",
                        "Source": (art.get("source") or {}).get("name", "N/D"),
                        "Published": art.get("publishedAt", "N/D"),
                        "URL": art.get("url", "")
                    }
                    for art in top_headlines.get("articles", [])
                    if art.get("url")
                ])
                if articulos.empty:
                    messagebox.showinfo("Sin resultados", "No se encontraron URLs válidas.", parent=win)
                else:
                    pintar_articulos(articulos)
            else:
                messagebox.showinfo("Sin resultados", "No hay titulares disponibles.", parent=win)
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al consultar la API:\n{e}", parent=win)

    btn_buscar.config(command=obtener_noticias)

    btn_enlace = ttk.Button(container, text="Abrir enlace seleccionado", command=abrir_enlace_desde_seleccion)
    btn_enlace.pack(pady=(0, 4))
