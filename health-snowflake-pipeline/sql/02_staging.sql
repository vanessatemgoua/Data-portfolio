USE WAREHOUSE HEALTH_WH;
USE DATABASE HEALTH_DB;
USE SCHEMA STAGING;

CREATE OR REPLACE TABLE HEALTH_DB.STAGING.PATIENTS_CLEAN AS
SELECT
    ROW_NUMBER() OVER (ORDER BY AGE)        AS PATIENT_ID,
    AGE::INT                                AS AGE,

    -- Décodage du sexe
    CASE SEX
        WHEN 1 THEN 'Homme'
        ELSE 'Femme'
    END                                     AS SEXE,

    -- Décodage type douleur thoracique
    CASE CP
        WHEN 0 THEN 'Angine typique'
        WHEN 1 THEN 'Angine atypique'
        WHEN 2 THEN 'Douleur non-angineuse'
        WHEN 3 THEN 'Asymptomatique'
    END                                     AS TYPE_DOULEUR,

    TRESTBPS::FLOAT                         AS PRESSION_ARTERIELLE,
    CHOL::FLOAT                             AS CHOLESTEROL,
    THALACH::FLOAT                          AS FREQ_CARDIAQUE_MAX,

    -- Décodage résultat ECG
    CASE RESTECG
        WHEN 0 THEN 'Normal'
        WHEN 1 THEN 'Anomalie ST-T'
        WHEN 2 THEN 'Hypertrophie ventriculaire'
    END                                     AS RESULTAT_ECG,

    OLDPEAK::FLOAT                          AS DEPRESSION_ST,

    -- Statut patient
    CASE TARGET
        WHEN 1 THEN 'Malade'
        ELSE 'Sain'
    END                                     AS STATUT,

    CURRENT_TIMESTAMP()                     AS LOADED_AT

FROM HEALTH_DB.RAW.PATIENTS_RAW
WHERE AGE IS NOT NULL
  AND CHOL > 0
  AND TRESTBPS > 0
  AND THALACH > 0;

-- Vérification
SELECT COUNT(*) AS NB_LIGNES FROM HEALTH_DB.STAGING.PATIENTS_CLEAN;
SELECT * FROM HEALTH_DB.STAGING.PATIENTS_CLEAN LIMIT 10;
