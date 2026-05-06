import pandas as pd
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import SNOWFLAKE_CONFIG

# ── 1. Charger le CSV ──────────────────────────
df = pd.read_csv("../data/heart.csv")
df.columns = [col.upper() for col in df.columns]

print(f"--> Dataset chargé : {df.shape[0]} lignes, {df.shape[1]} colonnes")
print(df.head(3))

# ── 2. Connexion Snowflake ─────────────────────
print("\n --> Connexion à Snowflake...")
conn = snowflake.connector.connect(
    user=SNOWFLAKE_CONFIG["user"],
    password=SNOWFLAKE_CONFIG["password"],
    account=SNOWFLAKE_CONFIG["account"],
    warehouse=SNOWFLAKE_CONFIG["warehouse"],
    database=SNOWFLAKE_CONFIG["database"],
    schema=SNOWFLAKE_CONFIG["schema"]
)
print("\n--> Connecté à Snowflake !")

# ── 3. Créer la table RAW ──────────────────────
cursor = conn.cursor()
cursor.execute("""
    CREATE OR REPLACE TABLE HEALTH_DB.RAW.PATIENTS_RAW (
        AGE       NUMBER,
        SEX       NUMBER,
        CP        NUMBER,
        TRESTBPS  NUMBER,
        CHOL      NUMBER,
        FBS       NUMBER,
        RESTECG   NUMBER,
        THALACH   NUMBER,
        EXANG     NUMBER,
        OLDPEAK   FLOAT,
        SLOPE     NUMBER,
        CA        NUMBER,
        THAL      NUMBER,
        TARGET    NUMBER
    )
""")
print("\n --> Table RAW créée")

# ── 4. Charger les données ─────────────────────
success, nchunks, nrows, _ = write_pandas(conn, df, "PATIENTS_RAW")
print(f"--> {nrows} lignes chargées dans HEALTH_DB.RAW.PATIENTS_RAW")

cursor.close()
conn.close()
print("\n --> Chargement terminé !")