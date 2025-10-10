# Importaciones modulos
from Monitor.firma.firma import construir_firma_html
from Monitor.log.log import agregar_log

# Importaciones adicionales
import win32com.client

# ************************************************************************************************************
def obtener_mensaje_por_id(id_correo):

    try:
        # Inicializa la conexión con Outlook
        outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        
        # Accede a la bandeja de entrada
        inbox = outlook.GetDefaultFolder(6)  # 6 representa la carpeta de Bandeja de Entrada

        # Itera por los mensajes en la bandeja de entrada
        for mensaje in inbox.Items:
            if mensaje.EntryID == id_correo:
                return mensaje  # Devuelve el objeto del mensaje encontrado
        
        return None  # Si no se encuentra el mensaje, devuelve None
    except Exception as e:
        print(f"Error al buscar el mensaje por ID: {str(e)}")
        return None

# ************************************************************************************************************
# Funcion para responder correos 
def responder_correo(mensaje, respuesta):
    try:
        
        # Crear la respuesta del correo original
        respuesta_correo = mensaje.Reply()

        # Obtener la firma HTML y la ruta de la imagen
        firma_html, ruta_imagen_local = construir_firma_html()

        # Verificar que la firma se haya generado correctamente
        if not firma_html or not ruta_imagen_local:
            agregar_log("No se pudo generar la firma. Envío de correo cancelado.")
            return print("No se pudo generar la firma. Envío de correo cancelado.")
            

        # Construir el cuerpo HTML del correo
        cuerpo_html = f"<p>{respuesta}</p><br>{firma_html}"

        # Insertar el cuerpo HTML en la respuesta
        respuesta_correo.HTMLBody = cuerpo_html + respuesta_correo.HTMLBody

        # Adjuntar la imagen como embebida con Content-ID
        adjunto = respuesta_correo.Attachments.Add(ruta_imagen_local)
        property_accessor = adjunto.PropertyAccessor
        property_accessor.SetProperty("http://schemas.microsoft.com/mapi/proptag/0x3712001F", "logo_anka")  
        
        agregar_log("Imagen adjuntada con Content-ID: logo_anka")

        # Enviar el correo
        respuesta_correo.Send()
        agregar_log("Respuesta enviada correctamente con firma y logo.")

    except Exception as e:
        agregar_log("Error al enviar la respuesta \n",e)

def enviar_correo_proceso_redgeoscan(mensaje, respuesta):
    try:
        print('/'*100)
        # Crear la respuesta del correo original
        respuesta_correo = mensaje.Reply()

        # Construir la firma HTML y obtener la ruta de la imagen
        firma_html, ruta_imagen_local = construir_firma_html()

        if not firma_html or not ruta_imagen_local:
            return print("No se pudo generar la firma. Envío de correo cancelado.")
        
        # Procesar la respuesta para formatearla en HTML
        lineas = respuesta.strip().split("\n")
        contenido_html = "<h3>Proyecto</h3>"
        contenido_html += f"<p>{lineas[0]}</p>"  # Primera línea como encabezado
        
        # Crear lista para el resto de las líneas
        contenido_html += "<ul>"
        for linea in lineas[1:]:
            contenido_html += f"<li>{linea}</li>"
        contenido_html += "</ul>"

        # Construir el cuerpo completo del correo
        cuerpo_html = f"{contenido_html}<br>{firma_html}"
        respuesta_correo.HTMLBody = cuerpo_html + respuesta_correo.HTMLBody

        # Adjuntar imagen embebida con Content-ID
        adjunto = respuesta_correo.Attachments.Add(ruta_imagen_local)
        property_accessor = adjunto.PropertyAccessor
        property_accessor.SetProperty("http://schemas.microsoft.com/mapi/proptag/0x3712001F", "logo_anka")
        #("Imagen adjuntada con Content-ID: logo_anka")

        # Enviar el correo
        respuesta_correo.Send()
        #print("Respuesta enviada correctamente con firma y formato HTML.")

    except Exception as e:
        print("Error al enviar la respuesta \n", e)
