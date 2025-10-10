# ajuste_gnss.py

# ------------------------------------------------------------------
# Importaciones de librerías y configuraciónes Globales
# ------------------------------------------------------------------
from typing import Tuple, Optional, Iterable
import Config.config as config
import numpy as np  # <-- añadido para limpiar la captura
import pyautogui
import time
import os  # <-- añadido

# ------------------------------------------------------------------
# Importaciones de Modulos
# ------------------------------------------------------------------
from Monitor.log.log import agregar_log

# ------------------------------------------------------------------
# Importaciones de Utils
# ------------------------------------------------------------------
from Utils.tools.puente_busqueda_img import puente_busqueda_img
from Utils.tools.esperar_cambio_region import esperar_cambio_region
from Utils.validar_archivos_carpetas.validar_txt import validar_txt
from Utils.tools.mensaje_en_pantalla import mensaje_en_pantalla



# Coordenadas de FALLBACK (clic directo si falla el reconocimiento)
FALLBACKS = {
    "Options": (360, 62),      # Botón Options (menú superior)
    "OutputMenu": (359, 30),   # Botón/menú Output (barra superior)
}

# Ruta del archivo donde se guardará SIEMPRE la mejor captura (se sobreescribe)
CAPTURA_MEJOR_PATH = "debug_monitoreo/captura_mejor_porcentaje.png"  # <-- añadido

# ------------------------------------------------------------------
# Helpers internos
# ------------------------------------------------------------------

def _texto_use(flag: bool) -> str:
    return "Use" if flag else "Don't Use"

def _force_click(x: int, y: int, label: str = "") -> bool:
    """Clic directo en coordenadas provistas como último recurso."""
    try:
        agregar_log(f"[FALLBACK] Click directo en {label or 'coords'} ({x},{y})")
        # Aparcar el mouse primero en una esquina para no tapar UI
        sw, sh = pyautogui.size()
        pyautogui.moveTo(sw - 5, sh - 5, duration=0.12)
        # Ir al punto de fallback y clic
        pyautogui.moveTo(x, y, duration=0.18)
        pyautogui.click()
        time.sleep(0.4)
        return True
    except Exception as e:
        agregar_log(f"[FALLBACK-ERROR] No se pudo clickeár fallback {label}: {e}")
        return False

def _try_click(dataset_imagenes: Iterable[str], mensajes: Iterable[str], fallback_key: Optional[str] = None) -> bool:
    """
    1) Intenta con el puente (búsqueda por imagen en pantalla completa).
    2) Si falla y hay fallback_key -> clic directo en coordenadas de FALLBACKS.
    Devuelve True si alguno de los dos métodos logra hacer clic.
    """
    ok = puente_busqueda_img(data_set_imagenes=dataset_imagenes, data_set_mensajes=mensajes)
    if ok is True:
        return True

    # Si el puente no encontró (None/False) y hay fallback definido, clic directo
    if fallback_key and fallback_key in FALLBACKS:
        fx, fy = FALLBACKS[fallback_key]
        return _force_click(fx, fy, label=fallback_key)

    return False

