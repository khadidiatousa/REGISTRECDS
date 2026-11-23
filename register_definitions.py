# Formulaires distincts issus des registres PDF sénégalais version 2018.
REGISTERS = {
  "consultation_generale": {
    "label": "Registre de consultation générale",
    "fields": [
      {
        "label": "N° d’ordre",
        "key": "numero_ordre",
        "type": "number"
      },
      {
        "label": "Date de consultation",
        "key": "date_consultation",
        "type": "date"
      },
      {
        "label": "Prénom(s) et nom du malade",
        "key": "nom",
        "type": "text"
      },
      {
        "label": "Âge (années, >15 ans)",
        "key": "age",
        "type": "number"
      },
      {
        "label": "Sexe",
        "key": "sexe",
        "type": "select",
        "options": [
          "M",
          "F"
        ]
      },
      {
        "label": "Femme enceinte",
        "key": "femme_enceinte",
        "type": "select",
        "options": [
          "Oui",
          "Non",
          "Non renseigné"
        ]
      },
      {
        "label": "Adresse exacte",
        "key": "adresse",
        "type": "textarea"
      },
      {
        "label": "Plaintes et symptômes",
        "key": "plaintes_symptomes",
        "type": "textarea"
      },
      {
        "label": "TDR paludisme",
        "key": "tdr",
        "type": "select",
        "options": [
          "Positif (+)",
          "Négatif (-)",
          "Non fait (NF)"
        ]
      },
      {
        "label": "Autres examens paracliniques",
        "key": "autres_examens",
        "type": "textarea"
      },
      {
        "label": "Diagnostic confirmé",
        "key": "diagnostic",
        "type": "textarea"
      },
      {
        "label": "Orientation",
        "key": "orientation",
        "type": "checkbox"
      },
      {
        "label": "Référence",
        "key": "reference",
        "type": "checkbox"
      },
      {
        "label": "Contre-référence",
        "key": "contre_reference",
        "type": "checkbox"
      },
      {
        "label": "Traitement prescrit et quantités",
        "key": "traitement",
        "type": "textarea"
      },
      {
        "label": "Recherche besoins PF",
        "key": "recherche_pf",
        "type": "checkbox"
      },
      {
        "label": "Mode de prise en charge PF",
        "key": "prise_en_charge_pf",
        "type": "select",
        "options": [
          "Offre",
          "Rendez-vous",
          "Référence",
          "Non applicable"
        ]
      },
      {
        "label": "Observations (traumatismes, circonstances, etc.)",
        "key": "observations",
        "type": "textarea"
      }
    ]
  },
  "cpn": {
    "label": "Registre de consultation prénatale",
    "fields": [
      {
        "label": "N° d’ordre annuel",
        "key": "numero_ordre",
        "type": "number"
      },
      {
        "label": "Date de consultation",
        "key": "date",
        "type": "date"
      },
      {
        "label": "Prénom(s) et nom de la femme",
        "key": "nom",
        "type": "text"
      },
      {
        "label": "Âge (années)",
        "key": "age",
        "type": "number"
      },
      {
        "label": "Adresse exacte / téléphone",
        "key": "adresse",
        "type": "textarea"
      },
      {
        "label": "Gestité",
        "key": "gestite",
        "type": "number"
      },
      {
        "label": "Parité",
        "key": "parite",
        "type": "number"
      },
      {
        "label": "Rang CPN",
        "key": "rang_cpn",
        "type": "select",
        "options": [
          "CPN 1 (1–3 mois)",
          "CPN 2 (4–6 mois)",
          "CPN 3 (7–8 mois)",
          "CPN 4 (9e mois)",
          "Premier contact / autre"
        ]
      },
      {
        "label": "Âge de grossesse / période",
        "key": "periode_grossesse",
        "type": "text"
      },
      {
        "label": "Poids (kg)",
        "key": "poids",
        "type": "number"
      },
      {
        "label": "Taille (cm)",
        "key": "taille",
        "type": "number"
      },
      {
        "label": "Périmètre brachial (mm)",
        "key": "pb",
        "type": "number"
      },
      {
        "label": "Tension artérielle",
        "key": "ta",
        "type": "text"
      },
      {
        "label": "Aspect des muqueuses",
        "key": "muqueuses",
        "type": "text"
      },
      {
        "label": "Œdèmes",
        "key": "oedemes",
        "type": "select",
        "options": [
          "Présents (+)",
          "Absents (0)"
        ]
      },
      {
        "label": "Hauteur utérine (cm)",
        "key": "hauteur_uterine",
        "type": "number"
      },
      {
        "label": "Bruits du cœur fœtal",
        "key": "bcf",
        "type": "select",
        "options": [
          "Présents (+)",
          "Absents (0)",
          "Non évalués"
        ]
      },
      {
        "label": "Toucher vaginal / clinique",
        "key": "toucher_vaginal",
        "type": "textarea"
      },
      {
        "label": "RPR / TPHA",
        "key": "rpr_tpha",
        "type": "text"
      },
      {
        "label": "Groupe sanguin / Rhésus",
        "key": "groupe_rhesus",
        "type": "text"
      },
      {
        "label": "Test d’Emmel",
        "key": "test_emmel",
        "type": "text"
      },
      {
        "label": "Autres bilans / observations",
        "key": "observations",
        "type": "textarea"
      }
    ]
  },
  "cpon": {
    "label": "Registre des consultations postnatales",
    "fields": [
      {
        "label": "N° d’ordre",
        "key": "numero_ordre",
        "type": "number"
      },
      {
        "label": "Date de consultation",
        "key": "date",
        "type": "date"
      },
      {
        "label": "Prénom(s) et nom de la mère",
        "key": "nom_mere",
        "type": "text"
      },
      {
        "label": "Âge de la mère",
        "key": "age_mere",
        "type": "number"
      },
      {
        "label": "Adresse exacte / téléphone",
        "key": "adresse",
        "type": "textarea"
      },
      {
        "label": "Date accouchement",
        "key": "date_accouchement",
        "type": "date"
      },
      {
        "label": "Date visite CPoN",
        "key": "date_visite",
        "type": "date"
      },
      {
        "label": "Rang / échéance CPoN",
        "key": "rang_cpon",
        "type": "select",
        "options": [
          "J3",
          "J8",
          "J15",
          "J41",
          "J42",
          "Autre"
        ]
      },
      {
        "label": "Prénom(s) et nom du nouveau-né",
        "key": "nom_nouveau_ne",
        "type": "text"
      },
      {
        "label": "Poids du nouveau-né (kg)",
        "key": "poids_nn",
        "type": "number"
      },
      {
        "label": "Taille du nouveau-né (cm)",
        "key": "taille_nn",
        "type": "number"
      },
      {
        "label": "Température",
        "key": "temperature",
        "type": "number"
      },
      {
        "label": "État du cordon",
        "key": "cordon",
        "type": "text"
      },
      {
        "label": "Infection / signes de danger",
        "key": "infection",
        "type": "textarea"
      },
      {
        "label": "Vaccination BCG",
        "key": "bcg",
        "type": "text"
      },
      {
        "label": "Vaccination Hep B",
        "key": "hep_b",
        "type": "text"
      },
      {
        "label": "Polio - O",
        "key": "polio_o",
        "type": "text"
      },
      {
        "label": "MILDA",
        "key": "milda",
        "type": "text"
      },
      {
        "label": "État de la mère",
        "key": "etat_mere",
        "type": "textarea"
      },
      {
        "label": "Fer / acide folique",
        "key": "fer_acide_folique",
        "type": "text"
      },
      {
        "label": "Test VIH / recherche",
        "key": "test_vih",
        "type": "text"
      },
      {
        "label": "Prise en charge / référence",
        "key": "prise_en_charge",
        "type": "textarea"
      },
      {
        "label": "Méthode PF",
        "key": "methode_pf",
        "type": "text"
      },
      {
        "label": "Observations",
        "key": "observations",
        "type": "textarea"
      }
    ]
  },
  "accouchements": {
    "label": "Registre des accouchements",
    "fields": [
      {
        "label": "N° d’ordre mensuel",
        "key": "numero_ordre",
        "type": "number"
      },
      {
        "label": "N° fiche partogramme",
        "key": "numero_partogramme",
        "type": "text"
      },
      {
        "label": "Date et heure d’entrée",
        "key": "date_heure_entree",
        "type": "text"
      },
      {
        "label": "Prénom(s) et nom de la femme",
        "key": "nom",
        "type": "text"
      },
      {
        "label": "Âge (années)",
        "key": "age",
        "type": "number"
      },
      {
        "label": "Adresse exacte / téléphone",
        "key": "adresse",
        "type": "textarea"
      },
      {
        "label": "Gestité",
        "key": "gestite",
        "type": "number"
      },
      {
        "label": "Parité",
        "key": "parite",
        "type": "number"
      },
      {
        "label": "Date et heure de l’accouchement",
        "key": "date_heure_accouchement",
        "type": "text"
      },
      {
        "label": "Lieu de l’accouchement",
        "key": "lieu",
        "type": "select",
        "options": [
          "Maternité",
          "Domicile",
          "Autre"
        ]
      },
      {
        "label": "Type d’accouchement",
        "key": "type_accouchement",
        "type": "select",
        "options": [
          "Normal",
          "Césarienne",
          "Forceps",
          "Ventouse",
          "Autre"
        ]
      },
      {
        "label": "Type de délivrance",
        "key": "delivrance",
        "type": "select",
        "options": [
          "Naturelle",
          "Artificielle",
          "Dirigée (GATPA)"
        ]
      },
      {
        "label": "Présentation",
        "key": "presentation",
        "type": "text"
      },
      {
        "label": "Qualification de l’agent",
        "key": "qualification",
        "type": "select",
        "options": [
          "Sage-femme",
          "Médecin",
          "Infirmier",
          "Assistant infirmier",
          "Autre"
        ]
      },
      {
        "label": "Nouveau-né : cri à la naissance (CRI)",
        "key": "cri",
        "type": "select",
        "options": [
          "Oui",
          "Non"
        ]
      },
      {
        "label": "État du nouveau-né",
        "key": "etat_nn",
        "type": "select",
        "options": [
          "Vivant bien portant (VBP)",
          "Mort-né frais (MNF)",
          "Mort-né macéré (MNM)",
          "Décédé (DCD)"
        ]
      },
      {
        "label": "Risque d’infection nouveau-né",
        "key": "risque_infection",
        "type": "checkbox"
      },
      {
        "label": "Nouveau-né référé",
        "key": "nn_refere",
        "type": "checkbox"
      },
      {
        "label": "Sexe du nouveau-né",
        "key": "sexe_nn",
        "type": "select",
        "options": [
          "M",
          "F"
        ]
      },
      {
        "label": "Poids du nouveau-né (g)",
        "key": "poids_nn",
        "type": "number"
      },
      {
        "label": "Soins immédiats du nouveau-né (MT, MS, SC, collyre, vitamine K)",
        "key": "soins_immediats",
        "type": "textarea"
      },
      {
        "label": "Antibiothérapie (ATB)",
        "key": "atb",
        "type": "select",
        "options": [
          "Oui",
          "Non"
        ]
      },
      {
        "label": "Réanimation (RAM)",
        "key": "ram",
        "type": "select",
        "options": [
          "Oui",
          "Non"
        ]
      },
      {
        "label": "Devenir de la mère",
        "key": "devenir_mere",
        "type": "select",
        "options": [
          "Vivante bien portante (VBP)",
          "Évacuée",
          "Décédée"
        ]
      },
      {
        "label": "Complications de l’accouchement",
        "key": "complications",
        "type": "textarea"
      },
      {
        "label": "VAT reçu pendant grossesse",
        "key": "vat",
        "type": "text"
      },
      {
        "label": "Fer / acide folique",
        "key": "fer_acide_folique",
        "type": "select",
        "options": [
          "Oui",
          "Non"
        ]
      },
      {
        "label": "PTME : test VIH",
        "key": "test_vih",
        "type": "select",
        "options": [
          "Oui",
          "Non"
        ]
      },
      {
        "label": "PTME : proposition / acceptation / réalisation",
        "key": "ptme_details",
        "type": "text"
      },
      {
        "label": "Counseling PF post-partum",
        "key": "counseling_pf",
        "type": "select",
        "options": [
          "Oui",
          "Non"
        ]
      },
      {
        "label": "Méthode PF choisie",
        "key": "methode_pf",
        "type": "text"
      },
      {
        "label": "Date et heure de sortie",
        "key": "date_heure_sortie",
        "type": "text"
      },
      {
        "label": "Journées d’hospitalisation",
        "key": "jours_hospitalisation",
        "type": "number"
      },
      {
        "label": "Observations",
        "key": "observations",
        "type": "textarea"
      }
    ]
  },
  "pf": {
    "label": "Registre de planification familiale",
    "fields": [
      {
        "label": "N° d’ordre mensuel",
        "key": "numero_ordre",
        "type": "number"
      },
      {
        "label": "Numéro / année de l’acceptante",
        "key": "numero_annee",
        "type": "text"
      },
      {
        "label": "Nouvelle dans le programme national PF",
        "key": "nouvelle_programme",
        "type": "select",
        "options": [
          "Oui",
          "Non"
        ]
      },
      {
        "label": "Prénom(s) et nom de l’acceptante",
        "key": "nom",
        "type": "text"
      },
      {
        "label": "Âge",
        "key": "age",
        "type": "number"
      },
      {
        "label": "Adresse exacte / téléphone",
        "key": "adresse",
        "type": "textarea"
      },
      {
        "label": "PF après avortement (<7 jours)",
        "key": "post_avortement",
        "type": "select",
        "options": [
          "Oui",
          "Non"
        ]
      },
      {
        "label": "PF post-partum",
        "key": "post_partum",
        "type": "select",
        "options": [
          "Immédiat (<48h)",
          "Tardif (jusqu’à 42 jours)",
          "Non"
        ]
      },
      {
        "label": "Pilule PP / POP (quantité)",
        "key": "pilule",
        "type": "text"
      },
      {
        "label": "DIU (I, R, R/I, C)",
        "key": "diu",
        "type": "text"
      },
      {
        "label": "Injectable IM / SC (prestataire ou auto-injection)",
        "key": "injection",
        "type": "textarea"
      },
      {
        "label": "Implant 1 capsule / 2 capsules (I, R, R/I, C)",
        "key": "implant",
        "type": "textarea"
      },
      {
        "label": "Anneau vaginal à progestérone",
        "key": "anneau",
        "type": "checkbox"
      },
      {
        "label": "Condom masculin (quantité)",
        "key": "condom_masculin",
        "type": "number"
      },
      {
        "label": "Condom féminin (quantité)",
        "key": "condom_feminin",
        "type": "number"
      },
      {
        "label": "Contraception d’urgence (CU)",
        "key": "cu",
        "type": "text"
      },
      {
        "label": "Méthode naturelle (MAMA, MJF, autre)",
        "key": "naturelle",
        "type": "text"
      },
      {
        "label": "Autres méthodes / CCV",
        "key": "autres_methodes",
        "type": "text"
      },
      {
        "label": "Raison de visite : arrêt",
        "key": "raison_arret",
        "type": "text"
      },
      {
        "label": "Raison de visite : changement",
        "key": "raison_changement",
        "type": "text"
      },
      {
        "label": "Bilan / informations",
        "key": "bilan_infos",
        "type": "textarea"
      },
      {
        "label": "Effets indésirables / complications",
        "key": "effets",
        "type": "textarea"
      },
      {
        "label": "Service additionnel SAD / porte d’entrée",
        "key": "sad",
        "type": "text"
      },
      {
        "label": "Observations / orientation / VIH / ISBC",
        "key": "observations",
        "type": "textarea"
      }
    ]
  },
  "enfants_malades": {
    "label": "Registre de consultation des enfants malades 0–14 ans",
    "fields": [
      {
        "label": "N° d’ordre mensuel",
        "key": "numero_ordre",
        "type": "number"
      },
      {
        "label": "Date de visite",
        "key": "date",
        "type": "date"
      },
      {
        "label": "N° enregistrement état civil",
        "key": "numero_etat_civil",
        "type": "text"
      },
      {
        "label": "Prénom(s) et nom de l’enfant",
        "key": "nom_enfant",
        "type": "text"
      },
      {
        "label": "Âge (mois 0–59 / années 5–14)",
        "key": "age",
        "type": "text"
      },
      {
        "label": "Sexe",
        "key": "sexe",
        "type": "select",
        "options": [
          "M",
          "F"
        ]
      },
      {
        "label": "Nom du parent / gardien et adresse",
        "key": "parent_adresse",
        "type": "textarea"
      },
      {
        "label": "Température (°C)",
        "key": "temperature",
        "type": "number"
      },
      {
        "label": "Mouvements respiratoires (cycles/min)",
        "key": "mouvements_respiratoires",
        "type": "number"
      },
      {
        "label": "Œdèmes",
        "key": "oedemes",
        "type": "select",
        "options": [
          "Oui",
          "Non"
        ]
      },
      {
        "label": "Périmètre brachial (mm)",
        "key": "pb",
        "type": "number"
      },
      {
        "label": "Poids (kg)",
        "key": "poids",
        "type": "number"
      },
      {
        "label": "Taille (cm)",
        "key": "taille",
        "type": "number"
      },
      {
        "label": "MA : classification et Z-score",
        "key": "ma_zscore",
        "type": "text"
      },
      {
        "label": "IP : classification et Z-score",
        "key": "ip_zscore",
        "type": "text"
      },
      {
        "label": "RC : classification et Z-score",
        "key": "rc_zscore",
        "type": "text"
      },
      {
        "label": "Signes généraux de danger",
        "key": "signes_danger",
        "type": "textarea"
      },
      {
        "label": "Plaintes / symptômes",
        "key": "plaintes",
        "type": "textarea"
      },
      {
        "label": "Diagnostic",
        "key": "diagnostic",
        "type": "textarea"
      },
      {
        "label": "Examens / résultats",
        "key": "examens",
        "type": "textarea"
      },
      {
        "label": "Traitement",
        "key": "traitement",
        "type": "textarea"
      },
      {
        "label": "Référence / orientation",
        "key": "reference",
        "type": "textarea"
      },
      {
        "label": "Observations",
        "key": "observations",
        "type": "textarea"
      }
    ]
  },
  "enfants_sains": {
    "label": "Registre des enfants sains 0–59 mois, vaccination et suivi nutritionnel",
    "fields": [
      {
        "label": "N° d’ordre unique de suivi",
        "key": "numero_ordre",
        "type": "number"
      },
      {
        "label": "N° enregistrement état civil",
        "key": "numero_etat_civil",
        "type": "text"
      },
      {
        "label": "Prénom(s) et nom de l’enfant",
        "key": "nom_enfant",
        "type": "text"
      },
      {
        "label": "Date de naissance",
        "key": "date_naissance",
        "type": "date"
      },
      {
        "label": "Sexe",
        "key": "sexe",
        "type": "select",
        "options": [
          "M",
          "F"
        ]
      },
      {
        "label": "Prénom(s) et nom mère / gardienne",
        "key": "nom_mere",
        "type": "text"
      },
      {
        "label": "Adresse exacte / téléphone",
        "key": "adresse",
        "type": "textarea"
      },
      {
        "label": "Date de visite",
        "key": "date_visite",
        "type": "date"
      },
      {
        "label": "Âge en mois (0–59)",
        "key": "age_mois",
        "type": "number"
      },
      {
        "label": "Vaccinations / antigènes et dates (selon calendrier du registre)",
        "key": "vaccinations",
        "type": "textarea"
      },
      {
        "label": "Dépistage : œdèmes",
        "key": "oedemes",
        "type": "select",
        "options": [
          "Oui",
          "Non"
        ]
      },
      {
        "label": "Poids (kg)",
        "key": "poids",
        "type": "number"
      },
      {
        "label": "Taille (cm)",
        "key": "taille",
        "type": "number"
      },
      {
        "label": "Périmètre brachial (mm)",
        "key": "pb",
        "type": "number"
      },
      {
        "label": "MA / surpoids / obésité : classification et Z-score",
        "key": "ma_zscore",
        "type": "text"
      },
      {
        "label": "IP : classification et Z-score",
        "key": "ip_zscore",
        "type": "text"
      },
      {
        "label": "RC : classification et Z-score",
        "key": "rc_zscore",
        "type": "text"
      },
      {
        "label": "Vitamine A",
        "key": "vitamine_a",
        "type": "checkbox"
      },
      {
        "label": "Déparasitage",
        "key": "deparasitage",
        "type": "checkbox"
      },
      {
        "label": "MILDA",
        "key": "milda",
        "type": "checkbox"
      },
      {
        "label": "AME (allaitement maternel exclusif)",
        "key": "ame",
        "type": "select",
        "options": [
          "Oui",
          "Non"
        ]
      },
      {
        "label": "Alimentation complémentaire (AC)",
        "key": "ac",
        "type": "select",
        "options": [
          "Oui",
          "Non"
        ]
      },
      {
        "label": "Suivi nutritionnel semestriel / dates et mesures",
        "key": "suivi_nutritionnel",
        "type": "textarea"
      },
      {
        "label": "Observations",
        "key": "observations",
        "type": "textarea"
      }
    ]
  },
  "cren": {
    "label": "Registre de suivi des enfants au CREN",
    "fields": [
      {
        "label": "N° d’ordre",
        "key": "numero_ordre",
        "type": "number"
      },
      {
        "label": "N° unique MAS",
        "key": "numero_mas",
        "type": "text"
      },
      {
        "label": "Prénom(s) et nom de l’enfant",
        "key": "nom_enfant",
        "type": "text"
      },
      {
        "label": "Sexe",
        "key": "sexe",
        "type": "select",
        "options": [
          "M",
          "F"
        ]
      },
      {
        "label": "Date de naissance ou âge (mois)",
        "key": "date_naissance_age",
        "type": "text"
      },
      {
        "label": "Nom mère / gardienne",
        "key": "nom_gardienne",
        "type": "text"
      },
      {
        "label": "Adresse exacte / téléphone",
        "key": "adresse",
        "type": "textarea"
      },
      {
        "label": "Date d’admission",
        "key": "date_admission",
        "type": "date"
      },
      {
        "label": "Type d’admission",
        "key": "type_admission",
        "type": "select",
        "options": [
          "Nouvelle admission – marasme",
          "Nouvelle admission – kwashiorkor",
          "Rechute",
          "Réadmission après abandon",
          "Transfert"
        ]
      },
      {
        "label": "Transfert interne de (UREN / CREN)",
        "key": "transfert_de",
        "type": "text"
      },
      {
        "label": "Poids admission (kg)",
        "key": "poids_admission",
        "type": "number"
      },
      {
        "label": "Taille admission (cm)",
        "key": "taille_admission",
        "type": "number"
      },
      {
        "label": "P/T Z-score admission",
        "key": "pt_zscore_admission",
        "type": "text"
      },
      {
        "label": "Œdèmes admission",
        "key": "oedemes_admission",
        "type": "select",
        "options": [
          "Oui",
          "Non"
        ]
      },
      {
        "label": "Périmètre brachial admission (mm)",
        "key": "pb_admission",
        "type": "number"
      },
      {
        "label": "Type de complication",
        "key": "complication",
        "type": "textarea"
      },
      {
        "label": "Date de sortie",
        "key": "date_sortie",
        "type": "date"
      },
      {
        "label": "Poids sortie (kg)",
        "key": "poids_sortie",
        "type": "number"
      },
      {
        "label": "Taille sortie (cm)",
        "key": "taille_sortie",
        "type": "number"
      },
      {
        "label": "P/T Z-score sortie",
        "key": "pt_zscore_sortie",
        "type": "text"
      },
      {
        "label": "Œdèmes sortie",
        "key": "oedemes_sortie",
        "type": "select",
        "options": [
          "Oui",
          "Non"
        ]
      },
      {
        "label": "PB sortie (mm)",
        "key": "pb_sortie",
        "type": "number"
      },
      {
        "label": "Type de sortie",
        "key": "type_sortie",
        "type": "select",
        "options": [
          "Traité avec succès",
          "Abandon",
          "Non répondant / référence médicale",
          "Guéri",
          "Décès",
          "Transfert"
        ]
      },
      {
        "label": "Transfert interne vers UREN / CREN",
        "key": "transfert_vers",
        "type": "text"
      },
      {
        "label": "Date du poids minimum",
        "key": "date_poids_min",
        "type": "date"
      },
      {
        "label": "Poids minimum enregistré",
        "key": "poids_min",
        "type": "number"
      },
      {
        "label": "Observations",
        "key": "observations",
        "type": "textarea"
      }
    ]
  },
  "deces": {
    "label": "Registre de décès",
    "fields": [
      {
        "label": "N° d’ordre",
        "key": "numero_ordre",
        "type": "number"
      },
      {
        "label": "Prénom(s) et nom du défunt",
        "key": "nom",
        "type": "text"
      },
      {
        "label": "Âge (mois si 0–23 mois, années dès 24 mois)",
        "key": "age",
        "type": "text"
      },
      {
        "label": "Sexe",
        "key": "sexe",
        "type": "select",
        "options": [
          "M",
          "F"
        ]
      },
      {
        "label": "Femme enceinte ou dans les 42 jours post-partum",
        "key": "grossesse_postpartum",
        "type": "select",
        "options": [
          "Oui",
          "Non",
          "Non applicable"
        ]
      },
      {
        "label": "Adresse exacte",
        "key": "adresse",
        "type": "textarea"
      },
      {
        "label": "Profession du défunt",
        "key": "profession",
        "type": "text"
      },
      {
        "label": "Date de décès",
        "key": "date_deces",
        "type": "date"
      },
      {
        "label": "Lieu de décès",
        "key": "lieu_deces",
        "type": "select",
        "options": [
          "Dans la structure",
          "À domicile",
          "Pendant le transfert",
          "Autre"
        ]
      },
      {
        "label": "Signes / motif / cause du décès",
        "key": "cause_deces",
        "type": "textarea"
      },
      {
        "label": "Observations complémentaires",
        "key": "observations",
        "type": "textarea"
      }
    ]
  },
  "laboratoire": {
    "label": "Registre d’examens de laboratoire",
    "fields": [
      {
        "label": "N° d’ordre mensuel",
        "key": "numero_ordre",
        "type": "number"
      },
      {
        "label": "Prénom(s) et nom du patient",
        "key": "nom",
        "type": "text"
      },
      {
        "label": "Mode de prise en charge",
        "key": "prise_en_charge",
        "type": "select",
        "options": [
          "Ticket",
          "Lettre de garantie",
          "Cas social",
          "Indigent",
          "Autre"
        ]
      },
      {
        "label": "Âge (années révolues)",
        "key": "age",
        "type": "number"
      },
      {
        "label": "Sexe",
        "key": "sexe",
        "type": "select",
        "options": [
          "M",
          "F"
        ]
      },
      {
        "label": "Adresse exacte",
        "key": "adresse",
        "type": "textarea"
      },
      {
        "label": "Patient interne (hospitalisé)",
        "key": "patient_interne",
        "type": "checkbox"
      },
      {
        "label": "Patient externe (non hospitalisé)",
        "key": "patient_externe",
        "type": "checkbox"
      },
      {
        "label": "Type(s) d’examen(s) demandé(s)",
        "key": "examens_demandes",
        "type": "textarea"
      },
      {
        "label": "Renseignements cliniques",
        "key": "renseignements_cliniques",
        "type": "textarea"
      },
      {
        "label": "Service demandeur",
        "key": "service_demandeur",
        "type": "text"
      },
      {
        "label": "Résultats des examens",
        "key": "resultats",
        "type": "textarea"
      },
      {
        "label": "Observations / rendez-vous / compte rendu",
        "key": "observations",
        "type": "textarea"
      }
    ]
  },
  "hospitalisation": {
    "label": "Registre d’hospitalisation",
    "fields": [
      {
        "label": "N° d’ordre mensuel",
        "key": "numero_ordre",
        "type": "number"
      },
      {
        "label": "Prénom(s) et nom du malade",
        "key": "nom",
        "type": "text"
      },
      {
        "label": "Âge (mois si 0–23 mois, années dès 24 mois)",
        "key": "age",
        "type": "text"
      },
      {
        "label": "Sexe",
        "key": "sexe",
        "type": "select",
        "options": [
          "M",
          "F"
        ]
      },
      {
        "label": "Femme enceinte",
        "key": "femme_enceinte",
        "type": "checkbox"
      },
      {
        "label": "Adresse exacte",
        "key": "adresse",
        "type": "textarea"
      },
      {
        "label": "Date d’entrée",
        "key": "date_entree",
        "type": "date"
      },
      {
        "label": "Diagnostic d’entrée",
        "key": "diagnostic_entree",
        "type": "textarea"
      },
      {
        "label": "Provenance (structure / unité / service)",
        "key": "provenance",
        "type": "text"
      },
      {
        "label": "Date de sortie",
        "key": "date_sortie",
        "type": "date"
      },
      {
        "label": "Durée de séjour (jours)",
        "key": "duree_sejour",
        "type": "number"
      },
      {
        "label": "Diagnostic de sortie",
        "key": "diagnostic_sortie",
        "type": "textarea"
      },
      {
        "label": "Devenir du malade",
        "key": "devenir",
        "type": "select",
        "options": [
          "Sorti vivant",
          "Évacué / transféré",
          "Décédé",
          "Autre"
        ]
      },
      {
        "label": "Précisions autre devenir",
        "key": "autre_devenir",
        "type": "text"
      },
      {
        "label": "Analyses effectuées",
        "key": "analyses",
        "type": "textarea"
      },
      {
        "label": "Observations",
        "key": "observations",
        "type": "textarea"
      }
    ]
  }
}
