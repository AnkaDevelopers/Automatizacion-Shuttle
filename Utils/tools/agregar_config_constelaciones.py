# agregar_config_constelaciones.py

# ------------------------------------------------------------------
# Importaciones de librerías y configuraciones Globales
# ------------------------------------------------------------------
import os

# ------------------------------------------------------------------
# Importaciones de Módulos
# ------------------------------------------------------------------
from Monitor.log.log import agregar_log


# ------------------------------------------------------------------
# Util: guardar configuración en CONFIG_CONSTELACIONES.txt (sin fecha)
# ------------------------------------------------------------------
def guardar_config_constelaciones_txt(ruta_base: str, linea: str) -> bool:
    """
    Crea (si no existe) y agrega una línea de configuración al archivo
    CONFIG_CONSTELACIONES.txt dentro de `ruta_base`, SIN timestamp.

    Retorna:
        True  -> si se escribió correctamente
        False -> si ocurrió algún error
    """
    try:
        if not ruta_base:
            agregar_log("[ERROR] Ruta base para guardar configuraciones no válida (None o vacía).")
            return False

        # Asegurar que el directorio exista
        os.makedirs(ruta_base, exist_ok=True)

        ruta_archivo = os.path.join(ruta_base, "CONFIG_CONSTELACIONES.txt")

        # Escribir la línea tal cual, sin fecha
        linea_a_escribir = f"{linea}\n"

        with open(ruta_archivo, "a", encoding="utf-8") as f:
            f.write(linea_a_escribir)

        agregar_log(f"[INFO] Configuración guardada en: {ruta_archivo}")
        return True

    except Exception as e:
        agregar_log(f"[ERROR] No se pudo guardar la configuración. Detalle: {e}")
        return False
