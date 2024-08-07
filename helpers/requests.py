import os
import requests

MAIN_URL = "https://api.restful-api.dev/"


def make_get_request(endpoint):
    response = requests.get(os.path.join(MAIN_URL, endpoint))
    status_code = response.status_code
    response_body = response.json()
    return status_code, response_body