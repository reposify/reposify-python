import json


class HTTPException(Exception):
    def __init__(self, response, *args, **kwargs):
        try:
            errors = json.loads(response.content.decode('utf8'))['errors']
            message = '\n'.join([error['message'] for error in errors])
        except Exception:
            if hasattr(response, 'status_code') and response.status_code == 401:
                message = response.content.decode('utf8')
            else:
                message = response
        super(HTTPException, self).__init__(message, *args, **kwargs)


class BadRequestMethod(Exception):
    pass


class BadResponse(Exception):
    pass


class DeleteError(Exception):
    pass


class HTTPBadRequest(HTTPException):
    """
    400
    """
    pass


class HTTPUnauthorized(HTTPException):
    """
    401
    """
    pass


class HTTPForbidden(HTTPException):
    """
    403
    """
    pass


class HTTPNotFound(HTTPException):
    """
    404
    """
    pass


class HTTPConflict(HTTPException):
    """
    409
    """
    pass


class HTTPTooManyRequests(HTTPException):
    """
    429
    """
    pass


class HTTPServerError(HTTPException):
    """
    500
    """
    pass
