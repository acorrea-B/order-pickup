from asyncio.log import logger
from urllib import request
import requests
import logging

from urllib.parse import urljoin

class RequestFailureException(Exception):
    """
        Raised when request did not Succeed and
        it not know what's happend in remote site
    """

    def __init__(self, *args, url='', response=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.response = response
        self.url = url

class UnknownResultException(Exception):
    """
        Raised when, don't know if request was completed
        or not.
    """

    def __init__(self, *args, url='', response=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.response = response
        self.url = url

class RestClient():

    GET_DRIVERS = "jeithc/96681e4ac7e2b99cfe9a08ebc093787c/raw/632ca4fc3ffe77b558f467beee66f10470649bb4/points.json"

    def __init__(self, base_url, timeout=10):
        self.logger = logging.getLogger(__name__)
        self.base_url = base_url
        self.api_timeout=timeout


    def post_request(self, url):

        url = urljoin(self.base_url, url)

        headers = {
            'Content-Type': 'application/json'
        }

        try:
            post_response = requests.get(
                url,
                headers=headers,
            )
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.ConnectTimeout,
        ) as exc:
            self.logger.error(
                'Could not connect to Drivers API',
                exec_info=True,
                extra={
                    'url':url,
                    'payload':data,
                    'api_timeout':self.api_timeout
                },
            )

            raise RequestFailureException(url=url) from exc
        except requests.exceptions.ReadTimeout as exc:
            self.logger.error(
                'Read tiem out to Drivers API',
                exec_info=True,
                extra={
                    'url':url,
                    'api_timeout':self.api_timeout
                },
            )

            raise UnknownResultException(url=url) from exc
        try:
            json_response = post_response.json()
        except ValueError as exc:
            self.logger.error(
                'Invalid JSON data Drivers API',
                exec_info=True,
                extra={
                    'url':url,
                    'response_status_code':post_response.status_code,
                    'response_content_truncated':post_response.content[:1024]
                },
            )

        return post_response

    def get_drivers(self):
        return self.post_request(
            self.GET_DRIVERS
        )
        
