from hmac import new
from re import U
from click import group
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from .. database import get_session

router = APIRouter(
    prefix='/users',
    tags=['Users']
)



@router.post('/', response_model=schemas.UserCreateOut)
def create_user(user: schemas.UserCreate, session: Session = Depends(get_session)):
    try:
        new_user = models.User(name = user.name, last_name = user.last_name)
        not_hashed_password = new_user.password
        new_user.password = utils.hash_password(new_user.password)
        session.add(new_user); session.commit(); session.refresh(new_user)
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")

    if user.role == 'student':
        return addStudent(new_user, user, session, not_hashed_password)
        
    else:
        return addTeacher(new_user, user, session, not_hashed_password)                          
    
    """
        This is to return the password to the user not hashed for testing purposes, in production this should be removed
        and the user should be forced to reset his password after creating the account, by getting an email with a link to reset the password
    """

            #user data from db      #user data from request body
        #           ||                    ||
        #           V                     V
def addStudent(user: models.User, User_info: schemas.UserCreate, session: Session, not_hashed_password):
    new_student = models.Student(id = user.id, group = User_info.group, semester = User_info.semester)
    session.add(new_student); session.commit()
    user.group = new_student.group
    user.semester = new_student.semester
    user.password = not_hashed_password
    return user

def addTeacher(user: models.User, User_info: schemas.UserCreate, session: Session, not_hashed_password):
    new_teacher = models.Teacher(id = user.id, subject = User_info.subject)
    session.add(new_teacher); session.commit()
    user.subject = new_teacher.subject
    user.password = not_hashed_password
    return user



"""
added hashing functionality, divided the create_user endpoint into two functions. 
"""