def _aplicar_constelaciones(gps: bool, glo: bool, gal: bool, bds: bool) -> bool:
    """
    Asume que ya estamos dentro de la ventana de 'GNSS User Params'
    y que los campos se alcanzan navegando con 'down' + 'tab' como en tu flujo actual.
    Ajusta: GPS, GLO, GAL, BDS en ese orden.
    Devuelve False si alguna búsqueda/entrada crítica falla.
    """
    time.sleep(1)

    # Abrir Options -> GNSS User Params
    agregar_log("[DEBUG] Buscar Boton Options")
    if not _try_click(config.imagenes_Btn_Options, config.mensajes_busquedas_imagenes, fallback_key="Options"):
        if not _try_click(config.imagenes_Btn_Options, config.mensajes_busquedas_imagenes, fallback_key="Options"):
            return False

    # Seleccionar opcion Gnss User Params
    agregar_log("[DEBUG] Buscar Boton Gnss User Params")
    if not _try_click(config.imagenes_Btn_Gnss_User_Params, config.mensajes_busquedas_imagenes):
        if not _try_click(config.imagenes_Btn_Gnss_User_Params, config.mensajes_busquedas_imagenes):
            return False

    # GPS
    time.sleep(2)
    pyautogui.press('down')  # ir a GPS
    pyautogui.press('tab')
    pyautogui.press('backspace')
    texto_gps = _texto_use(gps)
    pyautogui.write(texto_gps)

    # Re-enfocar panel
    if not _try_click(config.imagenes_Btn_Gnss_User_Params, config.mensajes_busquedas_imagenes):
        return False

    # GLO
    time.sleep(2)
    pyautogui.press('down', presses=2, interval=0.2)  # ir a GLO
    pyautogui.press('tab')
    pyautogui.press('backspace')
    texto_glo = _texto_use(glo)
    pyautogui.write(texto_glo)

    if not _try_click(config.imagenes_Btn_Gnss_User_Params, config.mensajes_busquedas_imagenes):
        return False

    # GAL
    time.sleep(2)
    pyautogui.press('down', presses=3, interval=0.2)  # ir a GAL
    pyautogui.press('tab')
    texto_gal = _texto_use(gal)
    if texto_gal == "Use":
        pyautogui.press('U')
    else:
        pyautogui.press('D')

    if not _try_click(config.imagenes_Btn_Gnss_User_Params, config.mensajes_busquedas_imagenes):
        return False

    # BDS
    time.sleep(2)
    pyautogui.press('down', presses=4, interval=0.2)  # ir a BDS
    pyautogui.press('tab')
    pyautogui.press('backspace')
    texto_bds = _texto_use(bds)
    pyautogui.write(texto_bds)

    return True

def _aplicar_mascara(valor_mascara: int | float) -> bool:
    # Navega al campo de máscara y escribe el valor_mascara (1..18)
    agregar_log(f"[DEBUG] configurar mascara valor: {valor_mascara}")

    if not _try_click(config.imagenes_Btn_Gnss_User_Params, config.mensajes_busquedas_imagenes):
        return False

    time.sleep(0.5)
    pyautogui.press('down', presses=6, interval=0.2)  # llegar al campo máscara (según tu flujo)
    pyautogui.press('tab')
    pyautogui.write(f"{float(valor_mascara)}")
    # Guardar Default
    pyautogui.press('tab', presses=3, interval=0.1)
    pyautogui.press('enter')
    # Aceptar configuración
    pyautogui.press('tab')
    pyautogui.press('enter')

    return True

def _ejecutar_cinematica_y_generar_reporte() -> bool:
    """
    Dispara el proceso Kinematic, espera, abre menú de Reporte/Output y confirma.
    Retorna False si falla algo crítico.
    """
    # Buscar y entrar a Kinematic diferencial GNSS
    agregar_log("[DEBUG] Busqueda Boton Kinematic diferencial GNSS")
    if not _try_click(config.imagenes_Btn_Kinematic, config.mensajes_busquedas_imagenes, "Kinematic"):
        return False

    # --- Espera por procesamiento dinámico ---
    agregar_log("[INFO] Esperando procesamiento Kinematic...")
    # Coordenada de pantalla
    centro_barra = (960, 540)

    if not esperar_cambio_region(mouse_pos=centro_barra, radio=400, timeout=300, intervalo=1.0, umbral=0.01):
        agregar_log("[WARN] No se detectó cambio visual en la barra de progreso tras timeout")
        return False

    # Ir a Reporte / OUTPUT (menú)
    agregar_log("[DEBUG] Busqueda Boton reportes ")
    if not _try_click(config.imagenes_Btn_Report, config.mensajes_busquedas_imagenes):
        return False  # si no aparece, consideramos falla crítica para esta corrida

    time.sleep(1)
    pyautogui.press('down')
    time.sleep(1)
    pyautogui.press('enter')

    # Botón/ventana OUTPUT (intento por imagen; si falla, fallback al menú superior)
    agregar_log("[DEBUG] Busqueda Boton OUTPUT 1")
    if not _try_click(config.imagenes_Btn_Output, config.mensajes_busquedas_imagenes):
        return False

    # (Opcional) Sacar mouse de la zona
    agregar_log("[DEBUG] Sacar Mouse de pantalla")
    x, y = pyautogui.position()
    pyautogui.moveTo(x + 100, y, duration=0.5)

    # Confirmación warning de reporte
    agregar_log("[DEBUG] Busqueda Boton reportes o OUTPUT warning")
    if not _try_click(config.imagenes_Btn_Report_Waring, config.mensajes_busquedas_imagenes, "ReportWarning"):
        return False

    pyautogui.press('enter')
    time.sleep(10)
    return True

