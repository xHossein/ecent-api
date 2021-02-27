
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from ecent.constants import BASE_URL, BASE_HEADERS
from ecent.exceptions import (ClientLoginRequired,UnknownError,
                        ClientLoginRequired,WrongPassword,)

class PrivateRequest():
    def __init__(self) -> None:
        self.private = requests.Session()
        self.private.headers = BASE_HEADERS
        self.authorized = False
        self.username = None
        self.password = None
        self._auth = None

    def private_request(self,endpoint,data=None,json=None,fields=None,
                            params=None,headers=None,need_login=True):
        if need_login and not self.authorized:
            raise ClientLoginRequired("to use this method, you need to login first.")

        if headers:
            self.private.headers.update(headers)

        response = None
        try:
            if data:
                response = self.private.post(BASE_URL.format(endpoint), data=data, params=params)
            elif json:
                response = self.private.post(BASE_URL.format(endpoint), json=json, params=params)
            elif fields:
                multipart_data = MultipartEncoder(fields=fields)
                response = self.private.post(BASE_URL.format(endpoint), data=multipart_data,
                                            headers={
                                                    **{'Content-Type': multipart_data.content_type},
                                                    **self.private.headers
                                                    }
                                            )
            else:
                response = self.private.get(BASE_URL.format(endpoint), params=params)
        except Exception as e: # TO DO
            raise UnknownError(e)

        if 'forgot_password.php' in response.text and need_login:
            isCorrenctPassword = self._auth.login(self.username,self.password)
            if not isCorrenctPassword:
                raise WrongPassword("it seems you changed your password.")
            return self.private_request(endpoint,data,json,fields,
                                params,headers,need_login)

        else:
            return response