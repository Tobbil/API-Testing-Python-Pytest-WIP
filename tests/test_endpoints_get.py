import logging
import pytest

from helpers.requests import make_get_request

LOGGER = logging.getLogger(__name__)

MAIN_URL = "https://api.restful-api.dev/"
OBJECTS_ENDPOINT = "objects"
NONEXISTENT_ENDPOINT = "wrong_endpoint"


def test_get_endpoint_resource():
    endpoint = f"{OBJECTS_ENDPOINT}/1/"
    status_code, response_body = make_get_request(endpoint)

    LOGGER.info("Checking if status code is 200")
    assert status_code == 200, f"Unexpected status code: {status_code}"
    LOGGER.info("Checking if response body has content")
    assert response_body, "Response body is empty"


def test_get_nonexistent_endpoint():
    expected_error_kv_pair = ('error', 'Not Found')
    status_code, response_body = make_get_request(NONEXISTENT_ENDPOINT)

    LOGGER.info("Checking if status code is 404")
    assert status_code == 404, f"Unexpected status code: {status_code}"
    LOGGER.info("Checking if error message is present in response body")
    assert expected_error_kv_pair in response_body.items()


@pytest.mark.parametrize("resource_id", [99999999999999, -1, 0.5, "!", "test"])
def test_get_invalid_resource(resource_id):
    expected_error_kv_pair = {"error": f"Oject with id={resource_id} was not found."}
    endpoint = f"{OBJECTS_ENDPOINT}/{resource_id}"
    status_code, response_body = make_get_request(endpoint)

    LOGGER.info("Checking if status code is 404")
    assert status_code == 404, f"Unexpected status code: {status_code}"
    LOGGER.info("Checking if error message is present in response body")
    assert response_body == expected_error_kv_pair # TYPO IN ERROR MESSAGE ('Oject')
