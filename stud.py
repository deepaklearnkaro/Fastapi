from fastapi import FastAPI, HTTPException # type: ignore
from pydantic import BaseModel # type: ignore
from typing import List

app = FastAPI()


class Student(BaseModel):
    id: int
    name: str
    class_name: str
    course: str
    university: str


students_db = []


@app.get("/students", response_model=List[Student])
def get_students():
    return students_db


@app.get("/students/{student_id}", response_model=Student)
def get_student(student_id: int):
    for student in students_db:
        if student.id == student_id:
            return student
    raise HTTPException(status_code=404, detail="Student not found")


@app.post("/students", response_model=Student)
def create_student(student: Student):
    for existing_student in students_db:
        if existing_student.id == student.id:
            raise HTTPException(status_code=400, detail="ID already exists")
    students_db.append(student)
    return student


@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, updated_student: Student):
    for index, student in enumerate(students_db):
        if student.id == student_id:
            students_db[index] = updated_student
            return updated_student
    raise HTTPException(status_code=404, detail="Student not found")

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for index, student in enumerate(students_db):
        if student.id == student_id:
            del students_db[index]
            return {"message": "Student deleted successfully"}
    raise HTTPException(status_code=404, detail="Student not found")


@app.get("/")
def home():
    return {"message": "Welcome to the FastAPI Student API"}
