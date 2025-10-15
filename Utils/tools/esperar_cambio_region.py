# esperar_cambio_region.py
# -----------------------------------------------------------------------------
# Importaciones de librerías y configuraciones globales
# -----------------------------------------------------------------------------
import os
import time
from typing import Tuple, Optional

import numpy as np
import pyautogui
from PIL import Image, ImageChops, ImageDraw

from Monitor.log.log import agregar_log


# -----------------------------------------------------------------------------
# Descripción general del módulo
# -----------------------------------------------------------------------------
# Este módulo monitorea cambios visuales en una región de la pantalla centrada
# en una posición del mouse. Compara capturas sucesivas contra una imagen
# baseline ya existente en disco (NO la vuelve a generar).
#
# Qué hace:
# 1) Define una región cuadrada alrededor de `mouse_pos` acotada a la pantalla.
# 2) Carga una baseline desde disco y compara capturas sucesivas contra ella.
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
# - baseline_path (str): ruta absoluta de la baseline a usar (no se sobrescribe).
# - debug_dir (str|None): carpeta para guardar evidencia (capturas).
# - guardar_overlay (bool): si True, guarda pantallazos completos con la región
#   marcada en rojo.
# - mantener_solo_ultimos (bool): si True, limpia imágenes previas (sin borrar
#   la baseline).
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
    las últimas capturas en cada ejecución. NO elimina la baseline.
    """
    nombres = [
        # "base_region.png",  # NO eliminar baseline
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


def _cargar_baseline_redimensionada(baseline_path: str, size: Tuple[int, int]) -> Optional[Image.Image]:
    """
    Carga la baseline desde disco y, si el tamaño no coincide con 'size',
    la adapta en memoria (sin modificar el archivo original).
    """
    try:
        if not os.path.exists(baseline_path):
            agregar_log(f"[ERROR] Baseline no encontrada: {baseline_path}")
            return None

        img = Image.open(baseline_path).convert("RGB")
        if img.size != size:
            agregar_log(
                f"[WARN] Tamaño baseline {img.size} != región {size}; "
                "se ajustará en memoria para comparar."
            )
            img = img.resize(size, Image.NEAREST)
        return img
    except Exception as e:
        agregar_log(f"[ERROR] No se pudo cargar baseline: {e}")
        return None


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
    baseline_path: str = r"C:\Automatizacion_Shuttle\debug_monitoreo\base_region.png",
    debug_dir: Optional[str] = r"C:\Automatizacion_Shuttle\debug_monitoreo",
    guardar_overlay: bool = False,
    mantener_solo_ultimos: bool = True,
) -> bool:
    """
    Espera cambios visuales en una región centrada en 'mouse_pos',
    comparando contra una baseline ya existente en 'baseline_path'.

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

    agregar_log(
        f"[INFO] Monitoreando cambios en región={region} por hasta {timeout}s... "
        f"Usando baseline: {baseline_path}"
    )

    # -------------------------------------------------------------------------
    # 3) Pausa inicial para estabilizar la interfaz
    # -------------------------------------------------------------------------
    if warmup and warmup > 0:
        time.sleep(warmup)

    t0 = time.time()

    # -------------------------------------------------------------------------
    # 4) Cargar baseline desde disco (NO se vuelve a capturar)
    # -------------------------------------------------------------------------
    # Tomar una captura actual SOLO para conocer el tamaño exacto de la región.
    # (No se guarda; se usa para dimensionar baseline si hiciera falta.)
    try:
        probe = pyautogui.screenshot(region=region).convert("RGB")
    except Exception as e:
        agregar_log(f"[ERROR] No se pudo capturar la región para 'probe': {e}")
        return False

    img_prev = _cargar_baseline_redimensionada(baseline_path, probe.size)
    if img_prev is None:
        # No hay baseline válida -> abortar
        return False

    # Si se desea, guardar overlay de la baseline (sin sobrescribir la baseline)
    if debug_dir and guardar_overlay:
        try:
            _guardar_overlay(region, os.path.join(debug_dir, "base_overlay.png"))
        except Exception as e:
            agregar_log(f"[DEBUG] No se pudo guardar base_overlay: {e}")

    # -------------------------------------------------------------------------
    # 5) Vigilancia periódica hasta timeout
    # -------------------------------------------------------------------------
    while time.time() - t0 < timeout:
        time.sleep(intervalo)

        # Captura actual
        try:
            img_new = pyautogui.screenshot(region=region).convert("RGB")
        except Exception as e:
            agregar_log(f"[ERROR] No se pudo capturar la región: {e}")
            return False

        # Asegurar coincidencia de tamaño con baseline cargada
        if img_new.size != img_prev.size:
            agregar_log(
                f"[WARN] Tamaño de captura {img_new.size} != baseline {img_prev.size}; "
                "se ajustará captura en memoria."
            )
            img_comp = img_new.resize(img_prev.size, Image.NEAREST)
        else:
            img_comp = img_new

        # Diferencia entre imágenes
        diff = ImageChops.difference(img_prev, img_comp)
        arr = np.array(diff)
        nonzero = np.count_nonzero(arr)
        total = arr.size
        ratio = nonzero / total

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

        # Importante: NO actualizamos la baseline. Siempre comparamos contra la baseline fija.
        # Esto responde al requisito de no modificar la baseline ya creada.

    # -------------------------------------------------------------------------
    # 6) Timeout: no se detectaron cambios
    # -------------------------------------------------------------------------
    agregar_log("[ERROR] Timeout: no hubo cambios visibles.")
    if debug_dir:
        try:
            probe.save(os.path.join(debug_dir, "timeout_region.png"))
            if guardar_overlay:
                _guardar_overlay(region, os.path.join(debug_dir, "timeout_overlay.png"))
        except Exception as e:
            agregar_log(f"[DEBUG] No se pudo guardar imágenes de timeout: {e}")

    return False
