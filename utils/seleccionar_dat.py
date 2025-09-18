# seleccionar_dat.py
from typing import Optional
from pathlib import Path
import shutil



#************************************************************************************
def seleccionar_dat(ruta_carpeta) -> Optional[str]:
    """
    Busca en 'ruta_carpeta' (no recursivo) archivos .dat (case-insensitive).
      - Si encuentra uno o más, elige el más pesado y lo copia a <carpeta_script>/Temp/dat/
      - Retorna la RUTA de esa carpeta 'Temp/dat'
    Si no encuentra nada, retorna None.
    """
    try:
        base = Path(ruta_carpeta)
        print(f"[DEBUG] Carpeta recibida: {base}")
        print(f"[DEBUG] Existe: {base.exists()} | Es carpeta: {base.is_dir()}")

        if not base.exists() or not base.is_dir():
            print("[WARN] La ruta no existe o no es una carpeta. Retornando None.")
            return None

        # --- Buscar .dat ---
        print("[DEBUG] --- Buscando archivos .dat ---")
        candidatos_dat = []
        total_items = 0

        for item in base.iterdir():
            total_items += 1
            if not item.is_file():
                # print(f"[DEBUG] Omitiendo no-archivo: {item}")
                continue
            suf = item.suffix.lower()
            if suf == ".dat":
                try:
                    size = item.stat().st_size
                except OSError as e:
                    print(f"[ERROR] No se pudo obtener tamaño de {item}: {e}")
                    continue
                candidatos_dat.append((size, item))
                print(f"[DEBUG] DAT candidato: {item} | tamaño={size} bytes")
            # else:
            #     print(f"[TRACE] No .dat: {item}")

        print(f"[DEBUG] Total elementos inspeccionados: {total_items}")
        print(f"[DEBUG] Candidatos .dat: {len(candidatos_dat)}")

        if not candidatos_dat:
            print("[WARN] No se encontraron archivos .dat. Retornando None.")
            return None

        # --- Elegir el más pesado ---
        _, mejor_dat = max(candidatos_dat, key=lambda t: t[0])
        print(f"[INFO] Seleccionado .dat más pesado: {mejor_dat} | tamaño={mejor_dat.stat().st_size} bytes")

        # --- Preparar carpeta destino: <carpeta_del_script>/Temp/dat ---
        script_dir = Path(__file__).resolve().parent
        dat_dir = script_dir / "Temp" / "dat"
        print(f"[DEBUG] Carpeta destino: {dat_dir}")

        try:
            dat_dir.mkdir(parents=True, exist_ok=True)
            print("[DEBUG] Carpeta destino creada/existente OK.")
        except Exception as e:
            print(f"[ERROR] No se pudo crear la carpeta destino: {e}")
            return None

        # --- Copiar preservando metadatos ---
        destino = dat_dir / mejor_dat.name
        print(f"[DEBUG] Copiando '{mejor_dat}' -> '{destino}'")
        try:
            shutil.copy2(mejor_dat, destino)
            print("[INFO] Copia completada con éxito.")
        except Exception as e:
            print(f"[ERROR] Falló la copia del .dat: {e}")
            return None

        # --- Retorno: carpeta 'Temp/dat' ---
        ruta_ret = str(dat_dir.resolve())
        print(f"[INFO] Retornando carpeta Temp/dat: {ruta_ret}")
        return ruta_ret

    except Exception as e:
        print(f"[ERROR] Excepción inesperada: {e}")
        return None

