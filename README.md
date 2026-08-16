# Banking System API

A REST API built with **FastAPI** and **SQLAlchemy**, connected to a **MySQL**
database. This extends my earlier `BankAccount` / `SavingsAccount` Python
classes (Tech4Girls Cohort 5 assignment) into a full backend API with
persistent storage - so accounts and customers survive after the program
closes, instead of living only in memory.

## What it does

Customers can open bank or savings accounts. Each customer can have
multiple accounts (a one-to-many relationship). You can create, view,
update, and delete both customers and accounts, and perform deposits,
withdrawals, and (for savings accounts) apply interest - the same rules
from my original classes, now enforced by the API and saved permanently
in MySQL.

## Tech stack

- **FastAPI** - the web framework that turns Python functions into URLs
- **SQLAlchemy** - the ORM (talks to MySQL using Python, no raw SQL)
- **MySQL** - the database
- **python-dotenv** - loads DB credentials from a `.env` file
- **Pydantic** - checks incoming data is valid before it reaches my code

## Project structure

```
Banking_System/
├── main.py               # starts the app, plugs in the routes
├── database.py             # connects to MySQL
├── schemas.py                # defines valid request/response shapes
├── models/
│   ├── base_models.py          # Base class + Customer table
│   ├── banking_account.py       # Account table
│   └── savings_account.py        # interest calculation logic
├── repositories/
│   ├── customer_repository.py       # all database queries for customers
│   ├── account_repository.py        # all database queries for accounts
│   └── transaction_repository.py    # all database queries for transactions
├── routes/
│   ├── customers.py                   # customer URLs (create/view/edit/delete)
│   ├── accounts.py                     # account URLs (create/view/edit/delete)
│   └── transactions.py                  # deposit/withdraw/apply-interest URLs
├── requirements.txt
├── .env.example                            # template - copy to .env and fill in
└── .gitignore
```

## Database design

**customers**
| column | type |
|---|---|
| id | int, primary key |
| name | string |
| email | string, unique |
| phone | string |
| created_at | datetime |

**accounts**
| column | type |
|---|---|
| id | int, primary key |
| customer_id | int, foreign key -> customers.id |
| account_type | enum ("bank" / "savings") |
| balance | float |
| interest_rate | float, nullable (savings only) |
| created_at | datetime |

Relationship: **one customer can have many accounts.**

## Setup instructions

### 1. Create the MySQL database
```sql
CREATE DATABASE banking_db;
```

### 2. Clone the repo and set up a virtual environment
```bash
git clone https://github.com/Thejamila/t4g-cohort5-final-project.git
cd t4g-cohort5-final-project
python -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set up your environment variables
Copy `.env.example` to `.env` and fill in your real MySQL username/password:
```bash
cp .env.example .env
```
`.env` is listed in `.gitignore`, so it never gets pushed to GitHub.

### 4. Run the API
```bash
uvicorn main:app --reload
```
The API runs at `http://127.0.0.1:8000`.
Interactive docs (auto-generated) are at `http://127.0.0.1:8000/docs` -
the easiest way to test every endpoint straight from the browser.

## Endpoints

| Method | Endpoint | What it does |
|---|---|---|
| POST | `/customers` | Create a customer |
| GET | `/customers` | List all customers |
| GET | `/customers/{id}` | View one customer, with their accounts |
| PUT | `/customers/{id}` | Update a customer |
| DELETE | `/customers/{id}` | Delete a customer (and their accounts) |
| POST | `/customers/{id}/accounts` | Open a new account for a customer |
| GET | `/accounts` | List all accounts |
| GET | `/accounts/{id}` | View one account |
| PUT | `/accounts/{id}` | Update an account |
| DELETE | `/accounts/{id}` | Close/delete an account |
| POST | `/accounts/{id}/deposit` | Deposit money |
| POST | `/accounts/{id}/withdraw` | Withdraw money |
| POST | `/accounts/{id}/apply-interest` | Apply interest (savings only) |

## Error handling

- `404` if a customer or account doesn't exist
- `400` for bad input (deposit below GHS 100, withdrawal exceeding balance,
  applying interest to a non-savings account, duplicate email)
- Proper HTTP status codes on every response (`201` create, `204` delete, etc.)

## What I learned / found challenging

Turning my original terminal-based `BankAccount` class into an API meant
rethinking where validation happens - instead of `input()` loops, FastAPI
and Pydantic validate the request before it even reaches my route code.
Keeping the repository layer (`repositories/`) separate from the routes also
made everything much easier to read, test, and debug.
