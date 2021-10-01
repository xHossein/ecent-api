import re
from ecent.mixins.request import PrivateRequest

class Auth(PrivateRequest):
    def __init__(self, relogin: bool) -> None:
        super().__init__(relogin)
        self.cookie = None
        self._auth = self

    def login(self, username: str, password: str, retries: int = 0) -> bool:
        if retries > 3:
            return False

        if self.is_authorized:
            self.logout()

        self.username = username
        self.password = password

        login_response = self.private_request('login/index.php', login_required = False)
        login_token = (re.findall(r'name="logintoken" value="(.*?)"', login_response.text) or [None])[0]
        if not login_token:
            return self.login(username, password, retries + 1)

        payload = {
            'anchor': '',
            'logintoken': login_token,
            'username': username,
            'password': password
        }
        response = self.private_request('login/index.php',
                                        data = payload,
                                        login_required = False)

        self._update_cookie(response)
        if 'actionmenuaction' in response.text:
            self.is_authorized = True
            self.session_key = re.findall(r'logout.php\?sesskey=(.*?)"', response.text)[0]
            
        return self.is_authorized

    def logout(self) -> None:
        if self.is_authorized:
            self.is_authorized = False
            response = self.private_request('login/logout.php', params = f'sesskey={self.session_key}', login_required = False)
            self._update_cookie(response)
            
    def _update_cookie(self, response):
        """Update `MoodleSession` in login & logout"""
        self.cookie = {
            'Cookie': 'MoodleSession={};'.format(
                response.history[0].cookies.get('MoodleSession')
                )
            }
        self.session.headers.update(self.cookie)