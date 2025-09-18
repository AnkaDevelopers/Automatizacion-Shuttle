# mover_archivos.py
from pathlib import Path
from typing import Optional
import os
import shutil
import errno


#*******************************************************************************
def cortar_archivos(ruta_origen, ruta_destino):
    """
    Corta (mueve) todos los archivos desde 'ruta_origen' hacia 'ruta_destino',
    reemplazando archivos si es necesario. No es recursivo (no entra a subcarpetas).

    Retorna:
      - True si movió al menos un archivo.
      - None si no movió nada o ocurrió un error.
    """
    try:
        origen = Path(ruta_origen)
        destino = Path(ruta_destino)

        print(f"[DEBUG] Origen: {origen} | Existe: {origen.exists()} | Carpeta: {origen.is_dir()}")
        print(f"[DEBUG] Destino: {destino} | Existe: {destino.exists()} | Carpeta: {destino.is_dir()}")

        if not origen.exists() or not origen.is_dir():
            print("[ERROR] La ruta de origen no existe o no es una carpeta. Cancelando.")
            return None

        # Crear destino si no existe
        try:
            destino.mkdir(parents=True, exist_ok=True)
            print("[DEBUG] Carpeta destino creada/existente OK.")
        except Exception as e:
            print(f"[ERROR] No se pudo crear la carpeta destino: {e}")
            return None

        # Evitar operación inútil si origen == destino
        if origen.resolve() == destino.resolve():
            print("[WARN] Origen y destino son la misma carpeta. No hay nada que mover.")
            return None

        movidos = 0
        total = 0

        for item in origen.iterdir():
            if not item.is_file():
                continue
            total += 1
            destino_archivo = destino / item.name
            print(f"[TRACE] Procesando: {item.name}")

            # Si existe en destino, lo reemplazamos
            if destino_archivo.exists():
                try:
                    if destino_archivo.is_file():
                        destino_archivo.unlink()
                        print(f"[DEBUG] Eliminado archivo existente en destino: {destino_archivo.name}")
                    else:
                        print(f"[WARN] En destino existe un directorio con el mismo nombre: {destino_archivo.name}. Saltando.")
                        continue
                except Exception as e:
                    print(f"[ERROR] No se pudo eliminar {destino_archivo}: {e}")
                    continue

            # Intentar mover con overwrite garantizado
            try:
                # 1) Intento rápido: os.replace (mismo filesystem) -> sobrescribe
                os.replace(item, destino_archivo)
                print(f"[INFO] Movido (rename/replace): {item.name} -> {destino_archivo}")
                movidos += 1
            except OSError as e:
                if e.errno == errno.EXDEV:
                    # 2) Filesystem diferente: copiar y borrar origen
                    try:
                        shutil.copy2(item, destino_archivo)
                        item.unlink()
                        print(f"[INFO] Movido (copy2+unlink): {item.name} -> {destino_archivo}")
                        movidos += 1
                    except Exception as e2:
                        print(f"[ERROR] Falló copy2+unlink para {item.name}: {e2}")
                        # Si el destino quedó a medio copiar, intentamos limpiar
                        try:
                            if destino_archivo.exists():
                                destino_archivo.unlink()
                        except Exception:
                            pass
                        continue
                else:
                    print(f"[ERROR] Falló os.replace para {item.name}: {e}")
                    continue

        print(f"[DEBUG] Archivos encontrados: {total} | Archivos movidos: {movidos}")
        return True if movidos > 0 else None

    except Exception as e:
        print(f"[ERROR] Excepción inesperada: {e}")
        return None

