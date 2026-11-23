-- Registres Santé — schéma de départ. Exécuter une seule fois via bootstrap.py.
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS public.posts (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(), name text NOT NULL UNIQUE,
 district text, address text, is_active boolean NOT NULL DEFAULT true,
 created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS public.profiles (
 id uuid PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
 display_name text NOT NULL, role text NOT NULL DEFAULT 'agent' CHECK(role IN ('admin','agent')),
 post_id uuid REFERENCES public.posts(id), is_active boolean NOT NULL DEFAULT true,
 created_at timestamptz NOT NULL DEFAULT now(), updated_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS public.register_catalog (
 code text PRIMARY KEY, label text NOT NULL, source_version text NOT NULL DEFAULT 'PDF Sénégal 2018', is_active boolean NOT NULL DEFAULT true
);
CREATE TABLE IF NOT EXISTS public.user_register_access (
 user_id uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
 register_code text NOT NULL REFERENCES public.register_catalog(code),
 granted_at timestamptz NOT NULL DEFAULT now(), granted_by uuid REFERENCES auth.users(id),
 PRIMARY KEY(user_id, register_code)
);
CREATE TABLE IF NOT EXISTS public.audit_logs (
 id bigserial PRIMARY KEY, actor_id uuid, post_id uuid, table_name text NOT NULL,
 record_id uuid, action text NOT NULL, occurred_at timestamptz NOT NULL DEFAULT now(),
 details jsonb NOT NULL DEFAULT '{}'::jsonb
);

INSERT INTO public.register_catalog(code,label) VALUES
('consultation_generale','Registre de consultation générale'), ('cpn','Registre de consultation prénatale'), ('cpon','Registre des consultations postnatales'), ('accouchements','Registre des accouchements'), ('pf','Registre de planification familiale'), ('enfants_malades','Registre de consultation des enfants malades 0–14 ans'), ('enfants_sains','Registre des enfants sains 0–59 mois, vaccination et suivi nutritionnel'), ('cren','Registre de suivi des enfants au CREN'), ('deces','Registre de décès'), ('laboratoire','Registre d’examens de laboratoire'), ('hospitalisation','Registre d’hospitalisation')
ON CONFLICT(code) DO UPDATE SET label=EXCLUDED.label;

CREATE OR REPLACE FUNCTION public.is_admin()
RETURNS boolean LANGUAGE sql STABLE SECURITY DEFINER SET search_path = '' AS $$
 SELECT EXISTS (SELECT 1 FROM public.profiles p WHERE p.id=(SELECT auth.uid()) AND p.role='admin' AND p.is_active)
$$;
CREATE OR REPLACE FUNCTION public.current_post_id()
RETURNS uuid LANGUAGE sql STABLE SECURITY DEFINER SET search_path = '' AS $$
 SELECT p.post_id FROM public.profiles p WHERE p.id=(SELECT auth.uid()) AND p.is_active
$$;
CREATE OR REPLACE FUNCTION public.user_has_register(p_code text)
RETURNS boolean LANGUAGE sql STABLE SECURITY DEFINER SET search_path = '' AS $$
 SELECT EXISTS (SELECT 1 FROM public.user_register_access a WHERE a.user_id=(SELECT auth.uid()) AND a.register_code=p_code)
$$;
CREATE OR REPLACE FUNCTION public.can_access_register(p_code text, p_post uuid)
RETURNS boolean LANGUAGE sql STABLE SECURITY DEFINER SET search_path = '' AS $$
 SELECT public.is_admin() OR (p_post=public.current_post_id() AND public.user_has_register(p_code))
$$;

ALTER TABLE public.posts ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.register_catalog ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_register_access ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.audit_logs ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "profiles_self_or_admin_read" ON public.profiles;
CREATE POLICY "profiles_self_or_admin_read" ON public.profiles FOR SELECT TO authenticated
 USING(id=(SELECT auth.uid()) OR public.is_admin());
DROP POLICY IF EXISTS "posts_assigned_or_admin_read" ON public.posts;
CREATE POLICY "posts_assigned_or_admin_read" ON public.posts FOR SELECT TO authenticated
 USING(public.is_admin() OR id=public.current_post_id());
DROP POLICY IF EXISTS "catalog_authenticated_read" ON public.register_catalog;
CREATE POLICY "catalog_authenticated_read" ON public.register_catalog FOR SELECT TO authenticated USING(is_active);
DROP POLICY IF EXISTS "access_self_or_admin_read" ON public.user_register_access;
CREATE POLICY "access_self_or_admin_read" ON public.user_register_access FOR SELECT TO authenticated
 USING(user_id=(SELECT auth.uid()) OR public.is_admin());
DROP POLICY IF EXISTS "audit_admin_read" ON public.audit_logs;
CREATE POLICY "audit_admin_read" ON public.audit_logs FOR SELECT TO authenticated USING(public.is_admin());

CREATE TABLE IF NOT EXISTS public.reg_consultation_generale (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id uuid NOT NULL REFERENCES public.posts(id),
    created_by uuid NOT NULL REFERENCES auth.users(id),
    record_date date NOT NULL DEFAULT CURRENT_DATE,
    data jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);
ALTER TABLE public.reg_consultation_generale ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS public.reg_cpn (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id uuid NOT NULL REFERENCES public.posts(id),
    created_by uuid NOT NULL REFERENCES auth.users(id),
    record_date date NOT NULL DEFAULT CURRENT_DATE,
    data jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);
ALTER TABLE public.reg_cpn ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS public.reg_cpon (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id uuid NOT NULL REFERENCES public.posts(id),
    created_by uuid NOT NULL REFERENCES auth.users(id),
    record_date date NOT NULL DEFAULT CURRENT_DATE,
    data jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);
ALTER TABLE public.reg_cpon ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS public.reg_accouchements (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id uuid NOT NULL REFERENCES public.posts(id),
    created_by uuid NOT NULL REFERENCES auth.users(id),
    record_date date NOT NULL DEFAULT CURRENT_DATE,
    data jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);
ALTER TABLE public.reg_accouchements ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS public.reg_pf (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id uuid NOT NULL REFERENCES public.posts(id),
    created_by uuid NOT NULL REFERENCES auth.users(id),
    record_date date NOT NULL DEFAULT CURRENT_DATE,
    data jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);
ALTER TABLE public.reg_pf ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS public.reg_enfants_malades (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id uuid NOT NULL REFERENCES public.posts(id),
    created_by uuid NOT NULL REFERENCES auth.users(id),
    record_date date NOT NULL DEFAULT CURRENT_DATE,
    data jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);
ALTER TABLE public.reg_enfants_malades ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS public.reg_enfants_sains (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id uuid NOT NULL REFERENCES public.posts(id),
    created_by uuid NOT NULL REFERENCES auth.users(id),
    record_date date NOT NULL DEFAULT CURRENT_DATE,
    data jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);
ALTER TABLE public.reg_enfants_sains ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS public.reg_cren (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id uuid NOT NULL REFERENCES public.posts(id),
    created_by uuid NOT NULL REFERENCES auth.users(id),
    record_date date NOT NULL DEFAULT CURRENT_DATE,
    data jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);
ALTER TABLE public.reg_cren ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS public.reg_deces (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id uuid NOT NULL REFERENCES public.posts(id),
    created_by uuid NOT NULL REFERENCES auth.users(id),
    record_date date NOT NULL DEFAULT CURRENT_DATE,
    data jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);
ALTER TABLE public.reg_deces ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS public.reg_laboratoire (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id uuid NOT NULL REFERENCES public.posts(id),
    created_by uuid NOT NULL REFERENCES auth.users(id),
    record_date date NOT NULL DEFAULT CURRENT_DATE,
    data jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);
ALTER TABLE public.reg_laboratoire ENABLE ROW LEVEL SECURITY;

CREATE TABLE IF NOT EXISTS public.reg_hospitalisation (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    post_id uuid NOT NULL REFERENCES public.posts(id),
    created_by uuid NOT NULL REFERENCES auth.users(id),
    record_date date NOT NULL DEFAULT CURRENT_DATE,
    data jsonb NOT NULL DEFAULT '{}'::jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);
ALTER TABLE public.reg_hospitalisation ENABLE ROW LEVEL SECURITY;


DROP POLICY IF EXISTS "consultation_generale_select_scope" ON public.reg_consultation_generale;
CREATE POLICY "consultation_generale_select_scope" ON public.reg_consultation_generale
FOR SELECT TO authenticated USING (public.can_access_register('consultation_generale', post_id));
DROP POLICY IF EXISTS "consultation_generale_insert_scope" ON public.reg_consultation_generale;
CREATE POLICY "consultation_generale_insert_scope" ON public.reg_consultation_generale
FOR INSERT TO authenticated WITH CHECK (
  created_by = (SELECT auth.uid()) AND public.can_access_register('consultation_generale', post_id)
);
DROP POLICY IF EXISTS "consultation_generale_update_scope" ON public.reg_consultation_generale;
CREATE POLICY "consultation_generale_update_scope" ON public.reg_consultation_generale
FOR UPDATE TO authenticated USING (
  public.is_admin() OR (post_id = public.current_post_id() AND created_by = (SELECT auth.uid()) AND public.user_has_register('consultation_generale'))
) WITH CHECK (
  public.is_admin() OR (post_id = public.current_post_id() AND created_by = (SELECT auth.uid()) AND public.user_has_register('consultation_generale'))
);


DROP POLICY IF EXISTS "cpn_select_scope" ON public.reg_cpn;
CREATE POLICY "cpn_select_scope" ON public.reg_cpn
FOR SELECT TO authenticated USING (public.can_access_register('cpn', post_id));
DROP POLICY IF EXISTS "cpn_insert_scope" ON public.reg_cpn;
CREATE POLICY "cpn_insert_scope" ON public.reg_cpn
FOR INSERT TO authenticated WITH CHECK (
  created_by = (SELECT auth.uid()) AND public.can_access_register('cpn', post_id)
);
DROP POLICY IF EXISTS "cpn_update_scope" ON public.reg_cpn;
CREATE POLICY "cpn_update_scope" ON public.reg_cpn
FOR UPDATE TO authenticated USING (
  public.is_admin() OR (post_id = public.current_post_id() AND created_by = (SELECT auth.uid()) AND public.user_has_register('cpn'))
) WITH CHECK (
  public.is_admin() OR (post_id = public.current_post_id() AND created_by = (SELECT auth.uid()) AND public.user_has_register('cpn'))
);


DROP POLICY IF EXISTS "cpon_select_scope" ON public.reg_cpon;
CREATE POLICY "cpon_select_scope" ON public.reg_cpon
FOR SELECT TO authenticated USING (public.can_access_register('cpon', post_id));
DROP POLICY IF EXISTS "cpon_insert_scope" ON public.reg_cpon;
CREATE POLICY "cpon_insert_scope" ON public.reg_cpon
FOR INSERT TO authenticated WITH CHECK (
  created_by = (SELECT auth.uid()) AND public.can_access_register('cpon', post_id)
);
DROP POLICY IF EXISTS "cpon_update_scope" ON public.reg_cpon;
CREATE POLICY "cpon_update_scope" ON public.reg_cpon
FOR UPDATE TO authenticated USING (
  public.is_admin() OR (post_id = public.current_post_id() AND created_by = (SELECT auth.uid()) AND public.user_has_register('cpon'))
) WITH CHECK (
  public.is_admin() OR (post_id = public.current_post_id() AND created_by = (SELECT auth.uid()) AND public.user_has_register('cpon'))
);


DROP POLICY IF EXISTS "accouchements_select_scope" ON public.reg_accouchements;
CREATE POLICY "accouchements_select_scope" ON public.reg_accouchements
FOR SELECT TO authenticated USING (public.can_access_register('accouchements', post_id));
DROP POLICY IF EXISTS "accouchements_insert_scope" ON public.reg_accouchements;
CREATE POLICY "accouchements_insert_scope" ON public.reg_accouchements
FOR INSERT TO authenticated WITH CHECK (
  created_by = (SELECT auth.uid()) AND public.can_access_register('accouchements', post_id)
);
DROP POLICY IF EXISTS "accouchements_update_scope" ON public.reg_accouchements;
CREATE POLICY "accouchements_update_scope" ON public.reg_accouchements
FOR UPDATE TO authenticated USING (
  public.is_admin() OR (post_id = public.current_post_id() AND created_by = (SELECT auth.uid()) AND public.user_has_register('accouchements'))
) WITH CHECK (
  public.is_admin() OR (post_id = public.current_post_id() AND created_by = (SELECT auth.uid()) AND public.user_has_register('accouchements'))
);


DROP POLICY IF EXISTS "pf_select_scope" ON public.reg_pf;
CREATE POLICY "pf_select_scope" ON public.reg_pf
FOR SELECT TO authenticated USING (public.can_access_register('pf', post_id));
DROP POLICY IF EXISTS "pf_insert_scope" ON public.reg_pf;
CREATE POLICY "pf_insert_scope" ON public.reg_pf
FOR INSERT TO authenticated WITH CHECK (
  created_by = (SELECT auth.uid()) AND public.can_access_register('pf', post_id)
);
DROP POLICY IF EXISTS "pf_update_scope" ON public.reg_pf;
CREATE POLICY "pf_update_scope" ON public.reg_pf
FOR UPDATE TO authenticated USING (
  public.is_admin() OR (post_id = public.current_post_id() AND created_by = (SELECT auth.uid()) AND public.user_has_register('pf'))
) WITH CHECK (
  public.is_admin() OR (post_id = public.current_post_id() AND created_by = (SELECT auth.uid()) AND public.user_has_register('pf'))
);


DROP POLICY IF EXISTS "enfants_malades_select_scope" ON public.reg_enfants_malades;
CREATE POLICY "enfants_malades_select_scope" ON public.reg_enfants_malades
FOR SELECT TO authenticated USING (public.can_access_register('enfants_malades', post_id));
DROP POLICY IF EXISTS "enfants_malades_insert_scope" ON public.reg_enfants_malades;
CREATE POLICY "enfants_malades_insert_scope" ON public.reg_enfants_malades
FOR INSERT TO authenticated WITH CHECK (
  created_by = (SELECT auth.uid()) AND public.can_access_register('enfants_malades', post_id)
);
DROP POLICY IF EXISTS "enfants_malades_update_scope" ON public.reg_enfants_malades;
CREATE POLICY "enfants_malades_update_scope" ON public.reg_enfants_malades
FOR UPDATE TO authenticated USING (
  public.is_admin() OR (post_id = public.current_post_id() AND created_by = (SELECT auth.uid()) AND public.user_has_register('enfants_malades'))
) WITH CHECK (
  public.is_admin() OR (post_id = public.current_post_id() AND created_by = (SELECT auth.uid()) AND public.user_has_register('enfants_malades'))
);


DROP POLICY IF EXISTS "enfants_sains_select_scope" ON public.reg_enfants_sains;
CREATE POLICY "enfants_sains_select_scope" ON public.reg_enfants_sains
FOR SELECT TO authenticated USING (public.can_access_register('enfants_sains', post_id));
DROP POLICY IF EXISTS "enfants_sains_insert_scope" ON public.reg_enfants_sains;
CREATE POLICY "enfants_sains_insert_scope" ON public.reg_enfants_sains
FOR INSERT TO authenticated WITH CHECK (
  created_by = (SELECT auth.uid()) AND public.can_access_register('enfants_sains', post_id)
);
DROP POLICY IF EXISTS "enfants_sains_update_scope" ON public.reg_enfants_sains;
CREATE POLICY "enfants_sains_update_scope" ON public.reg_enfants_sains
FOR UPDATE TO authenticated USING (
  public.is_admin() OR (post_id = public.current_post_id() AND created_by = (SELECT auth.uid()) AND public.user_has_register('enfants_sains'))
) WITH CHECK (
  public.is_admin() OR (post_id = public.current_post_id() AND created_by = (SELECT auth.uid()) AND public.user_has_register('enfants_sains'))
);


DROP POLICY IF EXISTS "cren_select_scope" ON public.reg_cren;
CREATE POLICY "cren_select_scope" ON public.reg_cren
FOR SELECT TO authenticated USING (public.can_access_register('cren', post_id));
DROP POLICY IF EXISTS "cren_insert_scope" ON public.reg_cren;
CREATE POLICY "cren_insert_scope" ON public.reg_cren
FOR INSERT TO authenticated WITH CHECK (
  created_by = (SELECT auth.uid()) AND public.can_access_register('cren', post_id)
);
DROP POLICY IF EXISTS "cren_update_scope" ON public.reg_cren;
CREATE POLICY "cren_update_scope" ON public.reg_cren
FOR UPDATE TO authenticated USING (
  public.is_admin() OR (post_id = public.current_post_id() AND created_by = (SELECT auth.uid()) AND public.user_has_register('cren'))
) WITH CHECK (
  public.is_admin() OR (post_id = public.current_post_id() AND created_by = (SELECT auth.uid()) AND public.user_has_register('cren'))
);


DROP POLICY IF EXISTS "deces_select_scope" ON public.reg_deces;
CREATE POLICY "deces_select_scope" ON public.reg_deces
FOR SELECT TO authenticated USING (public.can_access_register('deces', post_id));
DROP POLICY IF EXISTS "deces_insert_scope" ON public.reg_deces;
CREATE POLICY "deces_insert_scope" ON public.reg_deces
FOR INSERT TO authenticated WITH CHECK (
  created_by = (SELECT auth.uid()) AND public.can_access_register('deces', post_id)
);
DROP POLICY IF EXISTS "deces_update_scope" ON public.reg_deces;
CREATE POLICY "deces_update_scope" ON public.reg_deces
FOR UPDATE TO authenticated USING (
  public.is_admin() OR (post_id = public.current_post_id() AND created_by = (SELECT auth.uid()) AND public.user_has_register('deces'))
) WITH CHECK (
  public.is_admin() OR (post_id = public.current_post_id() AND created_by = (SELECT auth.uid()) AND public.user_has_register('deces'))
);


DROP POLICY IF EXISTS "laboratoire_select_scope" ON public.reg_laboratoire;
CREATE POLICY "laboratoire_select_scope" ON public.reg_laboratoire
FOR SELECT TO authenticated USING (public.can_access_register('laboratoire', post_id));
DROP POLICY IF EXISTS "laboratoire_insert_scope" ON public.reg_laboratoire;
CREATE POLICY "laboratoire_insert_scope" ON public.reg_laboratoire
FOR INSERT TO authenticated WITH CHECK (
  created_by = (SELECT auth.uid()) AND public.can_access_register('laboratoire', post_id)
);
DROP POLICY IF EXISTS "laboratoire_update_scope" ON public.reg_laboratoire;
CREATE POLICY "laboratoire_update_scope" ON public.reg_laboratoire
FOR UPDATE TO authenticated USING (
  public.is_admin() OR (post_id = public.current_post_id() AND created_by = (SELECT auth.uid()) AND public.user_has_register('laboratoire'))
) WITH CHECK (
  public.is_admin() OR (post_id = public.current_post_id() AND created_by = (SELECT auth.uid()) AND public.user_has_register('laboratoire'))
);


DROP POLICY IF EXISTS "hospitalisation_select_scope" ON public.reg_hospitalisation;
CREATE POLICY "hospitalisation_select_scope" ON public.reg_hospitalisation
FOR SELECT TO authenticated USING (public.can_access_register('hospitalisation', post_id));
DROP POLICY IF EXISTS "hospitalisation_insert_scope" ON public.reg_hospitalisation;
CREATE POLICY "hospitalisation_insert_scope" ON public.reg_hospitalisation
FOR INSERT TO authenticated WITH CHECK (
  created_by = (SELECT auth.uid()) AND public.can_access_register('hospitalisation', post_id)
);
DROP POLICY IF EXISTS "hospitalisation_update_scope" ON public.reg_hospitalisation;
CREATE POLICY "hospitalisation_update_scope" ON public.reg_hospitalisation
FOR UPDATE TO authenticated USING (
  public.is_admin() OR (post_id = public.current_post_id() AND created_by = (SELECT auth.uid()) AND public.user_has_register('hospitalisation'))
) WITH CHECK (
  public.is_admin() OR (post_id = public.current_post_id() AND created_by = (SELECT auth.uid()) AND public.user_has_register('hospitalisation'))
);


-- Triggers d'audit minimaux sur les enregistrements (les détails médicaux ne sont pas copiés dans le journal).
CREATE OR REPLACE FUNCTION public.log_register_change()
RETURNS trigger LANGUAGE plpgsql SECURITY DEFINER SET search_path = '' AS $$
DECLARE rid uuid; pid uuid; act text;
BEGIN
 IF TG_OP='DELETE' THEN rid:=OLD.id; pid:=OLD.post_id; act:='DELETE';
 ELSE rid:=NEW.id; pid:=NEW.post_id; act:=TG_OP; END IF;
 INSERT INTO public.audit_logs(actor_id,post_id,table_name,record_id,action)
 VALUES ((SELECT auth.uid()),pid,TG_TABLE_NAME,rid,act);
 IF TG_OP='DELETE' THEN RETURN OLD; ELSE RETURN NEW; END IF;
END; $$;

DROP TRIGGER IF EXISTS audit_reg_consultation_generale ON public.reg_consultation_generale;
CREATE TRIGGER audit_reg_consultation_generale AFTER INSERT OR UPDATE OR DELETE ON public.reg_consultation_generale
FOR EACH ROW EXECUTE FUNCTION public.log_register_change();

DROP TRIGGER IF EXISTS audit_reg_cpn ON public.reg_cpn;
CREATE TRIGGER audit_reg_cpn AFTER INSERT OR UPDATE OR DELETE ON public.reg_cpn
FOR EACH ROW EXECUTE FUNCTION public.log_register_change();

DROP TRIGGER IF EXISTS audit_reg_cpon ON public.reg_cpon;
CREATE TRIGGER audit_reg_cpon AFTER INSERT OR UPDATE OR DELETE ON public.reg_cpon
FOR EACH ROW EXECUTE FUNCTION public.log_register_change();

DROP TRIGGER IF EXISTS audit_reg_accouchements ON public.reg_accouchements;
CREATE TRIGGER audit_reg_accouchements AFTER INSERT OR UPDATE OR DELETE ON public.reg_accouchements
FOR EACH ROW EXECUTE FUNCTION public.log_register_change();

DROP TRIGGER IF EXISTS audit_reg_pf ON public.reg_pf;
CREATE TRIGGER audit_reg_pf AFTER INSERT OR UPDATE OR DELETE ON public.reg_pf
FOR EACH ROW EXECUTE FUNCTION public.log_register_change();

DROP TRIGGER IF EXISTS audit_reg_enfants_malades ON public.reg_enfants_malades;
CREATE TRIGGER audit_reg_enfants_malades AFTER INSERT OR UPDATE OR DELETE ON public.reg_enfants_malades
FOR EACH ROW EXECUTE FUNCTION public.log_register_change();

DROP TRIGGER IF EXISTS audit_reg_enfants_sains ON public.reg_enfants_sains;
CREATE TRIGGER audit_reg_enfants_sains AFTER INSERT OR UPDATE OR DELETE ON public.reg_enfants_sains
FOR EACH ROW EXECUTE FUNCTION public.log_register_change();

DROP TRIGGER IF EXISTS audit_reg_cren ON public.reg_cren;
CREATE TRIGGER audit_reg_cren AFTER INSERT OR UPDATE OR DELETE ON public.reg_cren
FOR EACH ROW EXECUTE FUNCTION public.log_register_change();

DROP TRIGGER IF EXISTS audit_reg_deces ON public.reg_deces;
CREATE TRIGGER audit_reg_deces AFTER INSERT OR UPDATE OR DELETE ON public.reg_deces
FOR EACH ROW EXECUTE FUNCTION public.log_register_change();

DROP TRIGGER IF EXISTS audit_reg_laboratoire ON public.reg_laboratoire;
CREATE TRIGGER audit_reg_laboratoire AFTER INSERT OR UPDATE OR DELETE ON public.reg_laboratoire
FOR EACH ROW EXECUTE FUNCTION public.log_register_change();

DROP TRIGGER IF EXISTS audit_reg_hospitalisation ON public.reg_hospitalisation;
CREATE TRIGGER audit_reg_hospitalisation AFTER INSERT OR UPDATE OR DELETE ON public.reg_hospitalisation
FOR EACH ROW EXECUTE FUNCTION public.log_register_change();

-- Aucun accès direct INSERT/UPDATE/DELETE aux tables de référence pour authenticated.
-- Le provisionnement (comptes, postes, affectations) est effectué par bootstrap.py / app admin
-- avec la clé serveur conservée exclusivement côté serveur.
REVOKE ALL ON FUNCTION public.is_admin() FROM PUBLIC;
GRANT EXECUTE ON FUNCTION public.is_admin() TO authenticated;
REVOKE ALL ON FUNCTION public.current_post_id() FROM PUBLIC;
GRANT EXECUTE ON FUNCTION public.current_post_id() TO authenticated;
REVOKE ALL ON FUNCTION public.user_has_register(text) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION public.user_has_register(text) TO authenticated;
REVOKE ALL ON FUNCTION public.can_access_register(text,uuid) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION public.can_access_register(text,uuid) TO authenticated;


-- Droits SQL explicites requis par l'API PostgREST.
GRANT USAGE ON SCHEMA public TO authenticated;
GRANT SELECT ON public.posts, public.profiles, public.register_catalog, public.user_register_access, public.audit_logs TO authenticated;
GRANT SELECT, INSERT, UPDATE ON public.reg_consultation_generale TO authenticated;
GRANT SELECT, INSERT, UPDATE ON public.reg_cpn TO authenticated;
GRANT SELECT, INSERT, UPDATE ON public.reg_cpon TO authenticated;
GRANT SELECT, INSERT, UPDATE ON public.reg_accouchements TO authenticated;
GRANT SELECT, INSERT, UPDATE ON public.reg_pf TO authenticated;
GRANT SELECT, INSERT, UPDATE ON public.reg_enfants_malades TO authenticated;
GRANT SELECT, INSERT, UPDATE ON public.reg_enfants_sains TO authenticated;
GRANT SELECT, INSERT, UPDATE ON public.reg_cren TO authenticated;
GRANT SELECT, INSERT, UPDATE ON public.reg_deces TO authenticated;
GRANT SELECT, INSERT, UPDATE ON public.reg_laboratoire TO authenticated;
GRANT SELECT, INSERT, UPDATE ON public.reg_hospitalisation TO authenticated;
