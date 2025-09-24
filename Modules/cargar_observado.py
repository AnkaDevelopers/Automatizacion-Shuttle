# cargar_observado.py

# ------------------------------------------------------------------
# Importaciones de Utils necesarios
# ------------------------------------------------------------------
from Utils.puente_busqueda_img import puente_busqueda_img
from Utils.cambio_en_pantalla import cambio_en_pantalla

# ------------------------------------------------------------------
# Importaciones globales y adicionales
# ------------------------------------------------------------------
import Config.config as config
from typing import Optional
import pyautogui
import time
import os

# ------------------------------------------------------------------
# Función: cargar_observado
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
def cargar_observado(ruta_archivo_obs, ruta_archivo_kqs):

    #************************************************************
    # Primera busqueda buscar Boton File
    print("[DEBUG] Busqueda Boton File")
    busqueda_btn_file = puente_busqueda_img(config.imagenes_Btn_File, config.mensajes_busquedas_imagenes)
    
    # Validacion de busqueda Boton File
    if busqueda_btn_file in (None, False): return None

    #************************************************************
    # Segunda busqueda buscar Boton New_Proyect
    print("[DEBUG] Busqueda Boton New Proyect")
    busqueda_btn_new_proyect = puente_busqueda_img(config.imagenes_Btn_New_Proyect, config.mensajes_busquedas_imagenes)

    # Validacion de busqueda Boton File
    if busqueda_btn_new_proyect in (None, False): return None
            
    #************************************************************
    # Nombrar nuevo Proyecto
    time.sleep(1)
    pyautogui.write(config.nombre_new_proyect)
    pyautogui.press('enter')
    
    #************************************************************
    # Tercera busqueda buscar Boton Add
    print("[DEBUG] Busqueda Boton Add")
    busqueda_btn_add = puente_busqueda_img(config.imagenes_Btn_Add, config.mensajes_busquedas_imagenes)
    
    # Validacion Boton Add
    if busqueda_btn_add in (None, False): return None
    
    #************************************************************
    # Seleccionar archivo .kqs
    print("[DEBUG] Seleccionar archivo observado")
    
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
    print("[DEBUG] Busqueda Boton Add")
    busqueda_btn_add = puente_busqueda_img(config.imagenes_Btn_Add, config.mensajes_busquedas_imagenes)
    
    # Validacion Boton Add
    if busqueda_btn_add in (None, False): return None
    
    #************************************************************
    # Agregar archivo .kqs
    print("[DEBUG] Seleccionar archivo kqs")
    
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
    
    #************************************************************
    # Quinta busqueda buscar Boton Aceptar
    print("[DEBUG] Busqueda Boton Aceptar")
    busqueda_btn_add = puente_busqueda_img(config.imagenes_Btn_Aceptar, config.mensajes_busquedas_imagenes)
    
    # Validacion Boton Add
    if busqueda_btn_add in (None, False): return None
    
    #***********************************************************
    # Esperade carga de modelo
    print("[DEBUG] Espera de carga de pantalla")
    time.sleep(60)
    
    
    # Si todo marcha bien
    return True
    
