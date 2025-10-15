# Utils/tools/cargar_mejor_config.py

import os
from typing import Optional
from Monitor.log.log import agregar_log
from Modules.e_aplicar_config_gnss import aplicar_constelaciones, aplicar_mascara
from Utils.tools.config_constelaciones_helpers import ruta_config_txt


def intentar_cargar_mejor_config_existente(ruta_donde_guardar_configuraciones) -> Optional[bool]:
    """
    Si existe CONFIG_CONSTELACIONES.txt, busca la mejor configuración por PORCENTAJE.
    Si encuentra una > 99.0, la aplica (constelaciones + máscara) y retorna True.
    Si no hay ninguna válida o no existe el archivo, retorna False.
    En caso de error al leer/parsear/aplicar, loguea y retorna None.
    """
    try:
        ruta_archivo_config = ruta_config_txt(ruta_donde_guardar_configuraciones)
        if not os.path.exists(ruta_archivo_config):
            agregar_log("[INFO] No existe CONFIG_CONSTELACIONES.txt aún. Se generará durante la ejecución.")
            return False

        mejor_linea = None
        mejor_porcentaje = -1.0

        with open(ruta_archivo_config, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or "PORCENTAJE" not in line:
                    continue
                try:
                    parte_pct = line.split("PORCENTAJE", 1)[1]
                    parte_pct = parte_pct.split("=", 1)[1].strip()
                    parte_pct = parte_pct.replace("%", "").replace(",", ".")
                    pct = float(parte_pct)
                except Exception:
                    continue

                if pct > mejor_porcentaje:
                    mejor_porcentaje = pct
                    mejor_linea = line

        if mejor_linea is None or mejor_porcentaje <= 99.0:
            return False

        # Parsear la mejor línea para obtener gps/glo/gal/bds/mascara
        try:
            partes = [p.strip() for p in mejor_linea.split(",")]
            kv = {}
            for p in partes:
                if "=" in p:
                    k, v = p.split("=", 1)
                    kv[k.strip().upper()] = v.strip()

            def _to_bool(s: str) -> bool:
                return s.strip().lower() in ("true", "1", "si", "sí")

            gps = _to_bool(kv.get("GPS", "False"))
            glo = _to_bool(kv.get("GLO", "False"))
            gal = _to_bool(kv.get("GAL", "False"))
            bds = _to_bool(kv.get("BDS", "False"))
            mascara = int(kv.get("MASCARA", "0"))

            agregar_log(
                f"[INFO] Se encontró configuración previa >99% ({mejor_porcentaje}). "
                f"Cargando: GPS={gps}, GLO={glo}, GAL={gal}, BDS={bds}, MASCARA={mascara}"
            )

            # Aplicar constelaciones y máscara
            estado_coinstelaciones = aplicar_constelaciones(gps, glo, gal, bds)
            if estado_coinstelaciones is None:
                agregar_log("[ERROR] Fallo al aplicar constelaciones de la mejor configuración.")
                return None

            estado_mascara = aplicar_mascara(mascara)
            if estado_mascara is None:
                agregar_log("[ERROR] Fallo al aplicar la máscara de la mejor configuración.")
                return None

            agregar_log("[INFO] Configuración previa >99% aplicada correctamente.")
            return True

        except Exception as e:
            agregar_log(f"[WARN] No se pudo parsear/aplicar la mejor configuración previa: {e}")
            return None

    except Exception as e:
        agregar_log(f"[WARN] Error al leer CONFIG_CONSTELACIONES.txt: {e}")
        return None
