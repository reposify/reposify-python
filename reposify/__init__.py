import requests
import reposify.exceptions


class Base(object):
    base_url = 'https://api.reposify.com'

    def request(self, token, endpoint, version=1, params=None, data=None, method='get'):
        """
        Returns a json object containing the requested resource
        """
        request_params = {"token": token}
        if params:
            request_params.update(params)

        if method == 'get':
            response = requests.get(self.compose_url(endpoint, version), params=request_params)
        elif method == 'post':
            response = requests.post(self.compose_url(endpoint, version), data=data, params=request_params)
        else:
            raise exceptions.BadRequestMethod

        if response.status_code == 401:
            raise exceptions.HTTPUnauthorized(response)
        elif response.status_code == 403:
            raise exceptions.HTTPForbidden(response)
        elif response.status_code == 404:
            raise exceptions.HTTPNotFound(response)
        elif response.status_code == 409:
            raise exceptions.HTTPConflict(response)
        elif response.status_code == 429:
            raise exceptions.HTTPTooManyRequests(response)
        elif response.status_code >= 500:
            raise exceptions.HTTPServerError(response)
        elif response.status_code >= 400:
            raise exceptions.HTTPBadRequest(response)

        return response.json()

    def compose_url(self, endpoint, version):
        """
        Returns the uri for an endpoint
        """
        return '{base_url}/v{version}/{endpoint}'.format(base_url=self.base_url, version=version, endpoint=endpoint)


class Insights(Base):
    """
    Implementation of Insights' endpoint
    """

    def __init__(self, token):
        self.token = token
        self.params = {}

    def search(self, banner=None, filters=None, page=1):
        search_params = self.params

        if banner:
            search_params.update({'banner': banner})
        if filters:
            search_params.update({'filters': filters})
        if page:
            search_params.update({'page': page})

        response = self.request(token=self.token, endpoint='insights/search', params=search_params)
        return response

    def count(self, banner=None, filters=None):
        count_params = self.params

        if banner:
            count_params.update({'banner': banner})
        if filters:
            count_params.update({'filters': filters})

        response = self.request(token=self.token, endpoint='insights/count', params=count_params)
        return response


class Account(Base):
    """
    Implementation of Account' endpoint
    """

    def __init__(self, token):
        self.token = token
        self.params = {}

    def status(self):
        response = self.request(token=self.token, endpoint='account/status')
        return response
