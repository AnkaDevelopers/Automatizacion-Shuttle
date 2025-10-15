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
from Modules.e_aplicar_config_gnss import aplicar_constelaciones , aplicar_mascara

# ------------------------------------------------------------------
# Importaciones de Utils
# ------------------------------------------------------------------
from Utils.tools.puente_busqueda_img import puente_busqueda_img
from Utils.tools.esperar_cambio_region import esperar_cambio_region
from Utils.tools.mensaje_en_pantalla import mensaje_en_pantalla
from Utils.validar_archivos_carpetas.validar_txt import validar_txt



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
#  Función principal: ajuste_gnss
# ------------------------------------------------------------------
#    Automatiza todas las posibles configuraciones (15 combinaciones de constelaciones válidas)
#    y para cada una prueba las 18 máscaras (1..18), hasta encontrar una que logre porcentaje >= 90%.
#    
#    Retorna:
#        - (True, porcentaje, (gps,glo,gal,bds), mascara)   -> si alguna configuración logra >= 90%
#        - (None, mejor_porcentaje, mejor_config, mejor_mascara) -> si ninguna lo logra (mejor intento)
#        - False -> si ocurre un error crítico de automatización/búsquedas
# ------------------------------------------------------------------
    

def ajuste_gnss(lista_carpetas_principales):

    # ruta donde quiero guardar mis configuraciones:
    ruta_donde_guardar_configuraciones=lista_carpetas_principales.get("Pos")

    for idx, (gps, glo, gal, bds) in enumerate(combinaciones_constelaciones, start=1):

        agregar_log(f"[INFO] Probando configuración #{idx}: GPS={gps}, GLO={glo}, GAL={gal}, BDS={bds}")
        
        # Probar máscaras 1..18
        for mascara in range(10, 19):
            
            # Aplicar constelaciones
            estado_coinstelaciones = aplicar_constelaciones(gps, glo, gal, bds)
            # Validacion en caso de fallo al aplicar las cosntelaciones
            if estado_coinstelaciones is None: return False

            # Aplicar Mascara
            estado_mascara = aplicar_mascara(mascara)
            # Validacion en caso de fallo al aplicar la mascara
            if estado_mascara is None: return False
            
            # Ejecuto la cinematica y genero el reporte
            estado_rpa_reporte, ruta_txt_reporte = generar_reporte(lista_carpetas_principales)
            # Si ocurre algun error saltamos esa mascara
            if estado_rpa_reporte is None: continue
            
            # Validar reporte
            estado_validar_txt, porcentaje = validar_txt(ruta_txt_reporte)
            # Si ocurre algun error saltamos esa mascara
            if estado_validar_txt in (None,False): continue
            
            print(porcentaje)
            time.sleep(1000)
            
    #        
    return 

