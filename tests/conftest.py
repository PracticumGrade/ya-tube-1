import pytest
from rest_framework.test import APIClient
from mixer.backend.django import mixer as _mixer

N_PER_FIXTURE = 3
POST_FIELDS = ["id", "text", "pub_date"]

pytest_plugins = [
    'fixtures.posts',
]


@pytest.fixture
def mixer():
    return _mixer


@pytest.fixture
def api_client():
    client = APIClient()
    return client
