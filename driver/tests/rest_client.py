import requests
import requests_mock

from unittest import TestCase
from common.test.test_helper import vcr
from django.conf import settings

from driver.rest_client import RestClient
from driver.rest_client import RequestFailureException
from driver.rest_client import UnknownResultException

class DriversTestCase(TestCase):

    def setUp(self):
        api_config = settings.DRIVERS_API_CONFIG
        self.__mocked_url = api_config.get('URL', '')
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
        self.assertIn( 'alfreds', json_response)
        self.assertGreater(len(json_response["alfreds"]), 5)
        self.assertEqual(1, json_response["alfreds"][0]["id"])

    @requests_mock.Mocker(real_http=True)
    def test_conection_error_get_drivers(self, mock):
        mocked_url = 'https://gist.githubusercontent.com/jeithc/96681e4ac7e2b99cfe9a08ebc093787c/raw/632ca4fc3ffe77b558f467beee66f10470649bb4/points.json'
        mock.get(
            mocked_url,
            exc=requests.exceptions.ConnectionError
        )
        with self.assertLogs(
            logger='driver.rest_client',
            level='ERROR'
        ) as cm:
            with self.assertRaises(RequestFailureException) as ctx:
                self.client.get_drivers()
        
        self.assertIsNone(ctx.exception.response)
        self.assertIn(
            'Could not connect to Drivers API',
            cm.output[0].split('\\n')[0]
        )
    
    @requests_mock.Mocker(real_http=True)
    def test_timeout_get_drivers(self, mock):
        mocked_url = 'https://gist.githubusercontent.com/jeithc/96681e4ac7e2b99cfe9a08ebc093787c/raw/632ca4fc3ffe77b558f467beee66f10470649bb4/points.json'
        mock.get(
            mocked_url,
            exc=requests.exceptions.ConnectTimeout
        )
        with self.assertLogs(
            logger='driver.rest_client',
            level='ERROR'
        ) as cm:
            with self.assertRaises(RequestFailureException) as ctx:
                self.client.get_drivers()
        
        self.assertIsNone(ctx.exception.response)
        self.assertIn(
            'Could not connect to Drivers API',
            cm.output[0].split('\\n')[0]
        )
    
    @requests_mock.Mocker(real_http=True)
    def test_read_timeout_get_drivers(self, mock):
        mocked_url = 'https://gist.githubusercontent.com/jeithc/96681e4ac7e2b99cfe9a08ebc093787c/raw/632ca4fc3ffe77b558f467beee66f10470649bb4/points.json'
        mock.get(
            mocked_url,
            exc=requests.exceptions.ReadTimeout
        )
        with self.assertLogs(
            logger='driver.rest_client',
            level='ERROR'
        ) as cm:
            with self.assertRaises(UnknownResultException) as ctx:
                self.client.get_drivers()
        
        self.assertIsNone(ctx.exception.response)
        self.assertIn(
            'Read time out to Drivers API',
            cm.output[0].split('\\n')[0]
        )
    
    @requests_mock.Mocker(real_http=True)
    def test_invalid_data_get_drivers(self, mock):
        mocked_url = 'https://gist.githubusercontent.com/jeithc/96681e4ac7e2b99cfe9a08ebc093787c/raw/632ca4fc3ffe77b558f467beee66f10470649bb4/points.json'
        mock.get(
            mocked_url,
            status_code=200
        )
        with self.assertLogs(
            logger='driver.rest_client',
            level='ERROR'
        ) as cm:
            with self.assertRaises(UnknownResultException) as ctx:
                self.client.get_drivers()
        
        self.assertIsNone(ctx.exception.response)
        self.assertIn(
            'Invalid JSON data Drivers API',
            cm.output[0].split('\\n')[0]
        )