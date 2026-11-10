import os
import pandas as pd

from notebook.simulaciones.simular_usuario import generar_datos_limpios, ensuciar

from notebook.exportaciones.exportar_usuario import exportar_usuarios_crudos, exportar_usuarios_limpios

from notebook.limpiezas.limpiar_usuario import limpiar_usuarios, resumen_nulos

# ============================================================
#                      TABLA USUARIO
# ============================================================

#1. Activando la simulacion
print("************ SIMULACIONES DE USUARIO ************")
usuarios_df=pd.DataFrame(generar_datos_limpios())
usuarios_sucios_df=ensuciar(usuarios_df)

#2. Exportando los datos crudos
print("************ EXPORTACIONES DE USUARIO ************")
rutas_crudas=exportar_usuarios_crudos(usuarios_sucios_df)
for ruta in rutas_crudas:
    print("Crudo:",ruta)

#3. Limpiando los datos
print("************ LIMPIEZA DE USUARIO ************")
usuarios_limpios_df=limpiar_usuarios(usuarios_sucios_df)
print(f"Filas antes: {len(usuarios_sucios_df)} | Filas despues: {len(usuarios_limpios_df)}")
print("Nulos por columna despues de limpiar:")
print(resumen_nulos(usuarios_limpios_df))

#4. Exportando los datos limpios
print("************ EXPORTACIONES DE USUARIO LIMPIOS ************")
rutas_limpias=exportar_usuarios_limpios(usuarios_limpios_df)
for ruta in rutas_limpias:
    print("Limpio:",ruta)


# ============================================================
#                      TABLA RETOS
# ============================================================
from notebook.exportaciones.exportar_reto import exportar_retos_sucios
from notebook.limpiezas.limpiar_reto import main as limpiar_retos


print("\n************ EXPORTACIONES DE RETO (SUCIOS) ************")
exportar_retos_sucios()

print("\n************ LIMPIEZA DE RETO ************")
limpiar_retos()



# ============================================================
#                      TABLA EMPRESAS
# ============================================================
from notebook.simulaciones.simular_empresa import generar_empresas
from notebook.exportaciones.exportar_empresa import exportar_empresas_crudas, exportar_empresas_limpias
from notebook.limpiezas.limpiar_empresa import limpiar_empresas, resumen_nulos as resumen_nulos_empresas

#1. Activando la simulacion
print("\n************ SIMULACIONES DE EMPRESA ************")
empresas_sucias_df=generar_empresas(300)

#2. Exportando los datos crudos
print("************ EXPORTACIONES DE EMPRESA ************")
rutas_crudas=exportar_empresas_crudas(empresas_sucias_df)
for ruta in rutas_crudas:
    print("Crudo:",ruta)

#3. Limpiando los datos
print("************ LIMPIEZA DE EMPRESA ************")
empresas_limpias_df=limpiar_empresas(empresas_sucias_df)
print(f"Filas antes: {len(empresas_sucias_df)} | Filas despues: {len(empresas_limpias_df)}")
print("Nulos por columna despues de limpiar:")
print(resumen_nulos_empresas(empresas_limpias_df))

#4. Exportando los datos limpios
print("************ EXPORTACIONES DE EMPRESA LIMPIAS ************")
rutas_limpias=exportar_empresas_limpias(empresas_limpias_df)
for ruta in rutas_limpias:
    print("Limpio:",ruta)
#Copia que leen los reportes: data/limpio/empresas_limpio.csv
os.makedirs("data/limpio",exist_ok=True)
empresas_limpias_df.to_csv("data/limpio/empresas_limpio.csv",index=False,sep=";",encoding="utf-8-sig")


# ============================================================
#                      TABLA CATEGORIAS
# ============================================================
from notebook.simulaciones.simular_categoria import generar_categorias
from notebook.exportaciones.exportar_categoria import exportar_categorias_crudas, exportar_categorias_limpias
from notebook.limpiezas.limpiar_categoria import limpiar_categorias, resumen_nulos as resumen_nulos_categorias

#1. Activando la simulacion
print("\n************ SIMULACIONES DE CATEGORIA ************")
categorias_sucias_df=generar_categorias()

#2. Exportando los datos crudos
print("************ EXPORTACIONES DE CATEGORIA ************")
rutas_crudas=exportar_categorias_crudas(categorias_sucias_df)
for ruta in rutas_crudas:
    print("Crudo:",ruta)

#3. Limpiando los datos
print("************ LIMPIEZA DE CATEGORIA ************")
categorias_limpias_df=limpiar_categorias(categorias_sucias_df)
print(f"Filas antes: {len(categorias_sucias_df)} | Filas despues: {len(categorias_limpias_df)}")
print("Nulos por columna despues de limpiar:")
print(resumen_nulos_categorias(categorias_limpias_df))

#4. Exportando los datos limpios
print("************ EXPORTACIONES DE CATEGORIA LIMPIAS ************")
rutas_limpias=exportar_categorias_limpias(categorias_limpias_df)
for ruta in rutas_limpias:
    print("Limpio:",ruta)


# ==================================================================================
#                      CONSULTAS ( RETOS, USUARIO, EMPRESA, CATEGORIA)
# ==================================================================================
from notebook.consultas.consultas_reto import main as consultas_retos
from notebook.consultas.consultas_usuario import main as consultas_usuario
from notebook.consultas.consultas_empresa import main as consultas_empresa
from notebook.consultas.consultas_categoria import main as consultas_categoria


print("\n************ CONSULTAS DE RETO ************")
consultas_retos()

print("\n************ CONSULTAS DE USUARIO ************")
consultas_usuario()

print("\n************ CONSULTAS DE EMPRESA ************")
consultas_empresa()

print("\n************ CONSULTAS DE CATEGORIA ************")
consultas_categoria()
#Copia que leen los reportes: data/limpio/categorias_limpio.csv
os.makedirs("data/limpio",exist_ok=True)
categorias_limpias_df.to_csv("data/limpio/categorias_limpio.csv",index=False,sep=";",encoding="utf-8-sig")


# ==================================================================================
#                      REPORTES (GRAFICAS Y CONCLUSIONES)
# ==================================================================================
from src.reporte_categorias import main as reporte_categorias
from src.reporte_empresas import main as reporte_empresas
from src.reporte_retos import main as reporte_retos

print("\n************ REPORTE DE CATEGORIAS ************")
reporte_categorias()

print("\n************ REPORTE DE EMPRESAS ************")
reporte_empresas()

print("\n************ REPORTE DE RETOS ************")
reporte_retos()
