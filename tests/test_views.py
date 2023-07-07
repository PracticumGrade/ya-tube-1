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


@pytest.fixture
def post_update_data():
    return {
        "text": "Новый текст заметки",
    }


@pytest.fixture
def post_pk_for_args(post):
    return post.pk,


@pytest.mark.parametrize(
    "method,name,args,status_code,data", [
        ("GET", "posts:posts-list", None, status.HTTP_200_OK, None,),
        ("POST", "posts:posts-list", None, status.HTTP_201_CREATED, pytest.lazy_fixture("post_create_data"),),
        ("GET", "posts:posts-detail", pytest.lazy_fixture("post_pk_for_args"), status.HTTP_200_OK, None,),
        ("PUT", "posts:posts-detail", pytest.lazy_fixture("post_pk_for_args"), status.HTTP_200_OK, pytest.lazy_fixture("post_update_data"),),
        ("PATCH", "posts:posts-detail", pytest.lazy_fixture("post_pk_for_args"), status.HTTP_200_OK, None,),
        ("DELETE", "posts:posts-detail", pytest.lazy_fixture("post_pk_for_args"), status.HTTP_204_NO_CONTENT, None,),
    ]
)
def test_post_status_code(api_client, post, method, name, args, status_code, data):
    url = reverse(name, args=args)
    request_method = getattr(api_client, method.lower())
    response = request_method(url, data=data)
    assert response.status_code == status_code, (
        f"Убедитесь, что при отправке {method}-запроса на url `{url}`  "
        f"возвращается статус-код {status_code}"
    )


@pytest.mark.parametrize(
    "method,data", [
        ("GET", None,),
        ("PUT", pytest.lazy_fixture("post_update_data"),),
        ("PATCH", None,),
        ("DELETE", None,),
    ]
)
def test_not_found_post(api_client, method, data):
    does_not_exists_pk = 123456789,
    url = reverse("posts:posts-detail", args=does_not_exists_pk)
    request_method = getattr(api_client, method.lower())
    response = request_method(url, data=data)

    status_code = status.HTTP_404_NOT_FOUND
    assert response.status_code == status_code, (
        f"Убедитесь, что при отправке {method}-запроса на url `{url}` "
        f"для получения несуществующего объекта возвращается статус-код {status_code}"
    )


@pytest.mark.parametrize(
    "method,name,args", [
        ("POST", "posts:posts-list", None,),
        ("PUT", "posts:posts-detail", pytest.lazy_fixture("post_pk_for_args"),),
    ]
)
def test_bad_request_and_errors(api_client, post, method, name, args):
    url = reverse(name, args=args)
    request_method = getattr(api_client, method.lower())
    bad_data = {}
    response = request_method(url, data=bad_data)

    status_code = status.HTTP_400_BAD_REQUEST
    assert response.status_code == status_code, (
        f"Убедитесь, что при отправке {method}-запроса на url `{url}`  "
        f"c некорректными данными, возвращается статус-код {status_code}"
    )

    data = response.json()
    expected_value = {"text": ["This field is required."]}
    assert data == expected_value, (
        f"Убедитесь, что при отправке {method}-запроса на url `{url}`  "
        f"c некорректными данными, в теле ответа возвращаются ошибки."
    )


def test_posts_list(api_client, posts):
    url = reverse("posts:posts-list")
    response = api_client.get(url)

    data = response.json()

    assert isinstance(data, list), (
        f"Убедитесь, что при отправке GET-запроса на url `{url}`  "
        f"возвращается список."
    )
    assert len(data) == N_PER_FIXTURE, (
        f"Убедитесь, что при отправке GET-запроса на url `{url}`  "
        f"для получение списка постов возвращаются все посты."
    )


@pytest.mark.parametrize(
    "method, name, args, data", [
        ("POST", "posts:posts-list", None, pytest.lazy_fixture("post_create_data"),),
        ("GET", "posts:posts-detail", pytest.lazy_fixture("post_pk_for_args"), None,),
        ("PUT", "posts:posts-detail", pytest.lazy_fixture("post_pk_for_args"), pytest.lazy_fixture("post_update_data"),),
        ("PATCH", "posts:posts-detail", pytest.lazy_fixture("post_pk_for_args"), None,),
    ]
)
def test_serialize_post(api_client, post, method, name, args, data):
    url = reverse(name, args=args)
    request_method = getattr(api_client, method.lower())
    response = request_method(url, data=data)

    data = response.json()
    assert isinstance(data, dict), (
        f"Убедитесь, что при отправке {method}-запроса на url `{url}` возвращается словарь"
    )


def test_create_post(api_client, post_create_data):
    url = reverse("posts:posts-list")
    response = api_client.post(url, data=post_create_data)

    assert Post.objects.count() == 1, (
        f"Убедитесь, что при отправке POST-запроса на url `{url}`  "
        f"для создания нового поста, объект был добавлен в БД."
    )

    data = response.json()
    assert data["text"] == post_create_data["text"], (
        f"Убедитесь, что при отправке POST-запроса на url `{url}`  "
        f"для создания нового поста, возвращаемый словарь содержит верное значение поля `text`"
    )


def test_incorrect_create_post(api_client):
    url = reverse("posts:posts-list")
    empty_data = {}
    api_client.post(url, data=empty_data)

    assert Post.objects.count() == 0, (
        f"Убедитесь, что при отправке POST-запроса с некорректными данными на url `{url}`  "
        f"для создания нового поста, объект не был добавлен в БД."
    )


@pytest.mark.parametrize(
    "method", [
        "PUT",
        "PATCH",
    ]
)
def test_update_post(api_client, post, post_pk_for_args, post_update_data, method):
    url = reverse("posts:posts-detail", args=post_pk_for_args)
    request_method = getattr(api_client, method.lower())
    response = request_method(url, data=post_update_data)

    assert Post.objects.count() == 1, (
        f"Убедитесь, что при отправке {method}-запроса на url `{url}`  "
        f"для обновления поста, новый объект не был добавлен в БД."
    )

    post.refresh_from_db()
    assert post.text == post_update_data["text"], (
        f"Убедитесь, что при отправке {method}-запроса на url `{url}`  "
        f"для обновления поста, пост был обновлен в БД."
    )

    data = response.json()
    assert data["text"] == post_update_data["text"], (
        f"Убедитесь, что при отправке {method}-запроса на url `{url}`  "
        f"для обновления поста, возвращается словарь с обновленным полем `text`"
    )
