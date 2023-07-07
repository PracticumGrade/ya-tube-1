import pytest
from mixer.backend.django import Mixer

from conftest import N_PER_FIXTURE


@pytest.fixture
def post(mixer: Mixer):
    return mixer.blend('posts.Post')


@pytest.fixture
def posts(mixer: Mixer):
    return mixer.cycle(N_PER_FIXTURE).blend('posts.Post')
