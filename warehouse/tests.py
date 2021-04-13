from django.test import TestCase

from warehouse.models import Item


class ItemTestCase(TestCase):
    def setUp(self):
        Item.objects.create(title="test", amount=100.2, unit='pcs', price=100, date='2021-01-01')

    def test_items_have_cost(self):
        """
        Корректно ли считается итоговая стоимость
        """
        item = Item.objects.get(title="test")
        self.assertEqual(item.cost, 100.2 * 100)
