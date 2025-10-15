# shuttle.py

# ------------------------------------------------------------------
# Importaciones de librerías y configuraciónes Globales
# ------------------------------------------------------------------
import Config.config as config
import time
import os

# ------------------------------------------------------------------
# Importaciones de Modulos
# ------------------------------------------------------------------
from Monitor.log.log import agregar_log, guardar_log_en_archivo
from Modules.a_validar_elementos_necesarios import validar_elementos_requeridos_particion_dat
from Modules.b_gestion_shuttle import abrir_shuttle, cerrar_shuttle
from Modules.c_descomprimir_dat import descomprimir_dat
from Modules.d_creacion_proyecto import creacion_proyecto
from Modules.e_ajuste_gnss import ajuste_gnss
from Modules.f_carga_ajustes import carga_ajuste


# ------------------------------------------------------------------
# Importaciones de Utils
# ------------------------------------------------------------------
from Utils.tools.formatear_config import formatear_config
from Utils.validar_archivos_carpetas.validar_archivos import validar_archivos



#***********************************************************************************************
# Funcion principal encargada del rpa de shuttle 
def shuttle():
    
    # ruta proyecto y ruta shuttle
    ruta_proyecto = config.rutaProyecto[4]
    ruta_shuttle = config.ruta_shuttle[1]
        
    #**********************************************************************
    # Validación de carpetación y archivos
    agregar_log("#################-VALIDAR ELMENTOS REQUERIDOS-#################")
    estado_insumos_proyecto, lista_carpetas_principales, ruta_archivo_kqs, ruta_archivo_observado = validar_elementos_requeridos_particion_dat(ruta_proyecto) #dev 0,1,2,3
    
    # En caso de que retorne False
    if type(estado_insumos_proyecto) is int:
        print("Envia correo al equipo de soporte sobre la falla") # hay que trabajar en esta parte
        return

    #**********************************************************************
    # Abrir Shuttle
    agregar_log("#################-ABRIR SHUTTLE-#################")
    estado_shuttle = abrir_shuttle(ruta_shuttle)  #dev 0,1
        
    # Validacion en caso de error al abrir el Shuttle
    if estado_shuttle is None:
        print("Envia correo al equipo de soporte sobre la falla") # hay que trabajar en esta parte
        return

    #**********************************************************************
    # En caso de que se deba descomprimir el archivo .dat    
    if estado_insumos_proyecto is True:
        
        #**********************************************************************
        # Descomprimir .dat
        agregar_log("#################-DESCOMPRIMIR DAT-#################")
        estado_descomprimir_dat, ruta_kqs = descomprimir_dat(ruta_archivo_kqs, lista_carpetas_principales)
        
        # Validacion en caso de error al extraer el .dat
        if estado_descomprimir_dat is None:  
            print("Envia correo al equipo de soporte sobre la falla") # hay que trabajar en esta parte
            return
        
        # Agregamos la tuta al archivo .kqs
        ruta_archivo_kqs = ruta_kqs
        
    #**********************************************************************
    # Creacion de proyecto
    #time.sleep(100)
    agregar_log("#################-CREACION DE UN NUEVO PROYECTO-#################")
    estado_creacion_proyecto = creacion_proyecto(ruta_archivo_observado, ruta_archivo_kqs)
    
    # Validacion en caso de error en la creacion de un nuevo proyecto
    if estado_creacion_proyecto is None:
        print("Envia correo al equipo de soporte sobre la falla") # hay que trabajar en esta parte
        return
    #**********************************************************************
    # Validar combinaciones GNSS
    
    
    agregar_log("#################-VALIDAR COMBINACION GNSS-#################")
    estado_combinaciones = ajuste_gnss(lista_carpetas_principales)
    
    cerrar_shuttle()
    
    # Validacion en caso de error al ejecutar las configuraciones
    if estado_combinaciones is False:
        print("Envia correo al equipo de soporte sobre la falla") # hay que trabajar en esta parte
        return 
    
    #**********************************************************************
    # Buscar archivo IMU.imu       
    agregar_log("#################-VALIDAR ARCHIVO IMU.imu -#################")
    ruta_archivo_imu = validar_archivos(lista_carpetas_principales.get("Pos"), ".imu")
    if ruta_archivo_imu is None:
        agregar_log("[ERROR] Error al buscar el archivo IMU.imu ")
        return        
    
    #**********************************************************************
    # Buscar archivo gnss.txt       
    agregar_log("#################-VALIDAR ARCHIVO GNSS.TXT-#################")
    ruta_archivo_gnss_txt = validar_archivos(lista_carpetas_principales.get("Pos"), ".txt")
    if ruta_archivo_gnss_txt is None:
        agregar_log("[ERROR] Error al buscar el archivo gnss.txt") 
        return   
             
    #**********************************************************************
    # Buscar archivo KQS.evt     
    agregar_log("#################-VALIDAR ARCHIVO KQS.evt-#################")
    ruta_archivo_evt = validar_archivos(lista_carpetas_principales.get("Pos"), ".evt")
    if ruta_archivo_evt is None:
        agregar_log("[ERROR] Error al buscar el archivo KQS.evt")
        return        
    #**********************************************************************
    # Carga Ajustes
    agregar_log("#################-CARGA AJUSTES-#################")
    resultado_carga_ajuste = carga_ajuste([ruta_archivo_imu,ruta_archivo_gnss_txt,ruta_archivo_evt],ruta_proyecto)
        
    if resultado_carga_ajuste is None:
        agregar_log("Error en carga Ajuste")
        return   

        pass
 
 
 
 
shuttle()
