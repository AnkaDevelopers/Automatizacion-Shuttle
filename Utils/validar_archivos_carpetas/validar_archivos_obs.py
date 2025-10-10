# validar_archivos_obs.py
# ------------------------------------------------------------------
# Importaciones de librerías y configuración
# ------------------------------------------------------------------
from Monitor.log.log import agregar_log
from pathlib import Path
from typing import Optional
import re

# ------------------------------------------------------------------
# Función: validar_archivo_obs
# ------------------------------------------------------------------
# Busca dentro de una carpeta un archivo con extensión tipo RINEX
# de observación (.??O), donde:
# - "??" es un número variable (ej. "24O", "25o", "26O").
# - La "O" final puede estar en mayúscula o minúscula.
#
# Parámetros:
# - ruta_carpeta: str | Path -> Carpeta donde se buscarán los archivos.
#
# Retorna:
# - str -> Ruta absoluta del archivo encontrado (el más grande si hay varios).
# - None -> Si no se encuentra ninguno o hay un error.
# ------------------------------------------------------------------
def validar_archivo_obs(ruta_carpeta) -> Optional[str]:
    try:
        # ------------------------------------------------------------------
        # 1. Validar que la ruta exista y sea un directorio
        # ------------------------------------------------------------------
        base = Path(ruta_carpeta)
        if not base.exists() or not base.is_dir():
            agregar_log(f"[ERROR] La ruta '{ruta_carpeta}' no existe o no es un directorio.")
            return None

        agregar_log(f"[INFO] Carpeta válida: {ruta_carpeta}")

        # ------------------------------------------------------------------
        # 2. Buscar archivos que cumplan con el patrón *.??O / *.??o
        # ------------------------------------------------------------------
        mejor_archivo = None
        mejor_peso = -1

        for item in base.iterdir():
            if not item.is_file():
                continue

            nombre = item.name.lower()  # Normalizar para comparación

            # FIX: Path(item).suffix incluye ".", ej. ".24o" → longitud = 4
            if re.fullmatch(r"\.[0-9]{2}[oO]", item.suffix):
                try:
                    peso = item.stat().st_size
                except OSError as e:
                    agregar_log(f"[WARNING] No se pudo obtener tamaño de '{item}': {e}")
                    continue

                agregar_log(f"[DEBUG] Archivo candidato: {item}, tamaño: {peso} bytes")

                if peso > mejor_peso:
                    mejor_peso = peso
                    mejor_archivo = item.resolve()

        # ------------------------------------------------------------------
        # 3. Retornar el archivo seleccionado
        # ------------------------------------------------------------------
        if mejor_archivo:
            agregar_log(f"[SUCCESS] Archivo RINEX encontrado: {mejor_archivo} ({mejor_peso} bytes)")
            return str(mejor_archivo)
        else:
            agregar_log(f"[INFO] No se encontraron archivos con extensión tipo '.??O' en {ruta_carpeta}")
            return None

    except Exception as e:
        # ------------------------------------------------------------------
        # 4. Manejo de errores inesperados
        # ------------------------------------------------------------------
        agregar_log(f"[EXCEPTION] Error inesperado al validar archivos en '{ruta_carpeta}': {e}")
        return None
