
from typing import List
from ecent.types import ShortCourse
from ecent.extractor import extract_short_course
from ecent.mixins.private import PrivateRequest

class AccountMixin(PrivateRequest):
    
    def my_courses(self) -> List[ShortCourse]:
        home = self.private_request("").text
        return extract_short_course(home)
  