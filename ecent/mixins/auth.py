import re

from ecent.mixins.private import PrivateRequest


class Auth(PrivateRequest):
    def __init__(self) -> None:
        super().__init__()
        self.cookie = None
        self._auth = self

    def login(self, username: str, password: str, retries: int = 0) -> bool:
        # prevent infinite recursion
        if retries > 3:
            return False

        if self.authorized:
            self.logout()

        self.username = username
        self.password = password

        login_response = self.private_request('login/index.php', need_login=False)
        login_token = (re.findall(r'name="logintoken" value="(.*?)"', login_response.text) or [None])[0]
        if not login_token:
            return False

        data = f'anchor=&logintoken={login_token}&username={username}&password={password}'
        response = self.private_request('login/index.php',
                                        data=data,
                                        need_login=False)

        self.cookie = {
            'Cookie': 'MoodleSession={};'.format(
                response.history[0].cookies.get('MoodleSession')
                )
            }

        self.private.headers.update(self.cookie)
        if 'actionmenuaction' in response.text:
            self.authorized = True
            self.session_key = (re.findall(r'logout.php\?sesskey=(.*?)"', response.text) or [None])[0]
        else:
            self.login(username, password, retries + 1)

        return self.authorized

    def logout(self) -> None:
        if self.authorized:
            self.authorized = False
            response = self.private_request('login/logout.php', params=f'sesskey={self.session_key}', need_login=False)
            self.cookie = {
                'Cookie': 'MoodleSession={};'.format(
                    response.history[0].cookies.get('MoodleSession')
                )
            }
            self.private.headers.update(self.cookie)
