from pydantic import BaseModel

class Student(BaseModel):
    id: int
    name: str
    class_name: str
    course: str
    university: str
