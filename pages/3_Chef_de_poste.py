import streamlit as st
from common import require_role, admin_client, REGISTERS, read_only_registers

_, profile = require_role(["chef_poste"])
st.title("CHEF DE POSTE — Supervision de mon poste")
if not profile.get("post_id"):
    st.error("Aucun poste de santé n’est associé à votre compte.")
    st.stop()
try:
    admin = admin_client()
    post = admin.table("posts").select("id,name,is_active").eq(
        "id", profile["post_id"]
    ).single().execute().data
    if not post or not post.get("is_active"):
        st.error("Ce poste de santé est désactivé.")
        st.stop()
    st.caption("Poste de santé : " + post["name"])
    read_only_registers(
        admin, "Consultation de tous les programmes de mon poste",
        list(REGISTERS), post_id=profile["post_id"],
        post_names={profile["post_id"]: post["name"]}
    )
except Exception as exc:
    st.error("Chargement du poste impossible : " + str(exc))
