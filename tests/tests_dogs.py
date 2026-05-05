from typing import Literal
from urllib.parse import urlparse

import pytest
from pydantic import BaseModel, ConfigDict, field_validator

pytestmark = pytest.mark.dogs


class RandomImageResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    message: str
    status: Literal["success"]

    @field_validator("message")
    @classmethod
    def validate_image_url(cls, value):
        parsed = urlparse(value)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("message must contain a valid image URL")
        if "images.dog.ceo" not in parsed.netloc:
            raise ValueError("image URL must belong to Dog CEO CDN")
        return value


def assert_url(value):
    parsed = urlparse(value)
    assert parsed.scheme in {"http", "https"}
    assert parsed.netloc


@pytest.mark.smoke
@pytest.mark.breeds
def test_get_all_breeds(api_client):
    response = api_client.get("/breeds/list/all")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"
    assert isinstance(body["message"], dict)
    assert "hound" in body["message"]
    assert isinstance(body["message"]["hound"], list)


@pytest.mark.smoke
@pytest.mark.images
@pytest.mark.schema
def test_get_random_image_with_schema_validation(api_client):
    response = api_client.get("/breeds/image/random")

    assert response.status_code == 200
    body = RandomImageResponse.model_validate(response.json())
    assert_url(body.message)


@pytest.mark.images
@pytest.mark.boundary
@pytest.mark.parametrize(
    "count, expected_count",
    [
        pytest.param(1, 1, id="min_valid_value"),
        pytest.param(3, 3, id="typical_valid_value"),
        pytest.param(50, 50, id="max_valid_value"),
        pytest.param(51, 50, id="above_max_value_is_capped"),
    ],
)
def test_get_multiple_random_images_by_count(api_client, count, expected_count):
    response = api_client.get(f"/breeds/image/random/{count}")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"
    assert isinstance(body["message"], list)
    assert len(body["message"]) == expected_count
    for image_url in body["message"]:
        assert_url(image_url)


@pytest.mark.smoke
@pytest.mark.images
def test_get_random_image_by_breed(api_client):
    response = api_client.get("/breed/retriever/images/random")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"
    assert isinstance(body["message"], str)
    assert_url(body["message"])
    assert "retriever" in body["message"]


@pytest.mark.smoke
@pytest.mark.breeds
def test_get_sub_breeds_by_breed(api_client):
    response = api_client.get("/breed/hound/list")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"
    assert isinstance(body["message"], list)
    assert {"afghan", "basset", "blood"}.issubset(set(body["message"]))
