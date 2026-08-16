 
 
from typing import Optional, List 
 
from sqlalchemy.orm import Session 
 
from models.base_models import Customer 
 
 
class CustomerRepository: 
 
    def __init__(self, db: Session): 
        self.db = db 
 
    def get_all(self) -> List[Customer]: 
        return self.db.query(Customer).all() 
 
    def get_by_id(self, customer_id: int) -> Optional[Customer]: 
        return ( 
            self.db.query(Customer) 
            .filter(Customer.id == customer_id) 
            .first() 
        ) 
 
    def get_by_email(self, email: str) -> Optional[Customer]: 
        return ( 
            self.db.query(Customer) 
            .filter(Customer.email == email) 
            .first() 
        ) 
 
    def create( 
        self, 
        name: str, 
        email: str, 
        phone: Optional[str] 
    ) -> Customer: 
 
        customer = Customer( 
            name=name, 
            email=email, 
            phone=phone 
        ) 
 
        self.db.add(customer) 
        self.db.commit() 
        self.db.refresh(customer) 
 
        return customer 
 
    def update( 
        self, 
        customer: Customer, 
        data: dict 
    ) -> Customer: 
 
        for key, value in data.items(): 
 
            if value is not None: 
                setattr(customer, key, value) 
 
        self.db.commit() 
        self.db.refresh(customer) 
 
        return customer 
 
    def delete(self, customer: Customer) -> None: 
 
        self.db.delete(customer) 
        self.db.commit()
