"""HU - Limpia los datos de retos con pandas.

Lee data/crudo/retos_sucio.csv y guarda data/limpio/retos_limpio.csv.

Uso (desde la raiz del proyecto):
    python notebook/limpiezas/limpiar_reto.py
"""
import os
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
RUTA_SUCIO = RAIZ / "data" / "crudo" / "retos_sucio.csv"
CARPETA_LIMPIO = RAIZ / "data" / "limpio"
RUTA_LIMPIO = CARPETA_LIMPIO / "retos_limpio.csv"

#Columnas que no pueden quedar con nulos. fecha_fin y duracion_dias quedan fuera
#porque un reto puede no tener fecha de fin todavia.
COLUMNAS_OBLIGATORIAS = ["id", "nombre", "descripcion", "fecha_inicio", "estado",
                         "id_empresa", "id_categoria", "id_prioridad"]


def imprimir_diagnostico(df, titulo):
    """Imprime shape, info, nulos por columna y duplicados exactos."""
    print(f"\n===== {titulo} =====")
    print("shape:", df.shape)
    df.info()
    print("\nNulos por columna:")
    print(df.isna().sum())
    print("\nDuplicados exactos:", df.duplicated().sum())


def convertir_fecha(serie):
    """Convierte texto en fechas aunque vengan en dos formatos (2026-03-02 y 02/03/2026).

    pandas con dayfirst=True lee mal el formato ISO ("2026-03-02" lo vuelve 3 de febrero),
    asi que primero se toman las fechas ISO y solo el resto se lee dia primero.
    """
    iso = pd.to_datetime(serie, format="%Y-%m-%d", errors="coerce")
    mixto = pd.to_datetime(serie, format="mixed", dayfirst=True, errors="coerce")
    return iso.fillna(mixto)


def limpiar_retos(df):
    """Aplica todas las limpiezas y devuelve el DataFrame limpio."""
    #Quitar los duplicados exactos
    df = df.drop_duplicates()

    #Convertir las fechas
    df["fecha_inicio"] = convertir_fecha(df["fecha_inicio"])
    df["fecha_fin"] = convertir_fecha(df["fecha_fin"])

    #Quitar espacios sobrantes del nombre
    df["nombre"] = df["nombre"].str.strip()

    #Unificar el estado: 'en_curso', 'EN CURSO' -> EN_CURSO
    df["estado"] = df["estado"].str.strip().str.upper().str.replace(" ", "_")

    #Rellenar las descripciones vacias
    df["descripcion"] = df["descripcion"].fillna("Sin descripcion")

    #Duracion en dias y marca de fechas incoherentes (fin antes que inicio)
    df["duracion_dias"] = (df["fecha_fin"] - df["fecha_inicio"]).dt.days
    df["fecha_valida"] = df["duracion_dias"] >= 0
    return df


def main():
    df = pd.read_csv(RUTA_SUCIO)

    #Diagnostico inicial
    imprimir_diagnostico(df, "DIAGNOSTICO INICIAL")
    nulos_antes = df.isna().sum()
    filas_antes = len(df)

    df = limpiar_retos(df)

    #Fechas incoherentes: fin antes que inicio (las que no tienen fecha_fin se cuentan aparte)
    incoherentes = int((df["duracion_dias"] < 0).sum())
    sin_fin = int(df["fecha_fin"].isna().sum())
    print(f"\nFechas incoherentes (fecha_fin antes que fecha_inicio): {incoherentes}")
    print(f"Retos sin fecha_fin (no se puede calcular la duracion): {sin_fin}")

    #Nulos antes y despues
    print("\nNulos ANTES de limpiar:")
    print(nulos_antes)
    print("\nNulos DESPUES de limpiar:")
    print(df.isna().sum())

    #Resultado final
    print("\nshape final:", df.shape)
    print(f"Filas eliminadas: {filas_antes - len(df)}")

    #Comprobacion: ningun nulo obligatorio ni duplicado exacto
    nulos_obligatorias = int(df[COLUMNAS_OBLIGATORIAS].isna().sum().sum())
    duplicados = int(df.duplicated().sum())
    print(f"Nulos en columnas obligatorias: {nulos_obligatorias} | Duplicados exactos: {duplicados}")
    assert nulos_obligatorias == 0 and duplicados == 0, "La limpieza dejo nulos o duplicados"

    #Guardar el resultado
    os.makedirs(CARPETA_LIMPIO, exist_ok=True)
    df.to_csv(RUTA_LIMPIO, index=False, encoding="utf-8")
    print("Guardado en:", RUTA_LIMPIO)


if __name__ == "__main__":
    main()