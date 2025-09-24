# calculo_porcentaje_de_conformidad_reporte_gnss.py
# ------------------------------------------------------------------
# Módulo: calculo_porcentaje_de_conformidad_reporte_gnss
# ------------------------------------------------------------------
# Este módulo recibe la ruta de un archivo .txt con datos GNSS
# Evalúa la última columna de cada fila y calcula el porcentaje
# de filas cuyo valor es 0.
#
# Retornos:
#   - (True, porcentaje)  -> Si porcentaje >= 90%
#   - (None, porcentaje)  -> Si porcentaje < 90%
#   - (False, None)       -> Si ocurre algún error
# ------------------------------------------------------------------

def calcular_conformidad(ruta_txt: str):
    try:
        total_filas = 0
        filas_cero = 0

        with open(ruta_txt, "r", encoding="utf-8", errors="ignore") as f:
            for linea in f:
                linea = linea.strip()
                if not linea:
                    continue  # saltar líneas vacías
                partes = linea.split()
                if not partes:
                    continue

                try:
                    # Tomar la última columna
                    valor_final = int(partes[-1])
                except ValueError:
                    continue  # Si no es número, ignorar fila

                total_filas += 1
                if valor_final == 0:
                    filas_cero += 1

        if total_filas == 0:
            return False, None  # Archivo vacío o inválido

        porcentaje = (filas_cero / total_filas) * 100

        if porcentaje >= 90:
            return True, round(porcentaje, 2)
        else:
            return None, round(porcentaje, 2)

    except Exception as e:
        # Si ocurre cualquier error no controlado
        return False, None


