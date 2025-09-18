# seleccionar_kqs_observado.py
from typing import Optional
from pathlib import Path
import shutil

def seleccionar_kqs_o_observado(ruta_carpeta) -> Optional[str]:
    """
    Busca en 'ruta_carpeta' (no recursivo) primero archivos .kqs (>1KB, case-insensitive).
      - Si encuentra uno o más, retorna la ruta del .kqs más pesado.
    Si no hay .kqs válidos, busca archivos 'observados' cuya extensión:
      - empiece con un dígito y termine con 'o' u 'O' (ej. .25o, .3O).
      - Si hay varios, copia el más pesado a <carpeta_script>/Temp/Observado/ y
        retorna la RUTA DE ESA CARPETA 'Observado'.
    Si no encuentra nada, retorna None.
    """
    try:
        base = Path(ruta_carpeta)
        print(f"[DEBUG] Carpeta recibida: {base}")
        print(f"[DEBUG] Existe: {base.exists()} | Es carpeta: {base.is_dir()}")

        if not base.exists() or not base.is_dir():
            print("[WARN] La ruta no existe o no es una carpeta. Retornando None.")
            return None

        # ---------- Paso 1: Buscar .kqs (>1 KB) ----------
        candidatos_kqs = []
        print("[DEBUG] --- Buscando archivos .kqs (>1KB) ---")
        total_items = 0
        for item in base.iterdir():
            total_items += 1
            if item.is_file():
                suf = item.suffix.lower()
                if suf == ".kqs":
                    try:
                        size = item.stat().st_size
                    except OSError as e:
                        print(f"[ERROR] No se pudo obtener tamaño de {item}: {e}")
                        continue
                    if size > 1024:
                        candidatos_kqs.append((size, item))
                        print(f"[DEBUG] KQS válido: {item} | tamaño={size} bytes")
                    else:
                        print(f"[DEBUG] KQS descartado (<1KB): {item} | tamaño={size} bytes")
                else:
                    # print opcional si quieres ver todo
                    pass
            else:
                # print opcional para subcarpetas
                pass

        print(f"[DEBUG] Total elementos inspeccionados: {total_items}")
        print(f"[DEBUG] Candidatos KQS válidos: {len(candidatos_kqs)}")

        if candidatos_kqs:
            # Elegir el más pesado
            _, mejor_kqs = max(candidatos_kqs, key=lambda t: t[0])
            ruta_final_kqs = str(mejor_kqs.resolve())
            print(f"[INFO] Seleccionado KQS más pesado: {ruta_final_kqs}")
            return ruta_final_kqs

        # ---------- Paso 2: Buscar 'observado' (ext comienza con dígito y termina en o/O) ----------
        print("[DEBUG] --- No hay KQS válidos. Buscando archivos 'observados' (ext tipo 25o/3O) ---")
        candidatos_obs = []
        for item in base.iterdir():
            if not item.is_file():
                continue
            suf = item.suffix[1:]  # sin el punto
            if not suf:
                continue
            if suf[0].isdigit() and suf[-1].lower() == "o":
                try:
                    size = item.stat().st_size
                except OSError as e:
                    print(f"[ERROR] No se pudo obtener tamaño de {item}: {e}")
                    continue
                candidatos_obs.append((size, item))
                print(f"[DEBUG] Observado candidato: {item} | ext=.{suf} | tamaño={size} bytes")

        print(f"[DEBUG] Candidatos Observado: {len(candidatos_obs)}")

        if candidatos_obs:
            # Elegir el más pesado
            _, mejor_obs = max(candidatos_obs, key=lambda t: t[0])
            print(f"[INFO] Observado seleccionado (más pesado): {mejor_obs}")

            # Preparar carpeta destino: <carpeta_del_script>/Temp/Observado
            script_dir = Path(__file__).resolve().parent
            observado_dir = script_dir / "Temp" / "Observado"
            print(f"[DEBUG] Carpeta destino Observado: {observado_dir}")

            try:
                observado_dir.mkdir(parents=True, exist_ok=True)
                print("[DEBUG] Carpeta destino creada/existente OK.")
            except Exception as e:
                print(f"[ERROR] No se pudo crear la carpeta destino: {e}")
                return None

            # Copiar preservando metadatos
            destino = observado_dir / mejor_obs.name
            print(f"[DEBUG] Copiando '{mejor_obs}' -> '{destino}'")
            try:
                shutil.copy2(mejor_obs, destino)
                print("[INFO] Copia completada con éxito.")
            except Exception as e:
                print(f"[ERROR] Falló la copia del observado: {e}")
                return None

            # Retornar la RUTA DE LA CARPETA Observado (no del archivo)
            ruta_observado = str(observado_dir.resolve())
            print(f"[INFO] Retornando carpeta Observado: {ruta_observado}")
            return ruta_observado

        # ---------- Nada encontrado ----------
        print("[WARN] No se encontraron archivos .kqs >1KB ni 'observados'. Retornando None.")
        return None

    except Exception as e:
        print(f"[ERROR] Excepción inesperada: {e}")
        return None
