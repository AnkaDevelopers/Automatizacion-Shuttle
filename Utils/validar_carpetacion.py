# validarCarpetacion.py

# ------------------------------------------------------------------
# Importaciones de librerías y configuración
# ------------------------------------------------------------------
from typing import Optional, Dict, List
from pathlib import Path


# ------------------------------------------------------------------
# Función: validar_carpetacion
# ------------------------------------------------------------------
# Verifica que en la ruta dada existan las subcarpetas requeridas.
#
# Parámetros:
#   - ruta: str -> Ruta a validar.
#   - requeridas: List[str] -> Lista de nombres de carpetas obligatorias.
#
# Retorna:
#   - Diccionario con rutas absolutas si todas existen.
#   - None si falta alguna carpeta o si la ruta no es válida.
# ------------------------------------------------------------------
def validar_carpetacion(ruta: str, requeridas: List[str]) -> Optional[Dict[str, str]]:
    try:
        # ------------------------------------------------------------------
        # 1. Validar que la ruta exista y sea un directorio
        # ------------------------------------------------------------------
        p = Path(ruta)
        if not p.exists() or not p.is_dir():
            print(f"[ERROR] La ruta '{ruta}' no existe o no es un directorio válido.")
            return None
        print(f"[INFO] Ruta válida: {ruta}")

        # ------------------------------------------------------------------
        # 2. Construir un mapa de subcarpetas (insensible a mayúsculas/minúsculas)
        # ------------------------------------------------------------------
        subdirs = {child.name.lower(): child for child in p.iterdir() if child.is_dir()}
        print(f"[DEBUG] Subcarpetas encontradas: {list(subdirs.keys())}")

        # ------------------------------------------------------------------
        # 3. Verificar la presencia de carpetas requeridas
        # ------------------------------------------------------------------
        if not all(r.lower() in subdirs for r in requeridas):
            print(f"[ERROR] Faltan carpetas requeridas. Se esperaban: {requeridas}")
            return None
        print("[INFO] Todas las carpetas requeridas están presentes.")

        # ------------------------------------------------------------------
        # 4. Devolver rutas absolutas/resueltas
        # ------------------------------------------------------------------
        resultado = {r: str(subdirs[r.lower()].resolve()) for r in requeridas}
        print(f"[SUCCESS] Estructura de carpetas validada correctamente: {resultado}")
        return resultado

    except Exception as e:
        # ------------------------------------------------------------------
        # 5. Manejo de errores inesperados
        # ------------------------------------------------------------------
        print(f"[EXCEPTION] Error inesperado al validar la ruta '{ruta}': {e}")
        return None

