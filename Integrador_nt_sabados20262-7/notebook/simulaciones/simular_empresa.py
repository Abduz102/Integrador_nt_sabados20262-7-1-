'''
Organizacion que registra o propone retos. Crea el script `src/simular_empresas.py`. Con la libreria **Faker** 
genera 300 filas falsas de la tabla `empresas`, con las MISMAS columnas que usa Backend II.
 Despues **ensucia los datos a proposito**: nulos, duplicados, espacios sobrantes, mayusculas mezcladas y formatos distintos. 
 Esos errores son los que vas a arreglar en la etapa de limpieza, asi que tienen que quedar bien puestos.

Usa `Faker("es_CO")` y fija la semilla con `Faker.seed(42)` y `random.seed(42)` para que el resultado sea SIEMPRE el mismo y
 tu compañero pueda reproducirlo.
'''

import random
import uuid
import faker
import pandas as pd
from faker import Faker

#1. sembrar semillas para los gatos a simular
random.seed(42)
Faker.seed(42)

#2. identificar los datos a simular con su tipo de datos
#id (texto (UUID)), 
#nombre (texto),
#nit (texto), 
#sector (texto) ***********, 
#contacto (texto), 
#correo (texto), 
#telefono (texto), 
#activa (booleano).


#3. establecer una constante para el numero de simulaciones
filas = 300
sectores = ["Tecnología", "Salud", "Educación", "Finanzas", "Manufactura", "Transporte", "Energía", "Alimentos y Bebidas", "Turismo", "Medios de Comunicación"]
falsito = Faker("es_CO")

#4. funcion generadora
def generar_datos(numero_filas=300):
    empresas = []
    for _ in range(numero_filas):
        empresas.append({
            "id": str(uuid.uuid4()),
            "nombre": falsito.company(),
            "nit": falsito.numerify(text="##########"),
            "sector": random.choice(sectores),
            "contacto": falsito.name(),
            "correo": falsito.email(),
            "telefono": falsito.phone_number(),
            "activa": random.choice([True, False])
        })
    return empresas
    
#5. convirtiendo los datos generados en un dataframe con PANDAS
tabla_ordenada_empresas = pd.DataFrame(generar_datos(filas))

#6. Probar la funcion generadora
print(tabla_ordenada_empresas)

#7. Preparar la simulacion para ensuciar mis daros

#7.1 Funcion para obtener una muestra de los datos
def obtener_muestra(daros,porcentaje):
    return daros.sample(frac=porcentaje,random_state=random.randint(0,9999)).index

#7.2 Funcion auxiliar para cambiar valores de un texto
def escribir_mal(texto):
    variantes = [texto.lower(), texto.title(), texto.capitalize(), f" {texto} "]
    return random.choice(variantes)

#7.3 Funcion Auxiliar para Nit
def formatear_nit(nit):
    return f"{nit[:3]}.{nit[3:6]}.{nit[6:9]}-{nit[9]}"

#7.4 Funcion auxiliar para cambiar valores de un telefono
def formatear_telefono(telefono):
    formatos = [
        telefono.replace(" ", "").replace("-", ""),  # '3001234567'
        f"{telefono[:3]} {telefono[3:6]} {telefono[6:]}",  # '300 123 4567'
        f"+57 {telefono[:3]}-{telefono[3:6]}-{telefono[6:]}"  # '+57 300-123-4567'
    ]
    return random.choice(formatos)

#7.5 FUncion auxiliar para cambiar los booleanos
def comvertir_boolano(valor):
    if valor:
        return random.choice(["SI","1" ])   
    else:
        return random.choice(["NO","0" ])

#7.6 Funcion para ensuciar los datos simulados 
def ensuciar(datos_df):
    datos_df = datos_df.copy()


    # Nombre 10% tenga espacio y el 15% este en mayuscula
    filas_elegidas = obtener_muestra(datos_df, 0.1)
    datos_df.loc[filas_elegidas, "nombre" ] = " " + datos_df.loc[filas_elegidas, "nombre" ] + " "

    filas_elegidas = obtener_muestra(datos_df, 0.15)
    datos_df.loc[filas_elegidas, "nombre" ] = datos_df.loc[filas_elegidas, "nombre" ].str.upper()
    
    # Nit: la mitad con puntos y guiones, la otra mitad sin nada
    filas_elegidas = obtener_muestra(datos_df, 0.50)
    datos_df.loc[filas_elegidas, "nit" ] = datos_df.loc[filas_elegidas, "nit" ].apply(formatear_nit)

    #Sector: Variantes del mismo sector "Logistica,logística, LOGISTICA"
    filas_elegidas = obtener_muestra(datos_df, 0.30)
    datos_df.loc[filas_elegidas, "sector" ] = datos_df.loc[filas_elegidas, "sector" ].apply(escribir_mal)

    # Contacto el 8% no debria tener ningun valor (None)
    filas_elegidas = obtener_muestra(datos_df, 0.08)
    datos_df.loc[filas_elegidas, "contacto" ] = None

    # Correo el 6% de los correos sin @
    filas_elegidas = obtener_muestra(datos_df, 0.06)
    datos_df.loc[filas_elegidas, "correo" ] = datos_df.loc[filas_elegidas, "correo" ].str.replace("@", "",)

    # Telefoneos: tres formatos distintos,'3001234567', '300 123 4567', '+57 300-123-4567'.
    datos_df["telefono"] = datos_df["telefono"].apply(formatear_telefono)

    # Activa: en ocasiones llega SI, NO, 1, 0 en lugar de True o False
    datos_df["activa"] = datos_df["activa"].astype(object)
    filas_elegidas = obtener_muestra(datos_df, 0.20)
    datos_df.loc[filas_elegidas, "activa" ] = datos_df.loc[filas_elegidas, "activa" ].map(comvertir_boolano)

    # Nit repetidos: 3% de los NIT son duplicados
    filas_elegidas = list(obtener_muestra(datos_df, 0.03))
    for i in filas_elegidas:
        donante = random.choice([x for x in datos_df.index if x != i])
        datos_df.loc[i, "nit"] = datos_df.loc[donante, "nit"]

    # Filas repetidas: 5% de las filas son duplicadas 
    duplicadas = datos_df.loc[obtener_muestra(datos_df, 0.05)]
    datos_df = pd.concat([datos_df, duplicadas], ignore_index=True)  

    return datos_df  

    # Funcion que devuelve un dataframe con los datos simulados y ensuciados
def simular_empresas(numero_filas=300):
    limpio = pd.DataFrame(generar_datos(numero_filas))
    sucio = ensuciar(limpio)

    return sucio

def generar_empresas(numero_filas=300):
    df = simular_empresas(numero_filas)
    return df

if __name__ == "__main__":
    df = generar_empresas(300)
    print(df.shape)
    print(df.head())
    print(df.isna().sum())
   
   
   
   
   
   
   
   
    # Formato de fecha
    #ISO => 2026-10-03 YYYY-MM-DD HH:MM:SS
    #LATAM => 03/10/2026 DD/MM/YYYY h:m
    #iso=datos_df["fecha_registro"].dt.strftime("%Y-%m-%d %H:%M:%S")
    #latam=datos_df["fecha_registro"].dt.strftime("%d/%m/%Y  %H:%M")
    #datos_df["fecha_registro"] = iso
    #filas_elegidas = obtener_muestra(datos_df, 0.25)
    #datos_df.loc[filas_elegidas, "fecha_registro" ] = latam[filas_elegidas]

    



