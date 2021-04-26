import pytest

from webtrap import create_app

@pytest.fixture
def app():
    app = create_app({"TESTING": True})
    yield app

@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client

@pytest.fixture
def runner(app):
    return app.test_cli_runner()