import requests
import reposify.exceptions


class Base(object):
    base_url = 'https://api.reposify.com'

    def __init__(self, token):
        self.token = token

    @staticmethod
    def raise_exception(response):
        code = response.status_code
        if code == 401:
            raise exceptions.HTTPUnauthorized(response)
        elif code == 403:
            raise exceptions.HTTPForbidden(response)
        elif code == 404:
            raise exceptions.HTTPNotFound(response)
        elif code == 409:
            raise exceptions.HTTPConflict(response)
        elif code == 429:
            raise exceptions.HTTPTooManyRequests(response)
        elif code >= 500:
            raise exceptions.HTTPServerError(response)
        elif code >= 400:
            raise exceptions.HTTPBadRequest(response)

    def request(self, endpoint_name, endpoint_action, version=1, params=None, data=None, method='get'):
        """
        Returns a json object containing the requested resource
        """

        url = self.compose_url(version, endpoint_name, endpoint_action)
        request_params = {"token": self.token}
        if params:
            request_params.update(params)

        if method == 'get':
            response = requests.get(url=url, params=request_params)
        elif method == 'post':
            response = requests.post(url=url, params=request_params, data=data)
        else:
            raise exceptions.BadRequestMethod

        if response.status_code != 200:
            self.raise_exception(response)

        return response.json()

    def compose_url(self, version, endpoint_name, endpoint_action):
        """
        Returns the uri for an endpoint
        """
        return '{base_url}/v{version}/{endpoint_name}/{endpoint_action}'.format(base_url=self.base_url,
                                                                                version=version,
                                                                                endpoint_name=endpoint_name,
                                                                                endpoint_action=endpoint_action)


class Insights(Base):
    """
    Implementation of Insights' endpoint
    """
    endpoint_name = 'insights'

    def search(self, banner=None, filters=None, page=1):
        endpoint_action = 'search'
        search_params = {}

        if banner:
            search_params.update({'banner': banner})
        if filters:
            search_params.update({'filters': filters})
        if page:
            search_params.update({'page': page})

        response = self.request(endpoint_name=self.endpoint_name,
                                endpoint_action=endpoint_action,
                                params=search_params)
        return response

    def count(self, banner=None, filters=None):
        endpoint_action = 'count'
        count_params = {}

        if banner:
            count_params.update({'banner': banner})
        if filters:
            count_params.update({'filters': filters})

        response = self.request(endpoint_name=self.endpoint_name,
                                endpoint_action=endpoint_action,
                                params=count_params)
        return response


class Account(Base):
    """
    Implementation of Account' endpoint
    """
    endpoint_name = 'account'

    def status(self):
        endpoint_action = 'status'
        response = self.request(endpoint_name=self.endpoint_name,
                                endpoint_action=endpoint_action)
        return response


class Discovery(Base):
    """
    Discovery endpoint implementation
    """
    endpoint_name = 'scan'

    def host(self, port=None, protocol=None, ip_addresses=None):
        endpoint_action = 'host'
        post_data = {}

        if protocol:
            post_data.update({'protocol': protocol})
        if port:
            post_data.update({'port': port})
        if ip_addresses:
            post_data.update({'ips': ip_addresses})
        response = self.request(endpoint_name=self.endpoint_name,
                                endpoint_action=endpoint_action,
                                method='post',
                                data=post_data)
        return response

    def internet(self, protocol=None, port=None):
        endpoint_action = 'internet'
        post_data = {}

        if protocol:
            post_data.update({'protocol': protocol})
        if port:
            post_data.update({'port': port})
        response = self.request(endpoint_name=self.endpoint_name,
                                endpoint_action=endpoint_action,
                                method='post',
                                data=post_data)
        return response

    def status(self, job_id=None):
        endpoint_action = 'status'
        params = {}

        if job_id:
            params.update({'job_id': job_id})
        response = self.request(endpoint_name=self.endpoint_name,
                                endpoint_action=endpoint_action,
                                params=params)
        return response
