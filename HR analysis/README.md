# 📊 Analyse des performances des employés (HR Analytics)

## 🎯 Objectif
Ce projet vise à explorer les performances des employés afin de :
- Comprendre la répartition des scores de performance
- Identifier les outliers
- Étudier les relations entre performance et variables (heures travaillées, âge, etc.)
- Fournir des recommandations pour l’amélioration RH

## 🗂 Données
- **Source** : [HR Analytics Dataset (Kaggle)](https://www.kaggle.com/datasets/rhuebner/human-resources-data-set)
- Nombre d’observations : XXX
- Variables clés : `PerformanceScore`, `EmpSatisfaction`, `Absences`, `PayRate`, etc.

## 🔎 Méthodologie
1. Importation et nettoyage des données
2. Statistiques descriptives (moyenne, médiane, quartiles…)
3. Visualisation des distributions (histogrammes, boxplots, heatmap…)
4. Détection des outliers (règle 1.5 * IQR)
5. Recommandations RH

## 📈 Résultats principaux
- La majorité des employés ont un score de performance **"Fully Meets"**
- Des outliers identifiés chez les employés travaillant beaucoup d’heures mais avec une performance faible
- Les heures travaillées et la satisfaction semblent corrélées avec la performance

## 🛠 Outils
- Python : `pandas`, `matplotlib`, `seaborn`
- Notebook Jupyter

## 🚀 Comment exécuter
```bash
git clone https://github.com/ton-profil/Projet-HR-Analytics.git
cd Projet-HR-Analytics
jupyter notebook Projet_2_V1.ipynb
