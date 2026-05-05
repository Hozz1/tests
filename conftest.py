import logging

import pytest
import requests


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
        def get(self, endpoint):
            url = f"{base_url}/{endpoint.lstrip('/')}"
            logging.info("GET %s", url)
            return requests.get(url, timeout=10)

    return DogApiClient()
