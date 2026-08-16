"""
These three URLs are the direct API version of the deposit(), withdraw(),
and apply_interest() methods from your original BankAccount and
SavingsAccount classes - same rules, now backed by MySQL:

POST /accounts/{id}/deposit
POST /accounts/{id}/withdraw
POST /accounts/{id}/apply-interest
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import schemas
from database import get_db
from models.banking_account import AccountType
from models.savings_account import apply_interest as apply_interest_logic
from repositories.account_repository import AccountRepository

router = APIRouter(prefix="/accounts", tags=["Transactions"])


@router.post("/{account_id}/deposit", response_model=schemas.AccountOut)
def deposit(
    account_id: int, tx: schemas.TransactionRequest, db: Session = Depends(get_db)
):
    repo = AccountRepository(db)
    account = repo.get_by_id(account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found.")

    # Same rule as the original: minimum GHS 100 deposit
    if account.account_type == AccountType.bank and tx.amount < 100:
        raise HTTPException(status_code=400, detail="Minimum deposit is GHS 100.")

    account.balance += tx.amount
    return repo.save(account)


@router.post("/{account_id}/withdraw", response_model=schemas.AccountOut)
def withdraw(
    account_id: int, tx: schemas.TransactionRequest, db: Session = Depends(get_db)
):
    repo = AccountRepository(db)
    account = repo.get_by_id(account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found.")

    if tx.amount > account.balance:
        raise HTTPException(status_code=400, detail="Insufficient balance.")

    account.balance -= tx.amount
    return repo.save(account)


@router.post("/{account_id}/apply-interest", response_model=schemas.AccountOut)
def apply_interest(account_id: int, db: Session = Depends(get_db)):
    repo = AccountRepository(db)
    account = repo.get_by_id(account_id)
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found.")

    try:
        apply_interest_logic(account)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return repo.save(account)
