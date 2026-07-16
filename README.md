# Portfolio - Vanessa Kenfack

Consultante Data, je conçois des solutions de reporting décisionnel, des pipelines de données et des dashboards qui aident les équipes métiers à prendre de meilleures décisions.

📧 vanessa.kenfack@outlook.fr | 🔗 [LinkedIn](https://www.linkedin.com/in/vanessa-kenfack-temgoua-028937248)

---

## 🗂️ Projets

### 1. Analyse du Taux de Désabonnement Client (Churn Rate Analysis)
**Power BI | DAX | Power Query**

Projet mené pour une entreprise de télécommunications (Databel) visant à réduire le taux de désabonnement en identifiant les facteurs de risque clés.

**Réalisations :**
- Nettoyage et transformation des données via Power Query (M Language)
- Calcul du Churn Rate global et par segment avec des mesures DAX avancées
- Identification des facteurs clés : démographie, type de contrat, usage des services
- Conception d'un dashboard interactif Power BI orienté décision marketing

📁 [Voir le projet](./Analyse%20du%20taux%20de%20d%C3%A9sabonnement%20des%20clients)

---

### 2. Atlas Labs - HR Analytics Dashboard
**Power BI | DAX | Power Query**

Tableau de bord RH interactif conçu pour suivre et analyser les effectifs et l'attrition d'une entreprise.

**Réalisations :**
- Suivi des effectifs globaux : 1 470 employés dont 1 233 actifs et 237 inactifs
- Calcul et visualisation du taux d'attrition (16,1%) par département et poste
- Analyse des tendances de recrutement entre 2012 et 2022 avec segmentation attrition/rétention
- Répartition des employés actifs par département (Technology, Sales, Human Resources) et par rôle métier
- Navigation multi-pages : Overview, Démographie, Suivi des performances, Attrition
- Exploration des données RH pour comprendre les facteurs qui influencent les performances des employés.

📁 [Voir le projet](./HR_Analytics_Dashboard)

---

### 3. Analyse Financière Apple (AAPL) et Machine Learning
**Python | Pandas | Plotly | Scikit-learn | XGBoost**

Exploitation des données financières d'Apple pour générer des insights stratégiques et des modèles prédictifs.

**Réalisations :**
- Extraction des données via `yfinance` et analyse exploratoire complète
- Feature engineering : indicateurs techniques (SMA, EMA, RSI, MACD, OBV)
- Backtesting d'une stratégie de trading algorithmique
- Comparaison de modèles prédictifs (Random Forest, XGBoost) sur le prix de clôture
- Dashboard interactif Plotly avec métriques de performance (RMSE, MAE, R²)

📁 [Voir le projet](./Financial%20Analysis)

---

### 4. HR Analytics - Analyse des Performances Employés
**Python | Pandas | NumPy | Matplotlib**

Exploration des données RH pour comprendre les facteurs qui influencent les performances des employés.

**Réalisations :**
- Analyse de la distribution des scores de performance
- Détection d'outliers et étude des corrélations (heures travaillées, âge, etc.)
- Recommandations concrètes pour l'amélioration des pratiques RH

📁 [Voir le projet](./HR%20analysis)

---

### 5. Analyse des Ventes sous Excel
**Excel | Power Query | Tableaux croisés dynamiques**

Suivi des performances commerciales par région et catégorie pour identifier les zones à améliorer.

**Réalisations :**
- Analyse de la répartition des performances régionales
- Identification des catégories à fort impact
- Recommandations actionnables pour l'optimisation des ventes

📁 [Voir le projet](./Sales%20analysis)

---
### 6. Global Superstore | Sales Performance Dashboard
**Power BI | DAX | Power Query**

Tableau de bord commercial interactif pour piloter les performances de ventes 
d'une entreprise internationale de distribution en temps réel.

**Réalisations :**
- Conception de 3 pages interactives : Vue d'ensemble, Analyse Produit, Analyse Géographique
- Calcul de KPIs avancés en DAX : CA N/N-1, taux de marge, variation directionnelle avec flèches
- Détection des produits déficitaires via scatter plot Remise vs Profit
- Analyse géographique mondiale avec carte à bulles et Top 10 pays par CA et Profit
- Modélisation en schéma en étoile avec table Calendrier et mesures DAX optimisées

📁 [Voir le projet](./Sales%20Performance%20Analysis%20with%20Power%20BI)

---
 
### 7. Health Data Pipeline - Snowflake + Power BI
**Python | SQL | Snowflake | Power BI | DAX**
 
Pipeline de données end-to-end sur des données cardiaques hospitalières, de l'ingestion brute jusqu'au dashboard décisionnel interactif.
 
**Réalisations :**
- Ingestion de 1 025 patients via Python (Pandas + snowflake-connector) dans la couche RAW Snowflake
- Transformation et décodage des données en SQL (couche STAGING) : sexe, type de douleur, statut
- Conception de 6 tables KPIs en couche GOLD : taux de risque, score patient, cholestérol, fréquence cardiaque
- Calcul d'un score de risque personnalisé par patient (Risque Faible / Modéré / Élevé)
- Dashboard Power BI 3 pages : Vue globale, Analyse du risque par âge, Analyse cholestérol
**Insights clés :**
- 51% des patients sont malades | 70% des cas concernent des hommes
- La tranche 40-54 ans présente le taux de risque le plus élevé (65,9%)
- 50% des patients ont un cholestérol élevé (240+ mg/dL)
  
📁 [Voir le projet](./health-snowflake-pipeline)
 
---

### 8. Rossmann Store Sales - Prévision de la Demande
**Python | LightGBM | SARIMA | Prophet | Streamlit | Plotly**

Projet end-to-end de prévision des ventes journalières pour la chaîne de pharmacies allemande Rossmann (dataset Kaggle - compétition 2015), couvrant **1 115 magasins** sur 2,5 ans de données historiques. L'objectif métier : fournir aux responsables de stores une prévision fiable à horizon 6 semaines pour anticiper les stocks, les effectifs et les campagnes promotionnelles.

**Problématique :** Comment anticiper la demande de chaque magasin en tenant compte des promotions, des jours fériés, de la saisonnalité hebdomadaire et annuelle, tout en déployant une solution scalable sur 1 115 stores aux profils très différents ?

**Comparaison des modèles testés**

| Modèle | RMSPE | Avantages | Limites |
|---|---|---|---|
| LightGBM | 11,94% | Très performant globalement, gère les interactions complexes entre features | Nécessite un feature engineering intensif (lags, rolling), peu interprétable pour les décideurs |
| SARIMA(1,1,1)(1,1,0)[52] | 7,23% | Meilleure performance sur le store test, modèle statistique rigoureux | Non scalable : un modèle par store, paramétrage manuel, trop lent sur 1 115 stores |
| **Prophet** | **9,38%** | **Scalable, interprétable, gère nativement les jours fériés et la saisonnalité multiple** | Légèrement moins précis que SARIMA sur un store isolé |

**Pourquoi Prophet a été retenu :**
Malgré un RMSPE légèrement supérieur à SARIMA sur un store test, Prophet a été choisi pour son **déploiement à l'échelle** : il s'entraîne automatiquement sur les 1 115 stores sans paramétrage manuel, intègre nativement les jours fériés allemands et la double saisonnalité (hebdomadaire + annuelle), et produit une décomposition lisible (tendance, saisonnalité, effet promo) directement exploitable par des non-techniciens. LightGBM, bien qu'efficace, ne fournit pas de lecture temporelle claire et ne se prête pas à une analyse store par store dans un outil décisionnel.

**Application décisionnelle - comment elle est utilisée**

Le dashboard Streamlit déployé est conçu pour être utilisé par des **responsables de magasin et des équipes commerciales** sans compétences techniques :

- **Sélection du store et de l'horizon** - Le responsable choisit son magasin et la durée de prévision (1 à 12 semaines), avec ou sans promotion activée
- **Lecture de la prévision** - Un graphique interactif affiche les ventes attendues jour par jour avec l'intervalle de confiance à 95%, permettant d'évaluer le meilleur et le pire scénario
- **Suivi de la performance** - La section *Réel vs Prédit* compare les prévisions passées aux ventes réelles observées, avec des indicateurs d'écart pour évaluer la fiabilité du modèle sur ce store
- **Compréhension des patterns** - La décomposition Prophet révèle la tendance long terme, l'effet jour de la semaine et la saisonnalité annuelle, utile pour planifier les pics d'activité
- **Benchmarking** - La vue globale permet de situer un store parmi les 1 115 en termes de précision de prévision (distribution RMSPE + top 20 meilleurs stores)

📁 [Voir le projet](./Demand_Forecast) | 🚀 [Application live](https://rossmanndemandforecast.streamlit.app/)

---

## 🛠️ Stack technique

| Catégorie | Outils |
|---|---|
| SQL & Bases de données | SQL, NoSQL, PostgreSQL, Snowflake, MongoDB |
| BI & Reporting | Power BI, DAX, Power Query, Tableau, Excel Avancé|
| Python | Pandas, NumPy, Scikit-learn, Plotly, Matplotlib, LightGBM, Prophet, Streamlit |
| Data Engineering | BigQuery, GCP |
| Versionning | Git, GitHub |

---

##  À propos

Je suis data analyst passionnée par la transformation de données brutes en informations décisionnelles concrètes. Rigoureuse et autonome, j'interviens sur l'ensemble de la chaîne data : de l'extraction SQL à la visualisation Power BI, en passant par la conception d'architectures data et la fiabilisation des données.

📧 [vanessa.kenfack@outlook.fr](mailto:vanessa.kenfack@outlook.fr) | 🔗 [LinkedIn](https://www.linkedin.com/in/vanessa-kenfack-temgoua-028937248)
