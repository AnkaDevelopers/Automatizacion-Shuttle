# b_gestion_shuttle.py

# ------------------------------------------------------------------
# Importaciones de librerías y configuración
# ------------------------------------------------------------------
from Monitor.log.log import agregar_log
import Config.config as config
from pathlib import Path
import subprocess
import platform


# ------------------------------------------------------------------
# Función: abrir_shuttle
# ------------------------------------------------------------------
# Ejecuta el programa Shuttle según el índice recibido.
#
# Parámetros:
#   - tipo_config_shuttle: int -> Índice dentro de config.ruta_shuttle
#     que define cuál ejecutable de Shuttle se abrirá.
#
# Retorna:
#   - True si Shuttle se abrió correctamente.
#   - None si la ruta no existe o ocurre un error al abrir.
# ------------------------------------------------------------------
def abrir_shuttle(tipo_shuttle):
    try:
        # ------------------------------------------------------------------
        # 1. Obtener la ruta del ejecutable desde la configuración
        # ------------------------------------------------------------------
        ruta_shuttle = Path(tipo_shuttle)
        agregar_log(f"[INFO] Intentando abrir Shuttle con índice {tipo_shuttle}...")

        # ------------------------------------------------------------------
        # 2. Validar que la ruta exista
        # ------------------------------------------------------------------
        if not ruta_shuttle.exists():
            agregar_log(f"[ERROR] La ruta no existe: {ruta_shuttle}")
            return None
        agregar_log(f"[DEBUG] Ruta encontrada: {ruta_shuttle}")

        # ------------------------------------------------------------------
        # 3. Ejecutar el programa Shuttle
        # ------------------------------------------------------------------
        subprocess.Popen([str(ruta_shuttle)])
        agregar_log(f"[SUCCESS] Shuttle abierto correctamente desde: {ruta_shuttle}")
        return True

    except Exception as e:
        # ------------------------------------------------------------------
        # 4. Manejo de errores inesperados
        # ------------------------------------------------------------------
        agregar_log(f"[EXCEPTION] Error al abrir Shuttle: {e}")
        return None


# ------------------------------------------------------------------
# Función: cerrar_shuttle
# ------------------------------------------------------------------
# Cierra todos los procesos en ejecución que correspondan a Shuttle,
# garantizando el cierre incluso si abre ventanas o procesos hijos.
#
# Retorna:
#   - True si se cerraron procesos de Shuttle.
#   - False si no había procesos activos.
#   - None si ocurre un error inesperado.
# ------------------------------------------------------------------
def cerrar_shuttle():
    try:
        # ------------------------------------------------------------------
        # 1. Detectar sistema operativo
        # ------------------------------------------------------------------
        sistema = platform.system().lower()
        agregar_log(f"[INFO] Intentando cerrar procesos Shuttle en {sistema}...")

        # ------------------------------------------------------------------
        # 2. Ejecutar comando según SO
        # ------------------------------------------------------------------
        if sistema == "windows":
            # /F fuerza el cierre, /T mata procesos hijos
            resultado = subprocess.run(
                ["taskkill", "/F", "/T", "/IM", "Shuttle.exe"],
                capture_output=True,
                text=True
            )
        else:
            # -9 = SIGKILL (fuerza cierre), -f busca en la línea de comando
            resultado = subprocess.run(
                ["pkill", "-9", "-f", "Shuttle"],
                capture_output=True,
                text=True
            )

        # ------------------------------------------------------------------
        # 3. Evaluar resultado del cierre
        # ------------------------------------------------------------------
        if resultado.returncode == 0:
            agregar_log("[SUCCESS] Shuttle cerrado correctamente.")
            return True
        else:
            agregar_log(f"[WARNING] No se encontraron procesos activos de Shuttle. {resultado.stderr.strip()}")
            return False

    except Exception as e:
        # ------------------------------------------------------------------
        # 4. Manejo de errores inesperados
        # ------------------------------------------------------------------
        agregar_log(f"[EXCEPTION] Error al cerrar Shuttle: {e}")
        return None
