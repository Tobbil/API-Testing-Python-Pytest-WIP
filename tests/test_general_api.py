import logging

from test_data.constants import Constants as const
from helpers.requests import make_get_request

LOGGER = logging.getLogger(__name__)

class TestGeneralAPI:
    """General tests for API"""
    def test_get_nonexistent_endpoint(self):
            expected_error_kv_pair = ("error", "Not Found")
            status_code, response_body = make_get_request(const.NONEXISTENT_ENDPOINT)

            LOGGER.info(f"Checking if status code is {const.STATUS_NOT_FOUND}")
            assert status_code == const.STATUS_NOT_FOUND, f"Unexpected status code: {status_code}"
            LOGGER.info("Checking if error message is present in response body")
            assert expected_error_kv_pair in response_body.items()