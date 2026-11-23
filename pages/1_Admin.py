import pandas as pd
import streamlit as st
from common import require_role, admin_client, REGISTERS, ROLES, fetch_records, record_view

_, profile = require_role(["admin"])
admin = admin_client()
st.title("ADMIN — Administration générale")
st.caption("Gestion des programmes, postes et comptes. Consultation des registres en lecture seule.")

tab1, tab2, tab3, tab4 = st.tabs([
    "Vue générale", "Programmes", "Postes de santé", "Utilisateurs et consultation"
])

with tab1:
    try:
        p = admin.table("programs").select("id", count="exact").execute()
        h = admin.table("posts").select("id", count="exact").execute()
        u = admin.table("profiles").select("id", count="exact").execute()
        total = 0
        for code in REGISTERS:
            result = admin.table("reg_" + code).select("id", count="exact").execute()
            total += result.count or 0
        cols = st.columns(4)
        cols[0].metric("Programmes", p.count or 0)
        cols[1].metric("Postes", h.count or 0)
        cols[2].metric("Comptes", u.count or 0)
        cols[3].metric("Fiches de registres", total)
    except Exception as exc:
        st.error("Statistiques indisponibles : " + str(exc))

with tab2:
    st.subheader("Créer un programme")
    with st.form("admin_create_program"):
        pname = st.text_input("Nom du programme")
        pcodes = st.multiselect("Registres rattachés", list(REGISTERS),
            format_func=lambda c: REGISTERS[c]["label"])
        create_program = st.form_submit_button("Créer le programme")
    if create_program:
        if not pname.strip() or not pcodes:
            st.error("Indiquez un nom et au moins un registre.")
        else:
            try:
                created = admin.table("programs").insert({
                    "name": pname.strip(), "is_active": True
                }).execute().data[0]
                for code in pcodes:
                    admin.table("program_register_access").upsert({
                        "program_id": created["id"], "register_code": code
                    }).execute()
                st.success("Programme créé et registres associés.")
                st.rerun()
            except Exception as exc:
                st.error("Création impossible : " + str(exc))
    try:
        programs = admin.table("programs").select(
            "id,name,is_active,created_at"
        ).order("name").execute().data or []
        if programs:
            st.dataframe(pd.DataFrame(programs), use_container_width=True, hide_index=True)
            choices = {f'{p["name"]} — {p["id"][:8]}': p for p in programs}
            chosen = choices[st.selectbox("Programme à modifier", list(choices), key="program_choice")]
            linked = admin.table("program_register_access").select("register_code").eq(
                "program_id", chosen["id"]
            ).execute().data or []
            with st.form("admin_edit_program"):
                new_name = st.text_input("Nom", value=chosen["name"])
                new_codes = st.multiselect("Registres du programme", list(REGISTERS),
                    default=[x["register_code"] for x in linked if x["register_code"] in REGISTERS],
                    format_func=lambda c: REGISTERS[c]["label"])
                active = st.checkbox("Programme actif", value=bool(chosen["is_active"]))
                save_program = st.form_submit_button("Enregistrer le programme")
            if save_program:
                if not new_name.strip() or not new_codes:
                    st.error("Le nom et au moins un registre sont obligatoires.")
                else:
                    try:
                        admin.table("programs").update({
                            "name": new_name.strip(), "is_active": active
                        }).eq("id", chosen["id"]).execute()
                        admin.table("program_register_access").delete().eq(
                            "program_id", chosen["id"]
                        ).execute()
                        for code in new_codes:
                            admin.table("program_register_access").upsert({
                                "program_id": chosen["id"], "register_code": code
                            }).execute()
                        st.success("Programme mis à jour.")
                        st.rerun()
                    except Exception as exc:
                        st.error("Mise à jour impossible : " + str(exc))
    except Exception as exc:
        st.error("Lecture des programmes impossible : " + str(exc))

