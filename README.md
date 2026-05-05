# Dog CEO API tests with Allure

Small pytest project for testing Dog CEO API: https://dog.ceo/dog-api/documentation

## Project structure

```text
.
├── conftest.py
├── pytest.ini
├── requirements.txt
├── docs
│   └── allure_report.png
└── tests
    └── tests_dogs.py
```

## Install

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run tests

```bash
pytest
```

The `pytest.ini` file already contains Allure launch options:

```ini
addopts = -ra --strict-markers --alluredir=allure-results --clean-alluredir
```

## Generate Allure report

```bash
allure generate allure-results -o allure-report --clean
allure open allure-report
```

Or open it immediately:

```bash
allure serve allure-results
```

After opening the report, take a screenshot and save it to:

```text
docs/allure_report.png
```

## Run by marker

```bash
pytest -m smoke
pytest -m schema
pytest -m boundary
```

## Custom API URL

```bash
pytest --base-url=https://dog.ceo/api
```
