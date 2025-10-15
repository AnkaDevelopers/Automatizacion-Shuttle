# config_constelaciones_helpers.py

import os
from Monitor.log.log import agregar_log

    # Devuelve la ruta absoluta al archivo CONFIG_CONSTELACIONES.txt.
def ruta_config_txt(ruta_base: str) -> str:
    return os.path.join(ruta_base, "CONFIG_CONSTELACIONES.txt")

    # Clave canónica (sin porcentaje) para detectar duplicados. 
def clave_config(gps: bool, glo: bool, gal: bool, bds: bool, mascara: int) -> str:
    return f"GPS={gps}, GLO={glo}, GAL={gal}, BDS={bds}, MASCARA={mascara}"

    # Lee CONFIG_CONSTELACIONES.txt (si existe) y devuelve un set de claves:
    #'GPS=..., GLO=..., GAL=..., BDS=..., MASCARA=...'
def cargar_configs_ejecutadas(ruta_base: str) -> set:
    
    ejecutadas = set()
    try:
        ruta_archivo = ruta_config_txt(ruta_base)
        if not os.path.exists(ruta_archivo):
            return ejecutadas

        with open(ruta_archivo, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                base = line.split(", PORCENTAJE")[0]  # descartar porcentaje si está
                base = ", ".join([p.strip() for p in base.split(",")])  # normalizar espacios
                ejecutadas.add(base)
    except Exception as e:
        agregar_log(f"[WARN] No se pudieron cargar configs ejecutadas: {e}")
    return ejecutadas
