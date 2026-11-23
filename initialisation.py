
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
ADMIN_NAME = os.getenv(
    "ADMIN_NAME",
    "Administrateur général"
)


def verifier_configuration():

    variables = {
        "SUPABASE_DB_URL": DATABASE_URL,
        "SUPABASE_URL": SUPABASE_URL,
        "SUPABASE_SERVICE_ROLE_KEY": SUPABASE_KEY,
        "ADMIN_EMAIL": ADMIN_EMAIL,
        "ADMIN_PASSWORD": ADMIN_PASSWORD,
    }

    manquantes = [
        nom for nom, valeur in variables.items()
        if not valeur
    ]

    if manquantes:
        raise RuntimeError(
            "Variables manquantes dans .env : "
            + ", ".join(manquantes)
        )

    if not REGISTERS:
        raise RuntimeError(
            "Aucun registre trouvé dans register_definitions.py."
        )


def initialiser_tables():

    verifier_configuration()

    with psycopg2.connect(DATABASE_URL) as conn:

        with conn.cursor() as cursor:

            # =========================================
            # TABLES PRINCIPALES
            # =========================================

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

                ALTER TABLE public.posts
                ADD COLUMN IF NOT EXISTS address TEXT;

                ALTER TABLE public.posts
                ADD COLUMN IF NOT EXISTS district TEXT;

                ALTER TABLE public.posts
                ADD COLUMN IF NOT EXISTS is_active
                BOOLEAN NOT NULL DEFAULT TRUE;

                CREATE TABLE IF NOT EXISTS public.profiles (
                    id UUID PRIMARY KEY
                        REFERENCES auth.users(id) ON DELETE CASCADE,
                    display_name TEXT,
                    role TEXT NOT NULL DEFAULT 'agent'
                        CHECK (role IN ('admin', 'agent')),
                    post_id UUID REFERENCES public.posts(id),
                    is_active BOOLEAN NOT NULL DEFAULT TRUE,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
                );

                ALTER TABLE public.profiles
                ADD COLUMN IF NOT EXISTS is_active
                BOOLEAN NOT NULL DEFAULT TRUE;

                CREATE TABLE IF NOT EXISTS public.user_register_access (
                    user_id UUID NOT NULL
                        REFERENCES auth.users(id) ON DELETE CASCADE,
                    register_code TEXT NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
                    PRIMARY KEY (user_id, register_code)
                );

                CREATE TABLE IF NOT EXISTS public.consultations (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    post_id UUID NOT NULL
                        REFERENCES public.posts(id),
                    created_by UUID NOT NULL
                        REFERENCES auth.users(id),
                    consultation_date DATE NOT NULL,
                    register_type TEXT NOT NULL,
                    age_years INT CHECK (
                        age_years BETWEEN 0 AND 120
                    ),
                    sex TEXT,
                    notes TEXT,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
                );

                -- Fonction sécurisée pour retrouver le poste
                -- de l'utilisateur connecté.
                CREATE OR REPLACE FUNCTION
                public.current_user_post_id()
                RETURNS UUID
                LANGUAGE SQL
                STABLE
                SECURITY DEFINER
                SET search_path = public
                AS $function$
                    SELECT post_id
                    FROM public.profiles
                    WHERE id = auth.uid()
                    AND is_active = TRUE
                    LIMIT 1;
                $function$;

                -- Fonction sécurisée pour vérifier
                -- l'autorisation sur un registre.
                CREATE OR REPLACE FUNCTION
                public.user_has_register_access(p_code TEXT)
                RETURNS BOOLEAN
                LANGUAGE SQL
                STABLE
                SECURITY DEFINER
                SET search_path = public
                AS $function$
                    SELECT EXISTS (
                        SELECT 1
                        FROM public.user_register_access
                        WHERE user_id = auth.uid()
                        AND register_code = p_code
                    );
                $function$;

                -- Activation de la sécurité.
                ALTER TABLE public.posts
                ENABLE ROW LEVEL SECURITY;

                ALTER TABLE public.profiles
                ENABLE ROW LEVEL SECURITY;

                ALTER TABLE public.user_register_access
                ENABLE ROW LEVEL SECURITY;

                ALTER TABLE public.consultations
                ENABLE ROW LEVEL SECURITY;

                -- Nettoyage des anciennes politiques.
                DROP POLICY IF EXISTS profiles_select_own
                ON public.profiles;

                DROP POLICY IF EXISTS profiles_select_admin
                ON public.profiles;

                DROP POLICY IF EXISTS access_select_own
                ON public.user_register_access;

                -- Chaque utilisateur lit uniquement son profil.
                CREATE POLICY profiles_select_own
                ON public.profiles
                FOR SELECT
                TO authenticated
                USING (auth.uid() = id);

                -- Chaque agent lit ses propres autorisations.
                CREATE POLICY access_select_own
                ON public.user_register_access
                FOR SELECT
                TO authenticated
                USING (user_id = auth.uid());

                GRANT USAGE ON SCHEMA public TO authenticated;

                GRANT SELECT ON public.profiles
                TO authenticated;

                GRANT SELECT ON public.user_register_access
                TO authenticated;

                GRANT EXECUTE
                ON FUNCTION public.current_user_post_id()
                TO authenticated;

                GRANT EXECUTE
                ON FUNCTION public.user_has_register_access(TEXT)
                TO authenticated;
            """)

            # =========================================
            # CREATION DES TABLES DES REGISTRES
            # =========================================

            for code, definition in REGISTERS.items():

                if not re.fullmatch(r"[a-z0-9_]+", code):
                    raise ValueError(
                        f"Code de registre invalide : {code}"
                    )

                table_name = "reg_" + code

                # Les accolades {{}} sont nécessaires ici :
                # elles produisent '{}' dans le SQL final.
                cursor.execute(
                    sql.SQL("""
                        CREATE TABLE IF NOT EXISTS public.{} (
                            id UUID PRIMARY KEY
                                DEFAULT gen_random_uuid(),

                            post_id UUID NOT NULL
                                REFERENCES public.posts(id),

                            created_by UUID NOT NULL
                                REFERENCES auth.users(id),

                            record_date DATE NOT NULL,

                            data JSONB NOT NULL
                                DEFAULT '{{}}'::jsonb,

                            created_at TIMESTAMPTZ NOT NULL
                                DEFAULT now()
                        );
                    """).format(
                        sql.Identifier(table_name)
                    )
                )

                # Activer RLS sur chaque registre.
                cursor.execute(
                    sql.SQL("""
                        ALTER TABLE public.{}
                        ENABLE ROW LEVEL SECURITY;
                    """).format(
                        sql.Identifier(table_name)
                    )
                )

                policy_select = table_name + "_select"
                policy_insert = table_name + "_insert"

                # Supprimer les anciennes politiques.
                cursor.execute(
                    sql.SQL("""
                        DROP POLICY IF EXISTS {}
                        ON public.{};
                    """).format(
                        sql.Identifier(policy_select),
                        sql.Identifier(table_name)
                    )
                )

                cursor.execute(
                    sql.SQL("""
                        DROP POLICY IF EXISTS {}
                        ON public.{};
                    """).format(
                        sql.Identifier(policy_insert),
                        sql.Identifier(table_name)
                    )
                )

                # Lecture limitée au poste et au registre autorisé.
                cursor.execute(
                    sql.SQL("""
                        CREATE POLICY {}
                        ON public.{}
                        FOR SELECT
                        TO authenticated
                        USING (
                            post_id = public.current_user_post_id()
                            AND public.user_has_register_access({})
                        );
                    """).format(
                        sql.Identifier(policy_select),
                        sql.Identifier(table_name),
                        sql.Literal(code)
                    )
                )

                # Insertion limitée au compte et au poste.
                cursor.execute(
                    sql.SQL("""
                        CREATE POLICY {}
                        ON public.{}
                        FOR INSERT
                        TO authenticated
                        WITH CHECK (
                            created_by = auth.uid()
                            AND post_id = public.current_user_post_id()
                            AND public.user_has_register_access({})
                        );
                    """).format(
                        sql.Identifier(policy_insert),
                        sql.Identifier(table_name),
                        sql.Literal(code)
                    )
                )

                cursor.execute(
                    sql.SQL("""
                        GRANT SELECT, INSERT
                        ON public.{}
                        TO authenticated;
                    """).format(
                        sql.Identifier(table_name)
                    )
                )

                print(
                    f"Table créée ou vérifiée : {table_name}"
                )

            # Demander à Supabase de recharger son schéma.
            cursor.execute("NOTIFY pgrst, 'reload schema';")

    print("Tables principales créées ou mises à jour.")
    print("Tables des registres configurées.")
    print("Politiques de sécurité configurées.")


def creer_administrateur():

    verifier_configuration()

    sb = create_client(
        SUPABASE_URL,
        SUPABASE_KEY
    )

    # Rechercher le compte existant.
    users = sb.auth.admin.list_users()

    existing = next(
        (
            user for user in users
            if user.email
            and user.email.lower() == ADMIN_EMAIL.lower()
        ),
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
            "user_metadata": {
                "display_name": ADMIN_NAME
            }
        })

        user_id = result.user.id

        print("Compte administrateur Auth créé.")

    # Créer ou mettre à jour son profil.
    with psycopg2.connect(DATABASE_URL) as conn:

        with conn.cursor() as cursor:

            cursor.execute(
                """
                INSERT INTO public.profiles (
                    id,
                    display_name,
                    role,
                    post_id,
                    is_active
                )
                VALUES (
                    %s,
                    %s,
                    'admin',
                    NULL,
                    TRUE
                )
                ON CONFLICT (id)
                DO UPDATE SET
                    display_name = EXCLUDED.display_name,
                    role = 'admin',
                    post_id = NULL,
                    is_active = TRUE;
                """,
                (user_id, ADMIN_NAME)
            )

            cursor.execute(
                "NOTIFY pgrst, 'reload schema';"
            )

    print("Profil administrateur créé ou mis à jour.")
    print("Adresse :", ADMIN_EMAIL)
    print("Rôle : administrateur général")
    print("Statut : actif")


if __name__ == "__main__":

    print("===================================")
    print("INITIALISATION DES REGISTRES SANTE")
    print("===================================")

    initialiser_tables()

    creer_administrateur()

    print("===================================")
    print("INITIALISATION TERMINEE")
    print("===================================")
