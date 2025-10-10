# esperar_cambio_region.py
# -----------------------------------------------------------------------------
# Importaciones de librerías y configuraciones globales
# -----------------------------------------------------------------------------
import os
import time
from typing import Tuple, Optional

import numpy as np
import pyautogui
from PIL import ImageChops, ImageDraw

from Monitor.log.log import agregar_log


# -----------------------------------------------------------------------------
# Descripción general del módulo
# -----------------------------------------------------------------------------
# Este módulo monitorea cambios visuales en una región de la pantalla centrada
# en una posición del mouse. Toma capturas periódicas y calcula la diferencia
# entre imágenes para determinar si hubo cambios significativos.
#
# Qué hace:
# 1) Define una región cuadrada alrededor de `mouse_pos` acotada a la pantalla.
# 2) Toma una captura base (baseline) y luego compara capturas sucesivas.
# 3) Si el porcentaje de píxeles distintos supera `umbral` antes de `timeout`,
#    devuelve True; si no, devuelve False.
# 4) Opcionalmente guarda capturas y “overlays” de la región y del estado.
#
# Parámetros clave:
# - mouse_pos (Tuple[int, int]): posición (x, y) para centrar la región.
# - radio (int): semitamaño de la región (ancho/alto finales = radio * 2).
# - timeout (int): segundos máximos de espera antes de abortar.
# - intervalo (float): segundos entre comparaciones.
# - umbral (float): fracción mínima de píxeles distintos para considerar cambio.
# - warmup (float): pausa inicial para estabilizar la UI.
# - debug_dir (str|None): carpeta para guardar evidencia (capturas).
# - guardar_overlay (bool): si True, guarda pantallazos completos con la región
#   marcada en rojo.
# - mantener_solo_ultimos (bool): si True, limpia imágenes previas en cada run.
#
# Retornos:
# - bool: True si se detecta cambio antes del timeout; False si no hay cambios.
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
# Utilidades de archivos e imágenes
# -----------------------------------------------------------------------------
def _asegurar_directorio(ruta: str) -> str:
    """Crea (si no existe) y devuelve la ruta del directorio."""
    os.makedirs(ruta, exist_ok=True)
    return ruta


def _limpiar_imagenes_previas(directorio_debug: str) -> None:
    """
    Elimina las imágenes generadas previamente para conservar solo
    las últimas capturas en cada ejecución.
    """
    nombres = [
        "base_region.png",
        "base_overlay.png",
        "cambio_region.png",
        "cambio_diff.png",
        "cambio_overlay.png",
        "timeout_region.png",
        "timeout_overlay.png",
    ]
    for nombre in nombres:
        ruta = os.path.join(directorio_debug, nombre)
        try:
            if os.path.exists(ruta):
                os.remove(ruta)
        except Exception as e:
            agregar_log(f"[DEBUG] No se pudo eliminar {ruta}: {e}")


def _guardar_overlay(region: Tuple[int, int, int, int], ruta_salida: str) -> None:
    """
    Guarda una captura de pantalla completa con la región de interés
    dibujada como un rectángulo rojo.
    """
    try:
        full = pyautogui.screenshot()
        draw = ImageDraw.Draw(full)
        rx, ry, rw, rh = region
        draw.rectangle([rx, ry, rx + rw, ry + rh], outline="red", width=3)
        full.save(ruta_salida)
    except Exception as e:
        agregar_log(f"[DEBUG] No se pudo guardar overlay: {e}")


