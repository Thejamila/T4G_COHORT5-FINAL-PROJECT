"""
This file defines the Account table.

In your original terminal project, BankAccount was a Python class
that lived only in memory (accounts = {} dict) and disappeared when
the program closed. Here, Account is a real MySQL table - every
account created through the API is saved permanently.

Instead of having two separate tables for "bank account" and
"savings account", we use ONE accounts table with an account_type
column that says whether it's "bank" or "savings". This keeps things
simple while still meeting the "2 tables with a relationship"
requirement (Customer <-> Account).
"""

import enum

from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from models.base_models import Base


class AccountType(str, enum.Enum):
    bank = "bank"
    savings = "savings"


class Account(Base):
    """One row in this table = one bank or savings account."""

    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)

    # This is the "foreign key" - it links every account back to exactly
    # one customer, using that customer's id number.
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)

    account_type = Column(Enum(AccountType), nullable=False, default=AccountType.bank)
    balance = Column(Float, nullable=False, default=100.0)

    # Only filled in when account_type is "savings" - see savings_account.py
    interest_rate = Column(Float, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # The other half of the relationship defined in Customer.
    customer = relationship("Customer", back_populates="accounts")
