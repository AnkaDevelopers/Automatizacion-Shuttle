# puente_busqueda_img.py

# ------------------------------------------------------------------
# Importaciones de Utils necesarios
# ------------------------------------------------------------------
from Utils.tools.buscar_img import buscar_y_click_en_set_imagenes
from Monitor.log.log import agregar_log


# ------------------------------------------------------------------
# Función: puente_busqueda_img
# ------------------------------------------------------------------
# Intenta localizar y hacer clic en una imagen probando distintas
# sensibilidades. Si se pasan coordenadas (mouse_pos), busca en una
# región alrededor; si no, busca en toda la pantalla.
#
# Parámetros:
#   - data_set_imagenes: iterable de rutas relativas dentro de Utils
#   - data_set_mensajes: iterable con mensajes de feedback
#   - mouse_pos: tuple[int, int] | None -> región local si se aporta
#   - radio: int -> tamaño de la región alrededor de mouse_pos
#   - timeout: float -> tiempo máximo por sensibilidad (opcional)
#
# Retorna:
#   - True  -> si alguna búsqueda fue exitosa.
#   - None  -> si tras probar todas las sensibilidades no encontró nada.
#   - False -> si ocurrió un fallo inesperado.
# ------------------------------------------------------------------
def puente_busqueda_img( data_set_imagenes, data_set_mensajes, timeout=5.0):
    try:
        sensibilidades = [0.9, 0.85, 0.8]

        for i, sensibilidad in enumerate(sensibilidades):
            ok = buscar_y_click_en_set_imagenes(
                rutas_imagenes=data_set_imagenes,
                sensibilidad=sensibilidad,
                timeout=timeout,
            )

            if ok:
                return True

            if i < len(data_set_mensajes):
                agregar_log(data_set_mensajes[i])

        return None

    except Exception as e:
        agregar_log(f"[EXCEPTION] Error en puente_busqueda_img: {e}")
        return False
