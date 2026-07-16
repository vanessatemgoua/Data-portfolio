# Rossmann Store Sales - Prevision de la Demande

Application de prevision des ventes journalieres deployee sur Streamlit Cloud.

🚀 [Application live](https://rossmanndemandforecast.streamlit.app/)

---

## Contexte

Rossmann est une chaine de pharmacies allemande comptant plus de 3 000 magasins en Europe. Dans le cadre d'une competition Kaggle (2015), l'entreprise met a disposition les donnees de ventes de **1 115 magasins** sur une periode de 2,5 ans (janvier 2013 - juillet 2015), soit plus de 1 million de lignes de transactions.

**Problematique metier :** Les responsables de stores doivent anticiper la demande a 6 semaines pour optimiser les commandes de stocks, planifier les effectifs et calibrer les campagnes promotionnelles. Une mauvaise prevision entraine soit des ruptures de stock (manque a gagner), soit un surstockage (couts supplementaires).

**Objectif :** Construire un pipeline de prevision end-to-end - de l'analyse exploratoire au deploiement d'un outil interactif utilisable sans competences techniques - en comparant plusieurs approches de modelisation pour retenir la plus adaptee au contexte.

---

## Architecture

```
Donnees brutes (Kaggle CSV)
        |
        v
01_EDA.ipynb          -- Analyse exploratoire, visualisations, identification des patterns
        |
        v
02_Modeling.ipynb     -- Feature engineering + LightGBM (modele global sur tous les stores)
        |
        v
03_TimeSeries.ipynb   -- SARIMA + Prophet par store, evaluation, sauvegarde des modeles
        |
        v
models/all_prophet_models.joblib   -- Bundle : 1 115 modeles Prophet + resultats
        |
        v
app.py (Streamlit)    -- Dashboard interactif deploye sur Streamlit Cloud
```

Le pipeline suit une progression logique : comprendre les donnees (EDA), modeliser globalement (LightGBM), affiner par store (Prophet), puis exposer les resultats via une application metier.

---

## Structure du projet

```
Demand_Forecast/
|
|-- dataset/
|   |-- train.csv           # Ventes historiques (1 115 stores, jan 2013 - jul 2015)
|   |-- test.csv            # Periode de prediction Kaggle
|   |-- store.csv           # Caracteristiques des stores (type, assortiment, Promo2...)
|
|-- src/
|   |-- features.py         # Pipeline feature engineering (lags, rolling, encodage)
|   |-- evaluate.py         # Metrique RMSPE + fonctions de visualisation
|   |-- __init__.py
|
|-- models/
|   |-- all_prophet_models.joblib        # Bundle : modeles + resultats + erreurs
|   |-- all_prophet_models_summary.csv   # Recapitulatif RMSPE par store
|
|-- 01_EDA.ipynb            # Analyse exploratoire des donnees
|-- 02_Modeling.ipynb       # Modelisation LightGBM
|-- 03_TimeSeries.ipynb     # SARIMA et Prophet
|-- app.py                  # Application Streamlit
|-- requirements.txt        # Dependances Python
```

---

## Stack technique

| Categorie | Outils |
|---|---|
| Langage | Python 3.11 |
| Manipulation des donnees | Pandas, NumPy |
| Machine Learning | LightGBM, Scikit-learn |
| Series temporelles | Statsmodels (SARIMA), Prophet (Meta) |
| Visualisation | Matplotlib, Seaborn, Plotly |
| Application | Streamlit |
| Serialisation des modeles | Joblib |
| Environnement | uv (gestionnaire de paquets) |
| Versionning | Git, GitHub |

---

## Dataset

Source : [Kaggle - Rossmann Store Sales](https://www.kaggle.com/competitions/rossmann-store-sales)

| Fichier | Lignes | Description |
|---|---|---|
| train.csv | 1 017 209 | Ventes journalieres par store (Open, Sales, Customers, Promo, StateHoliday...) |
| test.csv | 41 088 | Periode de test Kaggle (aout - septembre 2015) |
| store.csv | 1 115 | Metadonnees stores (StoreType, Assortment, CompetitionDistance, Promo2...) |

**Variable cible :** `Sales` - ventes journalieres en euros (predites uniquement les jours d'ouverture)

**Metrique d'evaluation :** RMSPE (Root Mean Square Percentage Error) - metrique officielle Kaggle penalisant les erreurs relatives plutot qu'absolues.

---

## Insights cles

**Sur les donnees (EDA) :**
- Les ventes suivent une distribution log-normale avec une forte saisonnalite hebdomadaire : pic le lundi, chute le dimanche
- Les promotions augmentent les ventes de 20% en moyenne et les clients de 15%
- Les stores de type B affichent des ventes medianes plus elevees que les types A, C et D
- Les jours feries scolaires n'ont pas d'impact significatif, contrairement aux jours feries publics

**Sur les modeles :**

| Modele | RMSPE | Commentaire |
|---|---|---|
| LightGBM | 11,94% | Modele global, fort mais peu interpretable |
| SARIMA(1,1,1)(1,1,0)[52] | 7,23% | Meilleur sur un store isole, non scalable |
| Prophet | 9,38% | Retenu : scalable sur 1 115 stores, interpretable, gere les jours feries |

**Pourquoi Prophet :** malgre un RMSPE legerement superieur a SARIMA sur un store test, Prophet s'entraine automatiquement sur l'ensemble des 1 115 stores, integre nativement les jours feries allemands et la double saisonnalite (hebdomadaire + annuelle), et produit une decomposition directement lisible par des non-techniciens.

**Performance globale Prophet :**
- 1 115 modeles entraines avec succes
- RMSPE median : ~9,5% sur la periode de validation (6 dernieres semaines)
- Erreur mediane journaliere : ~6,87% par store

---

## Installation et configuration

**Pre-requis :** Python 3.11+, Git

**1. Cloner le depot**
```bash
git clone https://github.com/vanessatemgoua/Data-portfolio.git
cd Data-portfolio/Demand_Forecast
```

**2. Creer l'environnement virtuel**
```bash
# Avec uv (recommande)
pip install uv
uv venv
uv pip install -r requirements.txt

# Ou avec pip classique
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
```

**3. Telecharger le dataset Kaggle**

Creer un compte sur [kaggle.com](https://www.kaggle.com), accepter les conditions de la competition Rossmann Store Sales, puis :
```bash
pip install kaggle
kaggle competitions download -c rossmann-store-sales -p dataset/
cd dataset && unzip rossmann-store-sales.zip && cd ..
```

---

## Execution

**Notebooks (dans l'ordre)**

Ouvrir le dossier `Demand_Forecast/` dans VSCode, puis selectionner le kernel `.venv` lors de la premiere ouverture d'un notebook.

Executer dans l'ordre : `01_EDA.ipynb` → `02_Modeling.ipynb` → `03_TimeSeries.ipynb`

> Le notebook `03_TimeSeries.ipynb` entraine les 1 115 modeles Prophet et genere `models/all_prophet_models.joblib`. Cette etape peut prendre 30 a 60 minutes selon la machine.

**Application Streamlit (en local)**
```bash
streamlit run app.py
```
L'application est accessible sur `http://localhost:8501`

**Application deployee**

Directement accessible sans installation : [https://rossmanndemandforecast.streamlit.app/](https://rossmanndemandforecast.streamlit.app/)
