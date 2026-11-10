"""Reporte de la tabla empresas.

Lee data/limpio/empresas_limpio.csv, arma tres graficas con matplotlib a
partir de las consultas de la etapa anterior, las guarda en reportes/ e
imprime las conclusiones.

Uso (desde cualquier carpeta):
    python src/reporte_empresas.py
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

RUTA_LIMPIO = "data/limpio/empresas_limpio.csv"
RUTA_CRUDO = "datos/crudos/empresa_crudo.csv"  # Solo se usa para contar los correos invalidos.


def a_booleano(valor):
    """Convierte True/False/'True'/'SI'/'1'... en booleano; lo desconocido queda vacio."""
    if isinstance(valor, bool):
        return valor
    if pd.isna(valor):
        return pd.NA
    texto = str(valor).strip().lower()
    if texto in ("true", "1", "si", "sí"):
        return True
    if texto in ("false", "0", "no"):
        return False
    return pd.NA


def leer_datos(ruta):
    """Lee el CSV limpio (nit y telefono como texto para no perder ceros)."""
    df = pd.read_csv(ruta, sep=None, engine="python", encoding="utf-8-sig",
                     dtype={"nit": str, "telefono": str})
    df["activa"] = df["activa"].map(a_booleano).astype(object)
    return df.dropna(subset=["activa"]).reset_index(drop=True)


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


# ---------- Graficas ----------

def grafica_1(df):
    """Grafica 1 (barras): cantidad de empresas por sector."""
    por_sector = df["sector"].value_counts()
    plt.figure(figsize=(9, 6))
    por_sector.plot(kind="bar")
    plt.xticks(rotation=45, ha="right")
    return guardar_grafica(
        "empresas_grafica_1.png",
        "Cantidad de empresas por sector",
        "Sector",
        "Cantidad de empresas",
    )


def grafica_2(df):
    """Grafica 2 (torta): empresas activas vs inactivas."""
    conteo = df["activa"].value_counts()
    etiquetas = ["Activas" if estado else "Inactivas" for estado in conteo.index]
    plt.figure(figsize=(6, 6))
    df["activa"].value_counts().plot(kind="pie", autopct="%1.1f%%", labels=etiquetas)
    return guardar_grafica(
        "empresas_grafica_2.png",
        "Empresas activas vs inactivas",
        "Estado de la empresa",
        "",
    )


def grafica_3(df):
    """Grafica 3 (barras apiladas): activas e inactivas por sector."""
    tabla = pd.crosstab(df["sector"], df["activa"])
    tabla = tabla.rename(columns={True: "Activas", False: "Inactivas"})
    tabla = tabla.reindex(columns=["Activas", "Inactivas"], fill_value=0)
    tabla = tabla.loc[tabla.sum(axis=1).sort_values(ascending=False).index]
    plt.figure(figsize=(9, 6))
    tabla.plot(kind="bar", stacked=True)
    plt.xticks(rotation=45, ha="right")
    plt.legend(title="Estado")
    return guardar_grafica(
        "empresas_grafica_3.png",
        "Empresas activas e inactivas por sector",
        "Sector",
        "Cantidad de empresas",
    )


# ---------- Conclusiones ----------

def contar_correos_invalidos(df):
    """Cuenta los correos invalidos (un correo sin @ queda vacio en la limpieza).

    Si el crudo existe se cuentan ahi (lo que realmente aparecio); si no, se cuentan
    los correos vacios del limpio.
    """
    if os.path.exists(RUTA_CRUDO):
        crudo = pd.read_csv(RUTA_CRUDO, sep=";", encoding="utf-8-sig", dtype=str)
        correo = crudo["correo"].dropna().str.strip()
        return int((~correo.str.contains("@")).sum()), "el crudo"
    return int(df["correo"].isna().sum()), "el limpio"


def conclusiones(df):
    """Arma el texto con las preguntas de la HU."""
    por_sector = df["sector"].value_counts()
    sector_top = por_sector.index[0]
    sin_sector = int(df["sector"].isna().sum())

    total = len(df)
    inactivas = int((df["activa"] == False).sum())  # noqa: E712
    porcentaje_inactivas = round(inactivas / total * 100, 1)

    invalidos, origen = contar_correos_invalidos(df)

    lineas = [
        "CONCLUSIONES",
        f"1. Sector con mas empresas: {sector_top} con {int(por_sector.iloc[0])} de {total} "
        f"({int(por_sector.index.size)} sectores en total; {sin_sector} empresas sin sector).",
        f"2. Empresas inactivas: {inactivas} de {total} ({porcentaje_inactivas}%). "
        "Significa que buena parte de las empresas registradas no esta operando en la plataforma: "
        "no publican retos ni reciben participantes, asi que el numero total de empresas exagera "
        "el uso real. Conviene medir la actividad (no solo el registro) y revisar por que se inactivan.",
        f"3. Correos invalidos en {origen}: {invalidos} (les faltaba la @). Hay que validarlos en el "
        "back porque el correo es el medio de contacto y de notificacion: si se guarda uno mal "
        "escrito, el mensaje nunca llega y despues no hay como corregirlo. Validar el formato al "
        "registrar (y pedir confirmacion) evita limpiar estos datos a mano.",
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
