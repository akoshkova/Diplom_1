import pytest
from burger import Burger
from bun import Bun
from ingredient import Ingredient

@pytest.fixture
def test_bun():
    return Bun("test_bun", 100)


@pytest.fixture
def sample_ingredients():
    return [
        Ingredient("SAUCE", "sauce1", 50),
        Ingredient("FILLING", "filling1", 75),
        Ingredient("SAUCE", "sauce2", 60)
    ]

