import logging
import pytest

from test_data.constants import Constants as const
from test_data.objects import TestObjects
from helpers.requests import make_post_request, make_get_request, make_put_request, make_delete_request

LOGGER = logging.getLogger(__name__)


class TestGetMethod:
    """Test GET method on '/objects' endpoint"""
    def test_get_valid_resource_status_code(self):
        """Test verifies that GET request to endpoint results in response with status code 200"""

        endpoint = const.OBJECTS_ENDPOINT + "/1/"
        status_code, _ = make_get_request(endpoint)

        LOGGER.info(f"Checking if status code is {const.STATUS_SUCCESS}")
        assert status_code == const.STATUS_SUCCESS, f"Unexpected status code: {status_code}"


    def test_get_valid_resource_response_body(self):
        """Test verifies that GET request to endpoint results in response with body that's not empty"""

        endpoint = const.OBJECTS_ENDPOINT + "/1/"
        _, response_body = make_get_request(endpoint)

        LOGGER.info("Checking if response body has content")
        assert response_body, "Response body is empty"


    @pytest.mark.parametrize("resource_id", [99999999999999, -1, 0.5, "!", "test", " "])
    def test_get_invalid_resource_from_valid_endpoint(self, resource_id):
        """Test verifies that requesting an invalid resource from valid endpoint results in error"""

        expected_error_kv_pair = {"error": f"Oject with id={resource_id} was not found."} # TYPO IN ERROR MESSAGE ('Oject')
        endpoint = f"{const.OBJECTS_ENDPOINT}/{resource_id}"
        status_code, response_body = make_get_request(endpoint)

        LOGGER.info(f"Checking if status code is {const.STATUS_NOT_FOUND}")
        assert status_code == const.STATUS_NOT_FOUND, f"Unexpected status code: {status_code}"
        LOGGER.info("Checking if error message is present in response body")
        assert response_body == expected_error_kv_pair


class TestPostMethod:
    """Test POST method on '/objects' endpoint"""
    def test_post_new_valid_resource(self):
        """Test verifies that POST method with valid payload creates a new resource"""

        LOGGER.info("Creating resource")
        status_code_post, response_body_post = make_post_request(const.OBJECTS_ENDPOINT, json=TestObjects.OBJECT_VALID)

        LOGGER.info(f"Checking if status code is {const.STATUS_CREATED}")
        assert status_code_post == const.STATUS_CREATED, f"Unexpected status code: {status_code_post}"
        LOGGER.info("Checking if response body has content")
        assert response_body_post, "Response body is empty"

        resource_id = response_body_post.get("id")
        status_code_get, response_body_get = make_get_request(f"{const.OBJECTS_ENDPOINT}/{resource_id}")

        test_object_with_id = TestObjects.OBJECT_VALID.copy()
        test_object_with_id.update({"id": resource_id})

        LOGGER.info(f"Checking if status code is {const.STATUS_SUCCESS}")
        assert status_code_get == const.STATUS_SUCCESS, f"Unexpected status code: {status_code_get}"
        LOGGER.info("Checking if created resource is correct")
        assert response_body_get == test_object_with_id, "Created resource is different than expected"

    def test_post_new_valid_resource_with_headers(self):
        """Test verifies that POST method with valid payload and headers creates a new resource"""

        headers = {"Content-Type": "application/json", "Custom-Header": "Custom-Value"}
        status_code, response_body = make_post_request(
            const.OBJECTS_ENDPOINT, json=TestObjects.OBJECT_VALID, headers=headers
        )

        LOGGER.info(f"Checking if status code is {const.STATUS_CREATED}")
        assert status_code == const.STATUS_CREATED, f"Unexpected status code: {status_code}"
        LOGGER.info("Checking if response body has content")
        assert response_body, "Response body is empty"


    def test_post_new_resource_payload_too_large(self):
        """Test verifies that POST request with too large payload results in error"""

        LOGGER.info("Creating resource with payload too big")
        status_code, response_body = make_post_request(
            const.OBJECTS_ENDPOINT, json=TestObjects.OBJECT_TOO_LARGE_PAYLOAD
        )

        LOGGER.info(f"Checking if status code is {const.STATUS_PAYLOAD_TOO_LARGE}")
        assert status_code == const.STATUS_PAYLOAD_TOO_LARGE, f"Unexpected status code: {status_code}"
        LOGGER.info("Checking if response body has content")
        assert response_body, "Response body is empty"


class TestPutMethod:
    """Test PUT method on '/objects' endpoint"""
    def test_put_change_existing_resource(self):
        """Test verifies that existing resource can be changed with PUT request"""

        LOGGER.info("Creating resource")
        _, response_body_post = make_post_request(const.OBJECTS_ENDPOINT, json=TestObjects.OBJECT_VALID)

        resource_id = response_body_post.get("id")
        test_object_with_id = TestObjects.OBJECT_VALID.copy()
        test_object_with_id.update({"id": resource_id})

        LOGGER.info("Checking if resource was created")
        status_code_get, response_body_get = make_get_request(f"{const.OBJECTS_ENDPOINT}/{resource_id}")
        assert response_body_get == test_object_with_id, "Created resource is different than expected"

        LOGGER.info("Updating resource")
        status_code_put, _ = make_put_request(
            f"{const.OBJECTS_ENDPOINT}/{resource_id}", json=TestObjects.OBJECT_VALID_PUT
        )
        assert status_code_put == const.STATUS_SUCCESS, f"Unexpected status code: {status_code_put}"

        updated_object_with_id = TestObjects.OBJECT_VALID_PUT.copy()
        updated_object_with_id.update({"id": resource_id})

        LOGGER.info("Checking if resource was updated")
        status_code_get, response_body_get = make_get_request(f"{const.OBJECTS_ENDPOINT}/{resource_id}")
        assert status_code_get == const.STATUS_SUCCESS, f"Unexpected status code: {status_code_get}"
        assert response_body_get == updated_object_with_id, "Resource wasn't updated successfully"
    

class TestDeleteMethod:
    """Test DELETE method on '/objects' endpoint"""
    def test_delete_resource(self):
        """Test verifies that existing resource can be deleted with DELETE request"""

        LOGGER.info("Creating resource to be deleted")
        _, response_body_post = make_post_request(const.OBJECTS_ENDPOINT, json=TestObjects.OBJECT_VALID)

        resource_id = response_body_post.get("id")
        test_object_with_id = TestObjects.OBJECT_VALID.copy()
        test_object_with_id.update({"id": resource_id})
        expected_response = {'message': f'Object with id = {resource_id} has been deleted.'}

        LOGGER.info("Checking if resource was created")
        status_code_get, response_body_get = make_get_request(f"{const.OBJECTS_ENDPOINT}/{resource_id}")
        assert response_body_get == test_object_with_id, "Created resource is different than expected"   

        LOGGER.info("Deleting resource")
        status_code_delete, response_body_delete = make_delete_request(f"{const.OBJECTS_ENDPOINT}/{resource_id}")
        assert status_code_delete == const.STATUS_SUCCESS, f"Unexpected status code: {status_code_delete}"
        LOGGER.info("Checking response body from DELETE request")
        assert response_body_delete == expected_response

        LOGGER.info("Checking if resource was deleted")
        status_code_get, response_body_get = make_get_request(f"{const.OBJECTS_ENDPOINT}/{resource_id}")
        assert status_code_get == const.STATUS_NOT_FOUND, f"Unexpected status code: {status_code_get}"
