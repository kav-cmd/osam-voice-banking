import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(80), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="user")
    created_at = Column(DateTime, default=datetime.utcnow)

    applications = relationship("LoanApplication", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")


class LoanApplication(Base):
    __tablename__ = "loan_applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    application_id = Column(String(40), unique=True, index=True, nullable=False)
    name = Column(String(120), nullable=False)
    pan_hash = Column(String(64), nullable=False)
    phone_encrypted = Column(String(255), nullable=False)
    email_hash = Column(String(64), nullable=False)
    dob = Column(String(20), nullable=False)
    income = Column(Float, default=0)
    existing_emi = Column(Float, default=0)
    amount = Column(Float, default=0)
    tenure = Column(Integer, default=36)
    employment = Column(String(40), default="salaried")
    company = Column(String(120), default="")
    docs = Column(Text, default="")
    purpose = Column(String(200), default="Personal Loan")
    status = Column(String(20), default="submitted")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="applications")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    account_number = Column(String(20), nullable=False)
    txn_type = Column(String(10), nullable=False)
    amount = Column(Float, nullable=False)
    description = Column(String(200), default="")
    balance_after = Column(Float, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="transactions")
