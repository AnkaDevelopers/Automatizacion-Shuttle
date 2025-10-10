# validar_txt.py

# ------------------------------------------------------------------
# Importaciones de Utils necesarios
# ------------------------------------------------------------------
from Utils.tools.calculo_porcentaje_de_conformidad_reporte_gnss import calcular_conformidad
from Utils.validar_archivos_carpetas.gestion_archivos_txt import cerrar_todos_txt
from Monitor.log.log import agregar_log

# ------------------------------------------------------------------
# Importaciones globales y adicionales
# ------------------------------------------------------------------
import Config.config as config
from typing import Optional
import pyautogui
import time
import os

# ------------------------------------------------------------------
# Función: validar_txt
# ------------------------------------------------------------------
# Automatiza la la validacion del modelo kinematic diferencial
# 
#
# Parámetros:
#   - 
#   - 
#
# Retorna:
#   - True  -> si todo el flujo se completa correctamente.
#   - None  -> si alguna búsqueda/acción crítica falla.
def validar_txt(rta_archivo_gnss_txt):
    
    #*******************************************************************
    # Cerrar archivo txt que se abrio
    time.sleep(2)
    rta_cerrar_txt = cerrar_todos_txt()

    if rta_cerrar_txt == False:
        agregar_log("[ERROR] Hubo un error al cerrar el archivo .txt")
        
    #*******************************************************************
    # Evaluar archivo .txt        
    rta_calculo_conformidad, porcentaje = calcular_conformidad(rta_archivo_gnss_txt)
    
    # Validar el proceso
    if rta_calculo_conformidad == False:
        agregar_log("[ERROR] Hubo un error en el caluclo de la conformidad")
        return False,porcentaje
    
    # Validar porcentaje de conformidad mayor al 90%
    if rta_calculo_conformidad == True:
        agregar_log(f"[INFO] EL porcentaje de conformidad es igual a {porcentaje}")
        return True,porcentaje
    
    agregar_log(f"[DEBUG] repetir calculo el procentaje es igual a: {porcentaje}")
    return None,porcentaje
    
    