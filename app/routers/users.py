from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from .. database import get_session
from typing import Optional

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.get('/teachers', response_model=List[schemas.TeacherOut])
def getTeachers(session: Session = Depends(get_session),
                subject: Optional[str] = None):
    
    query = session.query(
            models.User.name,
            models.User.last_name,
            models.User.email,
            models.Teacher.subject.label("subject"),
        ).join(models.Teacher, models.User.id == models.Teacher.id)

    if subject:
        query = query.filter(models.Teacher.subject == subject)

    teachers = query.all()
    return teachers

@router.get('/students', response_model=List[schemas.StudentOut])
def getStudents(session: Session = Depends(get_session),
                group: Optional[str] = None,
                semester: Optional[int] = None):
    
    query = session.query(
            models.User.name,
            models.User.last_name,
            models.User.email,
            models.Student.group.label("group"),
            models.Student.semester.label("semester"),
        ).join(models.Student, models.User.id == models.Student.id)

    if group:
        query = query.filter(models.Student.group == group)
    if semester:
        query = query.filter(models.Student.semester == semester)

    students = query.all()
    return students

@router.get('/', response_model=List[schemas.UserOut])
def getUsers(session: Session = Depends(get_session)):

    users = (
        session.query(
            models.User.id,
            models.User.name,
            models.User.last_name,
            models.User.email,
            models.User.role,
            models.Student.group.label("group"),
            models.Student.semester.label("semester"),
            models.Teacher.subject.label("subject")
        )
        .join(models.Student, models.User.id == models.Student.id, isouter=True) 
        .join(models.Teacher, models.User.id == models.Teacher.id, isouter=True) 
        .all() 
    )
    
    return users

@router.get('/{id}', response_model=schemas.UserOut)
def getUser(id: int, session: Session = Depends(get_session)):

    user, student, teacher = (
        session.query(models.User, models.Student, models.Teacher)
        .outerjoin(models.Student, models.User.id == models.Student.id)
        .outerjoin(models.Teacher, models.User.id == models.Teacher.id)
        .filter(models.User.id == id)
        .first()
    )

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_dict = user.__dict__.copy()

    
    if student:
        user_dict.update({k: v for k, v in student.__dict__.items()})
    if teacher:
        user_dict.update({k: v for k, v in teacher.__dict__.items()})

    return user_dict
           

@router.post('/', response_model=schemas.UserCreateOut, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, session: Session = Depends(get_session)):
    try:
        new_user = models.User(name = user.name, last_name = user.last_name, role=user.role)
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