with tab3:
    st.subheader("Créer un poste de santé")
    with st.form("admin_create_post"):
        post_name = st.text_input("Nom du poste")
        district = st.text_input("District sanitaire")
        address = st.text_area("Adresse")
        create_post = st.form_submit_button("Créer le poste")
    if create_post:
        if not post_name.strip():
            st.error("Le nom du poste est obligatoire.")
        else:
            try:
                admin.table("posts").insert({
                    "name": post_name.strip(), "district": district.strip(),
                    "address": address.strip(), "is_active": True
                }).execute()
                st.success("Poste créé.")
                st.rerun()
            except Exception as exc:
                st.error("Création impossible : " + str(exc))
    try:
        posts = admin.table("posts").select(
            "id,name,district,address,is_active,created_at"
        ).order("name").execute().data or []
        if posts:
            st.dataframe(pd.DataFrame(posts), use_container_width=True, hide_index=True)
            choices = {f'{p["name"]} — {p["id"][:8]}': p for p in posts}
            chosen = choices[st.selectbox("Poste à modifier", list(choices), key="post_choice")]
            with st.form("admin_edit_post"):
                new_name = st.text_input("Nom du poste", value=chosen.get("name") or "")
                new_district = st.text_input("District", value=chosen.get("district") or "")
                new_address = st.text_area("Adresse", value=chosen.get("address") or "")
                active = st.checkbox("Poste actif", value=bool(chosen.get("is_active", True)))
                save_post = st.form_submit_button("Enregistrer")
            if save_post:
                try:
                    admin.table("posts").update({
                        "name": new_name.strip(), "district": new_district.strip(),
                        "address": new_address.strip(), "is_active": active
                    }).eq("id", chosen["id"]).execute()
                    st.success("Poste mis à jour.")
                    st.rerun()
                except Exception as exc:
                    st.error("Modification impossible : " + str(exc))
    except Exception as exc:
        st.error("Lecture des postes impossible : " + str(exc))