def _capturar_region_centrada(x: int, y: int, radio: int, ruta_salida: str) -> bool:
    """
    Captura una región centrada en (x,y) con 'radio' px (cuadrado 2*radio),
    limpia grilla/UI dejando solo trazas sobre negro, recorta al contenido
    y guarda en 'ruta_salida' sobrescribiendo si existe.
    """
    try:
        sw, sh = pyautogui.size()
        left = max(0, x - radio)
        top = max(0, y - radio)
        width = min(2 * radio, sw - left)
        height = min(2 * radio, sh - top)

        # 1) Captura
        img = pyautogui.screenshot(region=(left, top, width, height))  # PIL.Image

        # 2) Limpieza por saturación/luminosidad (elimina grises de grilla y UI)
        SAT_MIN = 60  # súbelo si aún ves grilla tenue
        VAL_MIN = 40
        hsv_np = np.array(img.convert("HSV"))
        s = hsv_np[:, :, 1]
        v = hsv_np[:, :, 2]
        mask = (s > SAT_MIN) & (v > VAL_MIN)

        rgb_np = np.array(img)
        rgb_np[~mask] = [0, 0, 0]  # fondo negro

        # 3) Recorte automático al contenido detectado
        ys, xs = np.where(mask)
        if ys.size and xs.size:
            PADDING = 8
            y0 = max(0, ys.min() - PADDING)
            y1 = min(rgb_np.shape[0], ys.max() + 1 + PADDING)
            x0 = max(0, xs.min() - PADDING)
            x1 = min(rgb_np.shape[1], xs.max() + 1 + PADDING)
            rgb_np = rgb_np[y0:y1, x0:x1]

        # 4) Guardado (sobrescribe). Reutiliza PIL desde pyautogui para no añadir imports.
        dir_out = os.path.dirname(ruta_salida)
        if dir_out:
            os.makedirs(dir_out, exist_ok=True)
        Image = pyautogui._pyautogui_imports.Image  # PIL.Image
        Image.fromarray(rgb_np).save(ruta_salida)

        agregar_log(f"[CAPTURA] Guardada captura limpia en {ruta_salida} (left={left}, top={top}, w={width}, h={height})")
        return True

    except Exception as e:
        # Fallback: si algo falla, guarda la captura original sin limpiar
        try:
            if 'img' in locals():
                dir_out = os.path.dirname(ruta_salida)
                if dir_out:
                    os.makedirs(dir_out, exist_ok=True)
                img.save(ruta_salida)
                agregar_log(f"[CAPTURA-FALLBACK] Guardada captura sin limpiar por error: {e}")
                return True
        except Exception as e2:
            agregar_log(f"[CAPTURA-ERROR] No se pudo guardar captura: {e2}")
        return False


