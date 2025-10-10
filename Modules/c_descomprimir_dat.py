# c_descomprimir_dat.py

# ------------------------------------------------------------------
# Importaciones de librerías y configuraciónes Globales
# ------------------------------------------------------------------
import Config.config as config
import pyautogui
import time

# ------------------------------------------------------------------
# Importaciones de Modulos
# ------------------------------------------------------------------
from Monitor.log.log import agregar_log

# ------------------------------------------------------------------
# Importaciones de Utils
# ------------------------------------------------------------------
from Utils.validar_archivos_carpetas.validar_archivos import validar_archivos
from Utils.tools.puente_busqueda_img import puente_busqueda_img


#************************************************************
# Modulo que se encarga de automatizar la carga del archivo .dat
def descomprimir_dat(ruta_archivo_dat, lista_carpetas_principales):
    
    #************************************************************
    ancho, alto = pyautogui.size()  # Obtiene el tamaño de la pantalla
    pyautogui.moveTo(ancho / 2, alto / 2, duration=0.1)  # Mueve al centro en 0.1s
    time.sleep(1)
    
    #************************************************************
    # Primera busqueda buscar Boton File
    for i in range(12):
        agregar_log("[DEBUG] Busqueda Boton File...")
        busqueda_btn_file = puente_busqueda_img(config.imagenes_Btn_File, config.mensajes_busquedas_imagenes )
        
        # si busqueda_btn_fil retorna None o false lo intenta otra vez
        if busqueda_btn_file not in (None, False): break
        
        # si lo encoentra rompre el for
    else:
        agregar_log("[WARN] No se encontró Boton File tras 12 intentos.")
        return None, None
    
    #************************************************************
    # Segunda busqueda buscar Boton File Partition
    for i in range(12):
        agregar_log("[DEBUG] Busqueda Boton File Partition...")
        busqueda_btn_file_partition  = puente_busqueda_img(config.imagenes_Btn_File_Partition, config.mensajes_busquedas_imagenes)
        
        # si busqueda_btn_file_partition retorna None o false lo intenta otra vez
        if busqueda_btn_file_partition not in (None, False): break
        
        # si lo encoentra rompre el for
    else:
        agregar_log("[WARN] No se encontró Boton File Partition tras 12 intentos.")
        return None, None
    
    #************************************************************
    # Tercera busqueda buscar Boton Tres puntos
    for i in range(12):
        agregar_log("[DEBUG] Busqueda Boton Tres Puntos...")
        busqueda_btn_tres_puntos = puente_busqueda_img(config.imagenes_Btn_Tres_Puntos, config.mensajes_busquedas_imagenes)
        
        # si busqueda_btn_tres_puntos retorna None o false lo intenta otra vez
        if busqueda_btn_tres_puntos not in (None, False): break
        
        # si lo encoentra rompre el for
    else:
        agregar_log("[WARN] No se encontró Boton Tres Puntos tras 12 intentos.")
        return None, None    
    
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
    # Cuarta busqueda buscar Boton Tres Parce
    for i in range(12):
        agregar_log("[DEBUG] Busqueda Boton Parce...")
        busqueda_btn_parce = puente_busqueda_img(config.imagenes_Btn_Parce, config.mensajes_busquedas_imagenes)
        
        # si busqueda_btn_parce retorna None o false lo intenta otra vez
        if busqueda_btn_parce not in (None, False): break
        
        # si lo encoentra rompre el for
    else:
        agregar_log("[WARN] No se encontró Boton Parce tras 12 intentos.")
        return None, None   

    #************************************************************
    # Quinta busqueda buscar Ventana Partition_Complete
    for i in range(12):
        agregar_log(f"[DEBUG] Búsqueda Partition {i+1} Complete...")
        busqueda_ventana_partition_complete = puente_busqueda_img(config.imagenes_Btn_Parti_Com, config.mensajes_busquedas_imagenes)
        
        # si busqueda_ventana_partition_complete rotorna None o false lo intenta otra vez
        if busqueda_ventana_partition_complete not in (None, False): break
        
        # si lo encoentra rompre el for
    else:
        agregar_log("[WARN] No se encontró la ventana Partition Complete tras 12 intentos.")
        return None, None
           
    # Cerrar Ventana de Partition Complete
    pyautogui.press('enter')
    pyautogui.press('esc')
    
    #**********************************************************************
    # Buscar archivo .kqs
    agregar_log("------------------VALIDAR CREACION ARCHIVO .KQS------------------")
    ruta_archivo_kqs = validar_archivos(lista_carpetas_principales.get("Pos"), ".kqs")
    if ruta_archivo_kqs is False:
        agregar_log("[ERROR] Error al buscar el archivo .kqs")
        return None, None
    
    
    #************************************************************
    # Retornamos True si todo funciona bien
    return True, ruta_archivo_kqs