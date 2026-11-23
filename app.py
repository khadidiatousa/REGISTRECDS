import streamlit as st
from common import get_client, get_profile, logout, ROLES

st.set_page_config(
    page_title="Registres numériques de santé",
    page_icon="🩺",
    layout="wide",
)

def afficher_connexion(client):
    st.title("🩺 Registres numériques de santé")
    st.caption("Plateforme de gestion et de suivi des registres des postes de santé.")
    with st.form("login_form"):
        st.subheader("Connexion")
        email = st.text_input("Adresse e-mail")
        password = st.text_input("Mot de passe", type="password")
        submitted = st.form_submit_button("Se connecter", use_container_width=True)
    if submitted:
        try:
            result = client.auth.sign_in_with_password({
                "email": email.strip(),
                "password": password,
            })
            st.session_state.user_id = result.user.id
            st.session_state.tokens = {
                "access_token": result.session.access_token,
                "refresh_token": result.session.refresh_token,
            }
            st.success("Connexion réussie.")
            st.rerun()
        except Exception:
            st.error("Connexion échouée. Vérifiez votre adresse e-mail et votre mot de passe.")

client = get_client()

# Sans session, ne pas afficher de pages métier.
if not st.session_state.get("user_id"):
    afficher_connexion(client)
    st.stop()

profile = get_profile(client)
if not profile or not profile.get("is_active"):
    st.error("Profil absent ou désactivé. Contactez l’administrateur.")
    st.button("Déconnexion", on_click=logout)
    st.stop()

role = profile.get("role")
if role not in ROLES:
    st.error("Votre rôle n'est pas reconnu. Contactez l’administrateur.")
    st.button("Déconnexion", on_click=logout)
    st.stop()

st.sidebar.write("**Connecté :** " + (profile.get("display_name") or "Utilisateur"))
st.sidebar.write("**Rôle :** " + ROLES[role])
st.sidebar.button("Déconnexion", on_click=logout, key="logout_main")

# Navigation explicite : chaque utilisateur ne voit que son espace autorisé.
if role == "admin":
    pages = [
        st.Page("pages/1_Admin.py", title="Espace ADMIN", icon="🛡️", default=True),
    ]
elif role == "chef_programme":
    pages = [
        st.Page("pages/2_Chef_de_programme.py", title="Espace CHEF DE PROGRAMME", icon="📊", default=True),
    ]
elif role == "chef_poste":
    pages = [
        st.Page("pages/3_Chef_de_poste.py", title="Espace CHEF DE POSTE", icon="🏥", default=True),
    ]
elif role == "agent_programme":
    pages = [
        st.Page("pages/4_Agent_par_programme.py", title="Espace AGENT PAR PROGRAMME", icon="📝", default=True),
    ]

navigation = st.navigation(pages, position="sidebar")
navigation.run()
