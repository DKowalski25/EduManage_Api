import pytest
from dependency_injector.wiring import Provide, inject

from apps.events.schemas import mark as markschemas, assignment as assignmentschemas
from apps.events.storages import mark_storage as mstorage, AssignmentStorage
from apps.users.storages import UserStorage
from apps.users import schemas as userschemas


@pytest.fixture
@inject
async def student_data(user_storage: UserStorage = Provide["user_storage"]):
    student_create = userschemas.UserCreate(
        first_name="Test",
        last_name="Student",
        email="student@example.com",
        phone_number="1234567890",
        role="student",
        password="password123"
    )
    student = await user_storage.create_user(student_create)
    return student


@pytest.fixture
@inject
async def assignment_data(student_data, assignment_storage: AssignmentStorage = Provide["assignment_storage"]):
    assignment_create = assignmentschemas.AssignmentCreate(
        title="Test Assignment",
        description="Test Description",
        due_date="2024-12-31",
        teacher_id=student_data.id,  # Assuming the teacher is also created similarly
        type="homework"
    )
    assignment = await assignment_storage.create_assignment(assignment_create)
    return assignment


@pytest.fixture
def mark_data():
    return markschemas.MarkCreate(
        value=5,
        student_id=1,
        assignment_id=1
    )


@pytest.mark.with_db
@inject
async def test_mark_creation(
        mark_data: markschemas.MarkCreate,
        mark_storage: mstorage.MarkStorage = Provide["mark_storage"],
):
    create_mark = await mark_storage.create_mark(mark_data)

    assert create_mark.id is not None

    assert create_mark.value == mark_data.value
    assert create_mark.student_id == mark_data.student_id
    assert create_mark.assignment_id == mark_data.assignment_id
