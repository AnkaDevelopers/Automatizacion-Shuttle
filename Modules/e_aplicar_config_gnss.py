# e_aplicar_constelaciones.py

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
from Utils.tools.puente_busqueda_img import puente_busqueda_img




# ------------------------------------------------------------------
#  Función: aplicar_constelaciones
# ------------------------------------------------------------------
#    Ajusta: GPS, GLO, GAL, BDS en ese orden.
#    Devuelve False si alguna búsqueda/entrada crítica falla.
# ------------------------------------------------------------------
#********************************************************************
def aplicar_constelaciones(gps, glo, gal, bds):

    #************************************************************
    # Buscar Boton Boton Options
    for i in range(12):
        agregar_log("[DEBUG] Busqueda Boton Options...")
        busqueda_btn_options = puente_busqueda_img(config.imagenes_Btn_Options, config.mensajes_busquedas_imagenes)
        
        # si busqueda_btn_options retorna None o false lo intenta otra vez
        if busqueda_btn_options not in (None, False): break
        
        # si lo encoentra rompre el for
    else:
        agregar_log("[WARN] No se encontró Boton Options tras 12 intentos.")
        return None   

    #************************************************************
    # Buscar Boton Boton Gnss User Params
    for i in range(12):
        agregar_log("[DEBUG] Busqueda Boton Gnss User Params...")
        busqueda_btn_gnss_params = puente_busqueda_img(config.imagenes_Btn_Gnss_User_Params, config.mensajes_busquedas_imagenes)
        
        # si busqueda_btn_gnss_params retorna None o false lo intenta otra vez
        if busqueda_btn_gnss_params not in (None, False): break
        
        # si lo encuentra rompre el For
    else:
        agregar_log("[WARN] No se encontró Boton Gnss User Params tras 12 intentos.")
        return None   

    #************************************************************
    # GPS
    time.sleep(2)
    pyautogui.press('down')  # ir a GPS
    pyautogui.press('tab')
    pyautogui.press('backspace')
    texto_gps = "Use" if gps else "Don't Use"
    pyautogui.write(texto_gps)

    #************************************************************
    # Buscar Boton Boton Gnss User Params
    for i in range(12):
        agregar_log("[DEBUG] Busqueda Boton Gnss User Params...")
        busqueda_btn_gnss_params = puente_busqueda_img(config.imagenes_Btn_Gnss_User_Params, config.mensajes_busquedas_imagenes)
        
        # si busqueda_btn_gnss_params retorna None o false lo intenta otra vez
        if busqueda_btn_gnss_params not in (None, False): break
        
        # si lo encoentra rompre el for
    else:
        agregar_log("[WARN] No se encontró Boton Gnss User Params tras 12 intentos.")
        return None   

    #************************************************************    

    # GLO
    time.sleep(2)
    pyautogui.press('down', presses=2, interval=0.2)  # ir a GLO
    pyautogui.press('tab')
    pyautogui.press('backspace')
    texto_glo = "Use" if glo else "Don't Use"
    pyautogui.write(texto_glo)

    #************************************************************
    # Buscar Boton Boton Gnss User Params
    for i in range(12):
        agregar_log("[DEBUG] Busqueda Boton Gnss User Params...")
        busqueda_btn_gnss_params = puente_busqueda_img(config.imagenes_Btn_Gnss_User_Params, config.mensajes_busquedas_imagenes)
        
        # si busqueda_btn_gnss_params retorna None o false lo intenta otra vez
        if busqueda_btn_gnss_params not in (None, False): break
        
        # si lo encoentra rompre el for
    else:
        agregar_log("[WARN] No se encontró Boton Gnss User Params tras 12 intentos.")
        return None   

    #************************************************************

    # GAL
    time.sleep(2)
    pyautogui.press('down', presses=3, interval=0.2)  # ir a GAL
    pyautogui.press('tab')
    texto_gal = "Use" if gal else "Don't Use"
    if texto_gal == "Use":
        pyautogui.press('U')
    else:
        pyautogui.press('D')

    #************************************************************
    # Buscar Boton Boton Gnss User Params
    for i in range(12):
        agregar_log("[DEBUG] Busqueda Boton Gnss User Params...")
        busqueda_btn_gnss_params = puente_busqueda_img(config.imagenes_Btn_Gnss_User_Params, config.mensajes_busquedas_imagenes)
        
        # si busqueda_btn_gnss_params retorna None o false lo intenta otra vez
        if busqueda_btn_gnss_params not in (None, False): break
        
        # si lo encoentra rompre el for
    else:
        agregar_log("[WARN] No se encontró Boton Gnss User Params tras 12 intentos.")
        return None   

    #************************************************************

    # BDS
    time.sleep(2)
    pyautogui.press('down', presses=4, interval=0.2)  # ir a BDS
    pyautogui.press('tab')
    pyautogui.press('backspace')
    texto_bds = "Use" if bds else "Don't Use"
    pyautogui.write(texto_bds)

    return True



# ------------------------------------------------------------------
#  Función: aplicar_mascara
# ------------------------------------------------------------------
#    Ajusta: la mascara.
#    Devuelve False si falla.
# ------------------------------------------------------------------
#********************************************************************
def aplicar_mascara(valor_mascara: int | float):
    # Navega al campo de máscara y escribe el valor_mascara (1..18)
    agregar_log(f"[DEBUG] configurar mascara valor: {valor_mascara}")

    #************************************************************
    # Buscar Boton Boton Gnss User Params
    for i in range(12):
        agregar_log("[DEBUG] Busqueda Boton Gnss User Params...")
        busqueda_btn_gnss_params = puente_busqueda_img(config.imagenes_Btn_Gnss_User_Params, config.mensajes_busquedas_imagenes)
        
        # si busqueda_btn_gnss_params retorna None o false lo intenta otra vez
        if busqueda_btn_gnss_params not in (None, False): break
        
        # si lo encoentra rompre el for
    else:
        agregar_log("[WARN] No se encontró Boton Gnss User Params tras 12 intentos.")
        return None  
    #************************************************************
    time.sleep(0.5)
    pyautogui.press('down', presses=6, interval=0.2)  # llegar al campo máscara (según tu flujo)
    pyautogui.press('tab')
    pyautogui.write(f"{float(valor_mascara)}")
    # Aceptar configuración

    pyautogui.press('tab', presses=3, interval=0.2)
    pyautogui.press('enter')
    pyautogui.press('tab', presses=2, interval=0.2)
    pyautogui.press('enter')

    return True