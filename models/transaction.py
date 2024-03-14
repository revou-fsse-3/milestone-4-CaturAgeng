from db import db
from sqlalchemy import Column, Integer, String, ForeignKey, DECIMAL, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

class TransactionModel(db.Model):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    from_account_id = Column(Integer, ForeignKey("accounts.id"))
    to_account_id = Column(Integer, ForeignKey("accounts.id"))
    amount = Column(DECIMAL(10, 2), nullable=False)
    type = Column(String(255), nullable=False)
    description = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Define relationships with Accounts
    from_account = relationship("AccountModel", foreign_keys=[from_account_id], back_populates="outgoing_transactions")
    to_account = relationship("AccountModel", foreign_keys=[to_account_id], back_populates="incoming_transactions")
