import os
from datetime import date
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client
from register_definitions import REGISTERS

load_dotenv()
st.set_page_config(page_title="Registres Santé", page_icon="🩺", layout="wide")
URL=os.getenv("SUPABASE_URL"); ANON=os.getenv("SUPABASE_ANON_KEY")
if not URL or not ANON:
    st.error("SUPABASE_URL et SUPABASE_ANON_KEY doivent être renseignées dans .env")
    st.stop()

# Un client par session Streamlit : ne jamais partager le client authentifié entre agents.
def get_client():
    if "sb_client" not in st.session_state:
        st.session_state.sb_client=create_client(URL, ANON)
    c=st.session_state.sb_client
    tokens=st.session_state.get("tokens")
    if tokens:
        try: c.auth.set_session(tokens["access_token"],tokens["refresh_token"])
        except Exception: pass
    return c

sb=get_client()

def logout():
    try: sb.auth.sign_out()
    except Exception: pass
    for k in ["tokens","user_id","sb_client"]: st.session_state.pop(k,None)
    st.rerun()

def admin_client():
    key=os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    if not key: raise RuntimeError("Clé serveur absente. Configure SUPABASE_SERVICE_ROLE_KEY dans .env.")
    return create_client(URL,key)

def current_profile(uid):
    return sb.table("profiles").select("id,display_name,role,post_id,is_active").eq("id",uid).single().execute().data

def render_field(f):
    label=f["label"]; key=f["key"]; typ=f.get("type","text")
    if typ=="textarea": return st.text_area(label,key="field_"+key)
    if typ=="number": return st.number_input(label,min_value=0.0,value=0.0,step=1.0,key="field_"+key)
    if typ=="date": return st.date_input(label,value=date.today(),key="field_"+key).isoformat()
    if typ=="select": return st.selectbox(label,f.get("options",[]),key="field_"+key)
    if typ=="checkbox": return st.checkbox(label,key="field_"+key)
    return st.text_input(label,key="field_"+key)

def create_agent(admin, email, password, name, post_id, selected_registers):
    created=admin.auth.admin.create_user({"email":email,"password":password,"email_confirm":True,"user_metadata":{"display_name":name}})
    uid=created.user.id
    admin.table("profiles").upsert({"id":uid,"display_name":name,"role":"agent","post_id":post_id,"is_active":True}).execute()
    for code in selected_registers:
        admin.table("user_register_access").upsert({"user_id":uid,"register_code":code}).execute()
    return uid

st.title("🩺 Registres numériques de santé")
st.caption("Plateforme de saisie par poste — formulaires séparés selon les registres PDF de référence.")
if not st.session_state.get("user_id"):
    with st.form("login"):
        st.subheader("Connexion")
        email=st.text_input("Adresse e-mail")
        password=st.text_input("Mot de passe",type="password")
        go=st.form_submit_button("Se connecter",use_container_width=True)
    if go:
        try:
            res=sb.auth.sign_in_with_password({"email":email,"password":password})
            st.session_state.user_id=res.user.id
            st.session_state.tokens={"access_token":res.session.access_token,"refresh_token":res.session.refresh_token}
            st.rerun()
        except Exception: st.error("Connexion échouée. Vérifie l'adresse e-mail et le mot de passe.")
    st.stop()

uid=st.session_state.user_id
try: profile=current_profile(uid)
except Exception: profile=None
if not profile or not profile.get("is_active"):
    st.error("Profil absent ou désactivé. Contacte l'administrateur.")
    st.button("Déconnexion",on_click=logout); st.stop()
st.sidebar.write("**Connecté :** "+(profile.get("display_name") or "Utilisateur"))
st.sidebar.write("**Rôle :** "+profile["role"])
st.sidebar.button("Déconnexion",on_click=logout)

