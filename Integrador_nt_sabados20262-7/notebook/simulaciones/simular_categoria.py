import random
import uuid
import pandas as pd
from faker import Faker

# La semilla esta fija: Faker.seed(42) y random.seed(42), para que el archivo sea reproducible.
#1. sembrar semillas para los datos a simular
random.seed(42)
Faker.seed(42)

# Se generan 250 filas con estas columnas: id (texto (UUID)), nombre (texto), descripcion (texto), area_responsable (texto).
# OJO: area_responsable NO esta en el modelo de Backend II: es una columna EXTRA solo para este ejercicio de analisis, para poder agrupar.
#2. identificar los datos a simular con su tipo de datos
#id (texto (UUID))
#nombre (texto)
#descripcion (texto)
#area_responsable (texto) - EXTRA COLUMNA EJERCICIO

# Al inicio se declaran las constantes: CATEGORIAS, AREAS.
# Solo hay 10 categorias reales, pero se generan 250 filas: la gracia es que el catalogo llega REPETIDO y con variantes de escritura.
#3. establecer una constante para el numero de simulaciones
filas = 250
CATEGORIAS = ["Logística", "Ventas", "Marketing", "Recursos Humanos", "Finanzas", "Tecnología", "Atención al Cliente", "Producción", "Compras", "Calidad"]
AREAS = ["Operaciones", "Administración", "Comercial", "IT"]
falsito = Faker("es_CO")

#7. Preparar la simulacion para ensuciar mis datos

#7.1 Funcion para obtener una muestra de los datos
def obtener_muestra(datos, porcentaje):
    # Nota: se usa 'frac' en lugar de 'fraccion' porque es el argumento nativo de Pandas
    return datos.sample(frac=porcentaje, random_state=random.randint(0,9999)).index

# Se ensucia nombre: variantes del mismo nombre: 'Logistica', 'LOGISTICA', ' logistica ', 'logística'.
#7.2 Funcion auxiliar para cambiar valores de un texto
def escribir_mal(texto):
    variantes = [
        texto.lower(), 
        texto.title(), 
        texto.upper(), 
        f" {texto} ", 
        texto.replace('í', 'i').replace('ó', 'o').replace('á', 'a').replace('é', 'e').replace('ú', 'u')
    ]
    return random.choice(variantes)

#7.4 Funcion para ensuciar los datos simulados
def ensuciar(datos_df):
    datos_df = datos_df.copy()
    
    # Nombre: aplicar variantes
    datos_df["nombre"] = datos_df["nombre"].apply(escribir_mal)

    # Se ensucia descripcion: 15% en None (nulos).
    filas_elegidas = obtener_muestra(datos_df, 0.15)
    datos_df.loc[filas_elegidas, "descripcion"] = None
    
    # Se ensucia area_responsable: 10% en None.
    filas_elegidas = obtener_muestra(datos_df, 0.10)
    datos_df.loc[filas_elegidas, "area_responsable"] = None

    # 8% de las filas repetidas tal cual (duplicados exactos).
    filas_elegidas = obtener_muestra(datos_df, 0.08)
    datos_duplicados = datos_df.loc[filas_elegidas].copy()
    
    # Reemplazamos otras filas para mantener exactamente el mismo numero de registros (250)
    indices_restantes = datos_df.index[~datos_df.index.isin(filas_elegidas)]
    serie_restantes = pd.Series(indices_restantes)
    filas_a_sobrescribir = serie_restantes.sample(n=len(filas_elegidas), random_state=random.randint(0,9999)).values
    
    datos_df.loc[filas_a_sobrescribir] = datos_duplicados.values

    return datos_df

# Todo se arma en una funcion generar_categorias(n=250) que devuelve el DataFrame (return df), para poder importarla desde el script de exportacion.
#4. funcion generadora
def generar_categorias(n=250):
    categorias = []
    for _ in range(n):
        categorias.append({
            # id se genera con str(uuid.uuid4()).
            "id": str(uuid.uuid4()),
            # nombre se genera con random.choice(CATEGORIAS).
            "nombre": random.choice(CATEGORIAS),
            # descripcion se genera con fake.sentence(nb_words=8).
            "descripcion": falsito.sentence(nb_words=8),
            # area_responsable se genera con random.choice(AREAS).
            "area_responsable": random.choice(AREAS)
        })
        
    #5. convirtiendo los datos generados en un dataframe con PANDAS
    tabla_ordenada_categorias = pd.DataFrame(categorias)
    
    # Retornamos los datos ya ensuciados
    return ensuciar(tabla_ordenada_categorias)

# El bloque if __name__ == "__main__": solo imprime df.shape, df.head() y df.isna().sum() para revisar que los datos quedaron sucios.
#6. Probar la funcion generadora
if __name__ == "__main__":
    df = generar_categorias()
    print("Forma del DataFrame:", df.shape)
    print("\nPrimeros registros:")
    print(df.head())
    print("\nValores nulos por columna:")
    print(df.isna().sum())