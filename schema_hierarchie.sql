-- MIGRATION HIERARCHIE REGISTRES SANTE
-- Faire une sauvegarde avant exécution.
-- Le script initialisation.py contient les mêmes opérations de schéma.
-- Exécuter initialisation.py après cette migration, ou utiliser ce SQL seul.

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS public.programs (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    name text NOT NULL UNIQUE,
    is_active boolean NOT NULL DEFAULT true,
    created_at timestamptz NOT NULL DEFAULT now()
);

ALTER TABLE public.profiles
    ADD COLUMN IF NOT EXISTS program_id uuid REFERENCES public.programs(id) ON DELETE SET NULL;

DO $$
DECLARE c RECORD;
BEGIN
    FOR c IN
        SELECT conname FROM pg_constraint
        WHERE conrelid = 'public.profiles'::regclass
          AND contype = 'c'
          AND pg_get_constraintdef(oid) ILIKE '%role%'
    LOOP
        EXECUTE format('ALTER TABLE public.profiles DROP CONSTRAINT %I', c.conname);
    END LOOP;
END $$;

UPDATE public.profiles SET role = 'agent_programme' WHERE role = 'agent';
ALTER TABLE public.profiles ALTER COLUMN role SET DEFAULT 'agent_programme';
ALTER TABLE public.profiles
    ADD CONSTRAINT profiles_role_hierarchy_check
    CHECK (role IN ('admin','chef_programme','chef_poste','agent_programme'));

CREATE TABLE IF NOT EXISTS public.program_register_access (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    program_id uuid NOT NULL REFERENCES public.programs(id) ON DELETE CASCADE,
    register_code text NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    UNIQUE(program_id, register_code)
);

-- Les fonctions et politiques détaillées sont installées par initialisation.py.
