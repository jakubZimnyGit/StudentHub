from hmac import new
from click import group
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas
from .. database import get_session

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.post('/', response_model=schemas.UserCreateOut)
def create_user(user: schemas.UserCreate, session: Session = Depends(get_session)):
    try:
        new_user = models.User(name = user.name, last_name = user.last_name)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    if user.role == 'student':
        new_student = models.Student(id = new_user.id, group = user.group, semester = user.semester)
        session.add(new_student)
        session.commit()
        new_user.group = new_student.group
        new_user.semester = new_student.semester
        
        return new_user
    else:
        new_teacher = models.Teacher(id = new_user.id, subject = user.subject)
        session.add(new_teacher)
        session.commit()
        new_user.subject = new_teacher.subject
        return new_user