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
from Modules.b_gestion_shuttle import abrir_shuttle, cerrar_shuttle

# ------------------------------------------------------------------
# Importaciones de Utils
# ------------------------------------------------------------------
from Utils.tools.puente_busqueda_img import puente_busqueda_img
from Utils.tools.esperar_cambio_region import esperar_cambio_region
from Utils.tools.mensaje_en_pantalla import mensaje_en_pantalla
from Utils.validar_archivos_carpetas.validar_txt import validar_txt
from Utils.tools.agregar_config_constelaciones import guardar_config_constelaciones_txt
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
    ruta_donde_guardar_configuraciones = lista_carpetas_principales.get("Pos")
    if not ruta_donde_guardar_configuraciones:
        agregar_log("[ERROR] 'Pos' no encontrado en lista_carpetas_principales.")
        return False

    resultado_mejor = intentar_cargar_mejor_config_existente(ruta_donde_guardar_configuraciones)
    if resultado_mejor is True:
        return True
    
    # Cargar historial para evitar repetir
    configs_ejecutadas = cargar_configs_ejecutadas(ruta_donde_guardar_configuraciones)
    agregar_log(f"[INFO] Configs ya ejecutadas cargadas: {len(configs_ejecutadas)}")

    
    for idx, (gps, glo, gal, bds) in enumerate(combinaciones_constelaciones, start=1):

        agregar_log(f"[INFO] Probando configuración #{idx}: GPS={gps}, GLO={glo}, GAL={gal}, BDS={bds}")
        
        # Probar máscaras 10..18
        for mascara in range(10, 19):

            # Evitar repetir si ya existe en el historial
            clave = clave_config(gps, glo, gal, bds, mascara)
            if clave in configs_ejecutadas:
                agregar_log(f"[INFO] Config ya ejecutada, se salta: {clave}")
                continue
            
            
            # Aplicar constelaciones
            estado_coinstelaciones = aplicar_constelaciones(gps, glo, gal, bds)
            # Validacion en caso de fallo al aplicar las cosntelaciones
            if estado_coinstelaciones is None:
                agregar_log("[ERROR] Fallo al aplicar constelaciones. Abortando.")
                return False

            # Aplicar Mascara
            estado_mascara = aplicar_mascara(mascara)
            # Validacion en caso de fallo al aplicar la mascara
            if estado_mascara is None:
                agregar_log("[ERROR] Fallo al aplicar la máscara. Abortando.")
                return False
                        
            # Ejecuto la cinematica y genero el reporte
            estado_rpa_reporte, ruta_txt_reporte = generar_reporte(lista_carpetas_principales)
            # Si ocurre algun error saltamos esa mascara
            if estado_rpa_reporte is None:
                agregar_log(f"[WARN] No se pudo generar reporte para {clave}. Continuando.")
                continue
          
            # Validar reporte
            estado_validar_txt, porcentaje = validar_txt(ruta_txt_reporte)
            # Si ocurre algun error saltamos esa mascara
            if estado_validar_txt is False:
                agregar_log(f"[WARN] No se pudo validar reporte para {clave}. Continuando.")
                continue

            # Guardar configuraion a un archivo .txt que se guardara en ruta_donde_guardar_configuraciones con el nombre de CONFIG_CONSTELACIONES.txt
            configuracion_const = (f"GPS={gps}, GLO={glo}, GAL={gal}, BDS={bds}, "f"MASCARA={mascara}, PORCENTAJE={porcentaje}")
            estado_guardar_configs_constelaciones = guardar_config_constelaciones_txt(ruta_donde_guardar_configuraciones,configuracion_const)

            
            # Validar si se guardo la configuracion 
            if estado_guardar_configs_constelaciones is False:
                agregar_log(f"[WARN] No se agrego la configuracion {configuracion_const}")
                continue

            # Marcar como ejecutada para no repetir en la misma corrida
            configs_ejecutadas.add(clave)
            
                        
            # si el porcentaje es mayor al 96% y menor al 98% hay que aplicar una configuracion donde la mascara le restemos 0.5 ejemplo si vamos en mascara 14 y esta en el rangoaplicamos mascara 13.5    
            if porcentaje > 96 and porcentaje < 98:
                
                # Aplicar constelaciones
                estado_coinstelaciones = aplicar_constelaciones(gps, glo, gal, bds)
                # Validacion en caso de fallo al aplicar las cosntelaciones
                if estado_coinstelaciones is None:
                    agregar_log("[ERROR] Fallo al aplicar constelaciones. Abortando.")
                    return False
                
                # Aplicar Mascara
                estado_mascara = aplicar_mascara((mascara-0.5))
                # Validacion en caso de fallo al aplicar la mascara
                if estado_mascara is None:
                    agregar_log("[ERROR] Fallo al aplicar la máscara. Abortando.")
                    return False
                
                # Ejecuto la cinematica y genero el reporte
                estado_rpa_reporte, ruta_txt_reporte = generar_reporte(lista_carpetas_principales)
                # Si ocurre algun error saltamos esa mascara
                if estado_rpa_reporte is None:
                    agregar_log(f"[WARN] No se pudo generar reporte para {clave}. Continuando.")
                    continue
            
                # Validar reporte
                estado_validar_txt, porcentaje = validar_txt(ruta_txt_reporte)
                # Si ocurre algun error saltamos esa mascara
                if estado_validar_txt is False:
                    agregar_log(f"[WARN] No se pudo validar reporte para {clave}. Continuando.")
                    continue

                # Guardar configuraion a un archivo .txt que se guardara en ruta_donde_guardar_configuraciones con el nombre de CONFIG_CONSTELACIONES.txt
                configuracion_const = (f"GPS={gps}, GLO={glo}, GAL={gal}, BDS={bds}, "f"MASCARA={mascara}, PORCENTAJE={porcentaje}")
                estado_guardar_configs_constelaciones = guardar_config_constelaciones_txt(ruta_donde_guardar_configuraciones,configuracion_const)

                
                # Validar si se guardo la configuracion 
                if estado_guardar_configs_constelaciones is False:
                    agregar_log(f"[WARN] No se agrego la configuracion {configuracion_const}")
                    continue

                # Marcar como ejecutada para no repetir en la misma corrida
                configs_ejecutadas.add(clave)
                
            # Si porcentaje es mayor a 98%
            if porcentaje >= 98: return True    
             
             
            # si el porcentaje es mayor al 96% y menor al 98% hay que aplicar una configuracion donde la mascara le restemos 0.5 ejemplo si vamos en mascara 14 y esta en el rangoaplicamos mascara 13.5    
            if porcentaje > 96 and porcentaje < 98:
                
                # Aplicar constelaciones
                estado_coinstelaciones = aplicar_constelaciones(gps, glo, gal, bds)
                # Validacion en caso de fallo al aplicar las cosntelaciones
                if estado_coinstelaciones is None:
                    agregar_log("[ERROR] Fallo al aplicar constelaciones. Abortando.")
                    return False
                
                # Aplicar Mascara
                estado_mascara = aplicar_mascara((mascara+0.5))
                # Validacion en caso de fallo al aplicar la mascara
                if estado_mascara is None:
                    agregar_log("[ERROR] Fallo al aplicar la máscara. Abortando.")
                    return False
                
                # Ejecuto la cinematica y genero el reporte
                estado_rpa_reporte, ruta_txt_reporte = generar_reporte(lista_carpetas_principales)
                # Si ocurre algun error saltamos esa mascara
                if estado_rpa_reporte is None:
                    agregar_log(f"[WARN] No se pudo generar reporte para {clave}. Continuando.")
                    continue
            
                # Validar reporte
                estado_validar_txt, porcentaje = validar_txt(ruta_txt_reporte)
                # Si ocurre algun error saltamos esa mascara
                if estado_validar_txt is False:
                    agregar_log(f"[WARN] No se pudo validar reporte para {clave}. Continuando.")
                    continue

                # Guardar configuraion a un archivo .txt que se guardara en ruta_donde_guardar_configuraciones con el nombre de CONFIG_CONSTELACIONES.txt
                configuracion_const = (f"GPS={gps}, GLO={glo}, GAL={gal}, BDS={bds}, "f"MASCARA={mascara}, PORCENTAJE={porcentaje}")
                estado_guardar_configs_constelaciones = guardar_config_constelaciones_txt(ruta_donde_guardar_configuraciones,configuracion_const)

                
                # Validar si se guardo la configuracion 
                if estado_guardar_configs_constelaciones is False:
                    agregar_log(f"[WARN] No se agrego la configuracion {configuracion_const}")
                    continue

                # Marcar como ejecutada para no repetir en la misma corrida
                configs_ejecutadas.add(clave) 
                
            # Si porcentaje es mayor a 98%
            if porcentaje >= 98: return True 
              
    return True
