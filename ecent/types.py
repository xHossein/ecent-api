from typing import List, Optional
from pydantic import BaseModel
from pydantic.networks import HttpUrl

class ShortCourse(BaseModel):
    id: str
    link: HttpUrl
    title: str
    master: str


class Resource(BaseModel):
    id: str
    link: HttpUrl
    title: str
    size: str
    type: str

class Url(BaseModel):
    id: str
    link: HttpUrl
    title: str

class Assignment(BaseModel):
    id: str
    title: str
    status: str
    deadline: str
    remaining_time :str
    last_change: Optional[str]

class ShortAssignment(BaseModel):
    id: str
    link: HttpUrl
    title: str

class Course(BaseModel):
    id: str
    link: HttpUrl
    title: str
    adobe_connect: Optional[HttpUrl]
    urls: List[Url]
    resources: List[Resource]
    assignments: List[ShortAssignment]