# ------------------------------------------------------------------
#  Función principal: ajuste_gnss
# ------------------------------------------------------------------
#    Automatiza todas las posibles configuraciones (15 combinaciones de constelaciones válidas)
#    y para cada una prueba las 18 máscaras (1..18), hasta encontrar una que logre porcentaje >= 90%.
#    
#    Retorna:
#        - (True, porcentaje, (gps,glo,gal,bds), mascara)   -> si alguna configuración logra >= 90%
#        - (None, mejor_porcentaje, mejor_config, mejor_mascara) -> si ninguna lo logra (mejor intento)
#        - False -> si ocurre un error crítico de automatización/búsquedas
# ------------------------------------------------------------------
    

def ajuste_gnss():


    configuraciones = config.combinaciones_constelaciones
    agregar_log(configuraciones)
    mejor_porcentaje: float = -1.0
    mejor_config: Optional[Tuple[bool, bool, bool, bool]] = None
    mejor_mascara: Optional[int] = None

    for idx, (gps, glo, gal, bds) in enumerate(configuraciones, start=1):

        agregar_log(f"[INFO] Probando configuración #{idx}: GPS={gps}, GLO={glo}, GAL={gal}, BDS={bds}")
        # Aplicar constelaciones
        if not _aplicar_constelaciones(gps, glo, gal, bds):
            agregar_log("[ERROR] No se pudo aplicar constelaciones.")
            return False

        # Probar máscaras 1..18
        for mascara in range(10, 19):

            if mascara > 1:

                # Abrir Options -> GNSS User Params
                agregar_log("[DEBUG] Buscar Boton Options")
                if not _try_click(config.imagenes_Btn_Options, config.mensajes_busquedas_imagenes, fallback_key="Options"):
                    if not _try_click(config.imagenes_Btn_Options, config.mensajes_busquedas_imagenes, fallback_key="Options"):
                        return False

                # Seleccionar opcion Gnss User Params
                agregar_log("[DEBUG] Buscar Boton Gnss User Params")
                if not _try_click(config.imagenes_Btn_Gnss_User_Params, config.mensajes_busquedas_imagenes):
                    if not _try_click(config.imagenes_Btn_Gnss_User_Params, config.mensajes_busquedas_imagenes):
                        return False

            if not _aplicar_mascara(mascara):
                agregar_log(f"[ERROR] Fallo al aplicar máscara {mascara}")
                return False

            # Ejecutar proceso y generar reporte
            if not _ejecutar_cinematica_y_generar_reporte():
                agregar_log("[WARN] Fallo en ejecución/Reporte para esta corrida. Continúo con siguiente máscara.")
                continue  # no es crítico a nivel global; probamos siguiente máscara

            # Validar reporte
            rta_validar_txt, porcentaje = validar_txt(ruta_archivo_gnss_txt)

            if rta_validar_txt is False:
                agregar_log("[ERROR] Error en validación del reporte .txt")
                continue
            
            mensaje_en_pantalla(f"[INFO] Porcentaje {porcentaje:.2f}% | {idx} | Mascara {mascara}")
            
            
            
            # si el porcentaje es mayor al 97%
            if porcentaje > 96.0 and porcentaje < 100:
                
                # Abrir Options -> GNSS User Params
                agregar_log("[DEBUG] Buscar Boton Options")
                if not _try_click(config.imagenes_Btn_Options, config.mensajes_busquedas_imagenes, fallback_key="Options"):
                    if not _try_click(config.imagenes_Btn_Options, config.mensajes_busquedas_imagenes, fallback_key="Options"):
                        return False

                # Seleccionar opcion Gnss User Params
                agregar_log("[DEBUG] Buscar Boton Gnss User Params")
                if not _try_click(config.imagenes_Btn_Gnss_User_Params, config.mensajes_busquedas_imagenes):
                    if not _try_click(config.imagenes_Btn_Gnss_User_Params, config.mensajes_busquedas_imagenes):
                        return False
                    
                mascara_float = mascara - 0.5
                
                # Aplicar mascara con decimales
                if not _aplicar_mascara(mascara_float):
                    agregar_log(f"[ERROR] Fallo al aplicar máscara {mascara}")
                    continue
                
                # Ejecutar proceso y generar reporte
                if not _ejecutar_cinematica_y_generar_reporte():
                    agregar_log("[WARN] Fallo en ejecución/Reporte para esta corrida. Continúo con siguiente máscara.")
                    continue  # no es crítico a nivel global; probamos siguiente máscara

                # Validar reporte
                rta_validar_txt, porcentaje = validar_txt(ruta_archivo_gnss_txt)

                if rta_validar_txt is False:
                    agregar_log("[ERROR] Error en validación del reporte .txt")
                    continue
                
                if porcentaje < 98.0:
                    
                    # Abrir Options -> GNSS User Params
                    agregar_log("[DEBUG] Buscar Boton Options")
                    if not _try_click(config.imagenes_Btn_Options, config.mensajes_busquedas_imagenes, fallback_key="Options"):
                        if not _try_click(config.imagenes_Btn_Options, config.mensajes_busquedas_imagenes, fallback_key="Options"):
                            return False

                    # Seleccionar opcion Gnss User Params
                    agregar_log("[DEBUG] Buscar Boton Gnss User Params")
                    if not _try_click(config.imagenes_Btn_Gnss_User_Params, config.mensajes_busquedas_imagenes):
                        if not _try_click(config.imagenes_Btn_Gnss_User_Params, config.mensajes_busquedas_imagenes):
                            return False     

                    mascara_float = mascara + 0.5
                    
                    # Aplicar mascara con decimales
                    if not _aplicar_mascara(mascara_float):
                        agregar_log(f"[ERROR] Fallo al aplicar máscara {mascara}")
                        continue
                    
                    # Ejecutar proceso y generar reporte
                    if not _ejecutar_cinematica_y_generar_reporte():
                        agregar_log("[WARN] Fallo en ejecución/Reporte para esta corrida. Continúo con siguiente máscara.")
                        continue  # no es crítico a nivel global; probamos siguiente máscara

                    # Validar reporte
                    rta_validar_txt, porcentaje = validar_txt(ruta_archivo_gnss_txt)

                    if rta_validar_txt is False:
                        agregar_log("[ERROR] Error en validación del reporte .txt")
                        continue
                
                mensaje_en_pantalla(f"[INFO] Porcentaje {porcentaje:.2f}% | {idx} | Mascara {mascara}")
                
                # --- Captura centrada en (927,400) con radio 500; se sobrescribe siempre ---
                _capturar_region_centrada(960, 540, 400, CAPTURA_MEJOR_PATH)
                
                if rta_validar_txt is True:
                    agregar_log(f"[OK] Porcentaje suficiente: {porcentaje:.2f}% con config {idx} y máscara {mascara_float}")
                    return True, porcentaje, (gps, glo, gal, bds), mascara
                
            
            
            if rta_validar_txt is True:
                agregar_log(f"[OK] Porcentaje suficiente: {porcentaje:.2f}% con config {idx} y máscara {mascara}")
                return True, porcentaje, (gps, glo, gal, bds), mascara

            # rta_validar_txt is None -> porcentaje insuficiente
            if porcentaje is not None and porcentaje > mejor_porcentaje:
                mejor_porcentaje = porcentaje
                mejor_config = (gps, glo, gal, bds)
                mejor_mascara = mascara
                time.sleep(2)
                # --- Captura centrada en (927,400) con radio 500; se sobrescribe siempre ---
                _capturar_region_centrada(960, 540, 400, CAPTURA_MEJOR_PATH)

            agregar_log(f"[INFO] Porcentaje insuficiente ({porcentaje}%). Sigo probando...")

        agregar_log(f"[INFO] Fin de máscaras para config #{idx}.")

    agregar_log("[RESULT] No se encontró configuración >= 90%.")
    return None, mejor_porcentaje, mejor_config, mejor_mascara