# -----------------------------------------------------------------------------
# Función principal (NO cambiar el nombre)
# -----------------------------------------------------------------------------
def esperar_cambio_region(
    mouse_pos: Tuple[int, int],
    radio: int = 200,
    timeout: int = 600,
    intervalo: float = 1.0,
    umbral: float = 0.02,
    warmup: float = 5.0,
    debug_dir: Optional[str] = "./debug_monitoreo",
    guardar_overlay: bool = False,
    mantener_solo_ultimos: bool = True,
) -> bool:
    """
    Espera cambios visuales en una región centrada en 'mouse_pos'.

    Guarda capturas con nombres cortos en español y, si se solicita,
    overlays de pantalla completa resaltando la región.

    Retorna:
        True  -> si detecta cambio (ratio > umbral) antes de 'timeout'.
        False -> si no hubo cambios visibles dentro del tiempo límite.
    """
    # -------------------------------------------------------------------------
    # 1) Calcular región de interés (ROI) acotada a la pantalla
    # -------------------------------------------------------------------------
    screen_w, screen_h = pyautogui.size()
    x, y = mouse_pos

    rx = max(0, x - radio)
    ry = max(0, y - radio)
    rw = max(1, min(screen_w - rx, radio * 2))
    rh = max(1, min(screen_h - ry, radio * 2))
    region = (rx, ry, rw, rh)

    # -------------------------------------------------------------------------
    # 2) Preparar carpeta de depuración
    # -------------------------------------------------------------------------
    if debug_dir:
        debug_dir = _asegurar_directorio(debug_dir)
        if mantener_solo_ultimos:
            _limpiar_imagenes_previas(debug_dir)

    agregar_log(f"[INFO] Monitoreando cambios en región={region} por hasta {timeout}s...")

    # -------------------------------------------------------------------------
    # 3) Pausa inicial para estabilizar la interfaz
    # -------------------------------------------------------------------------
    if warmup and warmup > 0:
        time.sleep(warmup)

    t0 = time.time()

    # -------------------------------------------------------------------------
    # 4) Captura base (baseline)
    # -------------------------------------------------------------------------
    img_prev = pyautogui.screenshot(region=region)
    if debug_dir:
        ruta_base = os.path.join(debug_dir, "base_region.png")
        try:
            img_prev.save(ruta_base)
            agregar_log(f"[DEBUG] Baseline guardada: {ruta_base}")
            if guardar_overlay:
                _guardar_overlay(region, os.path.join(debug_dir, "base_overlay.png"))
        except Exception as e:
            agregar_log(f"[DEBUG] No se pudo guardar baseline: {e}")

    # -------------------------------------------------------------------------
    # 5) Vigilancia periódica hasta timeout
    # -------------------------------------------------------------------------
    while time.time() - t0 < timeout:
        time.sleep(intervalo)

        # Captura actual
        img_new = pyautogui.screenshot(region=region)

        # Diferencia entre imágenes
        diff = ImageChops.difference(img_prev, img_new)
        arr = np.array(diff)
        nonzero = np.count_nonzero(arr)
        total = arr.size
        ratio = nonzero / total

        # agregar_log(f"[DEBUG] Diferencia: {ratio:.4f}")

        # ¿Cambio significativo?
        if ratio > umbral:
            agregar_log(f"[SUCCESS] Cambio detectado (ratio={ratio:.4f}).")
            if debug_dir:
                try:
                    img_new.save(os.path.join(debug_dir, "cambio_region.png"))
                    diff.save(os.path.join(debug_dir, "cambio_diff.png"))
                    if guardar_overlay:
                        _guardar_overlay(region, os.path.join(debug_dir, "cambio_overlay.png"))
                except Exception as e:
                    agregar_log(f"[DEBUG] No se pudo guardar imágenes de cambio: {e}")
            return True

        # Actualizar baseline para la siguiente comparación
        img_prev = img_new

    # -------------------------------------------------------------------------
    # 6) Timeout: no se detectaron cambios
    # -------------------------------------------------------------------------
    agregar_log("[ERROR] Timeout: no hubo cambios visibles.")
    if debug_dir:
        try:
            img_prev.save(os.path.join(debug_dir, "timeout_region.png"))
            if guardar_overlay:
                _guardar_overlay(region, os.path.join(debug_dir, "timeout_overlay.png"))
        except Exception as e:
            agregar_log(f"[DEBUG] No se pudo guardar imágenes de timeout: {e}")

    return False
