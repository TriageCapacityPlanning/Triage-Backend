class FileError(Exception):
    """
    An exception class to raise an file exception when uploading to the api with
    a file has failed as seen in the Flask documentation.
    """
    status_code = 422

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """
        Convert the exception information to a dictionary.
        """
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


class Unauthorized(Exception):
    """
    An exception class to raise an unauthorized exception for unauthenticated or
    unprivileged users on protected endpoints as seen in the Flask documentation.
    """
    status_code = 401

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """
        Convert the exception information to a dictionary.
        """
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv
