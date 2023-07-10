import pytest
from django.shortcuts import reverse
from django.urls import NoReverseMatch


@pytest.mark.parametrize(
    "viewname, args",
    [
        ("posts:posts-list", None),
        ("posts:posts-detail", (1,))
    ]
)
def test_reverse_match(viewname, args):
    try:
        reverse(viewname, args=args)
    except NoReverseMatch as e:
        raise AssertionError(
            f"Проверьте, что в приложении `posts` в файле `posts/urls.py` "
            f"зарегистирован url под именем `{viewname}` согласно заданию. "
        ) from e
