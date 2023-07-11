from rest_framework.serializers import ModelSerializer

try:
    from posts.models import Post
except ImportError:
    raise AssertionError(
        'В приложении `posts` в файле `posts/models.py` '
        'не удаляйте модель `Post`.'
    )

try:
    from posts.serializers import PostSerializer
except ImportError:
    raise AssertionError(
        'В приложении `posts` в файле `posts/serializers.py` опишите '
        'класс сериализатора `PostSerializer` '
    )


def test_post_model_serializer():
    assert issubclass(PostSerializer, ModelSerializer), (
        'Убедитесь, что в файле `posts/serializers.py` класс `PostSerializer` унаследован от '
        'класса `ModelSerializer` библиотеки `rest_framework.serializers`.'
    )

    assert hasattr(PostSerializer.Meta, 'model'), (
        'Проверьте, что в подкласс `Meta` класса `PostSerializer` добавлено поле `model`.'
    )

    assert PostSerializer.Meta.model == Post, (
        'Проверьте, что в подклассе `Meta` класса `PostSerializer` значением поля `model` является модель `Post`.'
    )


def test_fields_in_post_serializer():
    assert hasattr(PostSerializer.Meta, 'fields'), (
        'Проверьте, что в подкласс `Meta` класса `PostSerializer` добавлено  поле `fields`.'
    )
    if PostSerializer.Meta.fields != '__all__':
        assert len(PostSerializer.Meta.fields) == 3, (
            'Проверьте, что в подклассе `Meta` класса `PostSerializer`  поле `fields` содержит все поля модели.'
        )
        for field in ('id', 'text', 'pub_date'):
            assert field in PostSerializer.Meta.fields, (
                f'Проверьте, что в подклассе `Meta` класса `PostSerializer` в поле `fields` добавлено поле `{field}`.'
            )
