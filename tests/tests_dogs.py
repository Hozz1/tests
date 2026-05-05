from typing import Literal
from urllib.parse import urlparse

import allure
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


@allure.step("Проверить, что строка является корректным URL")
def assert_url(value):
    parsed = urlparse(value)
    assert parsed.scheme in {"http", "https"}
    assert parsed.netloc


@allure.step("Проверить успешный статус-код")
def assert_status_code_ok(response):
    assert response.status_code == 200


@allure.step("Преобразовать тело ответа в JSON")
def get_json_body(response):
    return response.json()


@pytest.mark.smoke
@pytest.mark.breeds
@allure.title("Получение списка всех пород собак")
@allure.severity(allure.severity_level.CRITICAL)
def test_get_all_breeds(api_client):
    with allure.step("Отправить запрос на получение всех пород"):
        response = api_client.get("/breeds/list/all")

    assert_status_code_ok(response)

    with allure.step("Проверить структуру ответа со списком пород"):
        body = get_json_body(response)
        assert body["status"] == "success"
        assert isinstance(body["message"], dict)
        assert "hound" in body["message"]
        assert isinstance(body["message"]["hound"], list)


@pytest.mark.smoke
@pytest.mark.images
@pytest.mark.schema
@allure.title("Получение случайного изображения собаки с проверкой схемы")
@allure.severity(allure.severity_level.CRITICAL)
def test_get_random_image_with_schema_validation(api_client):
    with allure.step("Отправить запрос на получение случайного изображения"):
        response = api_client.get("/breeds/image/random")

    assert_status_code_ok(response)

    with allure.step("Проверить ответ через Pydantic-схему"):
        body = RandomImageResponse.model_validate(get_json_body(response))
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
@allure.title("Получение нескольких случайных изображений: count={count}")
@allure.severity(allure.severity_level.NORMAL)
def test_get_multiple_random_images_by_count(api_client, count, expected_count):
    with allure.step("Отправить запрос на получение нескольких изображений"):
        response = api_client.get(f"/breeds/image/random/{count}")

    assert_status_code_ok(response)

    with allure.step("Проверить количество и формат URL изображений"):
        body = get_json_body(response)
        assert body["status"] == "success"
        assert isinstance(body["message"], list)
        assert len(body["message"]) == expected_count
        for image_url in body["message"]:
            assert_url(image_url)


@pytest.mark.smoke
@pytest.mark.images
@allure.title("Получение случайного изображения по породе retriever")
@allure.severity(allure.severity_level.NORMAL)
def test_get_random_image_by_breed(api_client):
    with allure.step("Отправить запрос на получение изображения породы retriever"):
        response = api_client.get("/breed/retriever/images/random")

    assert_status_code_ok(response)

    with allure.step("Проверить, что ответ содержит URL изображения retriever"):
        body = get_json_body(response)
        assert body["status"] == "success"
        assert isinstance(body["message"], str)
        assert_url(body["message"])
        assert "retriever" in body["message"]


@pytest.mark.smoke
@pytest.mark.breeds
@allure.title("Получение списка подпород для hound")
@allure.severity(allure.severity_level.NORMAL)
def test_get_sub_breeds_by_breed(api_client):
    with allure.step("Отправить запрос на получение подпород hound"):
        response = api_client.get("/breed/hound/list")

    assert_status_code_ok(response)

    with allure.step("Проверить список подпород hound"):
        body = get_json_body(response)
        assert body["status"] == "success"
        assert isinstance(body["message"], list)
        assert {"afghan", "basset", "blood"}.issubset(set(body["message"]))
