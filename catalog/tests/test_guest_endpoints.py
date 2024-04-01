import pytest
from rest_framework.test import APITestCase

pytestmark = [pytest.mark.django_db]


class TestGuestEndpoints(APITestCase):

    def test_something(self):
        assert True == True
