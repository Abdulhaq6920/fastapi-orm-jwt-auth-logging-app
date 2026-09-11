import streamlit as st

from login import login_page, register_page
from user_management import user_management_page


st.set_page_config(
    page_title="ORM Application",
    layout="centered"
)



if "access_token" not in st.session_state:
    st.session_state.access_token = None

if "user_email" not in st.session_state:
    st.session_state.user_email = None

if "page" not in st.session_state:
    st.session_state.page = "login"


# -------------------------
# Logout
# -------------------------

def logout():

    st.session_state.access_token = None
    st.session_state.user_email = None
    st.session_state.page = "login"

    st.rerun()


# -------------------------
# Application flow
# -------------------------

if st.session_state.access_token is None:

    login_tab, register_tab = st.tabs(
        ["Login", "Register"]
    )

    with login_tab:
        login_page()

    with register_tab:
        register_page()

else:

    st.sidebar.title("Application")

    st.sidebar.write(
        f"Logged in as:\n"
        f"{st.session_state.user_email}"
    )

    if st.sidebar.button(
        "Logout",
        use_container_width=True
    ):
        logout()

    user_management_page()