# 🚀 Automatización Shuttle (RPA)

Este proyecto implementa un **RPA (Robotic Process Automation)** para el software **Shuttle**, con el objetivo de automatizar procesos GNSS de forma confiable y repetible.

---

## 📌 Objetivo

El sistema ejecuta automáticamente Shuttle y realiza un flujo completo de procesamiento:

1. **Abrir Shuttle**.
2. **Descomprimir un archivo `.dat`**.
3. **Crear un nuevo proyecto**.
4. **Cargar archivos GNSS** (base y rover).
5. **Generar un reporte** en Shuttle.
6. **Validar el reporte** sobre una columna específica:
   - ✅ Si **90% o más de los valores son 0** → el proceso se considera aprobado.  
   - ❌ Si **menos del 90%** → se dispara una **automatización secundaria**, ajustando parámetros de configuración (red de satélites, desactivaciones y máscara) hasta alcanzar conformidad.

---


