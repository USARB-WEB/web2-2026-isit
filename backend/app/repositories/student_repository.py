from __future__ import annotations

from collections.abc import Iterable
from copy import deepcopy


class StudentRepository:
    def __init__(self) -> None:
        self._students: dict[int, dict[str, object]] = {}
        self._next_id = 1

    def list(self) -> list[dict[str, object]]:
        return [deepcopy(student) for student in self._students.values()]

    def get(self, student_id: int) -> dict[str, object] | None:
        student = self._students.get(student_id)
        if student is None:
            return None
        return deepcopy(student)

    def create(self, student_data: dict[str, object]) -> dict[str, object]:
        student = deepcopy(student_data)
        student["id"] = self._next_id
        self._students[self._next_id] = student
        self._next_id += 1
        return deepcopy(student)

    def update(self, student_id: int, student_data: dict[str, object]) -> dict[str, object] | None:
        if student_id not in self._students:
            return None
        student = deepcopy(student_data)
        student["id"] = student_id
        self._students[student_id] = student
        return deepcopy(student)

    def delete(self, student_id: int) -> bool:
        if student_id not in self._students:
            return False
        del self._students[student_id]
        return True

    def replace_all(self, students: Iterable[dict[str, object]]) -> None:
        self._students = {int(student["id"]): deepcopy(student) for student in students}
        self._next_id = max(self._students, default=0) + 1
