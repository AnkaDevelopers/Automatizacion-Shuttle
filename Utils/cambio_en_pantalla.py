# cambio_en_pantalla.py

# ------------------------------------------------------------------
# Importaciones globales y adicionales
# ------------------------------------------------------------------
from skimage.metrics import structural_similarity as ssim
from typing import Optional
from PIL import ImageGrab
import numpy as np
import time


# ------------------------------------------------------------------
# Función: cambio_en_pantalla
# ------------------------------------------------------------------
# Monitorea la pantalla y detecta cambios usando SSIM entre capturas
# consecutivas en escala de grises.
#
# Parámetros:
#   - sensibilidad: float (0..1) -> Umbral; cuanto más alto, más sensible
#       a cambios pequeños (ej. 0.95).
#   - intervalo: float -> Segundos entre capturas (ej. 1.0).
#   - tiempo_max: float -> Tiempo máximo de espera antes de devolver None.
#
# Retorna:
#   - True  -> si se detecta un cambio (flujo OK).
#   - None  -> si no hay cambios antes de tiempo_max (timeout sin cambio).
#   - False -> si ocurre un error (parámetros inválidos, captura inicial fallida
#              u otro error no recuperable).
# ------------------------------------------------------------------
def cambio_en_pantalla(sensibilidad: float = 0.9, intervalo: float = 1.0, tiempo_max: float = 60.0) -> Optional[bool]:
    try:
        # ------------------------------------------------------------------
        # 1) Validaciones de parámetros
        # ------------------------------------------------------------------
        if not (0.0 < float(sensibilidad) <= 1.0):
            print(f"[ERROR] 'sensibilidad' fuera de rango: {sensibilidad}. Debe estar en (0, 1].")
            return False
        if intervalo <= 0:
            print(f"[ERROR] 'intervalo' inválido: {intervalo}. Debe ser > 0.")
            return False
        if tiempo_max <= 0:
            print(f"[ERROR] 'tiempo_max' inválido: {tiempo_max}. Debe ser > 0.")
            return False

        print(f"[INFO] Iniciando monitoreo de pantalla | sensibilidad={sensibilidad} intervalo={intervalo}s tiempo_max={tiempo_max}s")

        # ------------------------------------------------------------------
        # 2) Captura inicial (grayscale) y temporizador
        # ------------------------------------------------------------------
        t0 = time.time()
        try:
            captura_anterior = np.array(ImageGrab.grab().convert("L"))
        except Exception as e:
            print(f"[ERROR] No se pudo realizar la captura inicial de pantalla: {e}")
            return False
        print(f"[DEBUG] Captura inicial OK | tamaño={captura_anterior.shape} | t={(time.time()-t0):.3f}s")

        tiempo_inicio = time.time()

        # ------------------------------------------------------------------
        # 3) Bucle de monitoreo hasta agotar tiempo_max
        # ------------------------------------------------------------------
        while True:
            # 3.1) Verificar timeout antes de dormir (salida rápida)
            elapsed = time.time() - tiempo_inicio
            if elapsed >= tiempo_max:
                print("[INFO] Tiempo máximo alcanzado sin cambios.")
                return None  # ← Timeout sin cambios

            # 3.2) Esperar intervalo de muestreo
            restante = min(intervalo, max(0.0, tiempo_max - elapsed))
            time.sleep(restante)

            # 3.3) Nueva captura
            try:
                tcap = time.time()
                captura_actual = np.array(ImageGrab.grab().convert("L"))
                print(f"[DEBUG] Nueva captura | tamaño={captura_actual.shape} | t={(time.time()-tcap):.3f}s")
            except Exception as e:
                print(f"[WARNING] Falló una captura de pantalla: {e}")
                continue  # Intentar de nuevo en el siguiente ciclo

            # 3.4) Asegurar mismas dimensiones (puede haber cambios de DPI/escala)
            if captura_actual.shape != captura_anterior.shape:
                print(f"[WARNING] Dimensiones distintas. Reajustando referencia. prev={captura_anterior.shape} act={captura_actual.shape}")
                captura_anterior = captura_actual
                continue

            # 3.5) Calcular SSIM y decidir
            try:
                tssim = time.time()
                score, _ = ssim(captura_anterior, captura_actual, full=True)
                print(f"[DEBUG] SSIM={score:.5f} | t={(time.time()-tssim):.3f}s")
            except Exception as e:
                print(f"[ERROR] No se pudo calcular SSIM: {e}")
                # Reemplazar referencia para seguir
                captura_anterior = captura_actual
                continue

            if score < sensibilidad:
                print(f"[SUCCESS] Cambio detectado en pantalla (similitud={score:.4f} < {sensibilidad})")
                return True  # ← Cambio detectado (flujo OK)

            # 3.6) Actualizar referencia y continuar
            captura_anterior = captura_actual

    except Exception as e:
        # ------------------------------------------------------------------
        # X) Manejo de errores inesperados
        # ------------------------------------------------------------------
        print(f"[EXCEPTION] Error inesperado en 'cambio_en_pantalla': {e}")
        return False  # ← Error no recuperable
