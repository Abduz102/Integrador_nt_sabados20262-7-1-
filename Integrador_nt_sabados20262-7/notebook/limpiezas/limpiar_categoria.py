#Alistamiento para limpieza de categoria
import unicodedata
import pandas as pd
from notebook.limpiezas.limpiar_usuario import verificar_dato_vacio

#Definiendo los datos correctos
CATEGORIAS=["Logística","Ventas","Marketing","Recursos Humanos","Finanzas","Tecnología","Atención al Cliente","Producción","Compras","Calidad"]
AREAS=["Operaciones","Administración","Comercial","IT"]

#funciones base 
def quitar_tildes(texto):
    texto=unicodedata.normalize("NFD",texto)
    texto="".join(letra for letra in texto if unicodedata.category(letra)!="Mn")
    return texto.lower().strip()

CATEGORIAS_CORRECTAS={quitar_tildes(categoria):categoria for categoria in CATEGORIAS}
AREAS_CORRECTAS={quitar_tildes(area):area for area in AREAS}


#Funcion basica para la limpieza por datos
#Nombre
def limpiar_nombre(nombre):
    if verificar_dato_vacio(nombre):
        return None
    return CATEGORIAS_CORRECTAS.get(quitar_tildes(nombre))

#Descripcion
def limpiar_descripcion(descripcion):
    if verificar_dato_vacio(descripcion):
        return "Sin descripcion"
    return descripcion.strip()

#area_responsable (texto)
def limpiar_area(area):
    if verificar_dato_vacio(area):
        return "Sin area"
    return AREAS_CORRECTAS.get(quitar_tildes(area),"Sin area")

#Funcion que limpia toda la tabla de categorias
def limpiar_categorias(datos_sucios_df):
    datos_df=datos_sucios_df.copy()
    datos_df["nombre"]=datos_df["nombre"].map(limpiar_nombre)
    datos_df["descripcion"]=datos_df["descripcion"].map(limpiar_descripcion)
    datos_df["area_responsable"]=datos_df["area_responsable"].map(limpiar_area)
    #quitar filas repetidas por id
    datos_df=datos_df.drop_duplicates(subset="id",keep="first")
    return datos_df.reset_index(drop=True)

#Resumen de nulos por columna para revisar la calidad
def resumen_nulos(datos_df):
    return datos_df.isna().sum()