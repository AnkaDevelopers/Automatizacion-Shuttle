# capturarRuta.py
from tkinter import filedialog, messagebox
from pathlib import Path
import tkinter as tk
import re

#*****************************************************************************************
def seleccionar_y_guardar_ruta_proyecto(config_file="config.py", var_name="rutaProyecto"):
    """
    Abre una mini-UI para elegir una carpeta y guarda su ruta en config_file
    reemplazando el valor de la variable var_name.
    Retorna:
      - True  -> si se guardó correctamente
      - None  -> si no se guardó (cancelación/errores)
    """

    resultado = {"ok": None}  # bandera para devolver al final

    def _seleccionar_carpeta():
        carpeta = filedialog.askdirectory()
        if carpeta:
            ruta_var.set(carpeta)

    def _guardar_ruta():
        nueva_ruta = ruta_var.get()
        if not nueva_ruta:
            messagebox.showerror("Error", "No se ha seleccionado ninguna carpeta.")
            return None

        ruta_path = Path(nueva_ruta)
        if not ruta_path.exists() or not ruta_path.is_dir():
            messagebox.showerror("Error", "La ruta seleccionada no es válida.")
            return None

        # Leer config
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                contenido = f.read()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer {config_file}.\n{e}")
            return None

        try:
            # Patron: var = "lo_que_sea" (respeta espacios y comillas)
            patron = rf'(^\s*{re.escape(var_name)}\s*=\s*)(["\'])(.*?)\2'
            # Escapar backslashes para Windows
            ruta_escapada = nueva_ruta.replace("\\", "\\\\")

            if re.search(patron, contenido, flags=re.MULTILINE):
                nuevo_contenido = re.sub(
                    patron,
                    rf'\1"{ruta_escapada}"',
                    contenido,
                    count=1,
                    flags=re.MULTILINE,
                )
            else:
                # Si no existe la variable, la agregamos
                nuevo_contenido = contenido.rstrip() + f'\n{var_name} = "{ruta_escapada}"\n'

            with open(config_file, "w", encoding="utf-8") as f:
                f.write(nuevo_contenido)

            messagebox.showinfo("Éxito", f'Se guardó {var_name} en {config_file}')
            resultado["ok"] = True
            # Cerrar UI para poder retornar
            ventana.quit()
            ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar la ruta.\n{e}")

    # --- UI ---
    ventana = tk.Tk()
    ventana.title("Seleccionar ruta del proyecto")
    ventana.geometry("520x160")

    ruta_var = tk.StringVar()

    tk.Label(ventana, text="Ruta seleccionada:").pack(pady=5)
    tk.Entry(ventana, textvariable=ruta_var, width=62).pack(pady=5)
    tk.Button(ventana, text="Seleccionar carpeta", command=_seleccionar_carpeta).pack(pady=5)
    tk.Button(ventana, text="Guardar en config.py", command=_guardar_ruta).pack(pady=5)

    ventana.mainloop()
    return True if resultado["ok"] else None
