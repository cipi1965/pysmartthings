"""A Mock API for SmartThings."""

from collections import namedtuple

from requests import Request, Response
from requests_mock.response import create_response

from pysmartthings import api

from .utilities import get_json

API_TOKEN = "Test Token"
APP_ID = 'c6cde2b0-203e-44cf-a510-3b3ed4706996'
DEVICE_ID = '743de49f-036f-4e9c-839a-2f89d57607db'

UrlMock = namedtuple('UrlMock', 'method url request response')

URLS = [
    UrlMock('GET', api.API_LOCATIONS, None, 'locations.json'),
    UrlMock('GET', api.API_DEVICES, None, 'devices.json'),
    UrlMock('GET', api.API_DEVICE_STATUS.format(device_id=DEVICE_ID),
            None, 'device_main_status.json'),
    UrlMock('GET', api.API_APPS, None, 'apps.json'),
    UrlMock('GET', api.API_APP.format(app_id=APP_ID), None, 'app_get.json'),
    UrlMock('POST', api.API_APPS,
            'app_post_request.json', 'app_post_response.json'),
    UrlMock('PUT', api.API_APP.format(app_id=APP_ID),
            'app_put_request.json', 'app_put_response.json'),
    UrlMock('DELETE', api.API_APP.format(app_id=APP_ID), None, None),
    UrlMock('GET', api.API_APP_OAUTH.format(app_id=APP_ID),
            None, 'app_oauth_get_response.json'),
    UrlMock('PUT', api.API_APP_OAUTH.format(app_id=APP_ID),
            'app_oauth_put_request.json', 'app_oauth_put_response.json')
]


def setup(requests_mock):
    """Configure request mocks the API calls."""
    requests_mock.add_matcher(__matcher)


def __matcher(req: Request) -> Response:
    """Match against our registry."""
    match = next((obj for obj in URLS if __match_request(req, obj)), None)
    if match:
        body = {} if not match.response else get_json(match.response)
        return create_response(req, json=body)


def __match_request(req: Request, mock: UrlMock):
    """Match the request against the mock setup."""
    if not req.headers.get('Authorization', '') == "Bearer " + API_TOKEN:
        return False
    if not req.method == mock.method:
        return False
    if not req.url == api.API_BASE + mock.url:
        return False
    if mock.request and not req.json() == get_json(mock.request):
        return False
    return True