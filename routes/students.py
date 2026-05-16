from fastapi import APIRouter, HTTPException, status, Request
from pymongo.errors import DuplicateKeyError
from util.helper import parse_objectid
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from database.mongo import (
    create_student,
    get_all_students,
    get_student_by_id,
    update_student,
    delete_student,
    create_students_bulk,
)

from models.student import (
    StudentCreate,
    StudentUpdate,
    StudentResponse,
)


router = APIRouter()

templates = Jinja2Templates("templates")


@router.post(
    "/",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_new_student(student: StudentCreate):
    st = None
    try:
        st = create_student(student)
    except DuplicateKeyError as de:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=de.details)
    return st

@router.get(
    "/",
    response_model=list[StudentResponse]
)
def list_students():
    return get_all_students()


@router.get(
    "/{student_id}",
    response_model=StudentResponse
)
def get_student(student_id: str):
    student_id = parse_objectid(student_id)
    student = get_student_by_id(student_id)

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    return student




@router.patch(
    "/{student_id}",
    response_model=StudentResponse
)
def update_existing_student(student_id: str, student: StudentUpdate):
    student_id = parse_objectid(student_id)
    updated_student = update_student(student_id, student)

    if not updated_student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    return updated_student


@router.delete(
    "/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def remove_student(student_id: str):
    student_id = parse_objectid(student_id)
    was_deleted = delete_student(student_id)

    if not was_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    return None


@router.post(
    "/bulk",
    response_model=list[StudentResponse],
    status_code=status.HTTP_201_CREATED
)
def create_students(students: list[StudentCreate]):
    return create_students_bulk(students)

@router.get(
    "/partial/table",
    response_class=HTMLResponse,
    summary="Render html table for students"
)
def root(request: Request):
    """
    Renderiza el archivo templates/index.html
    """
    return templates.TemplateResponse(
        request=request,
        name="partials/students_table.html",
        context={"students":get_all_students()}
    )