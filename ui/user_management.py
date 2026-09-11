import streamlit as st

from api_client import (
    get_users,
    get_user,
    update_user,
    delete_user
)


def user_management_page():

    # ---------------------------------------------------------
    # PAGE HEADER
    # ---------------------------------------------------------

    st.title("👥 User Management")

    st.caption(
        f"Logged in as: {st.session_state.user_email}"
    )

    st.divider()


    # ---------------------------------------------------------
    # SEARCH USERS
    # ---------------------------------------------------------

    st.subheader("🔎 Search Users")

    search_col, button_col = st.columns([4, 1])

    with search_col:
        search = st.text_input(
            "Search",
            placeholder="Search by name or email",
            label_visibility="collapsed"
        )

    with button_col:
        load_users = st.button(
            "Load Users",
            use_container_width=True
        )


    # ---------------------------------------------------------
    # PAGINATION STATE
    # ---------------------------------------------------------

    if "user_page" not in st.session_state:
        st.session_state.user_page = 1

    if "current_users" not in st.session_state:
        st.session_state.current_users = []


    # ---------------------------------------------------------
    # LOAD USERS
    # ---------------------------------------------------------

    if load_users:

        st.session_state.user_page = 1

        response = get_users(
            st.session_state.access_token,
            search=search,
            page=st.session_state.user_page,
            page_size=10
        )

        if response.status_code == 200:

            st.session_state.current_users = response.json()

        else:

            st.error(
                f"Failed to load users: {response.status_code}"
            )


    # ---------------------------------------------------------
    # DISPLAY USERS
    # ---------------------------------------------------------

    if st.session_state.current_users:

        st.subheader("Users")

        for user in st.session_state.current_users:

            st.write(
                f"**{user['id']}**  |  "
                f"{user['name']}  |  "
                f"{user['email']}"
            )


        # -----------------------------------------------------
        # PAGINATION
        # -----------------------------------------------------

        previous_col, page_col, next_col = st.columns(
            [1, 1, 1]
        )

        with previous_col:

            if st.button(
                "⬅ Previous",
                disabled=st.session_state.user_page <= 1,
                use_container_width=True
            ):

                st.session_state.user_page -= 1

                response = get_users(
                    st.session_state.access_token,
                    search=search,
                    page=st.session_state.user_page,
                    page_size=10
                )

                if response.status_code == 200:
                    st.session_state.current_users = response.json()

                st.rerun()


        with page_col:

            st.markdown(
                f"<div style='text-align:center; padding-top:7px;'>"
                f"Page {st.session_state.user_page}"
                f"</div>",
                unsafe_allow_html=True
            )


        with next_col:

            if st.button(
                "Next ➡",
                disabled=len(st.session_state.current_users) < 10,
                use_container_width=True
            ):

                st.session_state.user_page += 1

                response = get_users(
                    st.session_state.access_token,
                    search=search,
                    page=st.session_state.user_page,
                    page_size=10
                )

                if response.status_code == 200:
                    st.session_state.current_users = response.json()

                st.rerun()


    st.divider()


    # ---------------------------------------------------------
    # GET + UPDATE USER
    # ---------------------------------------------------------

    get_col, update_col = st.columns(2)


    # =========================================================
    # GET USER
    # =========================================================

    with get_col:

        st.subheader("🔍 Get User")

        get_id = st.number_input(
            "User ID",
            min_value=1,
            step=1,
            key="get_user_id"
        )

        if st.button(
            "Get User",
            use_container_width=True
        ):

            response = get_user(
                st.session_state.access_token,
                get_id
            )

            if response.status_code == 200:

                st.json(response.json())

            else:

                st.error(
                    f"User not found: {response.status_code}"
                )


    # =========================================================
    # UPDATE USER
    # =========================================================

    with update_col:

        st.subheader("✏️ Update User")

        update_id = st.number_input(
            "User ID",
            min_value=1,
            step=1,
            key="update_user_id"
        )

        update_name = st.text_input(
            "New Name",
            key="update_name"
        )

        update_email = st.text_input(
            "New Email",
            key="update_email"
        )

        if st.button(
            "Update User",
            use_container_width=True
        ):

            response = update_user(
                st.session_state.access_token,
                update_id,
                update_name,
                update_email
            )

            if response.status_code == 200:

                st.success(
                    "User updated successfully."
                )

            else:

                st.error(
                    f"Update failed: {response.status_code}"
                )


    st.divider()


    # ---------------------------------------------------------
    # DELETE USER
    # ---------------------------------------------------------

    st.subheader("🗑️ Delete User")

    delete_col, delete_button_col = st.columns([4, 1])

    with delete_col:

        delete_id = st.number_input(
            "User ID",
            min_value=1,
            step=1,
            key="delete_user_id"
        )

    with delete_button_col:

        st.write("")

        if st.button(
            "Delete User",
            use_container_width=True
        ):

            response = delete_user(
                st.session_state.access_token,
                delete_id
            )

            if response.status_code == 200:

                st.success(
                    "User deleted successfully."
                )

            else:

                st.error(
                    f"Delete failed: {response.status_code}"
                )

