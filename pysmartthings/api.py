"""Utility for invoking the SmartThings Cloud API."""

import requests

from . import errors

API_BASE: str = 'https://api.smartthings.com/v1/'
API_LOCATIONS = "locations"
API_DEVICES: str = "devices"
API_DEVICE_STATUS: str = "devices/{device_id}/components/main/status"
API_DEVICE_COMMAND: str = "devices/{device_id}/commands"
API_APPS = "apps"
API_APP = "apps/{app_id}"
API_APP_OAUTH = "apps/{app_id}/oauth"
API_INSTALLEDAPPS = "installedapps"
API_INSTALLEDAPP = "installedapps/{installed_app_id}"
API_SUBSCRIPTIONS = API_INSTALLEDAPP + "/subscriptions"
API_SUBSCRIPTION = API_SUBSCRIPTIONS + "/{subscription_id}"


class API:
    """
    Utility for invoking the SmartThings Cloud API.

    https://smartthings.developer.samsung.com/docs/api-ref/st-api.html
    """

    def __init__(self, token: str):
        """Initialize a new instance of the API class."""
        self._headers = {"Authorization": "Bearer " + token}

    def get_locations(self) -> dict:
        """
        Get locations.

        https://smartthings.developer.samsung.com/docs/api-ref/st-api.html#operation/listLocations
        """
        return self._make_request('get', API_LOCATIONS)

    def get_devices(self) -> dict:
        """
        Get the device definitions.

        https://smartthings.developer.samsung.com/docs/api-ref/st-api.html#operation/getDevices
        """
        return self._make_request('get', API_DEVICES)

    def get_device_status(self, device_id: str) -> dict:
        """Get the status of a specific device."""
        return self._make_request(
            'get',
            API_DEVICE_STATUS.format(device_id=device_id))

    def post_command(self, device_id, capability, command, args,
                     component="main") -> object:
        """
        Execute commands on a device.

        https://smartthings.developer.samsung.com/docs/api-ref/st-api.html#operation/executeDeviceCommands
        """
        data = {
            "commands": [
                {
                    "component": component,
                    "capability": capability,
                    "command": command,
                }
            ]
        }
        if args:
            data["commands"][0]["arguments"] = args

        return self._make_request(
            'post',
            API_DEVICE_COMMAND.format(device_id=device_id),
            data)

    def get_apps(self) -> dict:
        """
        Get list of apps.

        https://smartthings.developer.samsung.com/develop/api-ref/st-api.html#operation/listApps
        """
        return self._make_request('get', API_APPS)

    def get_app_details(self, app_id: str) -> dict:
        """
        Get the details of the specific app.

        https://smartthings.developer.samsung.com/develop/api-ref/st-api.html#operation/getApp
        """
        return self._make_request(
            'get',
            API_APP.format(app_id=app_id))

    def create_app(self, data: dict) -> dict:
        """
        Create a new app.

        https://smartthings.developer.samsung.com/develop/api-ref/st-api.html#operation/createApp
        """
        return self._make_request('post', API_APPS, data)

    def update_app(self, app_id: str, data: dict) -> dict:
        """
        Update an existing app.

        https://smartthings.developer.samsung.com/develop/api-ref/st-api.html#operation/updateApp
        """
        return self._make_request(
            'put', API_APP.format(app_id=app_id), data)

    def delete_app(self, app_id: str):
        """
        Delete an app.

        https://smartthings.developer.samsung.com/develop/api-ref/st-api.html#operation/deleteApp
        """
        return self._make_request(
            'delete', API_APP.format(app_id=app_id))

    def get_app_oauth(self, app_id: str) -> dict:
        """
        Get an app's oauth settings.

        https://smartthings.developer.samsung.com/develop/api-ref/st-api.html#operation/getAppOauth
        """
        return self._make_request('get', API_APP_OAUTH.format(app_id=app_id))

    def update_app_oauth(self, app_id: str, data: dict) -> dict:
        """
        Update an app's oauth settings.

        https://smartthings.developer.samsung.com/develop/api-ref/st-api.html#operation/updateAppOauth
        """
        return self._make_request(
            'put', API_APP_OAUTH.format(app_id=app_id), data)

    def get_installedapps(self) -> dict:
        """
        Get list of installedapps.

        https://smartthings.developer.samsung.com/docs/api-ref/st-api.html#operation/listInstallations
        """
        return self._make_request('get', API_INSTALLEDAPPS)

    def get_installedapp(self, installed_app_id: str) -> dict:
        """
        Get the details of the specific installedapp.

        https://smartthings.developer.samsung.com/docs/api-ref/st-api.html#operation/getInstallation
        """
        return self._make_request(
            'get',
            API_INSTALLEDAPP.format(installed_app_id=installed_app_id))

    def delete_installedapp(self, installed_app_id: str):
        """
        Delete an app.

        https://smartthings.developer.samsung.com/docs/api-ref/st-api.html#operation/deleteInstallation
        """
        return self._make_request(
            'delete', API_INSTALLEDAPP.format(
                installed_app_id=installed_app_id))

    def get_subscriptions(self, installed_app_id: str) -> dict:
        """
        Get installedapp's subscriptions.

        https://smartthings.developer.samsung.com/develop/api-ref/st-api.html#operation/listSubscriptions
        """
        return self._make_request(
            'get',
            API_SUBSCRIPTIONS.format(installed_app_id=installed_app_id))

    def create_subscription(self, installed_app_id: str, data: dict) -> dict:
        """
        Create a subscription for an installedapp.

        https://smartthings.developer.samsung.com/develop/api-ref/st-api.html#operation/saveSubscription
        """
        return self._make_request(
            'post',
            API_SUBSCRIPTIONS.format(installed_app_id=installed_app_id),
            data)

    def delete_all_subscriptions(self, installed_app_id: str) -> dict:
        """
        Delete all subscriptions for an installedapp.

        https://smartthings.developer.samsung.com/develop/api-ref/st-api.html#operation/deleteAllSubscriptions
        """
        return self._make_request(
            'delete',
            API_SUBSCRIPTIONS.format(installed_app_id=installed_app_id))

    def get_subscription(self, installed_app_id: str, subscription_id: str) \
            -> dict:
        """
        Get an individual subscription.

        https://smartthings.developer.samsung.com/develop/api-ref/st-api.html#operation/getSubscription
        """
        return self._make_request(
            'get',
            API_SUBSCRIPTION.format(
                installed_app_id=installed_app_id,
                subscription_id=subscription_id))

    def delete_subscription(self, installed_app_id: str, subscription_id: str):
        """
        Delete an individual subscription.

        https://smartthings.developer.samsung.com/develop/api-ref/st-api.html#operation/deleteSubscription
        """
        return self._make_request(
            'delete',
            API_SUBSCRIPTION.format(
                installed_app_id=installed_app_id,
                subscription_id=subscription_id))

    def _make_request(self, method: str, resource: str, data: dict = None):
        response = requests.request(
            method,
            API_BASE + resource,
            json=data,
            headers=self._headers)

        if response.ok:
            return response.json()
        if response.status_code == 401:
            raise errors.APIUnauthorizedError
        elif response.status_code == 403:
            raise errors.APIForbiddenError
        raise errors.APIUnknownError
