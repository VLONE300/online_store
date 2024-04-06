import pytest
from rest_framework.test import APITestCase
from django.shortcuts import reverse

from catalog.models import Category
from conftest import EVERYTHING_EQUALS_NOT_NONE

pytestmark = [pytest.mark.django_db]


class TestGuestEndpoints(APITestCase):
    fixtures = ['catalog/tests/fixtures/categories_fixture.json', 'catalog/tests/fixtures/discounts_fixtures.json',
                'catalog/tests/fixtures/products_fixtures.json', 'catalog/tests/fixtures/sellers_fixtures.json']

    def test_categories_list(self):
        url = reverse('categories')
        response = self.client.get(url)
        print(response.data)
        assert response.status_code == 200
        assert response.data == [
            {'id': 1,
             'name': EVERYTHING_EQUALS_NOT_NONE,
             'description': EVERYTHING_EQUALS_NOT_NONE
             },
            {'id': 2,
             'name': EVERYTHING_EQUALS_NOT_NONE,
             'description': EVERYTHING_EQUALS_NOT_NONE
             },
            {'id': 3,
             'name': EVERYTHING_EQUALS_NOT_NONE,
             'description': EVERYTHING_EQUALS_NOT_NONE
             },
            {'id': 4,
             'name': EVERYTHING_EQUALS_NOT_NONE,
             'description': EVERYTHING_EQUALS_NOT_NONE
             },
        ]

    def test_sellers(self):
        url = reverse('sellers')
        response = self.client.get(url)
        print(response.data)
        assert response.status_code == 200
        assert response.data == [
            {
                "id": 1,
                "name": EVERYTHING_EQUALS_NOT_NONE,
                "contact": EVERYTHING_EQUALS_NOT_NONE
            },
            {
                "id": 2,
                "name": EVERYTHING_EQUALS_NOT_NONE,
                "contact": EVERYTHING_EQUALS_NOT_NONE
            },
            {
                "id": 3,
                "name": EVERYTHING_EQUALS_NOT_NONE,
                "contact": EVERYTHING_EQUALS_NOT_NONE
            },
        ]

    def test_discounts(self):
        url = reverse('discounts')
        response = self.client.get(url)
        print(response.data)
        assert response.status_code == 200
        assert response.data == [
            {
                "id": 1,
                "name": EVERYTHING_EQUALS_NOT_NONE,
                "percent": EVERYTHING_EQUALS_NOT_NONE,
            },
        ]

    def test_category_products(self):
        categories = [1, 2, 3, 4]
        for category_id in categories:
            url = reverse('category-products', kwargs={'category_id': category_id})
            response = self.client.get(url)
            print(response.data)
            assert response.status_code == 200
            assert response.data == [
                {'id': category_id,
                 'article': EVERYTHING_EQUALS_NOT_NONE,
                 'name': EVERYTHING_EQUALS_NOT_NONE,
                 'price': EVERYTHING_EQUALS_NOT_NONE,
                 'images': EVERYTHING_EQUALS_NOT_NONE
                 },
            ]
