from typing import Union
from ecent.extractor import extract_assignment
from ecent.mixins.request import PrivateRequest
from ecent.types import Assignment

class AssignmentMixin(PrivateRequest):
    def get_assignment(self, id: Union[int, str]) -> Assignment:
        response = self.private_request(f'mod/assign/view.php?id={str(id)}')
        return extract_assignment(response.text)