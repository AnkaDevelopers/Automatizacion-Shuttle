# AbrirShuttle.py
from pathlib import Path
import subprocess

# Importar la ruta desde config.py
from config.config import ruta_shuttle


# Función que ejecuta el el programa Shuttle
def abrir_shuttle(tipo_config_shuttle): # aca enviara el numero del indice del shuttle par abrir

    ruta = Path(ruta_shuttle[tipo_config_shuttle])

    if not ruta.exists():
        print(f"⚠️ La ruta no existe: {ruta}")
        return None

    try:
        # Ejecutar el programa Shuttle
        subprocess.Popen([str(ruta)])
        print(f"✅ Shuttle abierto desde: {ruta}")
        return True
    
    except Exception as e:
        print(f"❌ Error al abrir Shuttle: {e}")
        return None

