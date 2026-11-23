# Liste de vérification avant production

- [ ] Exécuter bootstrap sur un projet Supabase de test, pas sur des données réelles.
- [ ] Vérifier que les 11 tables `reg_*` et les politiques RLS existent.
- [ ] Tester une connexion admin, créer deux postes et deux agents.
- [ ] Vérifier qu'un agent A ne peut ni lire ni modifier les fiches du poste B, même par appel API direct.
- [ ] Vérifier qu'un agent ne peut pas s'auto-attribuer le rôle admin ni ajouter des droits de registre.
- [ ] Vérifier les règles d'export et la traçabilité des modifications.
- [ ] Tester le renouvellement/expiration des sessions.
- [ ] Vérifier les sauvegardes et une restauration réelle.
- [ ] Faire valider tous les champs et règles par les responsables des registres.
- [ ] Faire une revue indépendante de sécurité et conformité pour les données de santé au Sénégal.
