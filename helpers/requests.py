import json
import os
import requests

MAIN_URL = "https://api.restful-api.dev"


def make_get_request(endpoint):
    url = os.path.join(MAIN_URL, endpoint)
    response = requests.get(url)
    status_code = response.status_code
    response_body = response.json()
    return status_code, response_body


def make_post_request(endpoint, json, headers=None):
    url = os.path.join(MAIN_URL, endpoint)
    response = requests.post(url, json=json, headers=headers)
    status_code = response.status_code
    response_body = response.json()
    return status_code, response_body
