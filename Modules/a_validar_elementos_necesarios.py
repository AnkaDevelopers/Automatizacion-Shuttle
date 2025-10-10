# a_validar_elementos_necesarios.py

# ------------------------------------------------------------------
# Importaciones de librerías y configuraciónes globales
# ------------------------------------------------------------------
import Config.config as config
import os

# ------------------------------------------------------------------
# Importaciones de Modulos
# ------------------------------------------------------------------
from Monitor.log.log import agregar_log


# ------------------------------------------------------------------
# Importaciones de Utils
# ------------------------------------------------------------------
from Utils.validar_archivos_carpetas.validar_carpetacion import validar_carpetacion
from Utils.validar_archivos_carpetas.validar_archivos import validar_archivos
from Utils.validar_archivos_carpetas.validar_archivos_obs import validar_archivo_obs


# ------------------------------------------------------------------
# Función: validar_elementos_requeridos_particion_dat
# ------------------------------------------------------------------
# Este módulo revisa si el proyecto tiene todo lo necesario
# para que el RPA funcione correctamente.
#
# Qué hace:
# 1. Comprueba que la ruta del proyecto exista.
# 2. Revisa que estén las carpetas principales (“base” y “Pos”).
# 3. Busca los archivos requeridos (.kqs, .dat, .obs).
#
# Qué devuelve:
#   - (False, None, None): si falta algo o hay un error.
#   - (True, lista_carpetas_principales, ruta_archivo_dat, ruta_archivo_observado): si no se encontró el .kqs pero sí .dat 
#   - (None, lista_carpetas_principales, ruta_archivo_kqs, ruta_archivo_observado): si se encontró el .kqs (ya está todo listo).
# ------------------------------------------------------------------

#***********************************************************************************************
# Funcion encargadade validar los requisitos minimos para el RPA 
def validar_elementos_requeridos_particion_dat(ruta_proyecto):
        
    try:
        #**********************************************************************
        # Validar ruta del proyecto
        agregar_log("----------------VALIDAR RUTA DE PROYECTO----------------")
        if not os.path.exists(ruta_proyecto):
            agregar_log(f"[ERROR] La ruta {ruta_proyecto} no existe o no se encontro")
            return 0, None, None
        # Ruta encontrada
        agregar_log(f"Ruta encontrada exitosamente {ruta_proyecto}")
        
        #**********************************************************************
        # Validación de carpetación
        agregar_log("-----------------VALIDAR CARPETAS NECESARIAS----------------")
        lista_carpetas_principales = validar_carpetacion(ruta_proyecto, ["base","Pos"])
        if lista_carpetas_principales is None:
            agregar_log("[ERROR] Error en la carpetación")
            return 1, None, None
        
        # Carpetas necesarias encontradas
        agregar_log(f"Carpetas encontradas exitosamente {lista_carpetas_principales}")

        #**********************************************************************
        # Buscar archivo observado
        agregar_log("------------------VALIDAR ARCHIVO .OBS------------------")
        ruta_archivo_observado = validar_archivo_obs(lista_carpetas_principales.get("base"))
        if ruta_archivo_observado is None:
            agregar_log("[ERROR] Error al buscar archivo Observado")
            return 4, None, None

        #**********************************************************************
        # Buscar archivo .kqs
        agregar_log("------------------VALIDAR ARCHIVO .KQS------------------")
        ruta_archivo_kqs = validar_archivos(lista_carpetas_principales.get("Pos"), ".kqs")
        if ruta_archivo_kqs is False:
            agregar_log("[ERROR] Error al buscar el archivo .kqs")
            return 2, None, None
        
        # Ruta en caso de que el .dat no halla sido descomprimido 
        if ruta_archivo_kqs is None:
            agregar_log("No se encontro el archivo .kqs")
                
            #**********************************************************************
            # Buscar archivo .dat
            agregar_log("------------------VALIDAR ARCHIVO .DAT------------------")
            ruta_archivo_dat = validar_archivos(lista_carpetas_principales.get("Pos"), ".dat")
            if ruta_archivo_dat is None:
                agregar_log("[ERROR] Error al buscar el archivo .dat")
                return 3, None, None
        
            
            # Si todo marcha bien retornar rutas
            return True, lista_carpetas_principales, ruta_archivo_dat, ruta_archivo_observado
        
        # Si se encuentra el archivo .kqs quiere decir que el .dat y aha sido descomprimido
        return None, lista_carpetas_principales, ruta_archivo_kqs, ruta_archivo_observado
    
    #**********************************************************************
    # Manejo de errores inesperados
    except Exception as e:
        agregar_log(f"[EXCEPTION] Error inesperado al validar la ruta '{ruta_proyecto}': {e}")
        return False, None, None