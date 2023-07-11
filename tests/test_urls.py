import pytest
from django.shortcuts import reverse
from django.urls import NoReverseMatch


@pytest.mark.parametrize(
    "viewname, args, expected_url",
    [
        ("posts:post-list", None, "/api/v1/posts/"),
        ("posts:post-detail", (1,), "/api/v1/posts/1/")
    ]
)
def test_reverse_match(viewname, args, expected_url):
    try:
        url = reverse(viewname, args=args)
    except NoReverseMatch as e:
        raise AssertionError(
            f"Проверьте, что в приложении `posts` в файле `posts/urls.py` "
            f"зарегистирован url под именем `{viewname}` согласно заданию. "
        ) from e

    assert url == expected_url, (
        f"Проверьте, что в приложении `posts` в файле `posts/urls.py` "
        f"для имени `{viewname}` установлен верный шаблон url "
    )
