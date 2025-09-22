# puente_busqueda_img.py

# ------------------------------------------------------------------
# Importaciones de Utils necesarios
# ------------------------------------------------------------------
from Utils.buscar_img import buscar_y_click_en_set_imagenes


# ------------------------------------------------------------------
# Función: puente_busqueda_img
# ------------------------------------------------------------------
# Intenta localizar y hacer clic en una imagen dentro de un dataset
# probando con diferentes niveles de sensibilidad.
#
# Parámetros:
#   - data_set_imagenes: iterable
#       Conjunto de rutas/objetos de imágenes donde se intentará buscar.
#   - data_set_mensajes: iterable
#       Mensajes de feedback (ej. logs o textos informativos).
#
# Retorna:
#   - True  -> si alguna búsqueda fue exitosa.
#   - None  -> si no se encontró nada tras probar todas las sensibilidades.
#   - False -> si ocurrió un fallo inesperado.
# ------------------------------------------------------------------
def puente_busqueda_img(data_set_imagenes, data_set_mensajes):
    try:
        # ------------------------------------------------------------------
        # 1. Definir sensibilidades de búsqueda (de mayor a menor confianza)
        # ------------------------------------------------------------------
        sensibilidades = [0.9, 0.8, 0.7]

        # ------------------------------------------------------------------
        # 2. Intentar búsqueda secuencial con cada sensibilidad
        # ------------------------------------------------------------------
        for i, sensibilidad in enumerate(sensibilidades):
            busqueda = buscar_y_click_en_set_imagenes(
                data_set_imagenes, sensibilidad=sensibilidad
            )

            # --------------------------------------------------------------
            # 2.1 Si encuentra la imagen, retornar éxito inmediato
            # --------------------------------------------------------------
            if busqueda:
                return True

            # --------------------------------------------------------------
            # 2.2 Si no encuentra, mostrar feedback si hay mensajes disponibles
            # --------------------------------------------------------------
            if i < len(data_set_mensajes):
                print(data_set_mensajes[i])

        # ------------------------------------------------------------------
        # 3. Ninguna sensibilidad tuvo éxito -> retornar None
        # ------------------------------------------------------------------
        return None

    except Exception:
        # ------------------------------------------------------------------
        # 4. Manejo de errores inesperados -> retornar False
        # ------------------------------------------------------------------
        return False
