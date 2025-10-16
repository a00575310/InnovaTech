import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import date
import os, json

from storage import load_users
from session import get_user
from app import profile_store as store   # Para Mi perfil

PRIMARY = "#3B82F6"
PLAN_PATH = os.path.join(os.path.dirname(__file__), "action_plans.json")

# ---------- persistencia por usuario (historial local) ----------
def _ensure_file():
    if not os.path.exists(PLAN_PATH):
        with open(PLAN_PATH, "w", encoding="utf-8") as f:
            json.dump({"plans_by_user": {}}, f, ensure_ascii=False, indent=2)

def _read_all():
    _ensure_file()
    with open(PLAN_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def load_user_plans(email: str):
    data = _read_all()
    return data.get("plans_by_user", {}).get(email, [])

def save_user_plan(email: str, plan_text: str, score: float | None):
    data = _read_all()
    pb = data.setdefault("plans_by_user", {})
    lst = pb.setdefault(email, [])
    lst.append({"date": date.today().isoformat(), "score": score, "text": plan_text})
    with open(PLAN_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ---------- helpers de negocio ----------
def plan_level(score: float) -> str:
    if 0 <= score <= 2:   return "0-2"
    if 2 < score <= 5:    return "2-5"
    if 5 < score <= 7:    return "5-7"
    if 7 < score <= 9:    return "7-9"
    return "N/A"

def plan_text(score: float) -> str:
    s = score
    fecha = date.today().isoformat()

    if 0 <= s <= 2:
        return f"""Fecha: {fecha}

Tu empresa necesita construir pilares esenciales. Plan enfocado en fundamentos:

1) Presencia digital básica
• Si no tienes web: landing de 1 página (servicios, WhatsApp, ubicación).
• Google Business Profile y perfil social mínimo.
KPI: sitio y perfil activos en 7 días; 100% datos verificados.

2) Ventas en línea
• Habilitar canal simple: link de pago o catálogo básico.
• Definir oferta mínima y tiempos de respuesta estándar.
KPI: respuesta < 15 min; 100% pedidos registrados.

3) Redes sociales
• Empezar con 1 red clave: 3 posts/semana + 1 campaña chica.
• Publicar prueba social (testimonios/casos).
KPI: 12 publicaciones/mes, 1 campaña activa.

4) Software de gestión
• Registro simple de caja/ventas/compras (hoja o app ligera).
• 3 SOP en 1 página (ventas, compras, cobranza).
KPI: cierre de caja diario; 3 SOP publicados.

5) Alianzas
• 3 posibles aliados para referidos cruzados con beneficio simple.
KPI: 3 alianzas activas en 30 días.

Hitos 7–30 días
• Día 7: landing + Google Business + caja diaria.
• Día 14: 3 SOP + embudo simple (leads→ventas).
• Día 30: 3 alianzas activas + primer reporte mensual.
"""

    if 2 < s <= 5:
        return f"""Fecha: {fecha}

Ya hay movimiento; toca estandarizar y controlar:

1) Página web
• Propuesta de valor clara, CTA y formulario conectado a CRM ligero.
KPI: conversión visita→lead > 2%.

2) Ventas en línea
• Catálogo/precios formales y tablero semanal de oportunidades.
• Pagos integrados y confirmaciones automáticas.
KPI: % oportunidades con próxima acción ≥ 90%.

3) Redes sociales
• Calendario mensual (orgánico + pauta). 2 creatividades × 2 audiencias.
KPI: ROAS objetivo; CPL dentro de meta.

4) Software de gestión
• 3 SOP críticos con métricas (tiempo, calidad, cumplimiento).
• Tablero básico: ventas, margen, conversión, ticket promedio; cierre mensual.
KPI: tablero semanal; P&L mensual.

5) Alianzas
• Programa de referidos con UTM/códigos.
KPI: 15% de ventas nuevas por aliados en 60 días.

Hitos 30–60 días
• Semana 2: CRM funcionando + formularios web.
• Día 30: tablero KPIs y 3 SOP medidos.
• Día 60: campañas escaladas y referidos midiendo.
"""

    if 5 < s <= 7:
        return f"""Fecha: {fecha}

El sistema funciona; toca escalar con eficiencia:

1) Web / datos
• Analítica (GA4/Pixel) y pruebas A/B en páginas clave.
KPI: +20% conversión neta en 60 días.

2) Ventas en línea
• Automatizaciones (carrito abandonado, postventa).
KPI: recuperación ≥ 8%; repetición ≥ 15%.

3) Redes sociales
• Contenido por etapas de embudo (TOFU/MOFU/BOFU) + UGC.
KPI: CAC estable/a la baja; +frecuencia de compra.

4) Gestión
• Reporte financiero automatizado (P&L, flujo) + OKRs quincenales.
KPI: cierre a día 5; 80% KRs on track.

5) Alianzas
• Co-marketing con marcas de mayor alcance; paquetes conjuntos.
KPI: 2 campañas co-brandeadas/mes.

Hitos 30–90 días
• Mes 1: OKRs + reportería automática.
• Mes 2: automatizaciones de venta/retención.
• Mes 3: expansión por alianzas y eficiencia en CAC.
"""

    if 7 < s <= 9:
        return f"""Fecha: {fecha}

Vamos por optimización y profesionalización:

1) Performance y experimentación
• Cuadro de mando integral + ritmo de experimentos continuo.
KPI: ≥4 experimentos/mes con uplift neto.

2) Ecommerce / pricing
• LTV modelado; bundles/suscripciones; pricing dinámico.
KPI: LTV/CAC ≥ 3; payback < 3 meses.

3) Marca y canales
• UGC/creators/PR; ampliar canales (SEO, YouTube, partners).
KPI: % tráfico no pago creciente; share of voice.

4) Gestión/tecnología
• Auditoría Lean; gobierno de datos; BI confiable.
KPI: SLA de datos; incidentes críticos = 0.

5) Gobierno y expansión
• Comité asesor, minutas y accountability; pilotos en nuevos mercados.
KPI: cumplimiento de roadmap trimestral ≥ 85%.
"""

    return "Ingresá un valor entre 0 y 9 para generar tu plan de acción."

# ---------- ventana ----------
def open_win_list(parent: tk.Tk):
    win = tk.Toplevel(parent)
    win.title("Plan de acción según puntaje")
    win.geometry("900x580")
    win.transient(parent)

    # usuario actual (si hay)
    user_email = get_user()
    users = load_users()
    user = users.get(user_email, {}) if user_email else {}
    header_suffix = f" — {user.get('name','')} ({user.get('company','')})" if user else ""

    frm = ttk.Frame(win, padding=16)
    frm.pack(fill="both", expand=True)

    # Título elegante + línea azul
    title_lbl = ttk.Label(frm, text=f"Plan de acción{header_suffix}", style="Title.TLabel")
    title_lbl.configure(font=("Segoe UI", 20, "bold"))
    title_lbl.pack(anchor="w", pady=(0, 6))
    tk.Frame(frm, bg=PRIMARY, height=3).pack(fill="x", padx=120, pady=(0, 14))

    ttk.Label(
        frm,
        text="Bienvenid@, ya diste el primer paso hacia la vanguardia.\n"
             "Ingresá tu puntaje de «Conoce tu empresa» para generarte un plan de acción claro y accionable."
    ).pack(anchor="w", pady=(0, 12))

    # Entrada de puntaje
    top = ttk.Frame(frm); top.pack(fill="x", pady=(0, 8))
    ttk.Label(top, text="Puntaje (0–9):").pack(side="left")
    score_var = tk.DoubleVar()
    ttk.Spinbox(top, from_=0.0, to=9.0, increment=0.1, width=6, textvariable=score_var).pack(side="left", padx=(6,10))
    ttk.Button(top, text="Generar plan", style="Primary.TButton", command=lambda: generate()).pack(side="left")
    ttk.Button(top, text="Guardar como .txt", command=lambda: save_text()).pack(side="left", padx=8)
    ttk.Button(top, text="Guardar en historial", command=lambda: save_history()).pack(side="left", padx=8)

    # Contenedor de salida (el texto aparece solo después de generar)
    out_wrap = ttk.Frame(frm); out_wrap.pack(fill="both", expand=True, pady=(8,0))
    out_label = ttk.Label(out_wrap, text="Plan de acción generado:", font=("Segoe UI", 11, "bold"))
    out_text = tk.Text(out_wrap, wrap="word", height=22)
    out_scr = ttk.Scrollbar(out_wrap, orient="vertical", command=out_text.yview)
    out_text.configure(yscrollcommand=out_scr.set, state="disabled")

    # utilidades de salida
    def _ensure_output():
        if not out_label.winfo_ismapped():
            out_label.pack(anchor="w", pady=(0, 6))
        if not out_text.winfo_ismapped():
            out_text.pack(side="left", fill="both", expand=True)
            out_scr.pack(side="right", fill="y")

    def set_text(content: str):
        _ensure_output()
        out_text.configure(state="normal")
        out_text.delete("1.0", "end")
        if content:
            out_text.insert("1.0", content)
        out_text.configure(state="disabled")

    def get_text() -> str:
        return out_text.get("1.0", "end").strip()

    def save_text():
        content = get_text()
        if not content:
            messagebox.showinfo("Guardar", "Generá un plan antes de guardar."); return
        path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Texto","*.txt")],
                                            title="Guardar plan de acción")
        if not path: return
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        messagebox.showinfo("Guardado", "Archivo guardado con éxito.")

    def save_history():
        if not user_email:
            messagebox.showwarning("Sin sesión", "Iniciá sesión para guardar tu plan en tu historial."); return
        content = get_text()
        if not content:
            messagebox.showinfo("Guardar", "Generá un plan antes de guardar."); return
        try:
            s = float(score_var.get())
        except Exception:
            s = None
        save_user_plan(user_email, content, s)
        messagebox.showinfo("Guardado", "Plan guardado en tu historial.")

    # ===============  GENERADOR FINAL CON PROFILE_STORE  ===============
    def generate():
        try:
            s = float(score_var.get())
        except Exception:
            messagebox.showwarning("Puntaje inválido", "Ingresá un número entre 0 y 9."); return
        if not (0 <= s <= 9):
            messagebox.showwarning("Puntaje inválido", "Ingresá un número entre 0 y 9."); return

        text = plan_text(s)
        set_text(text)

        # ---- Guardar en profile_store (Mi perfil) ----
        try:
            lvl = plan_level(s)
            store.update_action_plan(score=s, level=lvl, plan_text=text)
            messagebox.showinfo("Plan guardado", "Tu plan se actualizó en 'Mi perfil'.")
        except Exception as e:
            print("No se pudo actualizar el plan en profile_store:", e)

    # Al abrir: sin salida visible hasta que generen
    # (No llamamos a _ensure_output aquí a propósito)
