# validar_archivos.py

# ------------------------------------------------------------------
# Importaciones de librerías y configuración
# ------------------------------------------------------------------
from Monitor.log.log import agregar_log
from pathlib import Path
from typing import Optional


# ------------------------------------------------------------------
# Función: validar_archivos
# ------------------------------------------------------------------
# Busca en la carpeta indicada un archivo con la extensión solicitada.
# - La búsqueda no distingue entre mayúsculas y minúsculas.
# - Si hay varios, retorna el de mayor tamaño.
#
# Parámetros:
#   - ruta_carpeta: str | Path -> Carpeta donde se buscarán los archivos.
#   - extension: str -> Extensión a buscar (ejemplo: ".dat", ".kqs").
#
# Retorna:
#   - str -> Ruta absoluta del archivo encontrado.
#   - None -> Si no se encuentra ningún archivo válido o hay un error.
# ------------------------------------------------------------------
def validar_archivos(ruta_carpeta, extension) -> Optional[str]:

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
        # 2. Validar que se haya proporcionado una extensión
        # ------------------------------------------------------------------
        if not extension:
            agregar_log("[ERROR] No se proporcionó ninguna extensión.")
            return None

        # ------------------------------------------------------------------
        # 3. Normalizar extensión (sin puntos iniciales y en minúsculas)
        # ------------------------------------------------------------------
        ext = str(extension).strip().lower()
        while ext.startswith("."):
            ext = ext[1:]
        if not ext:
            agregar_log("[ERROR] Extensión inválida tras normalización.")
            return None

        sufijo = "." + ext
        agregar_log(f"[DEBUG] Extensión normalizada: {sufijo}")

        # ------------------------------------------------------------------
        # 4. Buscar archivos con la extensión requerida
        # ------------------------------------------------------------------
        mejor_archivo = None
        mejor_peso = -1

        for item in base.iterdir():
            if not item.is_file():
                continue
            nombre = item.name.lower()

            if nombre.endswith(sufijo):
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
        # 5. Retornar el archivo seleccionado
        # ------------------------------------------------------------------
        if mejor_archivo:
            agregar_log(f"[SUCCESS] Archivo seleccionado: {mejor_archivo} ({mejor_peso} bytes)")
            return str(mejor_archivo)
        else:
            agregar_log(f"[INFO] No se encontraron archivos con extensión {sufijo} en {ruta_carpeta}")
            return None

    except Exception as e:
        # ------------------------------------------------------------------
        # 6. Manejo de errores inesperados
        # ------------------------------------------------------------------
        agregar_log(f"[EXCEPTION] Error inesperado al validar archivos en '{ruta_carpeta}': {e}")
        return False
