from app.repositories.student_repository import StudentRepository
from app.services.student_service import StudentService

student_repository = StudentRepository()


def get_student_service() -> StudentService:
    return StudentService(repository=student_repository)
