from flask_login import UserMixin
from app.db import Base
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import Column, Integer, String

# Admin class that is used for Sasha's front-end login implementation
class AdminUser(Base, UserMixin, SerializerMixin):
    __tablename__ = 'admins'
    id = Column(Integer, primary_key=True)
    username = Column(String(20), nullable=False, unique = True)
    password = Column(String(80), nullable=False)