#buscar_img.py
import pyautogui
import time
import sys
import os

# Detectar si estamos dentro de un bundle de PyInstaller
if getattr(sys, "frozen", False):
    BASE_DIR = sys._MEIPASS
    print(f"[DEBUG] Ejecutándose en modo PyInstaller, BASE_DIR = {BASE_DIR}")
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    print(f"[DEBUG] Ejecutándose en modo desarrollo, BASE_DIR = {BASE_DIR}")

def buscar_y_click_en_set_imagenes(rutas_imagenes, sensibilidad, timeout=5):
    """
    Busca un conjunto de imágenes en la pantalla y hace clic en la primera que detecte.

    Parámetros:
    - rutas_imagenes: set o lista de rutas relativas a imágenes dentro de BASE_DIR.
    Por ejemplo: {"Imagenes/CargaInterfaz.png", "Imagenes/OtroIcono.png", "Anka.png"}
    - sensibilidad: float entre 0 y 1 (por defecto 0.8)
    - timeout: tiempo máximo de espera en segundos (por defecto 5)

    Retorna:
    - True si encontró alguna imagen y realizó clic.
    - False si no encontró ninguna.
    """

    if not rutas_imagenes:
        print("⚠️ No se proporcionaron imágenes.")
        return False

    pantalla_ancho, pantalla_alto = pyautogui.size()
    print(f"[DEBUG] Tamaño de pantalla: ancho={pantalla_ancho}, alto={pantalla_alto}")
    pyautogui.moveTo(pantalla_ancho / 2, pantalla_alto / 2, duration=0.1)
    print("[DEBUG] Mouse movido al centro de la pantalla antes de iniciar la búsqueda.")

    tiempo_inicio = time.time()
    print(f"[DEBUG] Iniciando búsqueda con timeout={timeout}s y sensibilidad={sensibilidad}")

    while time.time() - tiempo_inicio < timeout:
        for ruta_relativa in rutas_imagenes:
            # Construir la ruta absoluta dentro de BASE_DIR
            ruta_imagen = os.path.join(BASE_DIR, ruta_relativa)
            print(f"[DEBUG] Intentando localizar imagen: {ruta_imagen}")

            # Capturar la pantalla completa antes de buscar (para debug)
            try:
                screenshot_path = os.path.join(BASE_DIR, "debug_last_capture.png")
                pyautogui.screenshot(screenshot_path)
                print(f"[DEBUG] Captura de pantalla guardada en {screenshot_path}")
            except Exception as e:
                print(f"[ERROR] No se pudo guardar captura de pantalla: {e}")

            try:
                start_locate = time.time()
                ubicacion = pyautogui.locateOnScreen(ruta_imagen, confidence=sensibilidad)
                tiempo_locate = time.time() - start_locate
                print(f"[DEBUG] locateOnScreen tardó {tiempo_locate:.3f}s para {ruta_imagen}, resultado: {ubicacion}")
                time.sleep(0.2)
                if ubicacion:
                    centro_icono = pyautogui.center(ubicacion)
                    print(f"[DEBUG] Centro del ícono: {centro_icono}")
                    pyautogui.moveTo(centro_icono.x, centro_icono.y, duration=0.2)
                    print(f"[DEBUG] Mouse movido a ({centro_icono.x}, {centro_icono.y})")
                    pyautogui.click()
                    print(f"✅ Imagen detectada y clic realizada: {ruta_imagen}")
                    return True
            except Exception as e:
                print(f"[ERROR] Error buscando {ruta_imagen}: {e}")

        tiempo_transcurrido = int(time.time() - tiempo_inicio)
        print(f"🔄 Buscando íconos... {tiempo_transcurrido}s transcurridos")
        time.sleep(1)

    print("❌ No se encontró ninguna de las imágenes en pantalla.")
    return False
