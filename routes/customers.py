"""
Every URL related to customers lives here:
POST   /customers            -> create a customer
GET    /customers             -> list all customers
GET    /customers/{id}         -> view one customer (with their accounts)
PUT    /customers/{id}          -> edit a customer
DELETE /customers/{id}           -> delete a customer

Notice this file never talks to the database directly - it always
goes through CustomerRepository from repositories/customer_repository.py.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import schemas
from database import get_db
from repositories.customer_repository import CustomerRepository

router = APIRouter(prefix="/customers", tags=["Customers"])


@router.post("", response_model=schemas.CustomerOut, status_code=status.HTTP_201_CREATED)
def create_customer(customer: schemas.CustomerCreate, db: Session = Depends(get_db)):
    repo = CustomerRepository(db)

    if repo.get_by_email(customer.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A customer with this email already exists.",
        )

    return repo.create(customer.name, customer.email, customer.phone)


@router.get("", response_model=list[schemas.CustomerOut])
def list_customers(db: Session = Depends(get_db)):
    return CustomerRepository(db).get_all()


@router.get("/{customer_id}", response_model=schemas.CustomerWithAccounts)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = CustomerRepository(db).get_by_id(customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found.")
    return customer


@router.put("/{customer_id}", response_model=schemas.CustomerOut)
def update_customer(
    customer_id: int, updates: schemas.CustomerUpdate, db: Session = Depends(get_db)
):
    repo = CustomerRepository(db)
    customer = repo.get_by_id(customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found.")

    return repo.update(customer, updates.model_dump(exclude_unset=True))


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    repo = CustomerRepository(db)
    customer = repo.get_by_id(customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found.")

    repo.delete(customer)
    return None
