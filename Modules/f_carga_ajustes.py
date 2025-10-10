# f_carga_ajuste.py

# ------------------------------------------------------------------
# Importaciones de Utils necesarios
# ------------------------------------------------------------------
from Utils.tools.puente_busqueda_img import puente_busqueda_img
from Utils.tools.esperar_cambio_region import esperar_cambio_region
from Utils.tools.captur import capturar_region_centrada
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
# Función: carga_ajuste
# ------------------------------------------------------------------
# Automatiza la carga de los siguientes archivos:
# 
# IMU.imu
# GNSS.txt
# KQS.evt
#
# Parámetros:
#   - Lista con las 3 rutas 
#    
#
# Retorna:
#   - True  -> si todo el flujo se completa correctamente.
#   - None  -> si alguna búsqueda/acción crítica falla.
def carga_ajuste(rutas_archivos, ruta_proyecto):

    #************************************************************
    # Primera busqueda buscar Boton Agregar Archivos
    agregar_log("[DEBUG] Busqueda Boton Agregar Archivos")
    busqueda_btn_Nuevo_Archivo = puente_busqueda_img(config.imagenes_Btn_Nuevo_Archivo , config.mensajes_busquedas_imagenes)
    
    # Validacion Boton Agregar Archivos
    if busqueda_btn_Nuevo_Archivo in (None, False): return None
    
    # Espera de carga 
    time.sleep(2)
    
    #************************************************************
    # Segunda busqueda buscar Boton Imu
    agregar_log("[DEBUG] Busqueda Boton Imu")
    busqueda_btn_Imu = puente_busqueda_img(config.imagenes_Btn_Imu , config.mensajes_busquedas_imagenes)
    
    # Validacion Boton Imu
    if busqueda_btn_Imu in (None, False): return None
    
    # Espera de carga 
    time.sleep(2)
    
    #************************************************************
    # Ingresar Ruta Imu
    pyautogui.press("backspace")
    pyautogui.write(f"{rutas_archivos[0]}")
    pyautogui.press("tab", presses=4, interval=0.2)
    pyautogui.press("n")
    
    #************************************************************
    # Tercera busqueda buscar Boton Results
    agregar_log("[DEBUG] Busqueda Boton Results")
    busqueda_btn_Results = puente_busqueda_img(config.imagenes_Btn_Results , config.mensajes_busquedas_imagenes)
    
    # Validacion Boton Results
    if busqueda_btn_Results in (None, False): return None
    
    # Espera de carga 
    time.sleep(2)
    
    #************************************************************
    # Ingresar Ruta Gnss.txt y Ruta KQS.evt
    pyautogui.press("backspace")
    pyautogui.write(f"{rutas_archivos[1]}")
    pyautogui.press("tab", presses=2, interval=0.2)
    pyautogui.press("backspace")
    pyautogui.write(f"{rutas_archivos[2]}")
    
    #************************************************************
    # Cuarta busqueda buscar Boton Aceptar
    pyautogui.press('tab',presses=2, interval=0.2)
    pyautogui.press('enter')
    # Espera de carga 
    time.sleep(20)
    
    #************************************************************
    # Quinta busqueda buscar Boton Integration Gnss
    agregar_log("[DEBUG] Busqueda Boton Integration Gnss")
    busqueda_btn_Integration_Gnss = puente_busqueda_img(config.imagenes_Btn_Integration_Gnss, config.mensajes_busquedas_imagenes)
    
    # Validacion Boton Integration Gnss
    if busqueda_btn_Integration_Gnss in (None, False): return None
    
    # Espera de carga Kinematic
    agregar_log("[INFO] Esperando procesamiento Kinematic...")
    
    # Centro de pantalla
    centro_barra = (960,540)
    
    if not esperar_cambio_region(mouse_pos=centro_barra, radio=400, timeout=300, intervalo=1.0, umbral=0.01):
        agregar_log("[WARN] No se detectó cambio visual en la barra de progreso tras timeout")
        return False
    ruta = f'{ruta_proyecto}'
    ruta_img = f"{ruta_proyecto}/pos.png"
    
    # --- Captura centrada en (927,400) con radio 500; se sobrescribe siempre ---
    capturar_region_centrada(960, 540, 400, f"{ruta_img}")
    
    #************************************************************
    # Sexta busqueda buscar Boton Report Waring
    agregar_log("[DEBUG] Busqueda Boton Export Pos")
    busqueda_btn_Export_Pos = puente_busqueda_img(config.imagenes_Btn_Export_Pos, config.mensajes_busquedas_imagenes)
    
    # Validacion Boton Export Pos
    if busqueda_btn_Export_Pos in (None, False): return None
    
    # Seleccion de ruta y nombre archivo POS
    pyautogui.press('tab')
    pyautogui.press('enter')
    pyautogui.press('tab', presses=5, interval=0.2)
    
    # Escribir ruta
    pyautogui.press('enter')
    pyautogui.press('backspace')
    pyautogui.write(ruta)
    pyautogui.press('enter')
   
    
    # Escribir nombre de archivo
    pyautogui.press('tab', presses=6, interval=0.2)
    pyautogui.write(f'Preciso_gnss')
    pyautogui.press('enter')

    # Seleccionar Pos como exportacion
    pyautogui.press('tab', presses=6, interval=0.2)
    pyautogui.press('down')
    pyautogui.press('enter')

    #************************************************************
    # Centro de pantalla
    centro_barra = (960,540)
    
    if not esperar_cambio_region(mouse_pos=centro_barra, radio=400, timeout=300, intervalo=1.0, umbral=0.01):
        agregar_log("[WARN] No se detectó cambio visual en la barra de progreso tras timeout")
        return False
    
    #************************************************************
    # Septima busqueda buscar Boton File
    for i in range(12):
        agregar_log("[DEBUG] Busqueda Boton Report Waring")
        Btn_Waring_Precises = puente_busqueda_img(config.imagenes_Btn_Waring_Precises, config.mensajes_busquedas_imagenes)
        
        # si Btn_Waring_Precises retorna None o false lo intenta otra vez
        if Btn_Waring_Precises not in (None, False): break
        
        # si lo encoentra rompre el for
    else:
        agregar_log("[WARN] No se encontró Boton File tras 12 intentos.")
        return None, None

    #************************************************************  
    # Damos enter
    pyautogui.press('enter')
    #************************************************************  
    # cerrar el txt
    cerrar_todos_txt("Preciso_gnss")
    
    

    
    
    #************************************************************
    return True
    