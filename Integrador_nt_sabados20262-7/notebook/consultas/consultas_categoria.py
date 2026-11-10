import pandas as pd
from notebook.exportaciones.exportar_usuario import CARPETA_LIMPIOS, CARPETA_REPORTES, preparar_carpeta

RUTA_LIMPIO=CARPETA_LIMPIOS/"categoria_limpio.csv"


def guardar(resultado,numero):
    """Guarda el resultado de una consulta como categoria_consulta_N.csv."""
    ruta=preparar_carpeta(CARPETA_REPORTES)/f"categoria_consulta_{numero}.csv"
    resultado.to_csv(ruta,index=False,sep=";",encoding="utf-8-sig")


def consulta_1(df):
    """Consulta 1: categorias que no tienen descripcion."""
    print("\nConsulta 1 - Que categorias no tienen descripcion?")
    sin_descripcion=df[df["descripcion"]=="Sin descripcion"]
    print(sin_descripcion[["nombre","area_responsable"]].head(10))
    print(f"Total sin descripcion: {len(sin_descripcion)}")
    guardar(sin_descripcion,1)
    return sin_descripcion


def consulta_2(df):
    """Consulta 2: cuantos registros hay por nombre de categoria."""
    print("\nConsulta 2 - Cuantos registros hay por categoria?")
    conteo=df["nombre"].value_counts()
    print(conteo)
    guardar(conteo.rename("cantidad").reset_index(),2)
    return conteo


def consulta_3(df):
    """Consulta 3 (GROUPBY): cuantas categorias tiene cada area responsable."""
    print("\nConsulta 3 - Cuantas categorias tiene cada area responsable?")
    por_area=df.groupby("area_responsable")["id"].count().sort_values(ascending=False)
    print(por_area)
    guardar(por_area.rename("cantidad").reset_index(),3)
    return por_area


def consulta_4(df):
    """Consulta 4 (GROUPBY): cuantas categorias de cada nombre maneja cada area."""
    print("\nConsulta 4 - Cuantas categorias de cada nombre maneja cada area?")
    cruce=df.groupby(["area_responsable","nombre"])["id"].count().rename("cantidad")
    print(cruce.head(15))
    guardar(cruce.reset_index(),4)
    return cruce


def consulta_5(df):
    """Consulta 5 (GROUPBY): porcentaje de categorias con descripcion por area."""
    print("\nConsulta 5 - Que porcentaje de categorias tiene descripcion en cada area?")
    df=df.assign(tiene_descripcion=(df["descripcion"]!="Sin descripcion"))
    porcentaje=(df.groupby("area_responsable")["tiene_descripcion"].mean()*100).round(1)
    print(porcentaje)
    guardar(porcentaje.rename("porcentaje_con_descripcion").reset_index(),5)
    return porcentaje


def main():
    #Se lee el archivo LIMPIO, no el crudo
    df=pd.read_csv(RUTA_LIMPIO,sep=";",encoding="utf-8-sig")
    for consulta in (consulta_1,consulta_2,consulta_3,consulta_4,consulta_5):
        consulta(df)


if __name__=="__main__":
    main()