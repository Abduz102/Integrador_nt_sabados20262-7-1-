#Rutina para exportar la tabla de empresas a CSV, JSON y Excel

from notebook.exportaciones.exportar_usuario import CARPETA_CRUDOS, CARPETA_LIMPIOS, exportar_csv, exportar_json, exportar_excel

#1. Configuracion (cambiar segun su tabla)
NOMBRE_ENTIDAD="empresa"

#2. Genero los archivos en mi proyecto
def exportar_empresas_crudas(datos_sucios_df):
    return [
        exportar_csv(datos_sucios_df,CARPETA_CRUDOS,f"{NOMBRE_ENTIDAD}_crudo"),

        exportar_json(datos_sucios_df,CARPETA_CRUDOS,f"{NOMBRE_ENTIDAD}_crudo"),

        exportar_excel(datos_sucios_df,CARPETA_CRUDOS,f"{NOMBRE_ENTIDAD}_crudo")
    ]

def exportar_empresas_limpias(datos_limpios_df):
    return [
        exportar_csv(datos_limpios_df,CARPETA_LIMPIOS,f"{NOMBRE_ENTIDAD}_limpio"),

        exportar_json(datos_limpios_df,CARPETA_LIMPIOS,f"{NOMBRE_ENTIDAD}_limpio"),

        exportar_excel(datos_limpios_df,CARPETA_LIMPIOS,f"{NOMBRE_ENTIDAD}_limpio")
    ]
