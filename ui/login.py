import streamlit as st

from api_client import login_user, register_user


def login_page():

    st.title("🔐 Welcome Back")
    st.write("Login to access the application.")

    st.divider()

    email = st.text_input(
        "Email",
        placeholder="Enter your email"
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter your password"
    )

    if st.button("Login", use_container_width=True):

        if not email or not password:
            st.error("Please enter email and password.")
            return

        response = login_user(email, password)

        if response.status_code == 200:

            data = response.json()

            st.session_state.access_token = data["access_token"]

            st.session_state.user_email = email

            st.success("Login successful!")

            st.rerun()

        else:
            st.error("Invalid email or password.")


def register_page():

    st.title("📝 Create Account")
    st.write("Create your account to get started.")

    st.divider()

    name = st.text_input(
        "Name",
        placeholder="Enter your name"
    )

    email = st.text_input(
    "Email",
    placeholder="Enter your email",
    key="login_email"
)

    password = st.text_input(
    "Password",
    type="password",
    placeholder="Enter your password",
    key="login_password"
)

    if st.button("Create Account", use_container_width=True):

        if not name or not email or not password:
            st.error("Please fill in all fields.")
            return

        response = register_user(
            name,
            email,
            password
        )

        if response.status_code == 200:

            st.success(
                "Account created successfully! "
                "You can now login."
            )

        else:

            try:
                detail = response.json().get(
                    "detail",
                    "Registration failed."
                )
            except Exception:
                detail = "Registration failed."

            st.error(detail)