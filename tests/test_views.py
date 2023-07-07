import pytest
from rest_framework import status
from django.shortcuts import reverse

from conftest import N_PER_FIXTURE, POST_FIELDS
from posts.models import Post


pytestmark = [
    pytest.mark.django_db
]


@pytest.fixture
def post_create_data():
    return {
        "text": "Текст заметки",
    }


def test_posts_list(api_client, posts):
    url = reverse("posts:posts-list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK, (
        f"Убедитесь, что при отправке GET-запроса на url `{url}`  "
        f"для получение списка постов возвращается статус-код {status.HTTP_200_OK}"
    )

    data = response.json()

    assert isinstance(data, list), (
        f"Убедитесь, что при отправке GET-запроса на url `{url}`  "
        f"возвращается список."
    )
    assert len(data) == N_PER_FIXTURE, (
        f"Убедитесь, что при отправке GET-запроса на url `{url}`  "
        f"для получение списка постов возвращаются все посты."
    )


def test_create_post(api_client, post_create_data):
    url = reverse("posts:posts-list")
    response = api_client.post(url, data=post_create_data)
    assert response.status_code == status.HTTP_201_CREATED, (
        f"Убедитесь, что при отправке POST-запроса на url `{url}`  "
        f"для создания нового поста возвращается статус-код {status.HTTP_201_CREATED}"
    )

    assert Post.objects.count() == 1, (
        f"Убедитесь, что при отправке POST-запроса на url `{url}`  "
        f"для создания нового поста, объект был добавлен в БД."
    )

    data = response.json()
    assert isinstance(data, dict), (
        f"Убедитесь, что при отправке POST-запроса на url `{url}`  "
        f"для создания нового поста возвращается словарь"
    )

    for field in POST_FIELDS:
        assert field in data, (
            f"Убедитесь, что при отправке POST-запроса на url `{url}`  "
            f"для создания нового поста, возвращаемый словарь содержит поле `{field}`"
        )

    text_field = "text"
    assert post_create_data[text_field] == data[text_field], (
        f"Убедитесь, что при отправке POST-запроса на url `{url}`  "
        f"для создания нового поста, возвращается словарь созданного объекта с заполненным полем `{text_field}`"
    )


def test_incorrect_create_post(api_client):
    url = reverse("posts:posts-list")
    empty_data = {}
    response = api_client.post(url, data=empty_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST, (
        f"Убедитесь, что при отправке POST-запроса на url `{url}`  "
        f"для создания нового поста c некорректными данными, возвращается статус-код {status.HTTP_400_BAD_REQUEST}"
    )

    assert Post.objects.count() == 0, (
        f"Убедитесь, что при отправке POST-запроса на url `{url}`  "
        f"для создания нового поста, объект не был добавлен в БД."
    )
