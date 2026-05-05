import logging

import allure
import pytest
import requests
import json


def pytest_addoption(parser):
    parser.addoption(
        "--base-url",
        action="store",
        default="https://dog.ceo/api",
        help="Base URL for Dog CEO API",
    )


@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("--base-url").rstrip("/")


@pytest.fixture
def api_client(base_url):
    class DogApiClient:
        @allure.step("Выполнить GET-запрос: {endpoint}")
        def get(self, endpoint):
            url = f"{base_url}/{endpoint.lstrip('/')}"
            logging.info("GET %s", url)
            allure.attach(
                url,
                name="Request URL",
                attachment_type=allure.attachment_type.TEXT,
            )

            response = requests.get(url, timeout=10)

            allure.attach(
                str(response.status_code),
                name="Response status code",
                attachment_type=allure.attachment_type.TEXT,
            )
            allure.attach(
                json.dumps(response.json(), indent=2, ensure_ascii=False),
                name="Response body",
                attachment_type=allure.attachment_type.JSON,
            )
            return response

    return DogApiClient()
