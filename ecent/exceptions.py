class ClientError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ClientLoginRequired(ClientError):
    pass

class PrivateError(ClientError):
    """For Private API"""
    
class BadCredentials(PrivateError):
    pass

class UnknownError(PrivateError):
    pass

