from db import db
from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class TransactionModel(db.Model):
    __tablename__ = "transactions"

    id = db.Column(Integer, primary_key=True)
    from_account_id = db.Column(Integer, ForeignKey("accounts.id"))
    to_account_id = db.Column(Integer, ForeignKey("accounts.id"))
    amount = db.Column(DECIMAL(10, 2), nullable=False)
    type = db.Column(String(255), nullable=False)
    description = db.Column(String(255))
    created_at = db.Column(DateTime(timezone=True), server_default=func.now())

    # Define relationships with Accounts
    # from_account = relationship("AccountModel", foreign_keys=[from_account_id], back_populates="outgoing_transactions")
    # to_account = relationship("AccountModel", foreign_keys=[to_account_id], back_populates="incoming_transactions")
