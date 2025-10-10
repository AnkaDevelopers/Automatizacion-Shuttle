# d_creacion_proyecto.py

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
# Importaciones de Utils
# ------------------------------------------------------------------
from Utils.tools.puente_busqueda_img import puente_busqueda_img
from Utils.tools.esperar_cambio_region import esperar_cambio_region


# ------------------------------------------------------------------
# Función: creacion_proyecto
# ------------------------------------------------------------------
# Automatiza la creacion de un nuevo proyecto
# la carga de un archivo observado y uno .kqs
#
# Parámetros:
#   - ruta_archivo_obs: str -> Ruta absoluta al archivo .25o
#   - ruta_archivo_kqs: str -> Ruta absoluta al archivo .kqs
#
# Retorna:
#   - True  -> si todo el flujo se completa correctamente.
#   - None  -> si alguna búsqueda/acción crítica falla.
# ------------------------------------------------------------------


#**************************************************************************
def creacion_proyecto(ruta_archivo_obs, ruta_archivo_kqs):

    #************************************************************
    # Primera busqueda buscar Boton File
    for i in range(12):
        agregar_log("[DEBUG] Busqueda Boton File...")
        busqueda_btn_file = puente_busqueda_img(config.imagenes_Btn_File, config.mensajes_busquedas_imagenes )
        
        # si busqueda_btn_file retorna None o false lo intenta otra vez
        if busqueda_btn_file not in (None, False): break
        
        # si lo encoentra rompre el for
    else:
        agregar_log("[WARN] No se encontró Boton File tras 12 intentos.")
        return None, None

    #************************************************************
    # Segunda busqueda buscar Boton New_Proyect
    for i in range(12):
        agregar_log("[DEBUG] Busqueda Boton New_Proyect...")
        busqueda_btn_new_proyect = puente_busqueda_img(config.imagenes_Btn_New_Proyect, config.mensajes_busquedas_imagenes)
        
        # si busqueda_btn_new_proyect retorna None o false lo intenta otra vez
        if busqueda_btn_new_proyect not in (None, False): break
        
        # si lo encoentra rompre el for
    else:
        agregar_log("[WARN] No se encontró Boton New_Proyect tras 12 intentos.")
        return None, None

            
    #************************************************************
    # Nombrar nuevo Proyecto
    time.sleep(1)
    pyautogui.write(config.nombre_new_proyect)
    pyautogui.press('enter')

    #************************************************************
    # Tercera busqueda buscar Boton Add
    for i in range(12):
        agregar_log("[DEBUG] Busqueda Boton Add...")
        busqueda_btn_add = puente_busqueda_img(config.imagenes_Btn_Add, config.mensajes_busquedas_imagenes)
        
        # si busqueda_btn_add retorna None o false lo intenta otra vez
        if busqueda_btn_add not in (None, False): break
        
        # si lo encoentra rompre el for
    else:
        agregar_log("[WARN] No se encontró Boton Add tras 12 intentos.")
        return None, None
   
    #************************************************************
    # Seleccionar archivo .kqs
    agregar_log("[DEBUG] Seleccionar archivo observado")
    
    # Separar la ruta de la carpeta del nombre del archivo
    ruta_carpeta_archivo_obs, nombre_archivo_obs = ruta_archivo_obs.rsplit("\\", 1)
    
    # Agregamos la barra al final de la carpeta
    ruta_carpeta_archivo_obs += "\\"
    
    # Escribir ruta a la carpeta donde se encuentra el observado
    pyautogui.press('tab', presses=5, interval=0.1)
    pyautogui.press('space')
    pyautogui.write(f"{ruta_carpeta_archivo_obs}")
    pyautogui.press('enter')
    
    # Escribir el nombre del Obsevado
    pyautogui.press('tab', presses=6, interval=0.1)
    pyautogui.write(f'{nombre_archivo_obs}')
    pyautogui.press('enter')
    
    #************************************************************
    # Cargar archivo descomprimido .kqs
    pyautogui.press('tab', presses=5, interval=0.1)
    pyautogui.press('right')
    
    #************************************************************
    # Cuarta busqueda buscar Boton Add
    for i in range(12):
        agregar_log("[DEBUG] Busqueda Boton Add...")
        busqueda_btn_add = puente_busqueda_img(config.imagenes_Btn_Add, config.mensajes_busquedas_imagenes)
        
        # si busqueda_btn_add retorna None o false lo intenta otra vez
        if busqueda_btn_add not in (None, False): break
        
        # si lo encoentra rompre el for
    else:
        agregar_log("[WARN] No se encontró Boton Add tras 12 intentos.")
        return None, None
    
    #************************************************************
    # Agregar archivo .kqs
    agregar_log("[DEBUG] Seleccionar archivo kqs")
    
    # Separar la ruta de la carpeta del nombre del archivo
    ruta_carpeta_archivo_kqs, nombre_archivo_kqs = ruta_archivo_kqs.rsplit("\\",1)
    
    # Agregamos la barra al final de la carpeta
    ruta_carpeta_archivo_kqs += "\\"
    
    # Escribir la ruta y seleccionar el archivo
    pyautogui.press('tab', presses=5, interval=0.1)    
    pyautogui.press('space')
    pyautogui.write(ruta_carpeta_archivo_kqs)
    pyautogui.press('enter')
    
    # Escribir el nomnbre del archivo .kqs 
    pyautogui.press('tab', presses=6, interval=0.1)
    pyautogui.write(nombre_archivo_kqs)
    pyautogui.press('enter')
    time.sleep(2)
    
    #************************************************************
    # Quinta busqueda buscar Boton Aceptar
    for i in range(12):
        agregar_log("[DEBUG] Busqueda Boton Aceptar...")
        busqueda_btn_Aceptar = puente_busqueda_img(config.imagenes_Btn_Aceptar, config.mensajes_busquedas_imagenes)
        
        # si busqueda_btn_Aceptar retorna None o false lo intenta otra vez
        if busqueda_btn_Aceptar not in (None, False): break
        
        # si lo encoentra rompre el for
    else:
        agregar_log("[WARN] No se encontró Boton Aceptar tras 12 intentos.")
        return None, None
    
    #***********************************************************
    # Esperade carga de modelo
    agregar_log("[DEBUG] Espera de carga de pantalla")
       
    # Coordenada de pantalla
    centro_barra = (960,540)

    if not esperar_cambio_region(mouse_pos=centro_barra, radio=400, timeout=300, intervalo=1.0, umbral=0.01):
        agregar_log("[WARN] No se detectó cambio visual en la barra de progreso tras timeout")
        return False
    # Si todo marcha bien
    return True
    
