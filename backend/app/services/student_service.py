from __future__ import annotations

from typing import Optional

from fastapi import HTTPException, status

from app.repositories.student_repository import StudentRepository
from app.schemas.student import StudentCreate, StudentQuery, StudentRead, StudentUpdate


class StudentService:
    def __init__(self, repository: StudentRepository) -> None:
        self._repository = repository

    def list_students(
        self,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        min_age: Optional[int] = None,
        max_age: Optional[int] = None,
    ) -> list[StudentRead]:
        students = [StudentRead.model_validate(student) for student in self._repository.list()]

        if first_name is not None:
            first_name_lower = first_name.lower()
            students = [student for student in students if student.first_name.lower() == first_name_lower]

        if last_name is not None:
            last_name_lower = last_name.lower()
            students = [student for student in students if student.last_name.lower() == last_name_lower]

        if email is not None:
            email_lower = email.lower()
            students = [student for student in students if student.email.lower() == email_lower]

        if min_age is not None:
            students = [student for student in students if student.age >= min_age]

        if max_age is not None:
            students = [student for student in students if student.age <= max_age]

        return students

    def query_students(self, query: StudentQuery) -> list[StudentRead]:
        return self.list_students(
            first_name=query.first_name,
            last_name=query.last_name,
            email=query.email,
            min_age=query.min_age,
            max_age=query.max_age,
        )

    def get_student(self, student_id: int) -> StudentRead:
        student = self._repository.get(student_id)
        if student is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
        return StudentRead.model_validate(student)

    def create_student(self, payload: StudentCreate) -> StudentRead:
        student = self._repository.create(payload.model_dump())
        return StudentRead.model_validate(student)

    def update_student(self, student_id: int, payload: StudentUpdate) -> StudentRead:
        student = self._repository.update(student_id, payload.model_dump())
        if student is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
        return StudentRead.model_validate(student)

    def delete_student(self, student_id: int) -> None:
        deleted = self._repository.delete(student_id)
        if not deleted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
