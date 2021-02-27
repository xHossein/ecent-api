from typing import List

from ecent.extractor import extract_short_course
from ecent.mixins.private import PrivateRequest
from ecent.types import ShortCourse


class AccountMixin(PrivateRequest):

    def my_courses(self) -> List[ShortCourse]:
        # TODO: handle access denied response
        home = self.private_request("").text
        return extract_short_course(home)
