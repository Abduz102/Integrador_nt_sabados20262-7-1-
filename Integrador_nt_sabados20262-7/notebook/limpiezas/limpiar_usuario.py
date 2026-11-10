#Alistamiento para ejecutar rutina de limpieza
import pandas as pd 
from datetime import datetime
from notebook.exportaciones.exportar_usuario import CARPETA_CRUDOS, NOMBRE_ENTIDAD

#Definiendo los datos correctos
ROLES=["ADMIN","EMPRESA","PARTICIPANTE"]


#Definiendo funciones base
def verificar_dato_vacio(dato):
    if pd.isna(dato):
        return True
    return isinstance(dato,str) and dato.strip()==""

#Funciones basicas de limpeiza por dato
 
#nombre (texto)
def limpiar_nombre(nombre):
    if verificar_dato_vacio(nombre):
        return None
    nombre=nombre.strip()
    return nombre.title()

#correo (texto)
def limpiar_correo(correo):
    if verificar_dato_vacio(correo):
        return None
    correo=correo.strip().lower()
    #un correo sin arroba no es valido
    if "@" not in correo:
        return None
    return correo

#contrasena_hash (texto)
def limpiar_contrasena(contrasena):
    if verificar_dato_vacio(contrasena):
        return None
    contrasena = contrasena.strip()
    return contrasena  # <--- Devuélvela sin alterar sus mayúsculas/minúsculas

#rol (texto)
def limpiar_rol(rol):
    if verificar_dato_vacio(rol):
        return None 
    rol=rol.strip().upper()
    if rol not in ROLES:
        return None
    return rol


#activo (booleano)
def limpiar_activos(activo):
    if verificar_dato_vacio(activo):
        return None 
    if isinstance(activo,bool):
        return activo
    activo=str(activo).strip()
    if activo in ["Si","SI","sí","si","1","True","TRUE","true"]:
        return True
    if activo in ["No","NO","no","0","False","FALSE","false"]:
        return False
    return None
#fecha_registro (fecha y hora)
#Formatos de fecha que llegan mezclados desde la simulacion
FORMATOS_FECHA=["%Y-%m-%d %H:%M:%S","%d/%m/%Y %H:%M"]

def limpiar_fecha(fecha):
    if verificar_dato_vacio(fecha):
        return None
    fecha=str(fecha).strip()
    for formato in FORMATOS_FECHA:
        try:
            return datetime.strptime(fecha,formato)
        except ValueError:
            continue
    return None

#Funcion que limpia toda la tabla de usuarios
def limpiar_usuarios(datos_sucios_df):
    datos_df=datos_sucios_df.copy()
    datos_df["nombre"]=datos_df["nombre"].map(limpiar_nombre)
    datos_df["correo"]=datos_df["correo"].map(limpiar_correo)
    datos_df["contrasena_hash"]=datos_df["contrasena_hash"].map(limpiar_contrasena)
    datos_df["rol"]=datos_df["rol"].map(limpiar_rol)
    #dtype object para conservar True/False/None sin convertir a texto
    datos_df["activo"]=datos_df["activo"].map(limpiar_activos).astype(object)
    datos_df["fecha_registro"]=datos_df["fecha_registro"].map(limpiar_fecha)
    #quitar filas repetidas por id
    datos_df=datos_df.drop_duplicates(subset="id",keep="first")
    return datos_df.reset_index(drop=True)

#Resumen de nulos por columna para revisar la calidad
def resumen_nulos(datos_df):
    return datos_df.isna().sum()