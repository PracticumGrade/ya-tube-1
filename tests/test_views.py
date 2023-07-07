import pytest
from rest_framework import status
from django.shortcuts import reverse

from conftest import N_PER_FIXTURE

pytestmark = [
    pytest.mark.django_db
]


def test_posts_list(api_client, posts):
    url = reverse("posts:posts-list")
    response = api_client.get(url)  # Выполняем запрос.
    assert response.status_code == status.HTTP_200_OK

    actual_data = response.json()
    assert len(actual_data) == N_PER_FIXTURE
