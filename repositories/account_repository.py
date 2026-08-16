"""
Repository layer for Account database operations.
"""

from typing import Optional, List

from sqlalchemy.orm import Session

from models.banking_account import Account, AccountType


class AccountRepository:

    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[Account]:
        return self.db.query(Account).all()

    def get_by_id(self, account_id: int) -> Optional[Account]:
        return (
            self.db.query(Account)
            .filter(Account.id == account_id)
            .first()
        )

    def get_by_customer(
        self,
        customer_id: int
    ) -> List[Account]:

        return (
            self.db.query(Account)
            .filter(Account.customer_id == customer_id)
            .all()
        )

    def create(
        self,
        customer_id: int,
        account_type: AccountType,
        balance: float,
        interest_rate: Optional[float],
    ) -> Account:

        account = Account(
            customer_id=customer_id,
            account_type=account_type,
            balance=balance,
            interest_rate=interest_rate,
        )

        self.db.add(account)
        self.db.commit()
        self.db.refresh(account)

        return account

    def update(
        self,
        account: Account,
        data: dict
    ) -> Account:

        for key, value in data.items():

            if value is not None:
                setattr(account, key, value)

        self.db.commit()
        self.db.refresh(account)

        return account

    def delete(self, account: Account) -> None:

        self.db.delete(account)
        self.db.commit()

    def save(self, account: Account) -> Account:

        self.db.commit()
        self.db.refresh(account)

        return account

