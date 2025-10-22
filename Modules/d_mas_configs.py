# e_ajuste_gnss.py

# ------------------------------------------------------------------
# Importaciones de librerías y configuraciónes Globales
# ------------------------------------------------------------------
from typing import Tuple, Optional, Iterable
import Config.config as config
import pyautogui
import time
  

# ------------------------------------------------------------------
# Importaciones de Modulos
# ------------------------------------------------------------------
from Monitor.log.log import agregar_log
from Modules.e_generar_reporte import generar_reporte
from Modules.e_aplicar_config_gnss import aplicar_constelaciones
from Modules.b_gestion_shuttle import abrir_shuttle, cerrar_shuttle
from Modules.d_creacion_proyecto import creacion_proyecto

# ------------------------------------------------------------------
# Importaciones de Utils
# ------------------------------------------------------------------
from Utils.tools.config_constelaciones_helpers import ruta_config_txt, clave_config, cargar_configs_ejecutadas
from Utils.tools.cargar_mejor_config import intentar_cargar_mejor_config_existente


# ------------------------------------------------------------------
#Combinaciones ordenadas
combinaciones_constelaciones = [
    (True,  True,  False, False),   # GPS+GLO mejor acierto
    (True,  False, True,  False),   # GPS+GAL
    (True,  False, False, True),    # GPS+BDS
    (False, True,  True,  False),   # GLO+GAL
    (False, True,  False, True),    # GLO+BDS
    (False, False, True,  True),    # GAL+BDS
    (True,  True,  True,  False),   # GPS+GLO+GAL
    (True,  True,  False, True),    # GPS+GLO+BDS
    (True,  False, True,  True),    # GPS+GAL+BDS
    (False, True,  True,  True),    # GLO+GAL+BDS
    (True,  True,  True,  True),    # GPS+GLO+GAL+BDS
    (True,  False, False, False),   # GPS
    (False, True,  False, False),   # GLO
    (False, False, True,  False),   # GAL
    (False, False, False, True),    # BDS
]

# ------------------------------------------------------------------
#  Función principal: d_mas_configs
# ------------------------------------------------------------------

# ------------------------------------------------------------------
    

def d_mas_configs(lista_carpetas_principales,ruta_shuttle,ruta_archivo_observado, ruta_archivo_kqs):

    #**********************************************************************
        
    
    for idx, (gps, glo, gal, bds) in enumerate(combinaciones_constelaciones, start=1):
   
        # Cerrar Shuttle
        cerrar_shuttle()
        
        time.sleep(5)
        
        # Abrir Shuttle
        agregar_log("#################-ABRIR SHUTTLE-#################")
        estado_shuttle = abrir_shuttle(ruta_shuttle)  #dev 0,1
        
        # Validacion en caso de error al abrir el Shuttle
        if estado_shuttle is None: return False
        
        # tiempo para abrir el shuttle
        time.sleep(5)    

        agregar_log(f"[INFO] Probando configuración #{idx}: GPS={gps}, GLO={glo}, GAL={gal}, BDS={bds}")
            
        # Aplicar constelaciones
        estado_coinstelaciones = aplicar_constelaciones(gps, glo, gal, bds)
        # Validacion en caso de fallo al aplicar las cosntelaciones
        
        if estado_coinstelaciones is None:
            agregar_log("[ERROR] Fallo al aplicar constelaciones. Abortando.")
            return False
        
        pyautogui.press('tab',presses=3, interval=0.2)
        pyautogui.press('enter')
        pyautogui.press('tab',presses=2, interval=0.2)
        pyautogui.press('enter')
        
        
        #**********************************************************************
        # Creacion de proyecto
        agregar_log("#################-CREACION DE UN NUEVO PROYECTO-#################")
        estado_creacion_proyecto = creacion_proyecto(ruta_archivo_observado, ruta_archivo_kqs)
        
        # prueba otra configuracion
        if estado_creacion_proyecto is False:
            cerrar_shuttle()
            continue
        
        # Hubo un fallo al crear el proyectyo
        if estado_creacion_proyecto is None:
            return False
        
        # si todo funciona bien
        if estado_creacion_proyecto is True:
            break
                              
    return True
