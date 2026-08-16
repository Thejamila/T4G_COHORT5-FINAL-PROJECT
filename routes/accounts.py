"""
Every URL related to accounts lives here:
POST   /customers/{id}/accounts   -> open a new account for a customer
GET    /accounts                    -> list all accounts
GET    /accounts/{id}                -> view one account
PUT    /accounts/{id}                 -> edit an account
DELETE /accounts/{id}                  -> close/delete an account
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import schemas
from database import get_db
from models.banking_account import AccountType
from repositories.customer_repository import CustomerRepository
from repositories.account_repository import AccountRepository

router = APIRouter(tags=["Accounts"])


@router.post(
    "/customers/{customer_id}/accounts",
    response_model=schemas.AccountOut,
    status_code=status.HTTP_201_CREATED,
)
def create_account(
    customer_id: int, account: schemas.AccountCreate, db: Session = Depends(get_db)
):
    # Make sure the customer this account belongs to actually exists first
    if CustomerRepository(db).get_by_id(customer_id) is None:
        raise HTTPException(status_code=404, detail="Customer not found.")

    # Same rule as your original BankAccount class: minimum GHS 100 to open
    if account.account_type == AccountType.bank and account.balance < 100:
        raise HTTPException(
            status_code=400, detail="Minimum starting balance is GHS 100."
        )

    return AccountRepository(db).create(
        customer_id, account.account_type, account.balance, account.interest_rate
    )


@router.get("/accounts", response_model=list[schemas.AccountOut])
def list_accounts(db: Session = Depends(get_db)):
    return AccountRepository(db).get_all()


@router.get("/accounts/{account_id}", response_model=schemas.AccountOut)
def get_account(account_id: int, db: Session = Depends(get_db)):
    account = AccountRepository(db).get_by_id(account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found.")
    return account


@router.put("/accounts/{account_id}", response_model=schemas.AccountOut)
def update_account(
    account_id: int, updates: schemas.AccountUpdate, db: Session = Depends(get_db)
):
    repo = AccountRepository(db)
    account = repo.get_by_id(account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found.")

    return repo.update(account, updates.model_dump(exclude_unset=True))


@router.delete("/accounts/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_account(account_id: int, db: Session = Depends(get_db)):
    repo = AccountRepository(db)
    account = repo.get_by_id(account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found.")

    repo.delete(account)
    return None
