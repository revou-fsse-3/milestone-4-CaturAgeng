# models/account.py

from db import db
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, DECIMAL, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

class AccountModel(db.Model):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    account_type = Column(Enum("savings", "checking", name="account_type_enum"), nullable=False)
    account_number = Column(String(255), default=lambda: "NFR-" + str(uuid.uuid4())[:8])
    balance = Column(DECIMAL(10, 2), nullable=False, default=0.0)
    created_at = Column(DateTime(timezone=True),nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True),nullable=False, server_default=func.now(), onupdate=func.now())

    # Define relationship with User
    user = relationship("UserModel", back_populates="accounts")

    # Define relationship with Transaction
    transactions_sent = relationship('TransactionModel', foreign_keys='TransactionModel.from_account_id', back_populates='from_account')
    transactions_received = relationship('TransactionModel', foreign_keys='TransactionModel.to_account_id', back_populates='to_account')