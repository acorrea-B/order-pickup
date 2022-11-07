from django.test import TestCase
from unittest.mock import patch
from common.test.test_helper import vcr
from django.conf import settings

from driver.rest_client import RestClient

class DriversTestCase(TestCase):

    def setUp(self):
        api_config = settings.DRIVERS_API_CONFIG
        self.client = RestClient(
            base_url=api_config.get('URL', ''),
            timeout=api_config.get('TIMEOUT', 10)
        )

    @vcr.use_cassette()
    def test_succesful_get_drivers(self):
        response = self.client.get_drivers()

        self.assertEqual(
            response.status_code,
            200
        )

        json_response = response.json()

        self.assertIsNotNone(json_response)