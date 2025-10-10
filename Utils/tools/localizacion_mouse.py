# localizacion_mouse.py
import time
import pyautogui

def obtener_localizacion_mouse(tiempo_espera=5):
    """
    Espera 'tiempo_espera' segundos, luego obtiene la posición actual del mouse.
    
    Parámetros:
        tiempo_espera (int): segundos a esperar antes de capturar la posición.
    
    Retorna:
        tuple: (x, y) coordenadas del mouse.
    """
    print(f"Mueve el mouse a la posición deseada. Tienes {tiempo_espera} segundos...")
    time.sleep(tiempo_espera)
    x, y = pyautogui.position()
    print(f"Coordenadas del mouse: X={x}, Y={y}")
    return x, y

# Para ejecutar directamente este módulo desde la terminal:
if __name__ == "__main__":
    obtener_localizacion_mouse()
