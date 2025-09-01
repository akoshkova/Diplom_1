import pytest
from bun import Bun
from ingredient import Ingredient

class TestBurger:

    def test_initialization(self, burger):
        assert burger.bun is None
        assert burger.ingredients == []

    def test_set_buns(self, burger, test_bun):
        burger.set_buns(test_bun)
        assert burger.bun == test_bun

    @pytest.mark.parametrize("ingredient_count,expected_length", [
        (1, 1),
        (3, 3),
        (0, 0)
    ])
    def test_add_ingredient(self, burger, sample_ingredients, ingredient_count, expected_length):
        for i in range(ingredient_count):
            burger.add_ingredient(sample_ingredients[i % len(sample_ingredients)])
        assert len(burger.ingredients) == expected_length

    def test_remove_ingredient(self, burger, sample_ingredients):
        for ingredient in sample_ingredients:
            burger.add_ingredient(ingredient)

        burger.remove_ingredient(1)
        assert len(burger.ingredients) == 2
        assert sample_ingredients[0] in burger.ingredients
        assert sample_ingredients[2] in burger.ingredients

    def test_move_ingredient(self, burger, sample_ingredients):
        for ingredient in sample_ingredients:
            burger.add_ingredient(ingredient)

        burger.move_ingredient(0, 2)
        assert burger.ingredients == [sample_ingredients[1], sample_ingredients[2], sample_ingredients[0]]

    def test_get_price(self, burger, test_bun, sample_ingredients, mocker):
        mocker.patch.object(Bun, 'get_price', return_value=100)
        mocker.patch.object(Ingredient, 'get_price', side_effect=[50, 75, 60])

        burger.set_buns(test_bun)
        for ingredient in sample_ingredients:
            burger.add_ingredient(ingredient)

        assert burger.get_price() == (100 * 2) + 50 + 75 + 60

    def test_get_receipt(self, burger, test_bun, sample_ingredients, mocker):
        mocker.patch.object(Bun, 'get_name', return_value="test_bun")
        mocker.patch.object(Ingredient, 'get_name', side_effect=["sauce1", "filling1", "sauce2"])
        mocker.patch.object(Ingredient, 'get_type', side_effect=["SAUCE", "FILLING", "SAUCE"])

        burger.set_buns(test_bun)
        burger.add_ingredient(sample_ingredients[0])
        burger.add_ingredient(sample_ingredients[1])

        expected = (
            "(==== test_bun ====)\n"
            "= sauce sauce1 =\n"
            "= filling filling1 =\n"
            "(==== test_bun ====)\n"
            "Price: 550"
        )
        assert burger.get_receipt() == expected

    def test_remove_from_empty_burger(self, burger):
        with pytest.raises(IndexError):
            burger.remove_ingredient(0)

    def test_move_invalid_indexes(self, burger, sample_ingredients):
        burger.add_ingredient(sample_ingredients[0])
        with pytest.raises(IndexError):
            burger.move_ingredient(0,5)
