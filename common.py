import os
from datetime import date
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client
from register_definitions import REGISTERS

load_dotenv(override=True)

URL = os.getenv("SUPABASE_URL")
ANON = os.getenv("SUPABASE_ANON_KEY")
ROLES = {
    "admin": "ADMIN",
    "chef_programme": "CHEF DE PROGRAMME",
    "chef_poste": "CHEF DE POSTE",
    "agent_programme": "AGENT PAR PROGRAMME",
}

def get_client():
    if not URL or not ANON:
        st.error("SUPABASE_URL et SUPABASE_ANON_KEY doivent être renseignées dans .env")
        st.stop()
    if "sb_client" not in st.session_state:
        st.session_state.sb_client = create_client(URL, ANON)
    client = st.session_state.sb_client
    tokens = st.session_state.get("tokens")
    if tokens:
        try:
            client.auth.set_session(tokens["access_token"], tokens["refresh_token"])
        except Exception:
            for key in ("tokens", "user_id", "sb_client"):
                st.session_state.pop(key, None)
            st.warning("Session expirée. Veuillez vous reconnecter.")
            st.stop()
    return client

def admin_client():
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    if not URL or not key:
        raise RuntimeError("SUPABASE_URL ou SUPABASE_SERVICE_ROLE_KEY absente du fichier .env")
    # Utilisé uniquement côté serveur Streamlit. Ne jamais exposer cette clé au navigateur.
    return create_client(URL, key)

def logout():
    try:
        get_client().auth.sign_out()
    except Exception:
        pass
    for key in ("tokens", "user_id", "sb_client"):
        st.session_state.pop(key, None)
    st.rerun()

def get_profile(client):
    uid = st.session_state.get("user_id")
    if not uid:
        return None
    try:
        result = client.table("profiles").select(
            "id,display_name,role,post_id,program_id,is_active"
        ).eq("id", uid).single().execute()
        return result.data
    except Exception:
        return None

def require_role(allowed_roles):
    client = get_client()
    profile = get_profile(client)
    if not profile or not profile.get("is_active"):
        st.error("Profil absent ou désactivé. Contactez l’administrateur.")
        st.button("Déconnexion", on_click=logout)
        st.stop()
    st.sidebar.write("**Connecté :** " + (profile.get("display_name") or "Utilisateur"))
    st.sidebar.write("**Rôle :** " + ROLES.get(profile.get("role"), "Inconnu"))
    st.sidebar.button("Déconnexion", on_click=logout, key="logout_" + "_".join(allowed_roles))
    if profile.get("role") not in allowed_roles:
        st.error("Vous n’êtes pas autorisé à accéder à cet espace.")
        st.stop()
    return client, profile

def fetch_records(client, code, post_id=None, limit=5000):
    if code not in REGISTERS:
        raise ValueError("Code de registre inconnu.")
    query = client.table("reg_" + code).select(
        "id,post_id,created_by,record_date,data,created_at"
    ).order("record_date", desc=True).limit(limit)
    if post_id:
        query = query.eq("post_id", post_id)
    return query.execute().data or []

def record_view(row, spec, post_names=None):
    data = row.get("data") or {}
    result = {
        "ID": str(row.get("id", "")),
        "Date": str(row.get("record_date", "")),
        "Poste": (post_names or {}).get(row.get("post_id"), str(row.get("post_id", ""))),
        "Créé par": str(row.get("created_by", "")),
        "Créé le": str(row.get("created_at", "")),
    }
    for field in spec["fields"]:
        result[field["label"]] = data.get(field["key"], "")
    return result

def render_field(field, prefix, existing=None):
    key, label = field["key"], field["label"]
    value = (existing or {}).get(key)
    kind = field.get("type", "text")
    widget_key = f"{prefix}_{key}"
    if kind == "textarea":
        return st.text_area(label, value=str(value or ""), key=widget_key)
    if kind == "number":
        try:
            number = float(value) if value not in (None, "") else 0.0
        except (TypeError, ValueError):
            number = 0.0
        return st.number_input(label, min_value=0.0, value=number, step=1.0, key=widget_key)
    if kind == "date":
        try:
            default = date.fromisoformat(str(value)) if value else date.today()
        except ValueError:
            default = date.today()
        return st.date_input(label, value=default, key=widget_key).isoformat()
    if kind == "select":
        options = field.get("options", [])
        if options:
            return st.selectbox(label, options, index=options.index(value) if value in options else 0, key=widget_key)
    if kind == "checkbox":
        return st.checkbox(label, value=bool(value), key=widget_key)
    return st.text_input(label, value=str(value or ""), key=widget_key)

