import streamlit as st
from common import require_role, agent_workspace

client, profile = require_role(["agent_programme"])
st.title("AGENT PAR PROGRAMME — Saisie des registres")
if not profile.get("post_id") or not profile.get("program_id"):
    st.error("Votre compte doit être associé à un poste de santé et à un programme.")
    st.stop()
agent_workspace(client, profile)
