PROJET REGISTRES DE SANTE — VERSION HIERARCHIQUE MULTIPAGE

FICHIERS
- app.py : connexion et accueil
- common.py : fonctions partagées, authentification, contrôles de rôle et saisie
- initialisation.py : création/mise à jour des tables, rôles et politiques RLS
- pages/1_Admin.py : administration et consultation des registres en lecture seule
- pages/2_Chef_de_programme.py : consultation du programme dans tous les postes
- pages/3_Chef_de_poste.py : consultation de tous les programmes de son poste
- pages/4_Agent_par_programme.py : saisie et gestion des registres autorisés
- schema_hierarchie.sql : migration SQL minimale
- requirements.txt : dépendances Python

RÔLES EXACTS
- admin
- chef_programme
- chef_poste
- agent_programme

INSTALLATION
1. Sauvegardez votre dossier actuel.
2. Copiez le contenu du ZIP dans le dossier racine du projet.
3. Conservez votre fichier .env et votre register_definitions.py actuels.
4. Vérifiez que .env contient :
   SUPABASE_URL
   SUPABASE_ANON_KEY
   SUPABASE_SERVICE_ROLE_KEY
   SUPABASE_DB_URL
   ADMIN_EMAIL
   ADMIN_PASSWORD
   ADMIN_NAME (facultatif)
5. Dans le terminal de PyCharm :
   python -m pip install -r requirements.txt
6. Exécutez :
   python initialisation.py
7. Lancez :
   streamlit run app.py

AFFECTATIONS
- ADMIN : aucun poste/programme requis. Peut gérer les programmes, postes et comptes.
- CHEF DE PROGRAMME : doit être associé à un programme. Consulte les registres associés à ce programme dans tous les postes.
- CHEF DE POSTE : doit être associé à un poste. Consulte tous les registres de ce poste.
- AGENT PAR PROGRAMME : doit être associé à un poste et à un programme, et recevoir les registres autorisés. Le registre doit aussi être associé à son programme.

SÉCURITÉ
- L'ADMIN peut consulter les données des registres mais aucun formulaire de création/modification/suppression des fiches de registre n'est présent dans son espace.
- Les chefs ont des espaces en consultation seule.
- Les agents utilisent le client authentifié ANON et les politiques RLS pour la saisie, la modification et la suppression.
- Le client SERVICE_ROLE est utilisé côté serveur Streamlit pour les tâches d'administration et les consultations inter-postes. Cette clé contourne RLS : elle doit rester dans .env sur le serveur, ne jamais être publiée ni intégrée dans un navigateur.
- Les pages contrôlent les rôles côté serveur Streamlit. Pour un déploiement public, ajouter aussi des tests de sécurité, limiter l'accès réseau au serveur, gérer les secrets dans l'environnement d'hébergement et faire auditer les règles RLS.
- Ce projet ne doit pas être utilisé avec des données réelles de patients avant validation complète, tests d'accès, sauvegardes et conformité réglementaire.

NOTE DE COMPATIBILITÉ
L'initialisation reprend les tables existantes posts, profiles, user_register_access et reg_<code>. CREATE TABLE IF NOT EXISTS ne modifie pas automatiquement les colonnes métier d'une table déjà existante. Si vos anciennes tables reg_<code> ont une structure différente, il faudra une migration dédiée.
