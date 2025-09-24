# director_shuttle.py

# ------------------------------------------------------------------
# Importaciones de librerías y configuración
# ------------------------------------------------------------------
import Config.config as config
import os

# ------------------------------------------------------------------
# Importaciones de Modulos
# ------------------------------------------------------------------
from Utils.validar_carpetacion import validar_carpetacion
from Utils.validar_archivos import validar_archivos
from Utils.validar_archivos_obs import validar_archivo_obs
from Modules.gestion_shuttle import abrir_shuttle, cerrar_shuttle
from Modules.descomprimir_dat import descomprimir_dat
from Modules.cargar_observado import cargar_observado
from Modules.generar_reporte import generar_reporte
from Modules.validar_txt import validar_reporte


# IMPORTACIONES LIBRERIAS
import time

#***********************************************************************************************
# Funcion principal encargada del rpa de shuttle 
def director_shuttle():
    
    # En caso de que la ruta no exista
    if not os.path.exists(config.rutaProyecto):
        return print("[DEBUG] La ruta no existe")
        
    #**********************************************************************
    # Validacion la integridad de la carpetacion
    lista_carpetas_principales = validar_carpetacion(config.rutaProyecto, ["base","Pos"])
    
    if lista_carpetas_principales is None:
        return print ("[ERROR] Error en la carpetacion")
    
    #**********************************************************************
    # Validacion archivos necesarios
    ruta_archivo_dat = validar_archivos(lista_carpetas_principales.get("Pos"),".dat")
    
    if ruta_archivo_dat is None:
        return print("[ERROR] Error al buscar el archivo .dat")
    
    ruta_archivo_observado = validar_archivo_obs(lista_carpetas_principales.get("base"))
    
    if ruta_archivo_observado is None:
        return print("[ERROR] Error al buscar archivo Observado")
    
    #**********************************************************************
    # Ejecuta el shuttle segun el tipo de procesamiento
    rta_shuttle = abrir_shuttle(2)
    
    # Tiempo de espera para que se ejecute el programa Shuttle
    time.sleep(0)
    
    if rta_shuttle is None:
        return print("[ERROR] Falla al abrir el Shuttle")
     
    #**********************************************************************
    # Ejecución descomprimir .dat
    rta_rpa_uno = descomprimir_dat(ruta_archivo_dat)
    
    if rta_rpa_uno is None:  
        return print("[ERROR] Error en rpa Uno")
    
    #**********************************************************************
    # Validacion archivos necesarios
    ruta_archivo_kqs = validar_archivos(lista_carpetas_principales.get("Pos"), ".kqs")
    
    if ruta_archivo_kqs is None:
        return print("[ERROR] Error al buscar el archivo .dat")
    
    #**********************************************************************
    # Ejecución cargar archivo Observado
    rta_rpa_dos = cargar_observado(ruta_archivo_observado, ruta_archivo_kqs)
    
    if rta_rpa_dos is None:
        return print("[ERROR] Error en rpa dos")
    
    
    #**********************************************************************
    # Ejecución generar reporte
    rta_rpa_tres = generar_reporte()
    
    if rta_rpa_tres is None:
        cerrar_shuttle()
        return print("[ERROR] Error en rpa tres")
    
    #**********************************************************************
    # Validacion archivos necesarios
    ruta_archivo_gnss_txt = validar_archivos(lista_carpetas_principales.get("Pos"),".txt")
    
    if ruta_archivo_gnss_txt is None:
        return print("[ERROR] Error al buscar el archivo .txt")
    
    #**********************************************************************
    # Ejecucion de validacion reporte
    rta_validar_reporte = validar_reporte(ruta_archivo_gnss_txt)
    
    if rta_validar_reporte == False:
        return print("[ERROR] Error en validaciond el reporte")

    if rta_validar_reporte == None:
        print("[INFO] Nuevo ajuste")
        time.sleep(600)
        cerrar_shuttle()
    
    #**********************************************************************
    # Tiempo dev y validacion
    cerrar_shuttle()
    print(f"[INFO] log:{rta_validar_reporte} ")
    time.sleep(2000)
    
    
    








# EJECUCION
director_shuttle()    
    
    
    
    
    