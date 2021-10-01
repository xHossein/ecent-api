from typing import Union
from ecent.extractor import extract_course
from ecent.types import Course
from ecent.mixins.request import PrivateRequest

class CourseMixin(PrivateRequest):
    def get_course(self, id: Union[int, str]) -> Course:
        """return course's assignment ids"""
        response = self.private_request(f'course/view.php?id={str(id)}')
        return extract_course(response.text)


