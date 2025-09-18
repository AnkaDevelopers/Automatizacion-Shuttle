# espera_carga_interfaz.py

# INPORTACIONES ADICIONALES
import pyautogui
import time


def esperar_carga_interfaz(imagen_referencia,timeout):
    print('🔎 Inicio del proceso de espera para la carga de la interfaz...')

    
    #timeout = 60  # Tiempo máximo de espera en segundos
    intervalo = 2  # Tiempo entre cada intento de búsqueda

    tiempo_inicio = time.time()
    intentos = 0

    while True:
        intentos += 1

        # Intentar localizar la imagen en la pantalla con manejo de errores
        try:
            ubicacion = pyautogui.locateOnScreen(imagen_referencia, confidence=0.7)
        except pyautogui.ImageNotFoundException:
            ubicacion = None
        except Exception as e:
            print(f"❌ Error inesperado al buscar imagen en pantalla: {e}")
            return None

        if ubicacion:
            tiempo_transcurrido = time.time() - tiempo_inicio
            print(f"✅ Imagen detectada tras {tiempo_transcurrido:.2f} segundos ({intentos} intentos).")
            return True

        tiempo_transcurrido = time.time() - tiempo_inicio
        if tiempo_transcurrido > timeout:
            print(f"⏰ Tiempo agotado: {tiempo_transcurrido:.2f} segundos sin detectar la imagen ({intentos} intentos).")
            return None

        time.sleep(intervalo)
