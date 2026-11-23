import os
import re
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
from supabase import create_client
from register_definitions import REGISTERS

load_dotenv(override=True)

DATABASE_URL = os.getenv("SUPABASE_DB_URL")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
ADMIN_NAME = os.getenv("ADMIN_NAME", "Administrateur général")

ROLES = ("admin", "chef_programme", "chef_poste", "agent_programme")

def verifier_configuration():
    variables = {
        "SUPABASE_DB_URL": DATABASE_URL,
        "SUPABASE_URL": SUPABASE_URL,
        "SUPABASE_SERVICE_ROLE_KEY": SUPABASE_KEY,
        "ADMIN_EMAIL": ADMIN_EMAIL,
        "ADMIN_PASSWORD": ADMIN_PASSWORD,
    }
    missing = [name for name, value in variables.items() if not value]
    if missing:
        raise RuntimeError("Variables manquantes dans .env : " + ", ".join(missing))
    if not REGISTERS:
        raise RuntimeError("Aucun registre trouvé dans register_definitions.py.")
    for code in REGISTERS:
        if not re.fullmatch(r"[a-z0-9_]+", code):
            raise ValueError(f"Code de registre invalide : {code}")

def initialiser_tables():
    verifier_configuration()
    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE EXTENSION IF NOT EXISTS pgcrypto;

                CREATE TABLE IF NOT EXISTS public.posts (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    name TEXT NOT NULL UNIQUE,
                    address TEXT,
                    district TEXT,
                    is_active BOOLEAN NOT NULL DEFAULT TRUE,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
                );
                ALTER TABLE public.posts ADD COLUMN IF NOT EXISTS address TEXT;
                ALTER TABLE public.posts ADD COLUMN IF NOT EXISTS district TEXT;
                ALTER TABLE public.posts ADD COLUMN IF NOT EXISTS is_active BOOLEAN NOT NULL DEFAULT TRUE;

                CREATE TABLE IF NOT EXISTS public.programs (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    name TEXT NOT NULL UNIQUE,
                    is_active BOOLEAN NOT NULL DEFAULT TRUE,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
                );

                CREATE TABLE IF NOT EXISTS public.profiles (
                    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
                    display_name TEXT,
                    role TEXT NOT NULL DEFAULT 'agent_programme',
                    post_id UUID REFERENCES public.posts(id) ON DELETE SET NULL,
                    program_id UUID REFERENCES public.programs(id) ON DELETE SET NULL,
                    is_active BOOLEAN NOT NULL DEFAULT TRUE,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
                );
                ALTER TABLE public.profiles ADD COLUMN IF NOT EXISTS is_active BOOLEAN NOT NULL DEFAULT TRUE;
                ALTER TABLE public.profiles ADD COLUMN IF NOT EXISTS program_id UUID REFERENCES public.programs(id) ON DELETE SET NULL;
                ALTER TABLE public.profiles ALTER COLUMN role SET DEFAULT 'agent_programme';

                -- Supprime l'ancienne contrainte role (qui n'acceptait que admin/agent).
                DO $$
                DECLARE c RECORD;
                BEGIN
                    FOR c IN
                        SELECT conname
                        FROM pg_constraint
                        WHERE conrelid = 'public.profiles'::regclass
                          AND contype = 'c'
                          AND pg_get_constraintdef(oid) ILIKE '%role%'
                    LOOP
                        EXECUTE format('ALTER TABLE public.profiles DROP CONSTRAINT %I', c.conname);
                    END LOOP;
                END $$;

                UPDATE public.profiles SET role = 'agent_programme' WHERE role = 'agent';
                ALTER TABLE public.profiles
                    ADD CONSTRAINT profiles_role_hierarchy_check
                    CHECK (role IN ('admin','chef_programme','chef_poste','agent_programme'));

                CREATE TABLE IF NOT EXISTS public.user_register_access (
                    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
                    register_code TEXT NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
                    PRIMARY KEY (user_id, register_code)
                );

                CREATE TABLE IF NOT EXISTS public.program_register_access (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    program_id UUID NOT NULL REFERENCES public.programs(id) ON DELETE CASCADE,
                    register_code TEXT NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
                    UNIQUE(program_id, register_code)
                );

                CREATE OR REPLACE FUNCTION public.current_user_post_id()
                RETURNS UUID LANGUAGE SQL STABLE SECURITY DEFINER
                SET search_path = public
                AS $$
                    SELECT post_id FROM public.profiles
                    WHERE id = auth.uid() AND is_active = TRUE
                    LIMIT 1;
                $$;

                CREATE OR REPLACE FUNCTION public.current_user_program_id()
                RETURNS UUID LANGUAGE SQL STABLE SECURITY DEFINER
                SET search_path = public
                AS $$
                    SELECT program_id FROM public.profiles
                    WHERE id = auth.uid() AND is_active = TRUE
                    LIMIT 1;
                $$;

                CREATE OR REPLACE FUNCTION public.current_user_role()
                RETURNS TEXT LANGUAGE SQL STABLE SECURITY DEFINER
                SET search_path = public
                AS $$
                    SELECT role FROM public.profiles
                    WHERE id = auth.uid() AND is_active = TRUE
                    LIMIT 1;
                $$;

                CREATE OR REPLACE FUNCTION public.user_has_register_access(p_code TEXT)
                RETURNS BOOLEAN LANGUAGE SQL STABLE SECURITY DEFINER
                SET search_path = public
                AS $$
                    SELECT
                        public.current_user_role() = 'agent_programme'
                        AND EXISTS (
                            SELECT 1 FROM public.user_register_access ura
                            WHERE ura.user_id = auth.uid()
                              AND ura.register_code = p_code
                        )
                        AND EXISTS (
                            SELECT 1 FROM public.program_register_access pra
                            WHERE pra.program_id = public.current_user_program_id()
                              AND pra.register_code = p_code
                        );
                $$;

                ALTER TABLE public.posts ENABLE ROW LEVEL SECURITY;
                ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
                ALTER TABLE public.user_register_access ENABLE ROW LEVEL SECURITY;
                ALTER TABLE public.programs ENABLE ROW LEVEL SECURITY;
                ALTER TABLE public.program_register_access ENABLE ROW LEVEL SECURITY;

                DROP POLICY IF EXISTS profiles_select_own ON public.profiles;
                CREATE POLICY profiles_select_own ON public.profiles
                    FOR SELECT TO authenticated USING (auth.uid() = id);

                DROP POLICY IF EXISTS access_select_own ON public.user_register_access;
                CREATE POLICY access_select_own ON public.user_register_access
                    FOR SELECT TO authenticated USING (user_id = auth.uid());

                REVOKE ALL ON public.programs FROM anon, authenticated;
                REVOKE ALL ON public.program_register_access FROM anon, authenticated;
                GRANT ALL ON public.programs TO service_role;
                GRANT ALL ON public.program_register_access TO service_role;
                GRANT SELECT ON public.profiles TO authenticated;
                GRANT SELECT ON public.user_register_access TO authenticated;
                GRANT ALL ON public.posts TO service_role;
                GRANT ALL ON public.profiles TO service_role;
                GRANT ALL ON public.user_register_access TO service_role;
                GRANT ALL ON public.programs TO service_role;
                GRANT ALL ON public.program_register_access TO service_role;
                GRANT EXECUTE ON FUNCTION public.current_user_post_id() TO authenticated;
                GRANT EXECUTE ON FUNCTION public.current_user_program_id() TO authenticated;
                GRANT EXECUTE ON FUNCTION public.current_user_role() TO authenticated;
                GRANT EXECUTE ON FUNCTION public.user_has_register_access(TEXT) TO authenticated;
            """)

            for code in REGISTERS:
                table_name = "reg_" + code
                cursor.execute(sql.SQL("""
                    CREATE TABLE IF NOT EXISTS public.{} (
                        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                        post_id UUID NOT NULL REFERENCES public.posts(id),
                        created_by UUID NOT NULL REFERENCES auth.users(id),
                        record_date DATE NOT NULL,
                        data JSONB NOT NULL DEFAULT '{{}}'::jsonb,
                        created_at TIMESTAMPTZ NOT NULL DEFAULT now()
                    );
                """).format(sql.Identifier(table_name)))

                cursor.execute(sql.SQL("ALTER TABLE public.{} ENABLE ROW LEVEL SECURITY;").format(sql.Identifier(table_name)))

                # Supprime toutes les anciennes politiques de cette table :
                # PostgreSQL combine les politiques permissives avec OR.
                # Garder une ancienne politique pourrait donc élargir les accès.
                cursor.execute("""
                    SELECT policyname
                    FROM pg_policies
                    WHERE schemaname = 'public' AND tablename = %s;
                """, (table_name,))
                old_policies = [row[0] for row in cursor.fetchall()]
                for old_policy in old_policies:
                    cursor.execute(sql.SQL("DROP POLICY IF EXISTS {} ON public.{};").format(
                        sql.Identifier(old_policy), sql.Identifier(table_name)
                    ))

                cursor.execute(sql.SQL("""
                    CREATE POLICY register_select_agent ON public.{}
                    FOR SELECT TO authenticated
                    USING (
                        public.current_user_role() = 'agent_programme'
                        AND post_id = public.current_user_post_id()
                        AND public.user_has_register_access({})
                    );
                """).format(sql.Identifier(table_name), sql.Literal(code)))

                cursor.execute(sql.SQL("""
                    CREATE POLICY register_insert_agent ON public.{}
                    FOR INSERT TO authenticated
                    WITH CHECK (
                        public.current_user_role() = 'agent_programme'
                        AND created_by = auth.uid()
                        AND post_id = public.current_user_post_id()
                        AND public.user_has_register_access({})
                    );
                """).format(sql.Identifier(table_name), sql.Literal(code)))

                cursor.execute(sql.SQL("""
                    CREATE POLICY register_update_agent ON public.{}
                    FOR UPDATE TO authenticated
                    USING (
                        public.current_user_role() = 'agent_programme'
                        AND post_id = public.current_user_post_id()
                        AND public.user_has_register_access({})
                    )
                    WITH CHECK (
                        public.current_user_role() = 'agent_programme'
                        AND post_id = public.current_user_post_id()
                        AND public.user_has_register_access({})
                    );
                """).format(sql.Identifier(table_name), sql.Literal(code), sql.Literal(code)))

                cursor.execute(sql.SQL("""
                    CREATE POLICY register_delete_agent ON public.{}
                    FOR DELETE TO authenticated
                    USING (
                        public.current_user_role() = 'agent_programme'
                        AND post_id = public.current_user_post_id()
                        AND public.user_has_register_access({})
                    );
                """).format(sql.Identifier(table_name), sql.Literal(code)))

                cursor.execute(sql.SQL("""
                    GRANT SELECT, INSERT, UPDATE, DELETE ON public.{} TO authenticated;
                    GRANT ALL ON public.{} TO service_role;
                """).format(sql.Identifier(table_name), sql.Identifier(table_name)))

                print(f"Table et politiques configurées : {table_name}")

            cursor.execute("NOTIFY pgrst, 'reload schema';")

    print("Tables principales et hiérarchie créées/mises à jour.")
    print("Politiques RLS des agents configurées.")

def creer_administrateur():
    verifier_configuration()
    sb = create_client(SUPABASE_URL, SUPABASE_KEY)
    users = sb.auth.admin.list_users()
    existing = next(
        (user for user in users if user.email and user.email.lower() == ADMIN_EMAIL.lower()),
        None
    )
    if existing:
        user_id = existing.id
        print("Compte administrateur Auth déjà existant.")
    else:
        result = sb.auth.admin.create_user({
            "email": ADMIN_EMAIL,
            "password": ADMIN_PASSWORD,
            "email_confirm": True,
            "user_metadata": {"display_name": ADMIN_NAME},
        })
        user_id = result.user.id
        print("Compte administrateur Auth créé.")

    with psycopg2.connect(DATABASE_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO public.profiles (id, display_name, role, post_id, program_id, is_active)
                VALUES (%s, %s, 'admin', NULL, NULL, TRUE)
                ON CONFLICT (id) DO UPDATE SET
                    display_name = EXCLUDED.display_name,
                    role = 'admin',
                    post_id = NULL,
                    program_id = NULL,
                    is_active = TRUE;
            """, (user_id, ADMIN_NAME))
            cursor.execute("NOTIFY pgrst, 'reload schema';")
    print("Profil ADMIN créé ou mis à jour.")
    print("Adresse :", ADMIN_EMAIL)
    print("Rôle : ADMIN")
    print("Statut : actif")

if __name__ == "__main__":
    print("===================================")
    print("INITIALISATION REGISTRES SANTE")
    print("===================================")
    initialiser_tables()
    creer_administrateur()
    print("INITIALISATION TERMINÉE AVEC SUCCÈS")
