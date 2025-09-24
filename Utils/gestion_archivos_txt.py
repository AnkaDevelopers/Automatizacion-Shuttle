# gestion_archivos_txt.py

# ------------------------------------------------------------------
# Importaciones necesarias
# ------------------------------------------------------------------
from typing import Optional
import subprocess
import shutil


# ------------------------------------------------------------------
# Función: abrir_txt
# ------------------------------------------------------------------
# Mantiene la versión anterior (solo abre desde Python si se necesita).
# No se usa para el caso de GNSS.txt que abre un proceso externo.
# ------------------------------------------------------------------
def abrir_txt(ruta: str, modo: str = "r"):
    try:
        f = open(ruta, modo, encoding="utf-8")
        print(f"[SUCCESS] Archivo abierto desde Python: {ruta} | modo={modo}")
        return f
    except Exception as e:
        print(f"[ERROR] No se pudo abrir el archivo '{ruta}' en modo '{modo}': {e}")
        return None


# ------------------------------------------------------------------
# Función: cerrar_todos_txt
# ------------------------------------------------------------------
# Cierra el/los procesos de Windows que mantienen abierto el archivo
# GNSS.txt (por ejemplo, Notepad).
#
# Retorna:
#   - True  -> si se cerró al menos un proceso.
#   - False -> si se intentó y falló.
#   - None  -> si no se encontraron procesos relevantes.
# ------------------------------------------------------------------
def cerrar_todos_txt(nombre_archivo: str = "GNSS.txt") -> Optional[bool]:
    try:
        print(f"[INFO] Buscando procesos que puedan tener abierto '{nombre_archivo}'...")

        # ------------------------------------------------------------------
        # 1. Procesos comunes que abren .txt en Windows
        # ------------------------------------------------------------------
        candidatos = ["notepad.exe", "notepad++.exe", "wordpad.exe"]

        # ------------------------------------------------------------------
        # 2. Buscar procesos en ejecución
        # ------------------------------------------------------------------
        lista_procesos = []
        proc = subprocess.run(
            ["tasklist"],
            capture_output=True,
            text=True,
            errors="replace"
        )
        salida = proc.stdout.lower()

        for cand in candidatos:
            if cand in salida:
                lista_procesos.append(cand)

        if not lista_procesos:
            print("[INFO] No se encontraron editores de texto abiertos.")
            return None

        # ------------------------------------------------------------------
        # 3. Intentar cerrar cada proceso detectado
        # ------------------------------------------------------------------
        exito = False
        error = False

        for proc_name in lista_procesos:
            try:
                resultado = subprocess.run(
                    ["taskkill", "/F", "/IM", proc_name],
                    capture_output=True,
                    text=True
                )
                if resultado.returncode == 0:
                    print(f"[SUCCESS] Proceso cerrado: {proc_name}")
                    exito = True
                else:
                    print(f"[ERROR] No se pudo cerrar {proc_name}: {resultado.stderr.strip()}")
                    error = True
            except Exception as e:
                print(f"[ERROR] Excepción al intentar cerrar {proc_name}: {e}")
                error = True

        if exito and not error:
            return True
        if exito and error:
            return False
        return False

    except Exception as e:
        print(f"[EXCEPTION] Error inesperado en 'cerrar_txt_externo': {e}")
        return False
