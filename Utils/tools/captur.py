from Monitor.log.log import agregar_log
# ------------------------------------------------------------------
# Importaciones globales y adicionales
# ------------------------------------------------------------------
import numpy as np
import pyautogui
import time
import os

CAPTURA_MEJOR_PATH = "pos.png"


def capturar_region_centrada(x: int, y: int, radio: int, ruta_salida: str) -> bool:
    """
    Captura una franja horizontal a TODO el ancho de la pantalla,
    centrada en y, con alto = 2*radio (clamp a pantalla).
    Limpia grilla/UI dejando solo trazas sobre negro y recorta SOLO en vertical.
    Guarda en 'ruta_salida' (sobrescribe si existe).
    """
    time.sleep(5)
    try:
        sw, sh = pyautogui.size()

        # --- Región: ancho completo, alto controlado por 'radio' ---
        left = 0
        width = sw
        top = max(0, y - radio)
        bottom = min(sh, y + radio)
        height = max(1, bottom - top)  # evitar 0

        # 1) Captura (PIL.Image)
        img = pyautogui.screenshot(region=(left, top, width, height))

        # 2) Limpieza por saturación/luminosidad
        SAT_MIN = 60
        VAL_MIN = 40
        hsv_np = np.array(img.convert("HSV"))
        s = hsv_np[:, :, 1]
        v = hsv_np[:, :, 2]
        mask = (s > SAT_MIN) & (v > VAL_MIN)

        rgb_np = np.array(img)
        rgb_np[~mask] = [0, 0, 0]  # fondo negro

        # 3) Recorte automático SOLO VERTICAL (mantener ancho completo)
        ys, xs = np.where(mask)
        if ys.size:
            PADDING_Y = 8
            y0 = max(0, ys.min() - PADDING_Y)
            y1 = min(rgb_np.shape[0], ys.max() + 1 + PADDING_Y)
            # mantener x completo (0 .. width)
            rgb_np = rgb_np[y0:y1, 0:rgb_np.shape[1]]

        # 4) Guardado (sobrescribe)
        dir_out = os.path.dirname(ruta_salida)
        if dir_out:
            os.makedirs(dir_out, exist_ok=True)
        Image = pyautogui._pyautogui_imports.Image  # PIL.Image
        Image.fromarray(rgb_np).save(ruta_salida)

        agregar_log(
            f"[CAPTURA] Guardada captura limpia en {ruta_salida} "
            f"(full_width={sw}, top={top}, height={height})"
        )
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
