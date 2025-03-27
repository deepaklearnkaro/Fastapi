from fastapi import APIRouter, HTTPException, Depends
from app.models import Student
from app.database import get_connection
from typing import List

router = APIRouter()

@router.get("/students", response_model=List[Student])
def get_students():
    conn = get_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM students;")
            students = cur.fetchall()
        conn.close()
        return students
    raise HTTPException(status_code=500, detail="Database connection failed")

@router.get("/students/{student_id}", response_model=Student)
def get_student(student_id: int):
    conn = get_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM students WHERE id = %s;", (student_id,))
            student = cur.fetchone()
        conn.close()
        if student:
            return student
    raise HTTPException(status_code=404, detail="Student not found")

@router.post("/students", response_model=Student)
def create_student(student: Student):
    conn = get_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO students (id, name, class_name, course, university) VALUES (%s, %s, %s, %s, %s) RETURNING *;",
                (student.id, student.name, student.class_name, student.course, student.university),
            )
            new_student = cur.fetchone()
        conn.commit()
        conn.close()
        return new_student
    raise HTTPException(status_code=500, detail="Database connection failed")

@router.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, updated_student: Student):
    conn = get_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE students SET name = %s, class_name = %s, course = %s, university = %s WHERE id = %s RETURNING *;",
                (updated_student.name, updated_student.class_name, updated_student.course, updated_student.university, student_id),
            )
            updated = cur.fetchone()
        conn.commit()
        conn.close()
        if updated:
            return updated
    raise HTTPException(status_code=404, detail="Student not found")

@router.delete("/students/{student_id}")
def delete_student(student_id: int):
    conn = get_connection()
    if conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM students WHERE id = %s RETURNING id;", (student_id,))
            deleted_id = cur.fetchone()
        conn.commit()
        conn.close()
        if deleted_id:
            return {"message": "Student deleted successfully"}
    raise HTTPException(status_code=404, detail="Student not found")
