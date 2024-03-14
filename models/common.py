from db import db
from flask_smorest import abort
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

class CommonModel(db.Model):
    __abstract__ = True

    @classmethod
    def get_items(cls):
        return cls.query.all()

    @classmethod
    def get_item(cls, item_id):
        item = cls.query.get(item_id)
        if item is None:
            abort(404, message=f"{cls.__name__} not found")
        return item

    def add_item(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete_item(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def update_item(self, item_data):
        try:
            for key, value in item_data.items():
                setattr(self, key, value)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

class UserModel(CommonModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    @classmethod
    def create(cls, username, email, password_hash):
        user = cls(username=username, email=email, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        return user