import unittest
from unittest.mock import patch
from parameterized import parameterized
from burger import Burger
from bun import Bun
from ingredient import Ingredient


class TestBurger(unittest.TestCase):
    def setUp(self):
        # Создаем тестовый экземпляр бургера
        self.burger = Burger()

        # Создаем тестовые булочки и ингредиенты
        self.bun = Bun("test_bun", 100)
        self.ingredient1 = Ingredient("SAUCE", "sauce1", 50)
        self.ingredient2 = Ingredient("FILLING", "filling1", 75)
        self.ingredient3 = Ingredient("SAUCE", "sauce2", 60)

    def test_init(self):
        # Проверяем, что при создании бургер пустой
        self.assertIsNone(self.burger.bun)
        self.assertEqual(self.burger.ingredients, [])

    def test_set_buns(self):
        # Проверяем установку булочки
        self.burger.set_buns(self.bun)
        self.assertEqual(self.burger.bun, self.bun)

    @parameterized.expand([
        ("add_one_ingredient", [self.ingredient1], 1),
        ("add_multiple_ingredients", [self.ingredient1, self.ingredient2, self.ingredient3], 3),
    ])
    def test_add_ingredient(self, ingredients, expected_length):
        # Проверяем добавление ингредиентов
        for ingredient in ingredients:
            self.burger.add_ingredient(ingredient)
        self.assertEqual(len(self.burger.ingredients), expected_length)

    def test_remove_ingredient(self):
        # Проверяем удаление ингредиента
        self.burger.add_ingredient(self.ingredient1)
        self.burger.add_ingredient(self.ingredient2)

        self.burger.remove_ingredient(0)
        self.assertEqual(len(self.burger.ingredients), 1)
        self.assertEqual(self.burger.ingredients[0], self.ingredient2)

    def test_move_ingredient(self):
        # Проверяем перемещение ингредиента
        self.burger.add_ingredient(self.ingredient1)
        self.burger.add_ingredient(self.ingredient2)

        self.burger.move_ingredient(0, 1)
        self.assertEqual(self.burger.ingredients[0], self.ingredient2)
        self.assertEqual(self.burger.ingredients[1], self.ingredient1)

    @patch.object(Bun, 'get_price')
    @patch.object(Ingredient, 'get_price')
    def test_get_price(self, mock_ingredient_price, mock_bun_price):
        # Проверяем расчет цены с моками
        mock_bun_price.return_value = 100
        mock_ingredient_price.side_effect = [50, 75, 60]

        self.burger.set_buns(self.bun)
        self.burger.add_ingredient(self.ingredient1)
        self.burger.add_ingredient(self.ingredient2)
        self.burger.add_ingredient(self.ingredient3)

        expected_price = 100 * 2 + 50 + 75 + 60
        self.assertEqual(self.burger.get_price(), expected_price)

    @patch.object(Bun, 'get_name')
    @patch.object(Ingredient, 'get_name')
    @patch.object(Ingredient, 'get_type')
    def test_get_receipt(self, mock_ingredient_type, mock_ingredient_name, mock_bun_name):
        # Проверяем формирование чека с моками
        mock_bun_name.return_value = "test_bun"
        mock_ingredient_name.side_effect = ["sauce1", "filling1"]
        mock_ingredient_type.side_effect = ["SAUCE", "FILLING"]

        self.burger.set_buns(self.bun)
        self.burger.add_ingredient(self.ingredient1)
        self.burger.add_ingredient(self.ingredient2)

        expected_receipt = "(==== test_bun ====)\n= sauce sauce1 =\n= filling filling1 =\n(==== test_bun ====)\nPrice: 550"
        self.assertEqual(self.burger.get_receipt(), expected_receipt)