"""HU - Cinco consultas sobre retos con pandas (incluye groupby).

Lee data/limpio/retos_limpio.csv y guarda cada resultado en
data/limpio/retos_consulta_N.csv.

Uso (desde la raiz del proyecto):
    python notebook/consultas/consultas_reto.py
"""
from pathlib import Path

import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
CARPETA_LIMPIO = RAIZ / "data" / "limpio"
RUTA_LIMPIO = CARPETA_LIMPIO / "retos_limpio.csv"


def guardar(resultado, numero):
    """Guarda el resultado de una consulta como retos_consulta_N.csv."""
    ruta = CARPETA_LIMPIO / f"retos_consulta_{numero}.csv"
    resultado.to_csv(ruta, index=False, encoding="utf-8")


def consulta_1(df):
    """Consulta 1: retos que estan en curso."""
    print("\nConsulta 1 - Que retos estan en curso?")
    en_curso = df[df["estado"] == "EN_CURSO"]
    print(en_curso[["nombre", "fecha_inicio", "fecha_fin"]].head(10))
    print(f"Total en curso: {len(en_curso)}")
    guardar(en_curso, 1)
    return en_curso


def consulta_2(df):
    """Consulta 2: los 10 retos mas largos (solo con fechas validas)."""
    print("\nConsulta 2 - Cuales son los 10 retos mas largos?")
    validos = df[df["fecha_valida"]]
    largos = validos.nlargest(10, "duracion_dias")[["nombre", "duracion_dias", "estado"]]
    print(largos)
    guardar(largos, 2)
    return largos


def consulta_3(df):
    """Consulta 3: cuantos retos hay por estado."""
    print("\nConsulta 3 - Cuantos retos hay por estado?")
    conteo = df["estado"].value_counts()
    print(conteo)
    guardar(conteo.rename("cantidad").reset_index(), 3)
    return conteo


def consulta_4(df):
    """Consulta 4 (GROUPBY): duracion promedio, minima y maxima por estado."""
    print("\nConsulta 4 - Cual es la duracion promedio, minima y maxima por estado?")
    validos = df[df["fecha_valida"]]
    resumen = validos.groupby("estado")["duracion_dias"].agg(["count", "mean", "min", "max"])
    print(resumen)
    guardar(resumen.reset_index(), 4)
    return resumen


def consulta_5(df):
    """Consulta 5 (GROUPBY): cuantos retos empiezan cada mes."""
    print("\nConsulta 5 - Cuantos retos empiezan cada mes?")
    por_mes = df.groupby(df["fecha_inicio"].dt.to_period("M"))["id"].count()
    print(por_mes)
    resultado = por_mes.rename("cantidad").reset_index()
    resultado["fecha_inicio"] = resultado["fecha_inicio"].astype(str)
    guardar(resultado, 5)
    return por_mes


def main():
    #Se lee el archivo LIMPIO, no el sucio
    df = pd.read_csv(RUTA_LIMPIO, parse_dates=["fecha_inicio", "fecha_fin"])
    for consulta in (consulta_1, consulta_2, consulta_3, consulta_4, consulta_5):
        consulta(df)


if __name__ == "__main__":
    main()