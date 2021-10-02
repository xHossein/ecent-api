from typing import List

from ecent.extractor import extract_grades, extract_short_course
from ecent.mixins.request import PrivateRequest
from ecent.types import Grade, ShortCourse


class AccountMixin(PrivateRequest):

    def courses(self) -> List[ShortCourse]:
        # TODO: handle access denied response
        home = self.private_request("").text
        return extract_short_course(home)

    def grades(self) -> List[Grade]:
        response = self.private_request("grade/report/overview/index.php")
        return extract_grades(response.text)