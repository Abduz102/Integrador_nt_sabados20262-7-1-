import pandas as pd
from notebook.exportaciones.exportar_usuario import CARPETA_LIMPIOS, CARPETA_REPORTES, preparar_carpeta

RUTA_LIMPIO=CARPETA_LIMPIOS/"empresa_limpio.csv"


def guardar(resultado,numero):
    """Guarda el resultado de una consulta como empresa_consulta_N.csv."""
    ruta=preparar_carpeta(CARPETA_REPORTES)/f"empresa_consulta_{numero}.csv"
    resultado.to_csv(ruta,index=False,sep=";",encoding="utf-8-sig")


def consulta_1(df):
    """Consulta 1: empresas que estan activas."""
    print("\nConsulta 1 - Que empresas estan activas?")
    activas=df[df["activa"]==True]
    print(activas[["nombre","sector","correo"]].head(10))
    print(f"Total activas: {len(activas)}")
    guardar(activas,1)
    return activas


def consulta_2(df):
    """Consulta 2: cuantas empresas hay por sector."""
    print("\nConsulta 2 - Cuantas empresas hay por sector?")
    conteo=df["sector"].value_counts()
    print(conteo)
    guardar(conteo.rename("cantidad").reset_index(),2)
    return conteo


def consulta_3(df):
    """Consulta 3 (GROUPBY): total, activas y porcentaje de activas por sector."""
    print("\nConsulta 3 - Cuantas empresas activas hay por sector y que porcentaje son?")
    df=df.assign(es_activa=(df["activa"]==True))
    resumen=df.groupby("sector")["es_activa"].agg(total="count",activas="sum")
    resumen["porcentaje_activas"]=(resumen["activas"]/resumen["total"]*100).round(1)
    resumen=resumen.sort_values("porcentaje_activas",ascending=False)
    print(resumen)
    guardar(resumen.reset_index(),3)
    return resumen


def consulta_4(df):
    """Consulta 4: empresas con datos de contacto incompletos (sin contacto o sin correo)."""
    print("\nConsulta 4 - Que empresas tienen el contacto o el correo vacio?")
    incompletas=df[df["contacto"].isna() | df["correo"].isna()]
    print(incompletas[["nombre","contacto","correo"]].head(10))
    print(f"Total incompletas: {len(incompletas)}")
    guardar(incompletas,4)
    return incompletas


def consulta_5(df):
    """Consulta 5 (GROUPBY): cuantas empresas usan cada dominio de correo."""
    print("\nConsulta 5 - Cuantas empresas hay por dominio de correo?")
    con_correo=df.dropna(subset=["correo"])
    dominio=con_correo["correo"].str.split("@").str[1]
    por_dominio=con_correo.groupby(dominio)["id"].count().sort_values(ascending=False)
    print(por_dominio)
    resultado=por_dominio.rename("cantidad").reset_index().rename(columns={"correo":"dominio"})
    guardar(resultado,5)
    return por_dominio


def main():
    #Se lee el archivo LIMPIO; nit y telefono como texto para no perder ceros
    df=pd.read_csv(RUTA_LIMPIO,sep=";",encoding="utf-8-sig",dtype={"nit":str,"telefono":str})
    for consulta in (consulta_1,consulta_2,consulta_3,consulta_4,consulta_5):
        consulta(df)


if __name__=="__main__":
    main()