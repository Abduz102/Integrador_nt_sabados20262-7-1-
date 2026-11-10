import re
import unicodedata
import pandas as pd

#Funciones base
from notebook.limpiezas.limpiar_usuario import verificar_dato_vacio, limpiar_correo, limpiar_activos

#Definiendo los datos correctos
SECTORES=["Tecnología","Salud","Educación","Finanzas","Manufactura","Transporte","Energía","Alimentos y Bebidas","Turismo","Medios de Comunicación"]

def quitar_tildes(texto):
    texto=unicodedata.normalize("NFD",texto)
    texto="".join(letra for letra in texto if unicodedata.category(letra)!="Mn")
    return texto.lower().strip()

SECTORES_CORRECTOS={quitar_tildes(sector):sector for sector in SECTORES}

def limpiar_nombre_empresa(nombre):
    if verificar_dato_vacio(nombre):
        return None
    nombre= " ".join(nombre.split())
    if nombre.isupper():
        nombre=nombre.title()
    return nombre

#nit
def limpiar_nit_empresa(nit):
    if verificar_dato_vacio(nit):
        return None
    digitos = re.sub(r"\D","", (nit))
    if len(digitos) !=10:
        return None
    return digitos

#sector
def limpiar_sector_empresa(sector):
    if verificar_dato_vacio(sector):
        return None
    #Se compara sin tildes ni mayusculas para no perder "Alimentos y Bebidas" ni "Medios de Comunicación"
    return SECTORES_CORRECTOS.get(quitar_tildes(sector))

#contacto
def limpiar_contacto_empresa(contacto):
    if verificar_dato_vacio(contacto):
        return None
    contacto= " ".join(contacto.split())
    return contacto.title()


#telefono
def limpiar_telefono_empresa(telefono):
    if verificar_dato_vacio(telefono):
        return None
    digitos = re.sub(r"\D","", str(telefono))
    while len(digitos)>10 and digitos.startswith("57"):
        digitos=digitos[2:]
    if len(digitos)==9 and digitos.startswith("57"):
        digitos=digitos[2:]   
    if len(digitos) in (7,10) or digitos.startswith("01800"):
        return digitos
    return None

#Funcion que limpia todos los datos de la empresa
def limpiar_empresas(datos_sucios_df):
    datos_df=datos_sucios_df.copy()
    datos_df["nombre"]=datos_df["nombre"].map(limpiar_nombre_empresa)
    datos_df["nit"]=datos_df["nit"].map(limpiar_nit_empresa)
    datos_df["sector"]=datos_df["sector"].map(limpiar_sector_empresa)
    datos_df["contacto"]=datos_df["contacto"].map(limpiar_contacto_empresa)
    datos_df["correo"]=datos_df["correo"].map(limpiar_correo)
    datos_df["telefono"]=datos_df["telefono"].map(limpiar_telefono_empresa)
    #dtype object para conservar True/False/None sin convertir a texto
    datos_df["activa"]=datos_df["activa"].map(limpiar_activos).astype(object)
    #quitar filas repetidas por id
    datos_df=datos_df.drop_duplicates(subset="id",keep="first")
    #un nit no puede estar en dos empresas distintas: se conserva la primera
    nit_repetido=datos_df["nit"].duplicated(keep="first") & datos_df["nit"].notna()
    datos_df=datos_df[~nit_repetido]
    return datos_df.reset_index(drop=True)

#Resumen de nulos por columna para revisar la calidad
def resumen_nulos(datos_df):
    return datos_df.isna().sum()