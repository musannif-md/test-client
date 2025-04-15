from requests import post, request
from config import BASE_URL, USERNAME, PASSWORD


class Client:
    def __init__(self, use_proto=True):
        if use_proto:
            self.headers = {"Content-Type": "application/x-protobuf"}
        else:
            self.headers = {"Content-Type": "application/json"}
        self.token = None

    def signup(self, username=USERNAME, password=PASSWORD):
        url = f"{BASE_URL}/signup"
        payload = {"username": username, "password": password}
        headers = {"Content-Type": "application/json"}
        response = post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            self.token = data.get("token")
        else:
            print(f"Registration failed: {response.status_code} - {response.text}")

    def login(self, username=USERNAME, password=PASSWORD):
        url = f"{BASE_URL}/login"
        payload = {"username": username, "password": password}
        headers = {"Content-Type": "application/json"}
        response = post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            self.token = data.get("token")
        else:
            print(f"Login failed: {response.status_code} - {response.text}")

    def request(self, method, endpoint, data_body=None, is_json=True, **kwargs):
        url = f"{BASE_URL}{endpoint}"
        if is_json:
            res = request(method, url, headers=self.headers, json=data_body, **kwargs)
        else:
            res = request(method, url, headers=self.headers, data=data_body, **kwargs)
        return res

    def authenticated_request(
        self, method, endpoint, data_body=None, is_json=True, **kwargs
    ):
        if not self.token:
            print("Error: No token found. Please login or signup first.")
            return None
        url = f"{BASE_URL}{endpoint}"
        auth_headers = {**self.headers, "Authorization": f"Bearer {self.token}"}
        if is_json:
            res = request(method, url, headers=auth_headers, json=data_body, **kwargs)
        else:
            res = request(method, url, headers=auth_headers, data=data_body, **kwargs)
        return res
