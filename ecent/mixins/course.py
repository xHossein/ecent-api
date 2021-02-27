from ecent.extractor import extract_course
from ecent.types import Course
from ecent.mixins.private import PrivateRequest

class CourseMixin(PrivateRequest):
    def get_course(self,id:str) -> Course:
        """return course's assignments id"""
        response = self.private_request(f'course/view.php?id={id}')
        return extract_course(response.text)


