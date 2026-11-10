import random
import uuid
from datetime import timedelta
import pandas as pd
from faker import Faker

#1. Constantes (listas fijas para que varios retos compartan empresa, categoria y prioridad)
ESTADOS = ["Abierto", "En curso", "Cerrado"]

#Variantes con las que se ensucia el estado
ESTADOS_SUCIOS = ["en_curso", "EN CURSO", " Cerrado "]

IDS_EMPRESA = [
    "e1000000-0000-0000-0000-000000000001",
    "e1000000-0000-0000-0000-000000000002",
    "e1000000-0000-0000-0000-000000000003",
]

IDS_CATEGORIA = [
    "c2000000-0000-0000-0000-000000000001",
    "c2000000-0000-0000-0000-000000000002",
    "c2000000-0000-0000-0000-000000000003",
]

#OJO: antes empezaban por "p", que no es hexadecimal y no es un UUID valido
IDS_PRIORIDAD = [
    "a3000000-0000-0000-0000-000000000001",
    "a3000000-0000-0000-0000-000000000002",
]


#2. Escoge, sin repetir, un porcentaje exacto de filas (para que el ensuciado sea predecible)
def elegir_filas(total, porcentaje, excluir=()):
    candidatas = [i for i in range(total) if i not in excluir]
    return random.sample(candidatas, round(total * porcentaje))


#3. Genera los N retos: 95% unicos + 5% duplicados exactos = N filas en total
def generar_retos(n=500):
    Faker.seed(42)
    random.seed(42)

    #es_ES y no es_CO: es_CO no tiene texto propio y Faker usa el lorem ipsum en latin
    fake = Faker("es_ES")
    num_duplicados = int(n * 0.05)
    base = n - num_duplicados
    filas = []

    for _ in range(base):
        fecha_inicio = fake.date_between(start_date="-1y", end_date="+3m")
        fecha_fin = fecha_inicio + timedelta(days=random.randint(15, 180))
        filas.append(
            {
                "id": str(uuid.uuid4()),
                "nombre": fake.sentence(nb_words=6).rstrip("."),
                "descripcion": fake.sentence(nb_words=12),
                "fecha_inicio": fecha_inicio,
                "fecha_fin": fecha_fin,
                "estado": random.choice(ESTADOS),
                "id_empresa": random.choice(IDS_EMPRESA),
                "id_categoria": random.choice(IDS_CATEGORIA),
                "id_prioridad": random.choice(IDS_PRIORIDAD),
            }
        )

    df = pd.DataFrame(filas)

    #4. Ensuciar los datos
    #nombre: 10% con espacios sobrantes
    for i in elegir_filas(base, 0.10):
        df.loc[i, "nombre"] = f"  {df.loc[i, 'nombre']}   "

    #descripcion: 12% en None
    for i in elegir_filas(base, 0.12):
        df.loc[i, "descripcion"] = None

    #fecha_inicio: dos formatos mezclados (2026-03-02 y 02/03/2026)
    formato_latino = set(elegir_filas(base, 0.50))
    inicio_str = []
    for i in range(base):
        formato = "%d/%m/%Y" if i in formato_latino else "%Y-%m-%d"
        inicio_str.append(df.loc[i, "fecha_inicio"].strftime(formato))

    #fecha_fin: 8% en None y 5% ANTERIOR a fecha_inicio (error logico)
    filas_none = elegir_filas(base, 0.08)
    filas_error = elegir_filas(base, 0.05, excluir=set(filas_none))
    fin_str = []
    for i in range(base):
        if i in filas_none:
            fin_str.append(None)
        elif i in filas_error:
            anterior = df.loc[i, "fecha_inicio"] - timedelta(days=random.randint(1, 30))
            fin_str.append(anterior.strftime("%Y-%m-%d"))
        else:
            fin_str.append(df.loc[i, "fecha_fin"].strftime("%Y-%m-%d"))

    df["fecha_inicio"] = inicio_str
    df["fecha_fin"] = fin_str

    #estado: 20% con variantes ('en_curso', 'EN CURSO', ' Cerrado ')
    for i in elegir_filas(base, 0.20):
        df.loc[i, "estado"] = random.choice(ESTADOS_SUCIOS)

    #5. 5% de filas repetidas tal cual (duplicados exactos)
    if num_duplicados > 0:
        duplicados = df.sample(n=num_duplicados, random_state=42)
        df = pd.concat([df, duplicados], ignore_index=True)

    return df


if __name__ == "__main__":
    df = generar_retos(500)
    print("--- SHAPE ---")
    print(df.shape)
    print("\n--- HEAD ---")
    print(df.head())
    print("\n--- NULOS POR COLUMNA ---")
    print(df.isna().sum())