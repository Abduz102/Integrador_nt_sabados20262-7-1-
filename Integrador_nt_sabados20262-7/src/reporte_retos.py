"""Reporte de la tabla retos.

Lee data/limpio/retos_limpio.csv, arma tres graficas con matplotlib a partir
de las consultas de la etapa anterior, las guarda en reportes/ e imprime las
conclusiones.

Uso (desde cualquier carpeta):
    python src/reporte_retos.py
"""
import os
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # Sin ventana: el script nunca se queda esperando.
import matplotlib.pyplot as plt
import pandas as pd

# Las rutas relativas (data/..., reportes/...) siempre parten de la raiz del proyecto.
RAIZ = Path(__file__).resolve().parents[1]
os.chdir(RAIZ)

RUTA_LIMPIO = "data/limpio/retos_limpio.csv"

MESES = {
    1: "enero", 2: "febrero", 3: "marzo", 4: "abril", 5: "mayo", 6: "junio",
    7: "julio", 8: "agosto", 9: "septiembre", 10: "octubre",
    11: "noviembre", 12: "diciembre",
}

# Posibles razones por las que los retos se concentran en cada mes.
RAZONES = {
    1: "la gente se pone propositos al empezar el ano",
    2: "muchos retos de enero se renuevan o se retoman un mes despues",
    3: "es el arranque del ano laboral y academico en muchos lugares",
    4: "es el inicio del segundo trimestre y se retoman metas",
    5: "se aprovecha la mitad del primer semestre para lanzar retos nuevos",
    6: "la gente se organiza antes de las vacaciones de mitad de ano",
    7: "las vacaciones de mitad de ano dan tiempo libre para retos nuevos",
    8: "se reinician las rutinas tras las vacaciones",
    9: "empieza el ultimo trimestre y se ponen metas de cierre de ano",
    10: "se busca cumplir metas antes de que termine el ano",
    11: "hay campanas de fin de ano como el Black Friday",
    12: "se aprovechan las fiestas y las vacaciones de fin de ano",
}


def leer_datos(ruta):
    """Lee el CSV limpio y convierte fechas y duracion a sus tipos correctos."""
    df = pd.read_csv(ruta, sep=None, engine="python", encoding="utf-8-sig")
    df["fecha_inicio"] = pd.to_datetime(df["fecha_inicio"], errors="coerce")
    df["fecha_fin"] = pd.to_datetime(df["fecha_fin"], errors="coerce")
    if "duracion_dias" in df.columns:
        df["duracion_dias"] = pd.to_numeric(df["duracion_dias"], errors="coerce")
    else:
        # Si el archivo no trae la duracion, se calcula con las fechas.
        df["duracion_dias"] = (df["fecha_fin"] - df["fecha_inicio"]).dt.days
    return df


def guardar_grafica(nombre_archivo, titulo, xlabel, ylabel):
    """Pone titulo y ejes, ajusta el diseno, guarda la imagen y cierra la figura."""
    plt.title(titulo)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    ruta = os.path.join("reportes", nombre_archivo)
    plt.savefig(ruta, dpi=120)
    plt.close()
    return ruta


def retos_por_mes(df):
    """Cuenta cuantos retos empiezan en cada mes (ano-mes), en orden cronologico."""
    meses = df["fecha_inicio"].dropna().dt.to_period("M")
    por_mes = meses.value_counts().sort_index()
    # Se incluyen los meses sin retos con valor 0 para que la linea no los salte.
    todos = pd.period_range(por_mes.index.min(), por_mes.index.max(), freq="M")
    por_mes = por_mes.reindex(todos, fill_value=0)
    por_mes.index = por_mes.index.astype(str)  # Etiquetas tipo "2026-01".
    return por_mes


def grafica_1(df):
    """Grafica 1 (barras): cantidad de retos por estado."""
    conteo = df["estado"].value_counts()
    plt.figure(figsize=(7, 5))
    conteo.plot(kind="bar")
    plt.xticks(rotation=0)
    return guardar_grafica(
        "retos_grafica_1.png", "Cantidad de retos por estado", "Estado", "Cantidad de retos"
    )


def grafica_2(df):
    """Grafica 2 (linea): retos que empiezan cada mes."""
    por_mes = retos_por_mes(df)
    plt.figure(figsize=(9, 5))
    por_mes.plot(kind="line", marker="o")
    plt.xticks(range(len(por_mes)), por_mes.index, rotation=45)
    return guardar_grafica(
        "retos_grafica_2.png", "Retos que empiezan cada mes", "Mes de inicio", "Cantidad de retos"
    )


def grafica_3(df):
    """Grafica 3 (histograma): como se reparte la duracion de los retos."""
    plt.figure(figsize=(7, 5))
    df["duracion_dias"].plot(kind="hist", bins=20)
    return guardar_grafica(
        "retos_grafica_3.png",
        "Distribucion de la duracion de los retos",
        "Duracion (dias)",
        "Cantidad de retos",
    )


def contar_fechas_invertidas(df):
    """Cuenta los retos cuya fecha de fin es anterior a la de inicio."""
    return int((df["fecha_fin"] < df["fecha_inicio"]).sum())


def conclusiones(df):
    """Arma el texto con las tres preguntas de la HU."""
    por_mes = retos_por_mes(df)
    mes_pico = por_mes.idxmax()
    numero_mes = int(mes_pico.split("-")[1])

    # El promedio solo usa retos con fechas coherentes: una duracion negativa no es real.
    validos = df[df["duracion_dias"] >= 0]
    promedios = validos.groupby("estado")["duracion_dias"].mean().round(1)
    lineas_estado = [f"   - {estado}: {dias} dias" for estado, dias in promedios.items()]
    descartados = int(df["duracion_dias"].notna().sum() - len(validos))
    sin_fin = int(df["fecha_fin"].isna().sum())

    invertidas = contar_fechas_invertidas(df)

    lineas = [
        "CONCLUSIONES",
        f"1. Mes de mayor concentracion: {MESES[numero_mes]} ({mes_pico}) con "
        f"{int(por_mes.max())} retos de {len(df)}. Puede ser porque {RAZONES[numero_mes]}.",
        "2. Duracion promedio de un reto segun su estado:",
        *lineas_estado,
        f"   (no cuentan {descartados} retos con fechas invertidas ni {sin_fin} sin fecha de fin)",
        f"3. Retos con la fecha de fin antes que la de inicio: {invertidas} "
        "(dato para el back: hay que validar que fecha_fin sea mayor o igual a fecha_inicio).",
    ]
    return "\n".join(lineas)


def main():
    """Lee el CSV, crea las graficas, imprime sus rutas y las conclusiones."""
    df = leer_datos(RUTA_LIMPIO)
    os.makedirs("reportes", exist_ok=True)

    print("Graficas guardadas:")
    for funcion in (grafica_1, grafica_2, grafica_3):
        print(f"  {funcion(df)}")

    print()
    print(conclusiones(df))


if __name__ == "__main__":
    main()
