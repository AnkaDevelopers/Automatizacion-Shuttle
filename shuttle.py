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
    ruta_proyecto = config.rutaProyecto[1]
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
    
    # Validacion en caso de error al ejecutar las configuraciones
    if estado_combinaciones is False:
        print("Envia correo al equipo de soporte sobre la falla") # hay que trabajar en esta parte
        return 
    
    time.sleep(1000)
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
    """
     
    try:
        
        
    #**********************************************************************
    # RPA 3: generar reporte
    agregar_log("#################-GENERAR PRIMER REPORTE-#################")
    rta_rpa_tres = generar_reporte()
        if rta_rpa_tres is None:
        agregar_log("[ERROR] Error en rpa tres (generar reporte)")
            return
        #**********************************************************************
        
        
        # Buscar archivo .txt
        agregar_log("#################-VALIDAR CREACION PRIMER REPORTE GNSS-#################")
        ruta_archivo_gnss_txt = validar_archivos(lista_carpetas_principales.get("Pos"), ".txt")
        if ruta_archivo_gnss_txt is None:
            agregar_log("[ERROR] Error al buscar el archivo .txt")
            return

        
        #**********************************************************************
        # Validación inicial del reporte
        agregar_log("#################-VALIDAR PORCENTAJE DE ACIERTO REPORTE GNSS-#################")
        rta_validar_txt, porcentaje = validar_txt(ruta_archivo_gnss_txt)
        if rta_validar_txt is False:
            agregar_log("[ERROR] Error en validación del reporte")
            return

        if rta_validar_txt is True:
            # Ya es válido (≥90%), no hace falta ajuste_gnss
            agregar_log("[INFO] log: Validación funcionó")
            mensaje_en_pantalla(f"[OK] Porcentaje válido: {porcentaje:.2f}%")
            
        
        #**********************************************************************
        # Si no alcanzó el 90%, ejecutar ajuste_gnss
        if rta_validar_txt is None:
            agregar_log("#################-VALIDAR COMBINACION GNSS-#################")
            resultado = ajuste_gnss(ruta_archivo_gnss_txt)

            # Error crítico en la automatización de GNSS
            if resultado is False:
                agregar_log("[ERROR] Error en configuración de GNSS")
                return

            # Éxito: (True, porc, cfg, mask)
            if isinstance(resultado, tuple) and resultado[0] is True:
                _, porc, cfg, mask = resultado
                mensaje_en_pantalla(f"[OK] {porc:.2f}% | {formatear_config(cfg)} | Mascara {mask}")
                agregar_log(f"[INFO] log: Validación funcionó, [OK] {porc:.2f}% | {formatear_config(cfg)} | Mascara {mask}")
                

            # Mejor intento: (None, porc, cfg, mask)
            if isinstance(resultado, tuple) and resultado[0] is None:
                _, porc, cfg, mask = resultado
                if cfg is not None:
                    mensaje_en_pantalla(f"[INFO] Mejor intento {porc:.2f}% | {formatear_config(cfg)} | Mascara {mask}")
                    agregar_log(f"[INFO] Mejor intento {porc:.2f}% | {formatear_config(cfg)} | Mascara {mask}")
                else:
                    mensaje_en_pantalla("[INFO] No hubo porcentajes válidos en las pruebas.")
                    agregar_log("[INFO] No hubo porcentajes válidos en las pruebas.")
                    
                agregar_log("[INFO] log: Validación funcionó")
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
        resultado_carga_ajuste = carga_ajuste([ruta_archivo_imu,ruta_archivo_gnss_txt,ruta_archivo_evt])
        
        if resultado_carga_ajuste is None:
            agregar_log("Error en carga Ajuste")
            return 
        
    finally:
        # Cierra shuttle 
        time.sleep(600)  
        cerrar_shuttle()
        guardar_log_en_archivo("shuttle")
        pass
    """

# EJECUCION
shuttle()
