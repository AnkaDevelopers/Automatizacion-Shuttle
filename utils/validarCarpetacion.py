# validarCarpetacion.py
from typing import Optional, Dict
from pathlib import Path

"""
    Verifica que en 'ruta' existan las subcarpetas: base, lidar, pos (sin importar mayúsculas).
    Retorna:
      - {'base': '...', 'lidar': '...', 'pos': '...'} si existen todas.
      - None si falta alguna o la ruta no es válida.
"""
#**********************************************************************
def validar_carpetacion(ruta) -> Optional[Dict[str, str]]:
    try:
        p = Path(ruta)
        if not p.exists() or not p.is_dir():
            return None

        # Mapa case-insensitive de subcarpetas inmediatas
        subdirs = {child.name.lower(): child for child in p.iterdir() if child.is_dir()}
        requeridas = ("base", "lidar", "pos")

        # Validar presencia de todas
        if not all(r in subdirs for r in requeridas):
            return None

        # Devolver rutas absolutas/resueltas
        return {r: str(subdirs[r].resolve()) for r in requeridas}
    except Exception:
        return None
