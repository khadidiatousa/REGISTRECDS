# Registres Santé — Streamlit + Supabase

## Ce que contient cette version
- Authentification Supabase e-mail / mot de passe.
- Initialisation du schéma Supabase par `bootstrap.py` depuis un poste de confiance.
- Création initiale de l'administrateur à partir des variables `.env`.
- Gestion des postes et création de comptes agents par l'administrateur.
- Affectation d'un agent à un poste et à une liste de registres autorisés.
- 11 formulaires indépendants, basés sur les PDF de registres Sénégal version 2018 fournis : consultation générale, CPN, CPoN, accouchements, PF, enfants malades 0–14, enfants sains 0–59 mois, CREN, décès, laboratoire, hospitalisation.
- Une table dédiée `reg_<code>` par registre ; contenu propre au formulaire conservé dans JSONB.
- RLS et journal d'audit des insertions/modifications/suppressions.

## Installation Windows / PowerShell

1. Place le dossier du projet dans `C:\Users\...\PycharmProjects\registrenumerique`.
2. Active ton environnement Python 3.13 :
   ```powershell
   .env313\Scripts\Activate.ps1
   ```
3. Installe les dépendances :
   ```powershell
   python -m pip install -r requirements.txt
   ```
4. Copie `.env.example` vers `.env` puis renseigne les variables :
   - `SUPABASE_URL` et `SUPABASE_ANON_KEY` depuis Supabase > Project Settings > API.
   - `SUPABASE_DB_URL` depuis Supabase > Project Settings > Database > Connection string (URI), avec le mot de passe DB.
   - `SUPABASE_SERVICE_ROLE_KEY` ou la clé secrète serveur depuis les paramètres API. Elle reste uniquement dans `.env` côté serveur.
   - `ADMIN_EMAIL`, `ADMIN_PASSWORD` (au moins 14 caractères, unique) et `ADMIN_NAME`.
5. Lance une seule fois l'initialisation :
   ```powershell
   python bootstrap.py
   ```
   Ce script crée les tables, les politiques RLS et le premier compte administrateur. Ne l'exécute que depuis un environnement de confiance.
6. Lance Streamlit :
   ```powershell
   python -m streamlit run app.py
   ```
7. Ouvre `http://localhost:8501` et connecte-toi avec `ADMIN_EMAIL` et `ADMIN_PASSWORD`.

## Premier usage
1. Connecte-toi comme administrateur.
2. Onglet « Postes de santé » : crée les postes.
3. Onglet « Utilisateurs » : crée les comptes agents, choisis leur poste et leurs registres autorisés.
4. L'agent se connecte avec ses propres identifiants et ne voit que les registres attribués à son poste.

## Sécurité impérative
- Ne partage jamais `.env`, la clé `SUPABASE_SERVICE_ROLE_KEY`, la chaîne PostgreSQL ni le mot de passe DB.
- N'ajoute pas `.env` à Git ou à une archive publique.
- La clé serveur est utilisée seulement par le processus Python Streamlit / bootstrap, jamais envoyée au navigateur.
- Le schéma RLS fourni est une base de travail à auditer. Tester les rôles admin/agent, les tentatives d'accès inter-postes, l'export, les mises à jour, les sauvegardes et la restauration avant données réelles.
- Les données de santé sont particulièrement sensibles. Confirmer les exigences réglementaires sénégalaises, la gouvernance, les habilitations, la conservation, les sauvegardes chiffrées, le contrôle d'accès, la traçabilité et l'hébergement autorisé avec les responsables compétents avant mise en production.
- Cette version ne remplace pas une validation clinique des formulaires. Les champs ont été structurés à partir des PDF reçus ; comparer chaque écran au registre officiel et faire valider par les responsables de santé avant toute saisie réelle.

## Limites connues à traiter avant production
- Les formulaires enfants sains et CPoN ont des séquences de visites / âges multiples : cette première version les capture sous forme de zones structurées à compléter ; une interface répétable par visite et un suivi longitudinal devront être ajoutés.
- Le calcul automatique des indicateurs mensuels et des statistiques de district n'est pas encore validé.
- Le flux de mot de passe oublié, la désactivation / réinitialisation des comptes, l'export réglementé, les sauvegardes et la revue de sécurité indépendante restent à mettre en place.
- Les suppressions de fiches ne sont pas exposées dans l'interface.
