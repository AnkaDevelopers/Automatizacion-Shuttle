# Utils/mensaje_en_pantalla.py
def mensaje_en_pantalla(texto: str, segundos: int = 3, posicion: str = "top-right", cancelable: bool = False) -> bool:
    """
    Muestra un popup con cuenta regresiva y BLOQUEA la ejecución hasta que termine.
    - texto: mensaje a mostrar
    - segundos: duración (por defecto 10)
    - posicion: "top-right" | "center" | "top-center"
    - cancelable: si True, el usuario puede cerrarlo haciendo clic (termina antes)
    Retorna True si se mostró correctamente, False si hubo error.
    """
    try:
        import tkinter as tk

        if segundos <= 0:
            segundos = 1

        root = tk.Tk()
        root.overrideredirect(True)        # sin bordes
        root.attributes("-topmost", True)  # al frente
        root.configure(bg="#111")

        frame = tk.Frame(root, bg="#111", padx=16, pady=12)
        frame.pack()

        lbl_msg = tk.Label(frame, text=texto, fg="#eee", bg="#111")
        lbl_msg.pack(anchor="w")

        restante = tk.IntVar(value=segundos)
        lbl_count = tk.Label(frame, text=f"Se cierra en {segundos} s", fg="#aaa", bg="#111")
        lbl_count.pack(anchor="e", pady=(8, 0))

        # Posicionar
        root.update_idletasks()
        w, h = root.winfo_width(), root.winfo_height()
        sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
        pad = 20
        if posicion == "center":
            x, y = (sw - w) // 2, (sh - h) // 2
        elif posicion == "top-center":
            x, y = (sw - w) // 2, pad
        else:  # top-right
            x, y = sw - w - pad, pad
        root.geometry(f"{w}x{h}+{x}+{y}")

        # Cierre manual opcional
        if cancelable:
            root.bind("<Button-1>", lambda _e: root.destroy())

        # Cuenta regresiva
        def tick():
            v = restante.get() - 1
            if v <= 0:
                root.destroy()
                return
            restante.set(v)
            lbl_count.config(text=f"Se cierra en {v} s")
            root.after(1000, tick)

        root.after(1000, tick)
        root.mainloop()   # <- BLOQUEA hasta que se destruya la ventana
        return True

    except Exception:
        # Fallback a consola (también bloqueante)
        import sys, time
        try:
            for s in range(segundos, 0, -1):
                sys.stdout.write(f"\r{texto}  |  Se cierra en {s} s")
                sys.stdout.flush()
                time.sleep(1)
            sys.stdout.write("\r" + " " * (len(texto) + 24) + "\r")
            sys.stdout.flush()
            return True
        except Exception as e:
            print(f"[ERROR] No se pudo mostrar el mensaje: {e}")
            return False

