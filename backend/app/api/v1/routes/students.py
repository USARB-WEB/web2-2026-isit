from typing import Optional

from fastapi import APIRouter, Depends, Query, Response, status

from app.api.v1.dependencies.students import get_student_service
from app.schemas.student import StudentCreate, StudentQuery, StudentRead, StudentUpdate
from app.services.student_service import StudentService

router = APIRouter(prefix="/students", tags=["students"])


@router.get("", response_model=list[StudentRead])
def list_students(service: StudentService = Depends(get_student_service)) -> list[StudentRead]:
    return service.list_students()


@router.get("/query", response_model=list[StudentRead])
def query_students(
    service: StudentService = Depends(get_student_service),
    first_name: Optional[str] = Query(default=None, description="Filter by exact first name"),
    last_name: Optional[str] = Query(default=None, description="Filter by exact last name"),
    email: Optional[str] = Query(default=None, description="Filter by exact email"),
    min_age: Optional[int] = Query(default=None, ge=16, le=120, description="Minimum age"),
    max_age: Optional[int] = Query(default=None, ge=16, le=120, description="Maximum age"),
) -> list[StudentRead]:
    return service.list_students(
        first_name=first_name,
        last_name=last_name,
        email=email,
        min_age=min_age,
        max_age=max_age,
    )


@router.api_route(
    "",
    methods=["QUERY"],
    response_model=list[StudentRead],
    summary="Query students",
    description=(
        "Filters students with a JSON body instead of the query string. QUERY is safe "
        "and idempotent like GET, but it accepts a body, so long or complex filters do "
        "not have to be URL-encoded. An empty JSON object `{}` returns every student."
    ),
)
def query_students_with_body(
    payload: StudentQuery,
    service: StudentService = Depends(get_student_service),
) -> list[StudentRead]:
    return service.query_students(payload)


@router.get("/{student_id}", response_model=StudentRead)
def get_student(student_id: int, service: StudentService = Depends(get_student_service)) -> StudentRead:
    return service.get_student(student_id)


@router.post("", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
def create_student(
    payload: StudentCreate,
    service: StudentService = Depends(get_student_service),
) -> StudentRead:
    return service.create_student(payload)


@router.put("/{student_id}", response_model=StudentRead)
def update_student(
    student_id: int,
    payload: StudentUpdate,
    service: StudentService = Depends(get_student_service),
) -> StudentRead:
    return service.update_student(student_id, payload)


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(
    student_id: int,
    service: StudentService = Depends(get_student_service),
) -> Response:
    service.delete_student(student_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
