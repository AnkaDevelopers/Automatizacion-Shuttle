from Monitor.log.log import agregar_log
# ------------------------------------------------------------------
# Importaciones globales y adicionales
# ------------------------------------------------------------------
import numpy as np  # <-- añadido para limpiar la captura
import pyautogui
import time
import os  # <-- añadido



# Ruta del archivo donde se guardará SIEMPRE la mejor captura (se sobreescribe)
CAPTURA_MEJOR_PATH = "pos.png"  # <-- añadido


def capturar_region_centrada(x: int, y: int, radio: int, ruta_salida:str) -> bool:
    
    """
    Captura una región centrada en (x,y) con 'radio' px (cuadrado 2*radio),
    limpia grilla/UI dejando solo trazas sobre negro, recorta al contenido
    y guarda en 'ruta_salida' sobrescribiendo si existe.
    """
    
    time.sleep(5)
    try:
        sw, sh = pyautogui.size()
        left = max(0, x - radio)
        top = max(0, y - radio)
        width = min(2 * radio, sw - left)
        height = min(2 * radio, sh - top)

        # 1) Captura
        img = pyautogui.screenshot(region=(left, top, width, height))  # PIL.Image

        # 2) Limpieza por saturación/luminosidad (elimina grises de grilla y UI)
        SAT_MIN = 60  # súbelo si aún ves grilla tenue
        VAL_MIN = 40
        hsv_np = np.array(img.convert("HSV"))
        s = hsv_np[:, :, 1]
        v = hsv_np[:, :, 2]
        mask = (s > SAT_MIN) & (v > VAL_MIN)

        rgb_np = np.array(img)
        rgb_np[~mask] = [0, 0, 0]  # fondo negro

        # 3) Recorte automático al contenido detectado
        ys, xs = np.where(mask)
        if ys.size and xs.size:
            PADDING = 8
            y0 = max(0, ys.min() - PADDING)
            y1 = min(rgb_np.shape[0], ys.max() + 1 + PADDING)
            x0 = max(0, xs.min() - PADDING)
            x1 = min(rgb_np.shape[1], xs.max() + 1 + PADDING)
            rgb_np = rgb_np[y0:y1, x0:x1]

        # 4) Guardado (sobrescribe). Reutiliza PIL desde pyautogui para no añadir imports.
        dir_out = os.path.dirname(ruta_salida)
        if dir_out:
            os.makedirs(dir_out, exist_ok=True)
        Image = pyautogui._pyautogui_imports.Image  # PIL.Image
        Image.fromarray(rgb_np).save(ruta_salida)

        agregar_log(f"[CAPTURA] Guardada captura limpia en {ruta_salida} (left={left}, top={top}, w={width}, h={height})")
        return True

    except Exception as e:
        # Fallback: si algo falla, guarda la captura original sin limpiar
        try:
            if 'img' in locals():
                dir_out = os.path.dirname(ruta_salida)
                if dir_out:
                    os.makedirs(dir_out, exist_ok=True)
                img.save(ruta_salida)
                agregar_log(f"[CAPTURA-FALLBACK] Guardada captura sin limpiar por error: {e}")
                return True
        except Exception as e2:
            agregar_log(f"[CAPTURA-ERROR] No se pudo guardar captura: {e2}")
        return False
