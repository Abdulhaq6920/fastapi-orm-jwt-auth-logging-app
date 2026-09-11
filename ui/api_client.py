import requests


API_URL = "http://127.0.0.1:8000"


def register_user(name: str, email: str, password: str):
    response = requests.post(
        f"{API_URL}/users",
        json={
            "name": name,
            "email": email,
            "password": password
        }
    )

    return response


def login_user(email: str, password: str):
    response = requests.post(
        f"{API_URL}/login",
        json={
            "email": email,
            "password": password
        }
    )

    return response


def get_users(token: str, search=None, page=1, page_size=10):

    headers = {
        "Authorization": f"Bearer {token}"
    }

    params = {
        "page": page,
        "page_size": page_size
    }

    if search:
        params["search"] = search

    return requests.get(
        f"{API_URL}/users",
        headers=headers,
        params=params
    )


def get_user(token: str, user_id: int):

    headers = {
        "Authorization": f"Bearer {token}"
    }

    return requests.get(
        f"{API_URL}/users/{user_id}",
        headers=headers
    )


def update_user(token: str, user_id: int, name: str, email: str):

    headers = {
        "Authorization": f"Bearer {token}"
    }

    return requests.put(
        f"{API_URL}/users/{user_id}",
        headers=headers,
        json={
            "name": name,
            "email": email
        }
    )


def delete_user(token: str, user_id: int):

    headers = {
        "Authorization": f"Bearer {token}"
    }

    return requests.delete(
        f"{API_URL}/users/{user_id}",
        headers=headers
    )