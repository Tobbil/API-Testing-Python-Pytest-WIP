import logging

from test_data.constants import Constants as const
from test_data.objects import TestObjects
from helpers.requests import make_post_request, make_get_request, make_put_request

LOGGER = logging.getLogger(__name__)


def test_put_change_existing_resource():
    LOGGER.info("Creating resource")
    _, response_body_post = make_post_request(const.OBJECTS_ENDPOINT, json=TestObjects.OBJECT_VALID)

    resource_id = response_body_post.get("id")
    test_object_with_id = TestObjects.OBJECT_VALID.copy()
    test_object_with_id.update({"id": resource_id})

    LOGGER.info("Checking if resource was created")
    status_code_get, response_body_get = make_get_request(f"{const.OBJECTS_ENDPOINT}/{resource_id}")
    assert response_body_get == test_object_with_id

    LOGGER.info("Updating resource")
    status_code_put, _ = make_put_request(f"{const.OBJECTS_ENDPOINT}/{resource_id}", json=TestObjects.OBJECT_VALID_PUT)
    assert status_code_put == 200, f"Unexpected status code: {status_code_put}"

    LOGGER.info("Checking if resource was updated")
    updated_object_with_id = TestObjects.OBJECT_VALID_PUT.copy()
    updated_object_with_id.update({"id": resource_id})
    status_code_get, response_body_get = make_get_request(f"{const.OBJECTS_ENDPOINT}/{resource_id}")
    assert status_code_get == 200, f"Unexpected status code: {status_code_get}"

    assert response_body_get == updated_object_with_id
