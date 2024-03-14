from db import db
from models.common import CommonModel
from sqlalchemy import Column, Integer, String, Enum


class UserModel(CommonModel):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}  

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(256), nullable=False)
    role = Column(Enum("admin", "user", name="role_enum"), nullable=False)

    
