from ecent.extractor import extract_assignment
from ecent.mixins.private import PrivateRequest
from ecent.types import Assignment

class AssignmentMixin(PrivateRequest):
    def get_assignment(self,id:str) -> Assignment:
        response = self.private_request(f'mod/assign/view.php?id={id}')
        return extract_assignment(response.text)