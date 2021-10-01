from typing import List, Optional
from pydantic import BaseModel

class ShortCourse(BaseModel):
    id: str
    link: str
    title: str
    master: str


class Resource(BaseModel):
    id: str
    link: str
    title: str
    size: str
    type: str

class Url(BaseModel):
    id: str
    link: str
    title: str

class Assignment(BaseModel):
    id: str
    link: str
    title: str
    is_submitted: bool
    deadline: str
    remaining_time :Optional[str]
    last_change: Optional[str]

class ShortAssignment(BaseModel):
    id: str
    link: str
    title: str

class Course(BaseModel):
    id: str
    link: str
    title: str
    adobe_connect: Optional[str]
    urls: List[Url]
    resources: List[Resource]
    short_assignments: List[ShortAssignment]