with tab4:
    st.subheader("Créer un utilisateur")
    try:
        programs = admin.table("programs").select("id,name").eq(
            "is_active", True
        ).order("name").execute().data or []
        posts = admin.table("posts").select("id,name").eq(
            "is_active", True
        ).order("name").execute().data or []
        post_map = {x["name"]: x["id"] for x in posts}
        program_map = {x["name"]: x["id"] for x in programs}
        with st.form("admin_create_user"):
            email = st.text_input("Adresse e-mail")
            display = st.text_input("Nom complet")
            password = st.text_input("Mot de passe provisoire (14 caractères minimum)", type="password")
            role = st.selectbox("Rôle", list(ROLES), format_func=lambda x: ROLES[x])
            post_choice = st.selectbox("Poste de santé", ["— Aucun —"] + list(post_map))
            program_choice = st.selectbox("Programme", ["— Aucun —"] + list(program_map))
            assigned = st.multiselect("Registres attribués à l’agent", list(REGISTERS),
                format_func=lambda c: REGISTERS[c]["label"])
            submit_user = st.form_submit_button("Créer le compte")
        if submit_user:
            needs_post = role in ("chef_poste", "agent_programme")
            needs_program = role in ("chef_programme", "agent_programme")
            if len(password) < 14 or not email.strip() or not display.strip():
                st.error("E-mail, nom et mot de passe d’au moins 14 caractères obligatoires.")
            elif needs_post and post_choice == "— Aucun —":
                st.error("Ce rôle nécessite un poste de santé.")
            elif needs_program and program_choice == "— Aucun —":
                st.error("Ce rôle nécessite un programme.")
            elif role == "agent_programme" and not assigned:
                st.error("Attribuez au moins un registre à cet agent.")
            else:
                try:
                    created = admin.auth.admin.create_user({
                        "email": email.strip(), "password": password,
                        "email_confirm": True,
                        "user_metadata": {"display_name": display.strip()}
                    })
                    uid = created.user.id
                    admin.table("profiles").upsert({
                        "id": uid, "display_name": display.strip(), "role": role,
                        "post_id": post_map.get(post_choice),
                        "program_id": program_map.get(program_choice),
                        "is_active": True
                    }).execute()
                    admin.table("user_register_access").delete().eq("user_id", uid).execute()
                    for code in assigned:
                        admin.table("user_register_access").upsert({
                            "user_id": uid, "register_code": code
                        }).execute()
                    st.success("Compte créé et rôle attribué.")
                    st.rerun()
                except Exception as exc:
                    st.error("Création impossible : " + str(exc))
    except Exception as exc:
        st.error("Chargement des postes/programmes impossible : " + str(exc))

    st.divider()
    st.subheader("Comptes existants")
    try:
        users = admin.table("profiles").select(
            "id,display_name,role,post_id,program_id,is_active,created_at"
        ).order("display_name").execute().data or []
        posts = admin.table("posts").select("id,name").execute().data or []
        programs = admin.table("programs").select("id,name").execute().data or []
        post_names = {x["id"]: x["name"] for x in posts}
        program_names = {x["id"]: x["name"] for x in programs}
        display_rows = []
        for user in users:
            item = dict(user)
            item["poste"] = post_names.get(user.get("post_id"), "")
            item["programme"] = program_names.get(user.get("program_id"), "")
            item["rôle affiché"] = ROLES.get(user.get("role"), user.get("role"))
            display_rows.append(item)
        if display_rows:
            st.dataframe(pd.DataFrame(display_rows), use_container_width=True, hide_index=True)
            user_choices = {f'{u.get("display_name") or u["id"]} — {u["id"][:8]}': u for u in users}
            target = user_choices[st.selectbox("Compte à modifier", list(user_choices), key="edit_user_choice")]
            with st.form("admin_edit_user"):
                new_name = st.text_input("Nom", value=target.get("display_name") or "")
                new_role = st.selectbox("Rôle", list(ROLES),
                    index=list(ROLES).index(target["role"]) if target.get("role") in ROLES else 0,
                    format_func=lambda x: ROLES[x])
                post_ids = [None] + [x["id"] for x in posts]
                post_labels = ["— Aucun —"] + [x["name"] for x in posts]
                program_ids = [None] + [x["id"] for x in programs]
                program_labels = ["— Aucun —"] + [x["name"] for x in programs]
                pi = post_ids.index(target.get("post_id")) if target.get("post_id") in post_ids else 0
                gi = program_ids.index(target.get("program_id")) if target.get("program_id") in program_ids else 0
                post_i = st.selectbox("Poste affecté", range(len(post_ids)), index=pi,
                    format_func=lambda i: post_labels[i])
                program_i = st.selectbox("Programme affecté", range(len(program_ids)), index=gi,
                    format_func=lambda i: program_labels[i])
                active = st.checkbox("Compte actif", value=bool(target.get("is_active", True)))
                save_user = st.form_submit_button("Mettre à jour le compte")
            if save_user:
                needs_post = new_role in ("chef_poste", "agent_programme")
                needs_program = new_role in ("chef_programme", "agent_programme")
                if needs_post and post_ids[post_i] is None:
                    st.error("Ce rôle doit avoir un poste affecté.")
                elif needs_program and program_ids[program_i] is None:
                    st.error("Ce rôle doit avoir un programme affecté.")
                elif target["id"] == st.session_state.user_id and (not active or new_role != "admin"):
                    st.error("Vous ne pouvez pas désactiver votre propre compte ni retirer votre rôle ADMIN.")
                else:
                    try:
                        admin.table("profiles").update({
                            "display_name": new_name.strip(), "role": new_role,
                            "post_id": post_ids[post_i], "program_id": program_ids[program_i],
                            "is_active": active
                        }).eq("id", target["id"]).execute()
                        st.success("Compte mis à jour.")
                        st.rerun()
                    except Exception as exc:
                        st.error("Modification impossible : " + str(exc))
    except Exception as exc:
        st.error("Gestion des utilisateurs impossible : " + str(exc))

    st.divider()
    st.subheader("Consultation de tous les registres — lecture seule")
    st.caption("L’ADMIN ne peut ni créer, ni modifier, ni supprimer les fiches des registres.")
    try:
        posts = admin.table("posts").select("id,name").order("name").execute().data or []
        post_names = {p["id"]: p["name"] for p in posts}
        code = st.selectbox("Registre à consulter", list(REGISTERS),
            format_func=lambda c: REGISTERS[c]["label"], key="admin_read_code")
        labels = ["Tous les postes"] + [p["name"] for p in posts]
        selected = st.selectbox("Filtrer par poste", labels, key="admin_read_post")
        post_id = None if selected == "Tous les postes" else next(
            p["id"] for p in posts if p["name"] == selected
        )
        rows = fetch_records(admin, code, post_id=post_id)
        if rows:
            frame = pd.DataFrame([record_view(r, REGISTERS[code], post_names) for r in rows])
            st.metric("Nombre de fiches", len(frame))
            st.dataframe(frame, use_container_width=True, hide_index=True)
            st.download_button("Exporter en CSV", frame.to_csv(index=False).encode("utf-8-sig"),
                file_name=f"{code}_tous_postes.csv", mime="text/csv")
        else:
            st.info("Aucune fiche trouvée.")
    except Exception as exc:
        st.error("Consultation impossible : " + str(exc))
