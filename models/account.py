# models/account.py

from db import db
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, UniqueConstraint, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class AccountModel(db.Model):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    account_type = Column(String(255), nullable=False)
    account_number = Column(String(255), unique=True, nullable=False)
    balance = Column(DECIMAL(10, 2), nullable=False, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Define relationship with User
    user = relationship("UserModel", back_populates="accounts")

    # Ensure uniqueness of (user_id, account_type)
    __table_args__ = (
        UniqueConstraint('user_id', 'account_type', name='_user_account_type_uc'),
    )

