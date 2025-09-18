# IMPORTACIONES DE MODULOS
from utils.capturarRuta import seleccionar_y_guardar_ruta_proyecto
from utils.validarCarpetacion import validar_carpetacion
from utils.AbrirShuttle import abrir_shuttle
from utils.validar_archivos import validar_archivos
from utils.seleccionar_kqs_observado import seleccionar_kqs_o_observado
from modules.rpa_config_inicial import rpa_uno

# IMPORTAR CONFIGURACIONES GLOBALES
import config.config as config

# IMPORTACIONES ADICIONALES
import time

#***********************************************************************************************
# Funcion principal encargada del rpa de shuttle 
def director_shuttle():
    
    # En caso de que la ruta no exista
    if config.rutaProyecto == "":
        
        # Capturar ruta carpeta proyecto Shuttle 
        rta_ruta_proyecto = seleccionar_y_guardar_ruta_proyecto()
     
        if rta_ruta_proyecto is None:
            return print("Falla al capturar la ruta del proyecto")
        
    #**********************************************************************
    # Validacion la integridad de la carpetacion
    rta_carpetacion = validar_carpetacion(config.rutaProyecto)
    
    if rta_carpetacion is None:
        return print ("Error en la carpetacion")
    
    #**********************************************************************
    # Validacion archivos necesarios
    rta_pos = validar_archivos(rta_carpetacion.get("pos"),"dat")
    
    if rta_pos is None:
        return print("Error al buscar el archivo")
    
    #**********************************************************************
    
    # pasar archivos temporales .kqs o Observado para RPA => Base/ .kqs,25o
    rta_base_temp = seleccionar_kqs_o_observado(rta_carpetacion.get("base"))
    
    if rta_base_temp is None:
        return print("No se encontro archivo .kqs ni archivo Observado")
     
    #**********************************************************************
    # Ejecuta el shuttle segun el tipo de procesamiento
    rta_shuttle = abrir_shuttle(0)
    
    if rta_shuttle is None:
        return print("Falla al abrir el Shuttle")
    
    # Ejecución rpa
    rta_rpa_uno = rpa_uno(rta_pos,rta_base_temp)
    
    if rta_rpa_uno is None:
        return print("Error en rpa Uno")
    
    # Tiempo dev y validacion
    print("log: ", rta_rpa_uno)
    time.sleep(200)
    
    
    






# EJECUCION
director_shuttle()    
    
    
    
    
    