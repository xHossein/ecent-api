import re

from ecent.mixins.private import PrivateRequest


class Auth(PrivateRequest):
    def __init__(self) -> None:
        super().__init__()
        self.cookie = None
        self._auth = self

    def login(self, username: str, password: str) -> bool:
        self.username = username
        self.password = password
        logintoken = re.findall(r'name="logintoken" value="(.*?)"',
                                self.private_request('login/index.php',
                                                     need_login=False).text)[0]

        response = self.private_request('login/index.php',
                                        data=f'anchor=&logintoken={logintoken}&username={username}&password={password}',
                                        need_login=False)

        if 'actionmenuaction' in response.text:
            ses_key = re.findall(r'logout.php\?sesskey=(.*?)"', response.text)
            self.session_key = ses_key[0] if len(ses_key) > 0 else None
            self.authorized = True

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
