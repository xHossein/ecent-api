
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from ecent.constants import BASE_URL, BASE_HEADERS
from ecent.exceptions import (ClientLoginRequired, ClientSessionExpired,UnknownError,
                        ClientLoginRequired,WrongPassword,)

class PrivateRequest():
    def __init__(self, relogin: bool = None) -> None:
        self.session = requests.Session()
        self.session.headers = BASE_HEADERS
        self.is_authorized = False
        self.username = None
        self.password = None
        self.cookie = None
        self._auth = None
        self.relogin = relogin

    def private_request(self, endpoint, data=None, json=None,
                        fields=None, params=None, headers=None,
                        login_required = True
                        ):
        if login_required and not self.is_authorized:
            raise ClientLoginRequired("This method requires authentication.")

        if headers:
            self.session.headers.update(headers)

        response = None
        try:
            if data:
                response = self.session.post(BASE_URL.format(endpoint), data=data, params=params)
            elif json:
                response = self.session.post(BASE_URL.format(endpoint), json=json, params=params)
            elif fields:
                multipart_data = MultipartEncoder(fields=fields)
                response = self.session.post(BASE_URL.format(endpoint), data=multipart_data,
                                            headers={
                                                    **{'Content-Type': multipart_data.content_type},
                                                    **self.session.headers
                                                    }
                                            )
            else:
                response = self.session.get(BASE_URL.format(endpoint), params=params)
        except Exception as e: # TO DO
            raise UnknownError(e)

        for history in response.history:
            if history.status_code == 303 and '/login/' in history.url and login_required:
                if self.relogin:
                    logged = self._auth.login(self.username,self.password)
                    if not logged:
                        raise WrongPassword("It seems you changed your password.")
                    return self.private_request(endpoint, data, json, fields,
                                                params, headers, login_required)

                raise ClientSessionExpired("Session has expired, need to login again.")

        return response