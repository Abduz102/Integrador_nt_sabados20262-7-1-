"""HU X01 - Exporta los datos sucios de retos a CSV, Excel y JSON.

Uso (desde la raiz del proyecto):
    python notebook/exportaciones/exportar_reto.py
"""
import os
import sys
from importlib import import_module
from pathlib import Path

#Carpeta raiz del proyecto (la que contiene src/ y data/)
RAIZ = Path(__file__).resolve().parents[2]
CARPETA_CRUDO = RAIZ / "data" / "crudo"

#Importa la funcion del script anterior; NO se copia el codigo de generacion
sys.path.insert(0, str(RAIZ))
generar_retos = import_module("notebook.simulaciones.simular_reto").generar_retos


def exportar_retos_sucios():
    """Genera el DataFrame sucio y lo guarda en CSV, Excel y JSON dentro de data/crudo."""
    df = generar_retos(500)

    #La carpeta se crea sola si no existe
    os.makedirs(CARPETA_CRUDO, exist_ok=True)

    ruta_csv = CARPETA_CRUDO / "retos_sucio.csv"
    df.to_csv(ruta_csv, index=False, encoding="utf-8")

    ruta_xlsx = CARPETA_CRUDO / "retos_sucio.xlsx"
    df.to_excel(ruta_xlsx, index=False, sheet_name="retos")

    ruta_json = CARPETA_CRUDO / "retos_sucio.json"
    df.to_json(ruta_json, orient="records", force_ascii=False, indent=2)

    #Al final se imprime la ruta y el tamano de cada archivo generado
    for ruta in (ruta_csv, ruta_xlsx, ruta_json):
        print(f"{ruta}  ->  {df.shape}")


if __name__ == "__main__":
    exportar_retos_sucios()