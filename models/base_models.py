"""
This file defines:
1. Base - every table in our database needs to be built on top of this.
2. Customer - the table that stores each bank customer's info.
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

# Base is like a blueprint template - every table class we write
# will say "class X(Base)" to become an actual MySQL table.
Base = declarative_base()


class Customer(Base):
    """One row in this table = one bank customer."""

    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # This line is what creates the relationship between the two tables.
    # It means: "a Customer can have many Accounts."
    # cascade="all, delete-orphan" means: if a customer is deleted,
    # their accounts get deleted too (no orphaned accounts left behind).
    accounts = relationship(
        "Account", back_populates="customer", cascade="all, delete-orphan"
    )
