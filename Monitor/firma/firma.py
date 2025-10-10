# Importaciones Adicionales
import os


# ************************************************************************************************************
# Rutas locales de la imagen y el texto de la firma
ruta_imagen_local = r"C:\RedGeoscan\data\logo_anka.jpg"
ruta_texto = r"C:\RedGeoscan\data\firma.txt"

# ************************************************************************************************************
# Función para cargar el texto de la firma desde un archivo
def cargar_texto(ruta_texto):
    try:
        with open(ruta_texto, "r", encoding="utf-8") as archivo:
            return archivo.read()
    except Exception as e:
        print(f"Error al cargar el texto del archivo: {e}")
        return ""

# ************************************************************************************************************
# Función modular para construir la firma HTML
def construir_firma_html():
    try:
        
        # Verificar la existencia de la imagen
        if os.path.exists(ruta_imagen_local):
            
            # Construir el cuerpo de la firma
            texto_firma = cargar_texto(ruta_texto)
            
            # Estructura HTML para el correo
            firma_html = f"""
            <div style="font-family: Arial, sans-serif; color: #333;">
                <img src="cid:logo_anka" alt="Logo ANKA" style="width: 200px; height: auto; margin-bottom: 1px;">
                <p>{texto_firma}</p>
            </div>
            """
            
            # Retorna el HTML y la ruta de la imagen
            return firma_html, ruta_imagen_local  
        
        else:
            
            # mensaje de depuración
            print("La imagen de la firma no existe en la ruta especificada.")
            
            return "", None
        
    except Exception as e:
        print(f"Error al construir la firma HTML: {e}")
        return "", None
