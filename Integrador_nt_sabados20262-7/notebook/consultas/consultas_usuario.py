import pandas as pd
from notebook.exportaciones.exportar_usuario import CARPETA_LIMPIOS, CARPETA_REPORTES, preparar_carpeta

RUTA_LIMPIO=CARPETA_LIMPIOS/"usuario_limpio.csv"


def guardar(resultado,numero):
    """Guarda el resultado de una consulta como usuario_consulta_N.csv."""
    ruta=preparar_carpeta(CARPETA_REPORTES)/f"usuario_consulta_{numero}.csv"
    resultado.to_csv(ruta,index=False,sep=";",encoding="utf-8-sig")


def consulta_1(df):
    """Consulta 1: usuarios que estan activos."""
    print("\nConsulta 1 - Que usuarios estan activos?")
    activos=df[df["activo"]==True]
    print(activos[["nombre","correo","rol"]].head(10))
    print(f"Total activos: {len(activos)}")
    guardar(activos.drop(columns=["contrasena_hash"]),1)
    return activos


def consulta_2(df):
    """Consulta 2: cuantos usuarios hay por rol."""
    print("\nConsulta 2 - Cuantos usuarios hay por rol?")
    conteo=df["rol"].value_counts()
    print(conteo)
    guardar(conteo.rename("cantidad").reset_index(),2)
    return conteo


def consulta_3(df):
    """Consulta 3 (GROUPBY): total, activos y porcentaje de activos por rol."""
    print("\nConsulta 3 - Cuantos usuarios activos hay por rol y que porcentaje son?")
    df=df.assign(es_activo=(df["activo"]==True))
    resumen=df.groupby("rol")["es_activo"].agg(total="count",activos="sum")
    resumen["porcentaje_activos"]=(resumen["activos"]/resumen["total"]*100).round(1)
    print(resumen)
    guardar(resumen.reset_index(),3)
    return resumen


def consulta_4(df):
    """Consulta 4 (GROUPBY): cuantos usuarios se registran cada mes."""
    print("\nConsulta 4 - Cuantos usuarios se registran cada mes?")
    por_mes=df.groupby(df["fecha_registro"].dt.to_period("M"))["id"].count()
    print(por_mes)
    resultado=por_mes.rename("cantidad").reset_index()
    resultado["fecha_registro"]=resultado["fecha_registro"].astype(str)
    guardar(resultado,4)
    return por_mes


def consulta_5(df):
    """Consulta 5: los 10 usuarios registrados mas recientemente."""
    print("\nConsulta 5 - Cuales son los 10 usuarios registrados mas recientemente?")
    recientes=df.nlargest(10,"fecha_registro")[["nombre","rol","fecha_registro"]]
    print(recientes)
    guardar(recientes,5)
    return recientes


def main():
    #Se lee el archivo LIMPIO, no el crudo
    df=pd.read_csv(RUTA_LIMPIO,sep=";",encoding="utf-8-sig",parse_dates=["fecha_registro"])
    for consulta in (consulta_1,consulta_2,consulta_3,consulta_4,consulta_5):
        consulta(df)


if __name__=="__main__":
    main()
