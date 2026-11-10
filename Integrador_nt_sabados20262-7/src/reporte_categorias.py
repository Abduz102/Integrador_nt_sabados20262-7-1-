"""Reporte de la tabla categorias.

Lee data/limpio/categorias_limpio.csv, arma tres graficas con matplotlib a
partir de las consultas de la etapa anterior, las guarda en reportes/ e
imprime las conclusiones.

Uso (desde cualquier carpeta):
    python src/reporte_categorias.py
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

RUTA_LIMPIO = "data/limpio/categorias_limpio.csv"
RUTA_CRUDO = "datos/crudos/categoria_crudo.csv"  # Solo se usa para contar lo que se elimino.
SIN_DESCRIPCION = "Sin descripcion"
CATEGORIAS_ESPERADAS = 10


def leer_datos(ruta):
    """Lee el CSV limpio (separador ; y utf-8-sig, como lo exporta el proyecto)."""
    return pd.read_csv(ruta, sep=None, engine="python", encoding="utf-8-sig")


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


# ---------- Consultas de la etapa anterior ----------

def consulta_conteo(df):
    """Consulta 2: cuantas veces aparece cada categoria."""
    return df["nombre"].value_counts()


def consulta_por_area(df):
    """Consulta 3: cuantas categorias tiene cada area responsable."""
    return df.groupby("area_responsable")["id"].count().sort_values(ascending=False)


def consulta_largos(df):
    """Largo promedio (en caracteres) de la descripcion por categoria.

    Se dejan por fuera las filas 'Sin descripcion': es un texto de relleno de la
    limpieza, no una descripcion real, y bajaria el promedio de forma artificial.
    """
    con_descripcion = df[df["descripcion"] != SIN_DESCRIPCION]
    largo = con_descripcion["descripcion"].str.len()
    return largo.groupby(con_descripcion["nombre"]).mean().round(1).sort_values(ascending=False)


# ---------- Graficas ----------

def grafica_1(conteo):
    """Grafica 1 (barras horizontales): cuantas veces aparece cada categoria."""
    plt.figure(figsize=(8, 5))
    conteo.sort_values().plot(kind="barh")
    return guardar_grafica(
        "categorias_grafica_1.png",
        "Cantidad de registros por categoria",
        "Cantidad de registros",
        "Categoria",
    )


def grafica_2(por_area):
    """Grafica 2 (torta): reparto de categorias por area responsable."""
    plt.figure(figsize=(7, 6))
    por_area.plot(kind="pie", autopct="%1.1f%%")
    return guardar_grafica(
        "categorias_grafica_2.png",
        "Reparto de categorias por area responsable",
        "Area responsable",
        "",
    )


def grafica_3(largos):
    """Grafica 3 (barras): largo promedio de la descripcion por categoria."""
    plt.figure(figsize=(9, 5))
    largos.plot(kind="bar")
    plt.xticks(rotation=45, ha="right")
    return guardar_grafica(
        "categorias_grafica_3.png",
        "Largo promedio de la descripcion por categoria",
        "Categoria",
        "Largo promedio (caracteres)",
    )


# ---------- Conclusiones ----------

def conclusiones(df, conteo, por_area, largos):
    """Arma el texto con las preguntas de la HU."""
    reales = df["nombre"].nunique()
    sin_descripcion = int((df["descripcion"] == SIN_DESCRIPCION).sum())

    if os.path.exists(RUTA_CRUDO):
        crudo = pd.read_csv(RUTA_CRUDO, sep=";", encoding="utf-8-sig")
        eliminadas = len(crudo) - len(df)
        variantes = crudo["nombre"].nunique()
        punto_1 = (
            f"1. Filas eliminadas: {eliminadas} (el crudo tenia {len(crudo)} y el limpio quedo con "
            f"{len(df)}, por ids repetidos). Ademas, los nombres escritos de {variantes} formas "
            f"distintas (mayusculas, tildes, espacios) se unificaron en {reales}."
        )
    else:
        punto_1 = (
            f"1. El limpio tiene {len(df)} filas. No se encontro {RUTA_CRUDO}, asi que no se puede "
            "contar cuantas se eliminaron."
        )

    estado = "coincide con las 10 esperadas" if reales == CATEGORIAS_ESPERADAS else (
        f"NO coincide con las {CATEGORIAS_ESPERADAS} esperadas"
    )
    mayor, menor = conteo.index[0], conteo.index[-1]
    area_mayor = por_area.index[0]
    sin_area = int(por_area.get("Sin area", 0))
    largo_max, largo_min = largos.index[0], largos.index[-1]

    lineas = [
        "CONCLUSIONES",
        punto_1,
        f"2. Categorias REALES al final: {reales} ({estado}). La mas repetida es {mayor} "
        f"({int(conteo.iloc[0])} filas) y la menos repetida {menor} ({int(conteo.iloc[-1])}).",
        "3. El back debe declarar `nombre` como UNICO porque hoy cada categoria aparece muchas veces "
        f"({len(df)} filas para solo {reales} nombres). Sin la restriccion UNIQUE la base de datos "
        "acepta 'Ventas', 'VENTAS' y ' ventas' como categorias distintas, se duplican y los conteos "
        "y filtros dejan de ser confiables. Con UNIQUE (y normalizando el texto antes de guardar) "
        "la base rechaza el duplicado desde el inicio.",
        f"4. Otros datos: el area con mas categorias es {area_mayor} ({int(por_area.iloc[0])}); "
        f"{sin_area} filas quedaron sin area y {sin_descripcion} sin descripcion. "
        f"La descripcion mas larga en promedio es la de {largo_max} ({largos.iloc[0]} caracteres) "
        f"y la mas corta la de {largo_min} ({largos.iloc[-1]}).",
    ]
    return "\n".join(lineas)


def main():
    """Lee el CSV, crea las graficas, imprime sus rutas y las conclusiones."""
    df = leer_datos(RUTA_LIMPIO)
    os.makedirs("reportes", exist_ok=True)

    conteo = consulta_conteo(df)
    por_area = consulta_por_area(df)
    largos = consulta_largos(df)

    print("Graficas guardadas:")
    print(f"  {grafica_1(conteo)}")
    print(f"  {grafica_2(por_area)}")
    print(f"  {grafica_3(largos)}")

    print()
    print(conclusiones(df, conteo, por_area, largos))


if __name__ == "__main__":
    main()