def record_form(client, code, spec, profile, existing=None, form_key="record_form"):
    existing = existing or {}
    old_data = existing.get("data") or {}
    try:
        default_date = date.fromisoformat(str(existing.get("record_date"))) if existing.get("record_date") else date.today()
    except ValueError:
        default_date = date.today()
    with st.form(form_key):
        record_date = st.date_input("Date de l’activité", value=default_date, key=form_key + "_date")
        payload = {field["key"]: render_field(field, form_key, old_data) for field in spec["fields"]}
        submitted = st.form_submit_button(
            "Mettre à jour la fiche" if existing.get("id") else "Enregistrer la fiche",
            use_container_width=True,
        )
    if submitted:
        values = {
            "post_id": profile["post_id"],
            "created_by": existing.get("created_by") or st.session_state.user_id,
            "record_date": record_date.isoformat(),
            "data": payload,
        }
        try:
            table = client.table("reg_" + code)
            if existing.get("id"):
                table.update(values).eq("id", existing["id"]).eq("post_id", profile["post_id"]).execute()
            else:
                table.insert(values).execute()
            st.success("Fiche enregistrée avec succès.")
            st.rerun()
        except Exception as exc:
            st.error("Enregistrement impossible : " + str(exc))

def read_only_registers(client, title, codes, post_id=None, post_names=None):
    st.header(title)
    codes = [code for code in codes if code in REGISTERS]
    if not codes:
        st.info("Aucun registre n’est associé à votre périmètre.")
        return
    code = st.selectbox(
        "Registre à consulter", codes,
        format_func=lambda value: REGISTERS[value]["label"],
        key=title + "_code",
    )
    try:
        rows = fetch_records(client, code, post_id=post_id)
        if rows:
            frame = pd.DataFrame([record_view(row, REGISTERS[code], post_names) for row in rows])
            st.metric("Nombre de fiches affichées", len(frame))
            st.dataframe(frame, use_container_width=True, hide_index=True)
            st.download_button(
                "Exporter en CSV", frame.to_csv(index=False).encode("utf-8-sig"),
                file_name=f"{code}_consultation.csv", mime="text/csv",
            )
        else:
            st.info("Aucune fiche trouvée pour ce registre.")
    except Exception as exc:
        st.error("Lecture des fiches impossible : " + str(exc))

def agent_workspace(client, profile):
    if not profile.get("post_id") or not profile.get("program_id"):
        st.error("Votre compte doit être associé à un poste de santé et à un programme.")
        return
    try:
        assigned = client.table("user_register_access").select("register_code").eq(
            "user_id", st.session_state.user_id
        ).execute().data or []
        programme_links = admin_client().table("program_register_access").select(
            "register_code"
        ).eq("program_id", profile["program_id"]).execute().data or []
        programme_codes = {item["register_code"] for item in programme_links}
        codes = [
            item["register_code"] for item in assigned
            if item["register_code"] in REGISTERS and item["register_code"] in programme_codes
        ]
    except Exception as exc:
        st.error("Impossible de charger vos autorisations : " + str(exc))
        return
    if not codes:
        st.warning("Aucun registre ne vous a été attribué pour ce programme. Contactez l’administrateur.")
        return
    st.header("Espace de saisie — Mon poste et mon programme")
    code = st.selectbox("Choisir le registre", codes, format_func=lambda c: REGISTERS[c]["label"])
    spec = REGISTERS[code]
    st.subheader("Créer une fiche")
    record_form(client, code, spec, profile, form_key="agent_create_" + code)
    st.divider()
    st.subheader("Consulter, modifier ou supprimer mes fiches")
    try:
        rows = fetch_records(client, code, post_id=profile["post_id"], limit=500)
        if not rows:
            st.info("Aucune fiche enregistrée pour ce registre.")
            return
        display = []
        for row in rows:
            data = row.get("data") or {}
            item = {"ID": str(row["id"])[:8], "Date": row.get("record_date", "")}
            item.update({field["label"]: data.get(field["key"], "") for field in spec["fields"]})
            display.append(item)
        st.dataframe(pd.DataFrame(display), use_container_width=True, hide_index=True)
        choices = {f"{row.get('record_date')} — {str(row['id'])[:8]}": row for row in rows}
        selected = choices[st.selectbox("Fiche à modifier ou supprimer", list(choices), key="agent_select_" + code)]
        with st.expander("Modifier cette fiche"):
            record_form(client, code, spec, profile, selected, "agent_edit_" + str(selected["id"]))
        with st.expander("Supprimer cette fiche"):
            confirm = st.checkbox("Je confirme la suppression définitive", key="agent_confirm_" + str(selected["id"]))
            if st.button("Supprimer cette fiche", disabled=not confirm, key="agent_delete_" + str(selected["id"])):
                try:
                    client.table("reg_" + code).delete().eq("id", selected["id"]).eq(
                        "post_id", profile["post_id"]
                    ).execute()
                    st.success("Fiche supprimée.")
                    st.rerun()
                except Exception as exc:
                    st.error("Suppression impossible. Vérifiez les politiques RLS : " + str(exc))
    except Exception as exc:
        st.error("Historique indisponible : " + str(exc))
