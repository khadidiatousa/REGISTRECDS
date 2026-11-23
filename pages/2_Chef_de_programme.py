import streamlit as st
from common import require_role, admin_client, REGISTERS, read_only_registers

_, profile = require_role(["chef_programme"])
st.title("CHEF DE PROGRAMME — Suivi du programme")
if not profile.get("program_id"):
    st.error("Aucun programme n’est associé à votre compte. Contactez l’administrateur.")
    st.stop()
try:
    admin = admin_client()
    program = admin.table("programs").select("id,name,is_active").eq(
        "id", profile["program_id"]
    ).single().execute().data
    if not program or not program.get("is_active"):
        st.error("Ce programme est désactivé.")
        st.stop()
    links = admin.table("program_register_access").select("register_code").eq(
        "program_id", profile["program_id"]
    ).execute().data or []
    codes = [x["register_code"] for x in links if x["register_code"] in REGISTERS]
    posts = admin.table("posts").select("id,name").execute().data or []
    post_names = {p["id"]: p["name"] for p in posts}
    st.caption("Programme : " + program["name"])
    read_only_registers(admin, "Consultation des registres de mon programme — tous les postes", codes, post_names=post_names)
except Exception as exc:
    st.error("Chargement du programme impossible : " + str(exc))
