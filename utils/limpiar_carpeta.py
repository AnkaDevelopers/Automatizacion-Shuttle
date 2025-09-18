from typing import Optional
from pathlib import Path
import os
import stat

#*******************************************************************************
def eliminar_archivos_en_carpeta(ruta_carpeta):
    """
    Elimina TODOS los archivos del primer nivel dentro de 'ruta_carpeta'.
    No elimina subcarpetas ni su contenido.

    Retorna:
      - True  -> si todos los archivos fueron eliminados correctamente (o no había archivos)
      - None  -> si la ruta no es válida o si algún archivo no pudo eliminarse
    """
    try:
        base = Path(ruta_carpeta)
        print(f"[DEBUG] Carpeta recibida: {base}")
        if not base.exists() or not base.is_dir():
            print("[ERROR] La ruta no existe o no es una carpeta. Retornando None.")
            return None

        archivos = [p for p in base.iterdir() if p.is_file() or p.is_symlink()]
        print(f"[DEBUG] Archivos detectados: {len(archivos)}")
        if not archivos:
            print("[INFO] No hay archivos para eliminar. Retornando True.")
            return True

        fallos = 0
        for f in archivos:
            try:
                print(f"[DEBUG] Eliminando: {f}")
                # Intento directo
                f.unlink()
                print(f"[INFO] Eliminado: {f}")
            except PermissionError:
                print(f"[WARN] Permiso denegado al borrar: {f}. Intentando quitar solo-lectura...")
                try:
                    # Quitar atributo de solo-lectura (Windows)
                    os.chmod(f, stat.S_IWRITE)
                    f.unlink()
                    print(f"[INFO] Eliminado tras ajustar permisos: {f}")
                except Exception as e:
                    fallos += 1
                    print(f"[ERROR] No se pudo eliminar {f} tras ajustar permisos: {e}")
            except Exception as e:
                fallos += 1
                print(f"[ERROR] No se pudo eliminar {f}: {e}")

        if fallos > 0:
            print(f"[ERROR] Hubo {fallos} archivo(s) que no se pudieron eliminar. Retornando None.")
            return None

        print("[INFO] Todos los archivos fueron eliminados correctamente. Retornando True.")
        return True

    except Exception as e:
        print(f"[ERROR] Excepción inesperada: {e}")
        return None
