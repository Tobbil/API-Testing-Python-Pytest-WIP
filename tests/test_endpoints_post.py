import logging

from test_data.objects import TestObjects
from helpers.requests import make_post_request, make_get_request

LOGGER = logging.getLogger(__name__)

MAIN_URL = "https://api.restful-api.dev/"
OBJECTS_ENDPOINT = "objects"


def test_post_new_resource():
    status_code, response_body = make_post_request(
        OBJECTS_ENDPOINT, json=TestObjects.OBJECT_VALID
    )
    assert status_code == 200, f"Unexpected status code: {status_code}"  # WHY NOT 201?
    assert response_body, "Response body is empty"


def test_created_resource_exists():
    status_code_post, response_body_post = make_post_request(
        OBJECTS_ENDPOINT, json=TestObjects.OBJECT_VALID
    )
    assert status_code_post == 200, f"Unexpected status code: {status_code_post}"  # WHY NOT 201?
    assert response_body_post, "Response body is empty"

    response_id = response_body_post.get("id")
    status_code_get, response_body_get = make_get_request(f"{OBJECTS_ENDPOINT}/{response_id}")

    updated_object = TestObjects.OBJECT_VALID.copy()
    updated_object.update({"id": response_id})

    assert status_code_get == 200, f"Unexpected status code: {status_code_get}"  # WHY NOT 201?
    assert updated_object == response_body_get, "Created object is different than expected"

