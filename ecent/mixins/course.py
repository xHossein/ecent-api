from typing import Union
from ecent.extractor import extract_course, extract_join_link
from ecent.types import Course
from ecent.mixins.request import PrivateRequest

class CourseMixin(PrivateRequest):
    def get_course(self, id: Union[int, str]) -> Course:
        """return course's assignment ids"""
        response = self.private_request(f'course/view.php?id={str(id)}')
        return extract_course(response.text)
    
    def get_online_session_link(self, adobe_connect_link: str):
        response = self.private_request(adobe_connect_link.split('guilan.ac.ir/')[1])
        join_link = extract_join_link(response.text)
        response = self.private_request(join_link.split('guilan.ac.ir/')[1])
        return response.history[0].headers.get('Location')
  

