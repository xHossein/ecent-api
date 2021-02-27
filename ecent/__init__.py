from ecent.mixins.assignment import AssignmentMixin
from ecent.mixins.account import AccountMixin
from ecent.mixins.course import CourseMixin
from ecent.mixins.auth import Auth

class Client(Auth,
            AccountMixin,
            AssignmentMixin,
            CourseMixin,
            ):
    def __init__(self) -> None:
        super().__init__()

    
