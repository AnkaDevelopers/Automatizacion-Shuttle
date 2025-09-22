# gestion_shuttle.py

# ------------------------------------------------------------------
# Importaciones de librerías y configuración
# ------------------------------------------------------------------
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
def abrir_shuttle(tipo_config_shuttle: int):
    try:
        # ------------------------------------------------------------------
        # 1. Obtener la ruta del ejecutable desde la configuración
        # ------------------------------------------------------------------
        ruta = Path(config.ruta_shuttle[tipo_config_shuttle])
        print(f"[INFO] Intentando abrir Shuttle con índice {tipo_config_shuttle}...")

        # ------------------------------------------------------------------
        # 2. Validar que la ruta exista
        # ------------------------------------------------------------------
        if not ruta.exists():
            print(f"[ERROR] La ruta no existe: {ruta}")
            return None
        print(f"[DEBUG] Ruta encontrada: {ruta}")

        # ------------------------------------------------------------------
        # 3. Ejecutar el programa Shuttle
        # ------------------------------------------------------------------
        subprocess.Popen([str(ruta)])
        print(f"[SUCCESS] Shuttle abierto correctamente desde: {ruta}")
        return True

    except Exception as e:
        # ------------------------------------------------------------------
        # 4. Manejo de errores inesperados
        # ------------------------------------------------------------------
        print(f"[EXCEPTION] Error al abrir Shuttle: {e}")
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
        print(f"[INFO] Intentando cerrar procesos Shuttle en {sistema}...")

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
            print("[SUCCESS] Shuttle cerrado correctamente.")
            return True
        else:
            print(f"[WARNING] No se encontraron procesos activos de Shuttle. {resultado.stderr.strip()}")
            return False

    except Exception as e:
        # ------------------------------------------------------------------
        # 4. Manejo de errores inesperados
        # ------------------------------------------------------------------
        print(f"[EXCEPTION] Error al cerrar Shuttle: {e}")
        return None
