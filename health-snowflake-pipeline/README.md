#  Health Data Pipeline — Snowflake + Power BI

## Contexte & Problématique

Dans un contexte de santé publique, l'analyse des données cardiaques permet d'identifier les profils à risque et d'orienter les décisions médicales. Ce projet simule une chaîne de traitement data complète : de l'ingestion des données brutes jusqu'à la restitution via un dashboard décisionnel interactif.

**Question métier :** Quels sont les profils de patients les plus à risque de maladie cardiaque ?

---

##  Architecture du pipeline

```
CSV (Kaggle)
     ↓
Python (Pandas + snowflake-connector)
     ↓
Snowflake — couche RAW
     ↓ (SQL)
Snowflake — couche STAGING (nettoyage + décodage)
     ↓ (SQL)
Snowflake — couche GOLD (KPIs + agrégations)
     ↓
Power BI (dashboard 3 pages)
```

---

## 🗂️ Structure du projet

```
health-snowflake-pipeline/
├── data/
│   └── heart.csv                  # Dataset Kaggle
├── python/
│   ├── config.py                  # Credentials Snowflake (non versionné)
│   └── load_to_snowflake.py       # Chargement RAW
├── sql/
│   ├── 01_setup.sql               # Création DB, schemas, warehouse
│   ├── 02_staging.sql             # Transformation & nettoyage
│   └── 03_gold.sql                # KPIs & agrégations
├── dashboard/
│   └── health_dashboard.pbix      # Fichier Power BI
├── screenshots/
│   ├── page1_vue_globale.png
│   ├── page2_risque_age.png
│   └── page3_cholesterol.png
├── .gitignore
└── README.md
```

---

##  Stack technique

| Outil | Usage |
|---|---|
| **Python** | Ingestion des données, connexion Snowflake |
| **Pandas** | Nettoyage et préparation du dataset |
| **Snowflake** | Data Warehouse 3 couches (RAW / STAGING / GOLD) |
| **SQL** | Transformation, décodage, agrégations, KPIs |
| **Power BI** | Dashboard décisionnel interactif 3 pages |
| **DAX** | Mesures calculées (taux, scores, moyennes) |

---

##  Dataset

- **Source** : [Heart Disease Dataset — Kaggle](https://www.kaggle.com/datasets/johnsmith88/heart-disease-dataset)
- **Volume** : 1 025 patients, 14 variables
- **Variables clés** : âge, sexe, type de douleur thoracique, cholestérol, pression artérielle, fréquence cardiaque, statut (malade/sain)

---

## ❄️ Modélisation Snowflake

### Couche RAW
Données brutes ingérées telles quelles depuis le CSV.

### Couche STAGING
Données nettoyées et décodées :
- `SEX` → Homme / Femme
- `CP` → Type de douleur (Angine typique, Asymptomatique...)
- `TARGET` → Malade / Sain
- Filtrage des valeurs nulles et aberrantes

### Couche GOLD (6 tables KPIs)

| Table | Description |
|---|---|
| `KPI_STATUT_SEXE` | Répartition par sexe et statut |
| `KPI_RISQUE_AGE` | Taux de risque par tranche d'âge |
| `KPI_CHOLESTEROL` | Impact du cholestérol sur le statut |
| `KPI_DOULEUR` | Risque par type de douleur thoracique |
| `KPI_FREQ_CARDIAQUE` | Fréquence cardiaque et risque |
| `KPI_SCORE_RISQUE` | Score de risque calculé par patient |

---

## Dashboard Power BI

### Page 1 — Vue globale
- 5 KPI Cards : Total patients, Malades, Taux malades %, Age moyen, Score risque moyen
- Répartition par sexe & statut
- Distribution Homme / Femme
- Distribution des niveaux de risque
- Slicer : Sexe

### Page 2 — Analyse du risque par âge
- Taux de risque par tranche d'âge
- Malades vs Sains par tranche d'âge
- Taux de risque par type de douleur
- Table détaillée avec mise en forme conditionnelle
- Slicers : Sexe | Type de douleur

### Page 3 — Analyse Cholestérol
- Patients par niveau de cholestérol & statut
- Répartition des niveaux de cholestérol
- Âge moyen par niveau de cholestérol
- Table détaillée
- Slicers : Niveau cholestérol | Statut

---

##  Insights clés

- **51%** des patients sont malades
- **70%** des cas concernent des hommes
- La tranche **40-54 ans** présente le taux de risque le plus élevé (65,9%)
- Les patients **asymptomatiques** ont paradoxalement le taux de risque le plus élevé
- **50%** des patients ont un cholestérol élevé (240+ mg/dL)
- Un cholestérol élevé est davantage présent chez les patients sains que malades dans ce dataset

---

## Lancer le projet

### Prérequis
- Python 3.8+
- Compte Snowflake (essai gratuit 30 jours)
- Power BI Desktop

### Installation

```bash
git clone https://github.com/ton_username/health-snowflake-pipeline.git
cd health-snowflake-pipeline
pip install pandas snowflake-connector-python "snowflake-connector-python[pandas]"
```

### Configuration

Crée le fichier `python/config.py` :

```python
SNOWFLAKE_CONFIG = {
    "user":      "ton_username",
    "password":  "ton_password",
    "account":   "ton_account_identifier",
    "warehouse": "HEALTH_WH",
    "database":  "HEALTH_DB",
    "schema":    "RAW"
}
```

### Exécution

```bash
# 1. Configurer Snowflake
# Exécuter sql/01_setup.sql dans Snowflake Worksheets

# 2. Charger les données RAW
cd python
python load_to_snowflake.py

# 3. Transformer les données
# Exécuter sql/02_staging.sql dans Snowflake Worksheets
# Exécuter sql/03_gold.sql dans Snowflake Worksheets

# 4. Ouvrir le dashboard
# Ouvrir dashboard/health_dashboard.pbix dans Power BI Desktop
```

