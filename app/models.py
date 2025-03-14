from http import server
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from . utils import generate_password

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    def __init__(self, name, last_name):
        self.name = name
        self.last_name = last_name
        self.email = f"{name}.{last_name}@StudentHub.com"
        self.password = generate_password()


class Student(Base):
    __tablename__ = 'students'
    
    id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True, index=True)
    semester = Column(Integer, nullable=False, default=1)
    group = Column(String, nullable=False)
    
    user = relationship('User')

class Teacher(Base):
    __tablename__ = 'teachers'
    
    id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True, index=True)
    subject = Column(String, nullable=False)
    
    user = relationship('User')

class Grade(Base):
    __tablename__ = 'grades'
    
    student_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    subject = Column(String, nullable=False, primary_key=True)
    grade = Column(Integer, nullable=False)
    teacher_id = Column(Integer, ForeignKey('teacher.id', ondelete='CASCADE'))
    
    