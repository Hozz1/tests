# Dog CEO API tests

Small pytest project for testing Dog CEO API: https://dog.ceo/dog-api/documentation

## Project structure

```text
.
├── conftest.py
├── pytest.ini
├── requirements.txt
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

Run with a custom API URL:

```bash
pytest --base-url=https://dog.ceo/api
```

Run by marker:

```bash
pytest -m smoke
pytest -m schema
pytest -m boundary
```