if profile["role"]=="admin":
    st.header("Administration générale")
    t1,t2,t3,t4=st.tabs(["Vue globale","Postes de santé","Utilisateurs","Données / registres"])
    with t1:
        cols=st.columns(3)
        try:
            posts=admin_client().table("posts").select("id",count="exact").execute()
            cols[0].metric("Postes",posts.count or 0)
            users=admin_client().table("profiles").select("id",count="exact").execute()
            cols[1].metric("Comptes",users.count or 0)
            total=0
            for code in REGISTERS:
                x=admin_client().table("reg_"+code).select("id",count="exact").execute(); total += x.count or 0
            cols[2].metric("Saisies",total)
        except Exception as e: st.warning("Statistiques indisponibles : "+str(e))
        st.info("Les tableaux de bord détaillés seront calculés à partir des données validées de chaque registre.")
    with t2:
        st.subheader("Créer un poste")
        with st.form("create_post"):
            pname=st.text_input("Nom du poste")
            district=st.text_input("District sanitaire")
            address=st.text_area("Adresse")
            save=st.form_submit_button("Créer le poste")
        if save:
            try:
                admin_client().table("posts").insert({"name":pname,"district":district,"address":address}).execute()
                st.success("Poste créé."); st.rerun()
            except Exception as e: st.error("Création impossible : "+str(e))
        try: st.dataframe(pd.DataFrame(admin_client().table("posts").select("id,name,district,address,is_active,created_at").execute().data),use_container_width=True)
        except Exception as e: st.warning(str(e))
    with t3:
        st.subheader("Créer un agent et attribuer ses droits")
        try: post_rows=admin_client().table("posts").select("id,name").eq("is_active",True).execute().data
        except Exception: post_rows=[]
        if not post_rows: st.info("Crée d'abord au moins un poste.")
        else:
            post_labels={p["name"]:p["id"] for p in post_rows}
            with st.form("create_agent"):
                a_email=st.text_input("E-mail de l'agent")
                a_name=st.text_input("Nom affiché")
                a_pass=st.text_input("Mot de passe provisoire (14 caractères minimum)",type="password")
                post_name=st.selectbox("Poste affecté",list(post_labels))
                selected=st.multiselect("Registres autorisés",[c for c in REGISTERS],format_func=lambda c:REGISTERS[c]["label"])
                create=st.form_submit_button("Créer le compte agent")
            if create:
                if len(a_pass)<14: st.error("Le mot de passe doit contenir au moins 14 caractères.")
                elif not selected: st.error("Sélectionne au moins un registre.")
                else:
                    try:
                        create_agent(admin_client(),a_email,a_pass,a_name,post_labels[post_name],selected)
                        st.success("Compte agent créé et droits attribués.")
                    except Exception as e: st.error("Création du compte impossible : "+str(e))
        st.caption("Les comptes et droits sont gérés côté serveur avec la clé secrète, jamais exposée dans le navigateur.")
        try:
            data=admin_client().table("profiles").select("id,display_name,role,post_id,is_active,created_at").execute().data
            st.dataframe(pd.DataFrame(data),use_container_width=True)
        except Exception as e: st.warning(str(e))
    with t4:
        st.subheader("Registres disponibles")
        st.dataframe(pd.DataFrame([{"Code":k,"Registre":v["label"],"Champs":len(v["fields"])} for k,v in REGISTERS.items()]),use_container_width=True)
        st.caption("Chaque registre dispose de sa propre table reg_<code> et de ses propres champs de formulaire.")
else:
    if not profile.get("post_id"):
        st.error("Ton compte n'est associé à aucun poste."); st.stop()
    try:
        allowed=sb.table("user_register_access").select("register_code").eq("user_id",uid).execute().data
        codes=[x["register_code"] for x in allowed if x["register_code"] in REGISTERS]
    except Exception: codes=[]
    if not codes: st.warning("Aucun registre ne t'a été attribué. Contacte l'administrateur."); st.stop()
    st.header("Espace de saisie — Mon poste")
    code=st.selectbox("Choisir le registre",codes,format_func=lambda c:REGISTERS[c]["label"])
    spec=REGISTERS[code]
    st.subheader(spec["label"])
    st.caption("Les champs ci-dessous sont spécifiques à ce registre. Respecte les instructions officielles de remplissage.")
    with st.form("entry_"+code,clear_on_submit=True):
        record_date=st.date_input("Date de l'activité",value=date.today())
        payload={}
        for f in spec["fields"]:
            payload[f["key"]]=render_field(f)
        submitted=st.form_submit_button("Enregistrer la fiche",use_container_width=True)
    if submitted:
        try:
            sb.table("reg_"+code).insert({"post_id":profile["post_id"],"created_by":uid,"record_date":record_date.isoformat(),"data":payload}).execute()
            st.success("Fiche enregistrée.")
        except Exception as e: st.error("Enregistrement refusé. Vérifie tes droits et ta connexion. Détail : "+str(e))
    st.divider(); st.subheader("Historique de mon registre")
    try:
        rows=sb.table("reg_"+code).select("id,record_date,data,created_at").eq("post_id",profile["post_id"]).order("record_date",desc=True).limit(100).execute().data
        if rows:
            view=[]
            for r in rows:
                d={"Date":r["record_date"],"ID":r["id"][:8]}
                d.update({f["label"]:r.get("data",{}).get(f["key"],"") for f in spec["fields"]})
                view.append(d)
            st.dataframe(pd.DataFrame(view),use_container_width=True)
            csv=pd.DataFrame(view).to_csv(index=False).encode("utf-8-sig")
            st.download_button("Exporter les lignes visibles en CSV",csv,file_name=f"{code}.csv",mime="text/csv")
        else: st.info("Aucune fiche enregistrée pour ce registre.")
    except Exception as e: st.warning("Historique indisponible : "+str(e))
