import hmac

import streamlit as st

from core import ui


def _users() -> dict:
    return dict(st.secrets.get("APP_USERS", {}))


def require_login() -> None:
    ui.setup()
    if st.session_state.get("authenticated"):
        with st.sidebar:
            st.caption(f"Logged in as {st.session_state.get('user')}")
            if st.button("Logout"):
                st.session_state.clear()
                st.rerun()
        return

    ui.hero(
        "Where Go Ah?",
        "Lost in the government maze? Don't worry lah, log in first and we'll tell you which counter to queue at. 🧭",
        "🧭",
    )
    _, mid, _ = st.columns([1, 3, 1])
    with mid, st.form("login"):
        st.markdown("**Eh, who goes there?** 🕵️ Show your credentials, then we talk.")
        username = st.text_input("Username", placeholder="Not 'admin' hor, too obvious")
        password = st.text_input("Password", type="password", placeholder="Shhh... we won't tell your auntie")
        submitted = st.form_submit_button("Open sesame, can or not? 🚪")
        st.caption("No queue number needed. Promise. 🎟️")
    if submitted:
        expected = _users().get(username)
        if expected is not None and hmac.compare_digest(str(expected), password):
            st.session_state["authenticated"] = True
            st.session_state["user"] = username
            st.toast("Welcome in! Kopi's on the house ☕", icon="🎉")
            st.rerun()
        st.error("Aiyo, wrong username or password leh. Try again, don't panic — nobody's judging. 🙈")
    st.stop()
