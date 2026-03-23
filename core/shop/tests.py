from django.test import TestCase
from rest_framework import serializers

from shop.serializers import MenuDetSer


class MenuDetSerTest(TestCase):
    def test_validate_without_discount_price_is_valid(self):
        serializer = MenuDetSer()

        data = {
            "price": 0,
            "discount_price": None,
            "weight": 200,
        }

        result = serializer.validate(data)

        self.assertEqual(result, data)

    def test_validate_with_discount_price_less_than_price_is_valid(self):
        serializer = MenuDetSer()

        data = {
            "price": 200,
            "discount_price": 100,
            "weight": 150,
        }

        result = serializer.validate(data)

        self.assertEqual(result, data)

    def test_validate_with_discount_price_equal_price_raises_error(self):
        serializer = MenuDetSer()

        data = {
            "price": 200,
            "discount_price": 200,
            "weight": 150,
        }

        with self.assertRaises(serializers.ValidationError) as exc:
            serializer.validate(data)

        self.assertIn("Скидочная цена должна быть меньше основной", str(exc.exception))

    def test_validate_with_discount_price_greater_than_price_raises_error(self):
        serializer = MenuDetSer()

        data = {
            "price": 200,
            "discount_price": 300,
            "weight": 150,
        }

        with self.assertRaises(serializers.ValidationError) as exc:
            serializer.validate(data)

        self.assertIn("Скидочная цена должна быть меньше основной", str(exc.exception))