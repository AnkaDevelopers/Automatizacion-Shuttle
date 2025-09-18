# IMPORTAR BUSCAR IMAGENES
from utils.buscar_img import buscar_y_click_en_set_imagenes


# IMPORTACIONES GLOBALES
import config.config as config

# IMPORTACIONES ADICIONALES
import pyautogui
import time


#************************************************************
def rpa_uno(rta_pos,rta_base_temp):
    
    ancho, alto = pyautogui.size()  # Obtiene el tamaño de la pantalla
    pyautogui.moveTo(ancho / 2, alto / 2, duration=0.1)  # Mueve al centro en 0.1s
    time.sleep(0.5)
    
    #************************************************************
    # Primera busqueda buscar Boton File
    busqueda = buscar_y_click_en_set_imagenes(config.imagenes_Btn_File, sensibilidad = 0.9)
        
    # segundo inteto busqueda de Boton File
    if not busqueda:
        print("⚠ No se encontró el iono de boton File.")
            
        busqueda = buscar_y_click_en_set_imagenes(config.imagenes_Btn_File, sensibilidad = 0.8)
            
        if not busqueda:
            
            busqueda = buscar_y_click_en_set_imagenes(config.imagenes_Btn_File, sensibilidad = 0.7)
            if not busqueda:
                msj_depuracion = "❌ No se encontró el iono de boton File"
                print(msj_depuracion)
                return None
    
    #************************************************************
    # segunda busqueda buscar Boton File
    busqueda = buscar_y_click_en_set_imagenes(config.imagenes_Btn_File_Partition, sensibilidad = 0.9)
        
    # segundo inteto busqueda de Boton File Partition
    if not busqueda:
        print("⚠ No se encontró el iono de boton File Partition.")
            
        busqueda = buscar_y_click_en_set_imagenes(config.imagenes_Btn_File_Partition, sensibilidad = 0.8)
            
        if not busqueda:
            
            busqueda = buscar_y_click_en_set_imagenes(config.imagenes_Btn_File_Partition, sensibilidad = 0.7)
            if not busqueda:
                msj_depuracion = "❌ No se encontró el iono de boton File Partition"
                print(msj_depuracion)
                return None
    
    
    #************************************************************
    # Tercera busqueda buscar Boton Tres puntos
    busqueda = buscar_y_click_en_set_imagenes(config.imagenes_Btn_Tres_Puntos, sensibilidad = 0.9)
        
    # segundo inteto busqueda de Boton Tres puntos
    if not busqueda:
        print("⚠ No se encontró el iono de Boton Tres puntos.")
            
        busqueda = buscar_y_click_en_set_imagenes(config.imagenes_Btn_Tres_Puntos, sensibilidad = 0.8)
            
        if not busqueda:
            
            busqueda = buscar_y_click_en_set_imagenes(config.imagenes_Btn_Tres_Puntos, sensibilidad = 0.7)
            if not busqueda:
                msj_depuracion = "❌ No se encontró el iono de Boton Tres puntos"
                print(msj_depuracion)
                return None
    
    #************************************************************
    # Colocar Primera Ruta
    pyautogui.press('tab', presses=5, interval=0.1)
    pyautogui.press('enter')
    
    # Formatear ruta
    rta_pos = rta_pos.rsplit("\\", 1)[0] + "\\"
    pyautogui.write(f'{rta_pos}')
    pyautogui.press('enter')
    
    # Selelcionar Archivo
    pyautogui.press('tab', presses=4 ,interval=0.1)
    pyautogui.press('space')
    pyautogui.press('enter')
    
    #************************************************************
    # Cuarta busqueda buscar Boton Parce
    busqueda = buscar_y_click_en_set_imagenes(config.imagenes_Btn_Parce, sensibilidad = 0.9)
        
    # segundo inteto busqueda de Boton Parce
    if not busqueda:
        print("⚠ No se encontró el iono de Boton Parce.")
            
        busqueda = buscar_y_click_en_set_imagenes(config.imagenes_Btn_Parce, sensibilidad = 0.8)
            
        if not busqueda:
            
            busqueda = buscar_y_click_en_set_imagenes(config.imagenes_Btn_Parce, sensibilidad = 0.7)
            if not busqueda:
                msj_depuracion = "❌ No se encontró el iono de Boton Parce"
                print(msj_depuracion)
                return None    
    
    #************************************************************
    # Quinta busqueda buscar Shuttle Waring
    busqueda = buscar_y_click_en_set_imagenes(config.imagenes_Shut_Waring, sensibilidad = 0.9)
    
    # En caso de que los archivos ya existan
    if busqueda:
        pyautogui.press('enter', presses=5, interval=0.1)
        print("Esperando carga de archivos...")
        time.sleep(27)
    if not busqueda:
        print("Esperando carga de archivos...")
        time.sleep(30)
    
    #************************************************************
    # Sexta busqueda buscar Boton Partition_Complete
    busqueda = buscar_y_click_en_set_imagenes(config.imagenes_Btn_Parti_Com, sensibilidad = 0.9)
    
    # segundo inteto busqueda de Boton Partition_Complete
    if not busqueda:
        
        print("⚠ No se encontró el iono de Boton Partition_Complete.")
        print("Reintentando...")

        
        busqueda = buscar_y_click_en_set_imagenes(config.imagenes_Btn_Parti_Com, sensibilidad = 0.8)
                
        if not busqueda:
                
            busqueda = buscar_y_click_en_set_imagenes(config.imagenes_Btn_Parti_Com, sensibilidad = 0.7)
            if not busqueda:
                msj_depuracion = "❌ No se encontró el iono de Boton Partition_Complete"
                print(msj_depuracion)
                return None 

    #************************************************************)
    pyautogui.press('enter')
    pyautogui.press('esc')
    
    #************************************************************
    # Septima busqueda buscar Boton File
    busqueda = buscar_y_click_en_set_imagenes(config.imagenes_Btn_File, sensibilidad = 0.9)
        
    # segundo inteto busqueda de Boton File
    if not busqueda:
        print("⚠ No se encontró el iono de boton File.")
            
        busqueda = buscar_y_click_en_set_imagenes(config.imagenes_Btn_File, sensibilidad = 0.8)
            
        if not busqueda:
            
            busqueda = buscar_y_click_en_set_imagenes(config.imagenes_Btn_File, sensibilidad = 0.7)
            if not busqueda:
                msj_depuracion = "❌ No se encontró el iono de boton File"
                print(msj_depuracion)
                return None
            
    #************************************************************
    # Ocatava busqueda buscar Boton New_Proyect
    busqueda = buscar_y_click_en_set_imagenes(config.imagenes_Btn_New_Proyect, sensibilidad = 0.9)
        
    # segundo inteto busqueda de Boton New_Proyect
    if not busqueda:
        print("⚠ No se encontró el iono de boton New_Proyect.")
            
        busqueda = buscar_y_click_en_set_imagenes(config.imagenes_Btn_New_Proyect, sensibilidad = 0.8)
            
        if not busqueda:
            
            busqueda = buscar_y_click_en_set_imagenes(config.imagenes_Btn_New_Proyect, sensibilidad = 0.7)
            if not busqueda:
                msj_depuracion = "❌ No se encontró el iono de boton New_Proyect"
                print(msj_depuracion)
                return None
    
    #************************************************************
    # Colocar Segunda Ruta para New Proyect
    pyautogui.press('tab', presses=6, interval=0.1)
    time.sleep(1)
    pyautogui.press('enter')
    
    pyautogui.write(config.rutaProyecto)
    pyautogui.press('enter')
            
    #************************************************************
    pyautogui.press('tab', presses=6, interval=0.2)
    pyautogui.write(config.nombre_new_proyect)
    pyautogui.press('enter')
    
    #************************************************************
    # Novena busqueda buscar Boton Add
    busqueda = buscar_y_click_en_set_imagenes(config.imagenes_Btn_Add, sensibilidad = 0.9)
        
    # segundo inteto busqueda de Boton Add
    if not busqueda:
        print("⚠ No se encontró el iono de boton Add.")
            
        busqueda = buscar_y_click_en_set_imagenes(config.imagenes_Btn_Add, sensibilidad = 0.8)
            
        if not busqueda:
            
            busqueda = buscar_y_click_en_set_imagenes(config.imagenes_Btn_Add, sensibilidad = 0.7)
            if not busqueda:
                msj_depuracion = "❌ No se encontró el iono de boton Add"
                print(msj_depuracion)
                return None
            
    #************************************************************
    pyautogui.press('tab', presses=5, interval=0.2)
    pyautogui.press('enter')
    pyautogui.write(f"{rta_base_temp}")
    pyautogui.press('enter')
    pyautogui.press('tab', presses=4, interval=0.1)
    pyautogui.press('space')
    pyautogui.press('enter')
    pyautogui.press('tab', presses=2, interval=0.1)
    pyautogui.press('left')
            
    return True    