# buscar_img.py

# ------------------------------------------------------------------
# Importaciones de librerías y configuraciónes Globales
# ------------------------------------------------------------------
from typing import Iterable, Optional
import pyautogui
import time
import os


# ---------------------------------------------------------------------------
#    Busca imágenes en pantalla y hace clic en la primera coincidencia.
#
#    Args:
#        rutas_imagenes: rutas de las imágenes a buscar.
#        sensibilidad: nivel de coincidencia (0–1, por defecto 0.8).
#        timeout: tiempo máximo en segundos (por defecto 5).
#
#    Returns:
#        True si hizo clic en alguna imagen, False si no encontró ninguna.
# ---------------------------------------------------------------------------


#******************************************************************************
def buscar_y_click_en_set_imagenes( rutas_imagenes, sensibilidad, timeout ):
    
    rutas = list(rutas_imagenes or [])
    if not rutas:
        return False

    sensibilidad = max(0.0, min(1.0, float(sensibilidad)))
    timeout = max(0.0, float(timeout))

    w, h = pyautogui.size()
    pyautogui.moveTo(w / 2, h / 2, duration=0.1)

    inicio = time.time()

    while (time.time() - inicio) < timeout:
        for ruta_rel in rutas:
            ruta_img = os.path.abspath(ruta_rel)
            try:
                box: Optional[pyautogui.Box] = pyautogui.locateOnScreen(
                    ruta_img, confidence=sensibilidad
                )
            except Exception:
                box = None

            if box:
                centro = pyautogui.center(box)
                pyautogui.moveTo(centro.x, centro.y, duration=0.2)
                pyautogui.click()
                return True

        time.sleep(0.8)

    return False
