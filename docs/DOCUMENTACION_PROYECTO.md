# Proyecto Integrador – MVP (Tkinter)

Este documento describe la arquitectura, módulos y funcionamiento del proyecto **GUI con Tkinter**. Incluye instrucciones de instalación/ejecución, explicación de cada ventana y notas para extender el código.

---

## 1) Visión general

La aplicación es un **MVP de escritorio** con Tkinter que demuestra:
- **Pantalla principal** con botones para abrir ventanas secundarias.
- **Ventana Home** (mensaje de bienvenida y `messagebox`).
- **Formulario** con validación y guardado a archivo de texto.
- **Lista (CRUD básico)** sobre un `Listbox`.
- **Tabla (Treeview)** que carga datos desde un CSV.
- **Canvas (dibujo)** con figuras de ejemplo.

Arquitectura modular por ventanas: cada ventana vive en un archivo `win_*.py` con una función `open_win_*` que recibe el `parent` (root) y crea un `Toplevel` independiente.

---

## 2) Estructura sugerida del proyecto

```
repo/
├─ data/
│  └─ sample.csv               # Datos de ejemplo para la tabla
├─ src/
│  └─ app/
│     ├─ main.py               # Ventana principal y navegación
│     ├─ win_home.py           # Ventana de bienvenida
│     ├─ win_form.py           # Formulario con validación y guardado
│     ├─ win_list.py           # Lista con CRUD básico
│     ├─ win_table.py          # Tabla (Treeview) que lee CSV
│     └─ win_canvas.py         # Canvas de dibujo
└─ .vscode/
   └─ launch.json              # Configuración de depuración en VS Code
```

> **Nota**: El `launch.json` define `PYTHONPATH=src` y ejecuta `src/app/main.py`. Si tus archivos están actualmente en otra ruta, reubícalos según el árbol anterior o ajusta la configuración.

---

## 3) Ejecución rápida

### Opción A: VS Code (recomendada)
1. Ubica los archivos en `src/app/` y el `launch.json` en `.vscode/`.
2. Asegúrate de tener Python 3.8+.
3. En VS Code presiona **Run and Debug** y elige **Programa con PYTHONPATH=src**.

### Opción B: Terminal
```bash
# Establecer PYTHONPATH para que 'app' sea un paquete importable
export PYTHONPATH="$(pwd)/src"
python src/app/main.py
```

---

## 4) Dependencias

- **Python estándar**: `tkinter`, `csv`, `pathlib`
- No se requieren librerías externas.

---

## 5) Módulos y funciones

### 5.1 `main.py`
- Crea la ventana raíz (`Tk`), define título/tamaño y un `Frame` principal.
- Muestra botones que abren cada ventana mediante `open_win_*`.
- Ejecuta `root.mainloop()` para iniciar el loop de eventos.

**Puntos clave**  
- Arquitectura simple: cada botón delega a un módulo independiente.  
- Usa `ttk` para estilos nativos (`Frame`, `Label`, `Button`, `Separator`).

### 5.2 `win_home.py`
- Abre `Toplevel` con título y tamaño.
- Muestra un saludo y un botón **“Mostrar mensaje”** que lanza `messagebox.showinfo`.
- Incluye botón **Cerrar**.

**Útil para**: pantallas de bienvenida, dashboards iniciales o mensajes de estado.

### 5.3 `win_form.py`
- Crea un formulario con campos **Nombre** (texto) y **Edad** (entero).
- Validación: nombre requerido, edad debe ser número entero.
- Botón **Guardar**: abre un diálogo `asksaveasfilename` y escribe un `.txt` con los datos.
- Botón **Cerrar**.

**Extensiones sugeridas**  
- Tipado y conversión de edad a `int`.  
- Más validaciones (rango de edad, formato).  
- Guardado en CSV/JSON/SQLite.

### 5.4 `win_list.py`
- `Listbox` con operaciones:
  - **Agregar**: inserta texto del `Entry` si no está vacío.
  - **Eliminar seleccionado**: borra el item activo.
  - **Limpiar**: elimina todos los items.
- Botón **Cerrar**.

**Patrones útiles**: manejo de selección con `curselection`, validación simple y feedback con `messagebox`.

### 5.5 `win_table.py`
- Crea un `Treeview` con columnas `nombre`, `valor1`, `valor2`.
- Calcula la ruta de `data/sample.csv` a partir del archivo actual (`parents[2]` → raíz del repo).
- Si el CSV no existe: `messagebox.showwarning` con instrucción para crearlo.
- Si existe: usa `csv.DictReader` y agrega cada fila al `Treeview`.

**Formato esperado del CSV**
```csv
nombre,valor1,valor2
Alice,10,20
Bob,5,7
...
```

**Sugerencias**
- Ajustar `stretch`, `anchor` y `width` para columnas.
- Encadenar ordenación por encabezado (bind de `<Button-1>` en el heading).

### 5.6 `win_canvas.py`
- Crea un `Canvas` donde dibuja:
  - Un rectángulo, un óvalo, una línea y un texto.
- Sirve de ejemplo de dibujo 2D básico.

**Extensiones**
- Manejo de eventos de mouse para dibujo libre.
- Exportar a imagen (via `PIL`/`pillow` si se desea).

---

## 6) Buenas prácticas aplicadas

- Separación por ventanas/módulos (`open_win_*`), lo que **reduce acoplamiento**.
- Uso de `ttk` para consistencia visual.
- Comprobaciones y **mensajes de error/aviso** en operaciones de E/S.
- `pathlib.Path` para rutas portables.

---

## 7) Roadmap de mejora (ideas)

1. **Paquetizar** como módulo (`src/app/__init__.py`) y usar `if __name__ == "__main__"` en `main.py` (ya presente).  
2. **Gestor de estados** (por ejemplo, un objeto `AppState`) compartido entre ventanas.  
3. **Persistencia** con SQLite para el CRUD.  
4. **Temas** (`ttkbootstrap` o estilos propios) para mejorar UI.  
5. **Tests** unitarios para lógica no-UI (validadores, carga CSV, etc.).  
6. **Accesibilidad**: atajos de teclado, foco, navegación por Tab.  
7. **Internacionalización** (i18n) si se requieren varios idiomas.

---

## 8) Snippets útiles

**Apertura de ventanas**  
```python
# En main.py
ttk.Button(frame, text="2) Formulario", command=lambda: open_win_form(root)).pack(pady=4, fill="x")
```

**Validación de edad**  
```python
if not edad_txt.isdigit():
    messagebox.showerror("Error", "La edad debe ser un número entero.")
    return
```

**Lectura de CSV**  
```python
with open(ruta, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        tv.insert("", "end", values=(row["nombre"], row["valor1"], row["valor2"]))
```

---

## 9) Troubleshooting

- **ImportError: No module named `app.*`**  
  Asegúrate de tener `PYTHONPATH=src` o ejecuta siempre con `python src/app/main.py` desde la raíz del repo.

- **No se encontró `data/sample.csv`**  
  Crea el archivo en `data/` con cabeceras `nombre,valor1,valor2`.

- **La UI no aparece**  
  Verifica que `mainloop()` se esté ejecutando y no haya excepciones en la consola.

---

## 10) Licencia y créditos

Este es un ejemplo educativo. Ajusta la licencia según tu necesidad.
