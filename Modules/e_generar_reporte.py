# generar_reporte.py

# ------------------------------------------------------------------
# Importaciones de librerías y configuraciónes Globales
# ------------------------------------------------------------------
from typing import Optional
import Config.config as config
import pyautogui
import time
import os

# ------------------------------------------------------------------
# Importaciones de Modulos
# ------------------------------------------------------------------
from Monitor.log.log import agregar_log

# ------------------------------------------------------------------
# Importaciones de Utils necesarios
# ------------------------------------------------------------------
from Utils.tools.puente_busqueda_img import puente_busqueda_img
from Utils.tools.esperar_cambio_region import esperar_cambio_region
from Utils.validar_archivos_carpetas.validar_archivos import validar_archivos
from Utils.validar_archivos_carpetas.gestion_archivos_txt import cerrar_todos_txt


# ------------------------------------------------------------------
# Función: generar_reporte
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
def generar_reporte(lista_carpetas_principales, tiempo_max_de_carga):

    #************************************************************
    # Primera busqueda buscar Boton Kinematic difrencial GNSS
    for i in range(12):
        agregar_log("[DEBUG] Busqueda Boton Kinematic difrencial GNSS...")
        busqueda_btn_kinematic_gnss = puente_busqueda_img(config.imagenes_Btn_Kinematic, config.mensajes_busquedas_imagenes)
        
        # si busqueda_btn_kinematic_gnss retorna None o false lo intenta otra vez
        if busqueda_btn_kinematic_gnss not in (None, False): break
        
        # si lo encuentra rompre el for
    else:
        agregar_log("[WARN] No se encontró Boton Kinematic difrencial GNSS tras 12 intentos.")
        return None, None

    #************************************************************
    # Espera de carga Kinematic
    agregar_log("[INFO] Esperando procesamiento Kinematic...")
    
    # Centro de pantalla
    centro_barra = (960,540)
    
    if not esperar_cambio_region(mouse_pos=centro_barra, radio=400, timeout=tiempo_max_de_carga, intervalo=1.0, umbral=0.01):
        agregar_log("[WARN] No se detectó cambio visual en la barra de progreso tras timeout")
        return False, None
    
    #************************************************************
    # Segunda busqueda buscar Boton Reportes
    for i in range(12):
        agregar_log("[DEBUG] Busqueda Boton Reportes...")
        busqueda_btn_file = puente_busqueda_img(config.imagenes_Btn_Report, config.mensajes_busquedas_imagenes)
        
        # si busqueda_btn_file retorna None o false lo intenta otra vez
        if busqueda_btn_file not in (None, False): break
        
        # si lo encuentra rompre el for
    else:
        agregar_log("[WARN] No se encontró Boton Reportes tras 12 intentos.")
        return None, None

    #************************************************************
    # Seleccion opcion
    time.sleep(1)
    pyautogui.press('down')
    time.sleep(1)
    pyautogui.press('enter')

    #************************************************************
    # Tercera busqueda buscar Boton Output Wizard
    for i in range(12):
        agregar_log("[DEBUG] Busqueda Boton Output Wizard...")
        busqueda_btn_Output = puente_busqueda_img(config.imagenes_Btn_Output, config.mensajes_busquedas_imagenes)
        
        # si busqueda_btn_Output retorna None o false lo intenta otra vez
        if busqueda_btn_Output not in (None, False): break
        
        # si lo encuentra rompre el for
    else:
        agregar_log("[WARN] No se encontró Boton Output Wizard tras 12 intentos.")
        return None, None

    #************************************************************
    # Cuarta busqueda buscar Reportes o OUTPUT Waring
    for i in range(12):
        agregar_log("[DEBUG] Busqueda Reportes o OUTPUT Waring...")
        busqueda_btn_Output_waring = puente_busqueda_img(config.imagenes_Btn_Report_Waring, config.mensajes_busquedas_imagenes)
        
        # si busqueda_btn_Output_waring retorna None o false lo intenta otra vez
        if busqueda_btn_Output_waring not in (None, False): break
        
        # si lo encoentra rompre el for
    else:
        agregar_log("[WARN] No se encontró Reportes o OUTPUT Waring tras 12 intentos.")
        return None, None

    #************************************************************
    # Aceptar
    time.sleep(1)
    pyautogui.press('enter')

    #************************************************************
    # Buscar archivo .txt
    agregar_log("------------------VALIDAR ARCHIVO GNSS.TXT------------------")
    ruta_archivo_gnss_txt = validar_archivos(lista_carpetas_principales.get("Pos"), ".txt")
    if ruta_archivo_gnss_txt is None:
        agregar_log("[ERROR] Error al buscar el archivo .txt")
        return None, None
    time.sleep(2)
    #************************************************************
    # Cerrar archivo .txt
    try:
        ok = cerrar_todos_txt()
        if ok in (None, False):
            agregar_log("[WARN] No se pudo cerrar el .txt (retornó None/False). Continuo igual.")
    except Exception as e:
        agregar_log(f"[WARN] Error al cerrar el .txt: {e}. Continuo igual.")

    # Si todo marcha bien Retornamos True
    return True, ruta_archivo_gnss_txt
    