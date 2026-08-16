"""
This file defines what a valid request or response looks like.

FastAPI uses these to:
1. Reject bad input automatically (e.g. someone sends balance as text
   instead of a number - FastAPI blocks it before your code even runs).
2. Control exactly what fields get sent back in a response.

Think of these as "forms" - CustomerCreate is the form someone fills
out to create a customer, CustomerOut is what we hand back to them.
"""

from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr, Field

from models.banking_account import AccountType


# ---------- Forms related to Accounts ----------

class AccountBase(BaseModel):
    account_type: AccountType = AccountType.bank
    balance: float = Field(default=100.0, ge=0)  # ge=0 means "must be 0 or more"
    interest_rate: Optional[float] = Field(default=None, ge=0)


class AccountCreate(AccountBase):
    """What someone sends us when opening a new account."""
    pass


class AccountUpdate(BaseModel):
    """What someone sends us when editing an account. All fields optional."""
    account_type: Optional[AccountType] = None
    balance: Optional[float] = Field(default=None, ge=0)
    interest_rate: Optional[float] = Field(default=None, ge=0)


class TransactionRequest(BaseModel):
    """What someone sends us to deposit or withdraw money."""
    amount: float = Field(..., gt=0)  # gt=0 means "must be greater than 0"


class AccountOut(AccountBase):
    """What we send back after showing/creating/updating an account."""
    id: int
    customer_id: int
    created_at: datetime

    class Config:
        from_attributes = True  # lets this read straight from a database object


# ---------- Forms related to Customers ----------

class CustomerBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class CustomerOut(CustomerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class CustomerWithAccounts(CustomerOut):
    """Same as CustomerOut, but also includes their list of accounts.
    This is what proves the relationship between the two tables works."""
    accounts: List[AccountOut] = []

    class Config:
        from_attributes = True
