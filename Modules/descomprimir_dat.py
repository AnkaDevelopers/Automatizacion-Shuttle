# descomprimir_dat.py

# ------------------------------------------------------------------
# Importaciones de Utils necesarios
# ------------------------------------------------------------------
from Utils.puente_busqueda_img import puente_busqueda_img


# IMPORTACIONES GLOBALES
import Config.config as config

# IMPORTACIONES ADICIONALES
import pyautogui
import time


#************************************************************
# Moduloq ue se encarga de automatizar la carga del archivo .dat
def descomprimir_dat(ruta_archivo_dat):
    
    #************************************************************
    ancho, alto = pyautogui.size()  # Obtiene el tamaño de la pantalla
    pyautogui.moveTo(ancho / 2, alto / 2, duration=0.1)  # Mueve al centro en 0.1s
    time.sleep(1)
    
    #************************************************************
    # Primera busqueda buscar Boton File
    print("Busqueda Boton File...")
    busqueda_btn_file = puente_busqueda_img(config.imagenes_Btn_File, config.mensajes_busquedas_imagenes )
        
    # Validacion de busqueda Boton File
    if busqueda_btn_file in (None, False): return None 
         
    #************************************************************
    # segunda busqueda buscar Boton File Partition
    print("Busqueda Boton File Partition...")
    busqueda_btn_file_partition  = puente_busqueda_img(config.imagenes_Btn_File_Partition, config.mensajes_busquedas_imagenes)
        
    # Validacion de busqueda Boton File Partition
    if busqueda_btn_file_partition in (None, False): return None
    
    #************************************************************
    # Tercera busqueda buscar Boton Tres puntos
    print("Busqueda Boton Tres Puntos...")
    busqueda_btn_tres_puntos = puente_busqueda_img(config.imagenes_Btn_Tres_Puntos, config.mensajes_busquedas_imagenes)
    
    # Validacion de busqueda Boton Tres Puntos
    if busqueda_btn_tres_puntos in (None, False): return None
    
    #************************************************************
    # Ingreso de la ruta a el archivo .dat
    pyautogui.press('tab', presses=5, interval=0.1)
    pyautogui.press('enter')
    
    # Separar la ruta de la carpeta del nombre del archivo
    ruta_carpeta_archivo_dat, nombre_archivo_dat = ruta_archivo_dat.rsplit("\\", 1)
    
    # Agregamos la barra al final de la carpeta
    ruta_carpeta_archivo_dat += "\\"
    
    # Escribimos la ruta a la carpeta del archivo .dat
    pyautogui.write(f'{ruta_carpeta_archivo_dat}')
    pyautogui.press('enter')
    
    # Selelcionar Archivo .dat
    pyautogui.press('tab', presses=6 ,interval=0.1)
    pyautogui.write(f'{nombre_archivo_dat}')
    pyautogui.press('enter')
    
    #************************************************************
    # Cuarta busqueda buscar Boton Parce
    busqueda_btn_parce = puente_busqueda_img(config.imagenes_Btn_Parce, config.mensajes_busquedas_imagenes)
    
    # Validacion de busqueda Boton Parce
    if busqueda_btn_parce in (None, False): return None
    
    #************************************************************
    # Quinta busqueda buscar Ventana de Advertencia
    print("Busqueda Ventana de Advertencia...")
    busqueda_ventana_advertencia = puente_busqueda_img(config.imagenes_Shut_Waring, config.mensajes_busquedas_imagenes)
    
    # Validacion de busqueda Ventana de Advertencia
    if busqueda_ventana_advertencia in (None, False):
        print("Esperando carga de archivos...")
        time.sleep(10)
    
    else:
        pyautogui.press('enter', presses=5, interval=0.1)
        print("Esperando carga de archivos...")
        time.sleep(27)  

    #************************************************************
    # Sexta busqueda buscar Ventana Partition_Complete
    print("Busqueda de Ventana Partition Complete...")
    busqueda_ventana_partition_complete = puente_busqueda_img(config.imagenes_Btn_Parti_Com, config.mensajes_busquedas_imagenes)
    
    # Validacion de busqueda Boton Parce
    if busqueda_ventana_partition_complete in (None, False): return None
    
    # Cerrar Ventana de Partition Complete
    pyautogui.press('enter')
    pyautogui.press('esc')
    
    #************************************************************
    # Retornamos True si todo funciona bien
    return True