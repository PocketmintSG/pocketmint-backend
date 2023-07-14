import requests
import json


def signup(email: str, password: str):
    body = {"email": email, "password": password}
    response = requests.post(url="http://127.0.0.1:8000/signup", json=body)
    return response.text


# print(signup("abcd@abcd.com", "password"))


def login(email: str, password: str):
    body = {"email": email, "password": password}
    response = requests.post(url="http://127.0.0.1:8000/login", json=body)
    return json.loads(response.text)["token"]


# print(login("abcd@abcd.com", "password"))

token = login("abcd@abcd.com", "password")


def ping(token: str):
    headers = {"authorization": token}
    response = requests.post(url="http://127.0.0.1:8000/ping", headers=headers)
    return response.text


print(ping(token))
