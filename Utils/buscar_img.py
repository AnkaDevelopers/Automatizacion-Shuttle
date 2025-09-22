# buscar_img.py


# ------------------------------------------------------------------
# Importaciones de librerías y configuración
# ------------------------------------------------------------------
from typing import Iterable, Set, List, Union
import pyautogui
import time
import sys
import os


# ------------------------------------------------------------------
# 0. Detección de entorno (PyInstaller vs desarrollo)
# ------------------------------------------------------------------
if getattr(sys, "frozen", False):
    BASE_DIR = sys._MEIPASS  # type: ignore[attr-defined]
    print(f"[DEBUG] Ejecutándose en modo PyInstaller, BASE_DIR = {BASE_DIR}")
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    print(f"[DEBUG] Ejecutándose en modo desarrollo, BASE_DIR = {BASE_DIR}")


# ------------------------------------------------------------------
# Función: buscar_y_click_en_set_imagenes
# ------------------------------------------------------------------
# Busca un conjunto de imágenes en la pantalla y hace clic en la primera
# que detecte, utilizando coincidencia por confianza.
#
# Parámetros:
#   - rutas_imagenes: Iterable[str]
#       Rutas relativas de imágenes dentro de BASE_DIR
#       (p.ej. {"Imagenes/CargaInterfaz.png", "Imagenes/OtroIcono.png"})
#   - sensibilidad: float (0..1)
#       Confianza mínima para localizar la imagen (ej. 0.8)
#   - timeout: int | float
#       Tiempo máximo de búsqueda en segundos (default: 5)
#
# Retorna:
#   - True  -> si encontró alguna imagen y realizó clic.
#   - False -> si no encontró ninguna o hubo errores recuperables.
# ------------------------------------------------------------------
def buscar_y_click_en_set_imagenes(
    rutas_imagenes: Union[Set[str], List[str], Iterable[str]],
    sensibilidad: float,
    timeout: Union[int, float] = 5
) -> bool:
    try:
        # ------------------------------------------------------------------
        # 1. Validaciones de entrada
        # ------------------------------------------------------------------
        if not rutas_imagenes:
            print("[WARNING] No se proporcionaron rutas de imágenes.")
            return False

        try:
            rutas_iterables = list(rutas_imagenes)
        except TypeError:
            print("[ERROR] 'rutas_imagenes' no es iterable.")
            return False

        if not (0.0 < float(sensibilidad) <= 1.0):
            print(f"[ERROR] Sensibilidad fuera de rango: {sensibilidad}. Debe ser (0, 1].")
            return False

        try:
            timeout = float(timeout)
        except Exception:
            print(f"[ERROR] Timeout inválido: {timeout}")
            return False

        # ------------------------------------------------------------------
        # 2. Preparación de entorno de búsqueda
        # ------------------------------------------------------------------
        pantalla_ancho, pantalla_alto = pyautogui.size()
        print(f"[INFO] Tamaño de pantalla: {pantalla_ancho}x{pantalla_alto}")
        pyautogui.moveTo(pantalla_ancho / 2, pantalla_alto / 2, duration=0.1)
        print("[DEBUG] Mouse movido al centro antes de iniciar la búsqueda.")

        tiempo_inicio = time.time()
        print(f"[INFO] Búsqueda iniciada | timeout={timeout:.1f}s | sensibilidad={sensibilidad}")

        # ------------------------------------------------------------------
        # 3. Bucle de búsqueda hasta timeout
        # ------------------------------------------------------------------
        while time.time() - tiempo_inicio < timeout:
            for ruta_relativa in rutas_iterables:
                # ----------------------------------------------------------
                # 3.1 Construir ruta absoluta y preparar captura para debug
                # ----------------------------------------------------------
                ruta_imagen = os.path.join(BASE_DIR, str(ruta_relativa))
                print(f"[DEBUG] Intentando localizar: {ruta_imagen}")

                try:
                    screenshot_path = os.path.join(BASE_DIR, "debug_last_capture.png")
                    pyautogui.screenshot(screenshot_path)
                    print(f"[DEBUG] Captura guardada en: {screenshot_path}")
                except Exception as e:
                    print(f"[WARNING] No se pudo guardar captura de pantalla: {e}")

                # ----------------------------------------------------------
                # 3.2 Intentar localizar en pantalla con confianza dada
                # ----------------------------------------------------------
                try:
                    t0 = time.time()
                    ubicacion = pyautogui.locateOnScreen(ruta_imagen, confidence=float(sensibilidad))
                    dt = time.time() - t0
                    print(f"[DEBUG] locateOnScreen {dt:.3f}s | resultado={ubicacion}")
                    time.sleep(0.2)

                    # ------------------------------------------------------
                    # 3.3 Si encontró, mover y hacer clic
                    # ------------------------------------------------------
                    if ubicacion:
                        centro = pyautogui.center(ubicacion)
                        print(f"[DEBUG] Centro detectado: ({centro.x}, {centro.y})")
                        pyautogui.moveTo(centro.x, centro.y, duration=0.2)
                        print(f"[DEBUG] Mouse movido a ({centro.x}, {centro.y})")
                        pyautogui.click()
                        print(f"[SUCCESS] Imagen detectada y clic realizada: {ruta_imagen}")
                        return True

                except Exception as e:
                    print(f"[ERROR] Error durante búsqueda de '{ruta_imagen}': {e}")

            # --------------------------------------------------------------
            # 3.4 Feedback de progreso mientras continúa la búsqueda
            # --------------------------------------------------------------
            elapsed = int(time.time() - tiempo_inicio)
            print(f"[INFO] Buscando íconos... {elapsed}s transcurridos")
            time.sleep(1)

        # ------------------------------------------------------------------
        # 4. Timeout alcanzado sin coincidencias
        # ------------------------------------------------------------------
        print("[ERROR] Timeout alcanzado. No se encontró ninguna de las imágenes en pantalla.")
        return False

    except Exception as e:
        # ------------------------------------------------------------------
        # 5. Manejo de errores inesperados
        # ------------------------------------------------------------------
        print(f"[EXCEPTION] Error inesperado en 'buscar_y_click_en_set_imagenes': {e}")
        return False
