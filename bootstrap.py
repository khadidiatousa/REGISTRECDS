"""Initialisation serveur : crée le schéma et le premier administrateur.
À exécuter depuis un poste de confiance, jamais depuis le navigateur.
"""
import os, sys
from dotenv import load_dotenv
import psycopg2
from supabase import create_client

load_dotenv()
REQUIRED = ["SUPABASE_URL", "SUPABASE_SERVICE_ROLE_KEY", "SUPABASE_DB_URL", "ADMIN_EMAIL", "ADMIN_PASSWORD"]
missing = [x for x in REQUIRED if not os.getenv(x)]
if missing:
    raise SystemExit("Variables manquantes dans .env : " + ", ".join(missing))
if os.getenv("ADMIN_PASSWORD", "").startswith("REMPLACER") or len(os.getenv("ADMIN_PASSWORD", "")) < 14:
    raise SystemExit("Choisis dans .env un mot de passe administrateur d'au moins 14 caractères.")

schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
with open(schema_path, encoding="utf-8") as f:
    schema = f.read()
print("Création / mise à jour du schéma Supabase...")
with psycopg2.connect(os.environ["SUPABASE_DB_URL"]) as conn:
    with conn.cursor() as cur:
        cur.execute(schema)
print("Schéma créé.")

admin = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_SERVICE_ROLE_KEY"])
email = os.environ["ADMIN_EMAIL"].strip().lower()
found = None
page = 1
while page <= 20 and found is None:
    batch = admin.auth.admin.list_users(page=page, per_page=100)
    users = getattr(batch, "users", batch if isinstance(batch, list) else [])
    for u in users:
        if (getattr(u, "email", "") or "").lower() == email:
            found = u; break
    if len(users) < 100: break
    page += 1
if found:
    uid = found.id
    print("Utilisateur administrateur déjà présent : profil mis à jour.")
else:
    result = admin.auth.admin.create_user({
        "email": email,
        "password": os.environ["ADMIN_PASSWORD"],
        "email_confirm": True,
        "user_metadata": {"display_name": os.getenv("ADMIN_NAME", "Administrateur général")}
    })
    uid = result.user.id
with psycopg2.connect(os.environ["SUPABASE_DB_URL"]) as conn:
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO public.profiles(id,display_name,role,post_id,is_active)
            VALUES (%s,%s,'admin',NULL,true)
            ON CONFLICT(id) DO UPDATE SET display_name=EXCLUDED.display_name,
                role='admin',post_id=NULL,is_active=true,updated_at=now()
        """, (uid, os.getenv("ADMIN_NAME", "Administrateur général")))
print("Administrateur prêt :", email)
print("Tu peux maintenant lancer : python -m streamlit run app.py")
