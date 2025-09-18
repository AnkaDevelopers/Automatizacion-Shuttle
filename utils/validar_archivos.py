# validar_archivos.py
from pathlib import Path
from typing import Optional


"""
    Busca en 'ruta_carpeta' un archivo con la extensión indicada (sin importar mayúsculas).
    Si hay varios, retorna el de mayor tamaño. Si no encuentra, retorna None.

    Parámetros:
      - ruta_carpeta: str | Path
      - extencion: str  (ej. ".dat", ".kqs")

    Retorna:
      - str (ruta absoluta del archivo encontrado) o None
"""

#******************************************************************************************   
def validar_archivos(ruta_carpeta, extencion) -> Optional[str]:
    try:
        base = Path(ruta_carpeta)
        if not base.exists() or not base.is_dir():
            return None

        if not extencion:
            return None

        # Normalizar extensión: quitar puntos al inicio y pasar a minúsculas
        ext = str(extencion).strip().lower()
        while ext.startswith("."):
            ext = ext[1:]
        if not ext:
            return None

        # Soporta multi-parte (p.ej. "tar.gz"): comparamos por sufijo completo
        sufijo = "." + ext

        mejor_archivo = None
        mejor_peso = -1

        for item in base.iterdir():
            if not item.is_file():
                continue
            nombre = item.name.lower()
            if nombre.endswith(sufijo):
                try:
                    peso = item.stat().st_size
                except OSError:
                    continue
                if peso > mejor_peso:
                    mejor_peso = peso
                    mejor_archivo = item.resolve()

        return str(mejor_archivo) if mejor_archivo else None
    except Exception:
        return None
