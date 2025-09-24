# generar_reportr.py

# ------------------------------------------------------------------
# Importaciones de Utils necesarios
# ------------------------------------------------------------------
from Utils.puente_busqueda_img import puente_busqueda_img

# ------------------------------------------------------------------
# Importaciones globales y adicionales
# ------------------------------------------------------------------
import Config.config as config
from typing import Optional
import pyautogui
import time
import os

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
def generar_reporte():

    #************************************************************
    # busqueda buscar Boton Aceptar
    print("[DEBUG] Busqueda Boton Kinematic diferencial GNSS")
    busqueda_btn_kinematic_gnss = puente_busqueda_img(config.imagenes_Btn_Kinematic, config.mensajes_busquedas_imagenes)
    
    # Validacion Boton Add
    if busqueda_btn_kinematic_gnss in (None, False): return None
    
    # Espera de carga Cinematic
    time.sleep(60)
    
    #************************************************************
    # Primera busqueda buscar boton reportes
    print("[DEBUG] Busqueda Boton reportes o OUTPUT")
    busqueda_btn_file = puente_busqueda_img(config.imagenes_Btn_Report, config.mensajes_busquedas_imagenes)
    
    # Validacion de busqueda Boton File
    if busqueda_btn_file in (None, False): return None
    
    # Seleccion opcion
    time.sleep(1)
    pyautogui.press('down')
    time.sleep(1)
    pyautogui.press('enter')

    #************************************************************
    # Segunda busqueda buscar boton de Output
    print("[DEBUG] Busqueda Boton OUTPUT")
    busqueda_btn_Output = puente_busqueda_img(config.imagenes_Btn_Output, config.mensajes_busquedas_imagenes)
    
    # Validacion de busqueda Boton Output
    if busqueda_btn_Output in (None, False): return None
    
    #************************************************************
    # Sacar Mouse de pantalla
    print("[DEBUG] Sacar Mouse de pantalla")
    
    # Obtener posición actual del mouse
    x, y = pyautogui.position()

    # Mover el mouse 100 píxeles a la derecha
    pyautogui.moveTo(x + 100, y, duration=0.5)
    
    
    #************************************************************
    # Tercera busqueda buscar boton de confirmacion de reporte
    print("[DEBUG] Busqueda Boton reportes o OUTPUT waring")
    busqueda_btn_file = puente_busqueda_img(config.imagenes_Btn_Report_Waring, config.mensajes_busquedas_imagenes)
    
    # Validacion de busqueda Boton File
    if busqueda_btn_file in (None, False): return None
    
    # Aceptar
    pyautogui.press('enter')
    
    return True
    