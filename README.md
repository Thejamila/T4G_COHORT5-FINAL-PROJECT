# Banking System API

## About the Project

This project is a simple **Banking System REST API** built with Python.

It started as a terminal-based Python banking program using two classes:

* `BankAccount`
* `SavingsAccount`

In the original program, customer and account information was kept in memory. When the program stopped, the information was lost.

For this project, I developed the banking system into a backend API using **FastAPI**, **SQLAlchemy**, and **MySQL**. Customer and account information is now stored permanently in a database.

The API allows customers to be created and managed, bank and savings accounts to be opened, money to be deposited and withdrawn, and interest to be applied to savings accounts.

The API uses **UUIDs as public identifiers** for customers and accounts. The database still uses internal numeric IDs for its relationships, but those internal IDs are not exposed through the API.

---

## What the Banking System Can Do

### Customer Management

The API allows you to:

* Create a customer
* View all customers
* View one customer
* Update customer information
* Delete a customer

One customer can have multiple accounts.

### Account Management

Customers can open:

* A regular bank account
* A savings account

The API can:

* Create accounts
* View accounts
* Update accounts
* Delete accounts
* Check account information

### Banking Transactions

The API supports:

* Depositing money
* Withdrawing money
* Applying interest to savings accounts

The rules from the original Python banking project are still used.

For example:

* Regular bank accounts require a minimum starting balance of **GHS 100**.
* Deposits into regular bank accounts must be at least **GHS 100**.
* A customer cannot withdraw more money than the account balance.
* Interest can only be applied to savings accounts.

---

## Technology Used

### Python

Python is the main programming language used to build the application.

### FastAPI

FastAPI is the framework used to create the REST API.

It allows the application to receive requests such as creating a customer, opening an account, depositing money, or withdrawing money and then return the appropriate response.

### MySQL

MySQL is used to store customer and account information permanently.

### SQLAlchemy

SQLAlchemy is the ORM used to allow Python to communicate with the MySQL database.

### Pydantic

Pydantic is used to validate information sent to the API before it reaches the application logic.

For example, it checks that email addresses are valid and transaction amounts are greater than zero.

### Python-dotenv

Python-dotenv loads database credentials from the `.env` file.

The `.env` file is excluded from GitHub using `.gitignore` so that private database credentials are not uploaded.

---

## Project Structure

```text
Banking_System/
│
├── main.py
├── database.py
├── schemas.py
├── uuid_generator.py
│
├── models/
│   ├── __init__.py
│   ├── base_models.py
│   ├── banking_account.py
│   └── savings_account.py
│
├── repositories/
│   ├── __init__.py
│   ├── customer_repository.py
│   └── account_repository.py
│
├── routes/
│   ├── __init__.py
│   ├── main.py
│   ├── customers.py
│   ├── accounts.py
│   └── transactions.py
│
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

---

## Important Files

### `main.py`

Starts the FastAPI application and connects the routes.

### `database.py`

Creates the connection between the Python application and MySQL.

### `schemas.py`

Defines the information the API expects to receive and return.

### `uuid_generator.py`

Generates unique UUIDs for customers and accounts.

### `models/`

Contains the database models that describe the customer and account tables.

### `repositories/`

Contains database operations. This keeps database access separate from the API routes.

### `routes/`

Contains the API endpoints that users interact with.

---

## Database Design

The application uses two main tables:

* Customers
* Accounts

### Customers Table

| Column       | Purpose                                |
| ------------ | -------------------------------------- |
| `id`         | Internal database ID                   |
| `uuid`       | Public customer identifier             |
| `name`       | Customer's name                        |
| `email`      | Customer's email address               |
| `phone`      | Customer's phone number                |
| `created_at` | Date and time the customer was created |

### Accounts Table

| Column          | Purpose                               |
| --------------- | ------------------------------------- |
| `id`            | Internal database ID                  |
| `uuid`          | Public account identifier             |
| `customer_id`   | Links the account to its customer     |
| `account_type`  | Bank or savings                       |
| `balance`       | Current account balance               |
| `interest_rate` | Interest rate for savings accounts    |
| `created_at`    | Date and time the account was created |

### Relationship

One customer can have many accounts.

For example:

```text
Customer
   │
   ├── Bank Account
   │
   ├── Savings Account
   │
   └── Bank Account
```

The database uses `customer_id` internally to create this relationship.

The API uses UUIDs when identifying customers and accounts publicly.

---

## Why UUIDs Are Used

The database has internal numeric IDs, but the API uses **UUIDs as public identifiers**.

Instead of exposing an internal ID such as:

```text
/customers/1
```

the API uses a UUID such as:

```text
/customers/6afceb90-8695-4018-b2bf-8ab28b94e267
```

This separates the database's internal identifiers from the identifiers used by API users.

UUIDs are generated automatically when a customer or account is created.

---

## API Endpoints

### Customer Endpoints

| Method   | Endpoint                     | Purpose            |
| -------- | ---------------------------- | ------------------ |
| `POST`   | `/customers`                 | Create a customer  |
| `GET`    | `/customers`                 | View all customers |
| `GET`    | `/customers/{customer_uuid}` | View one customer  |
| `PUT`    | `/customers/{customer_uuid}` | Update a customer  |
| `DELETE` | `/customers/{customer_uuid}` | Delete a customer  |

### Account Endpoints

| Method   | Endpoint                              | Purpose           |
| -------- | ------------------------------------- | ----------------- |
| `POST`   | `/customers/{customer_uuid}/accounts` | Open an account   |
| `GET`    | `/accounts`                           | View all accounts |
| `GET`    | `/accounts/{account_uuid}`            | View one account  |
| `PUT`    | `/accounts/{account_uuid}`            | Update an account |
| `DELETE` | `/accounts/{account_uuid}`            | Delete an account |

### Transaction Endpoints

| Method | Endpoint                                  | Purpose                |
| ------ | ----------------------------------------- | ---------------------- |
| `POST` | `/accounts/{account_uuid}/deposit`        | Deposit money          |
| `POST` | `/accounts/{account_uuid}/withdraw`       | Withdraw money         |
| `POST` | `/accounts/{account_uuid}/apply-interest` | Apply savings interest |

---

## Validation and Error Handling

The API validates information before processing requests.

Examples include:

* Customer names cannot be empty.
* Customer emails must be valid.
* Customer emails must be unique.
* Account balances cannot be negative.
* Regular bank accounts require a minimum starting balance of **GHS 100**.
* Regular bank account deposits must be at least **GHS 100**.
* Withdrawals cannot be greater than the available balance.
* Customers that do not exist return a `404` response.
* Accounts that do not exist return a `404` response.
* Interest can only be applied to savings accounts with an interest rate.

The API uses appropriate HTTP status codes, including:

| Status Code | Meaning                       |
| ----------- | ----------------------------- |
| `200`       | Successful request            |
| `201`       | Resource successfully created |
| `400`       | Invalid request               |
| `404`       | Resource not found            |
| `204`       | Resource successfully deleted |

---

## Savings Account Interest

Savings accounts can have an interest rate.

For example, if a savings account has:

* **Balance:** GHS 1,000
* **Interest rate:** 5%

The interest is calculated as:

```text
GHS 1,000 × 5 / 100 = GHS 50
```

The new balance becomes:

```text
GHS 1,050
```

The interest calculation is handled in:

```text
models/savings_account.py
```

Interest is only applied to accounts whose account type is savings.

---

## Setting Up the Project

### 1. Create the MySQL Database

Open MySQL and run:

```sql
CREATE DATABASE banking_db;
```

### 2. Clone the Repository

```bash
git clone https://github.com/Thejamila/T4G_COHORT5-FINAL-PROJECT.git
cd T4G_COHORT5-FINAL-PROJECT
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Linux/WSL:

```bash
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

### 4. Install the Requirements

```bash
pip install -r requirements.txt
```

### 5. Configure the Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Open `.env` and enter your own MySQL details:

```text
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=banking_db
```

The real `.env` file is ignored by Git and should never be uploaded to GitHub because it contains private database credentials.

### 6. Start the API

```bash
uvicorn main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

---

## Testing the API

FastAPI automatically provides an interactive documentation page called **Swagger UI**.

After starting the application, open:

```text
http://127.0.0.1:8000/docs
```

Swagger allows you to test the API directly from your browser.

A typical test process is:

1. Create a customer.
2. Copy the customer's UUID from the response.
3. Use the UUID to open a bank or savings account.
4. Copy the account UUID.
5. Deposit money into the account.
6. Withdraw money from the account.
7. If it is a savings account, apply interest.
8. Check the updated account balance.

This makes it possible to test the backend without building a separate frontend application.

---

## What I Learned

One of the biggest lessons from this project was learning how to turn a simple Python program into a real backend application.

My original `BankAccount` and `SavingsAccount` classes worked inside the Python program, but the information disappeared when the program stopped.

With this project, I learned how to:

* Build REST APIs with FastAPI.
* Connect Python to a MySQL database.
* Use SQLAlchemy to work with database tables.
* Use Pydantic to validate user input.
* Create relationships between database tables.
* Separate database operations using a repository layer.
* Use UUIDs as public identifiers.
* Handle errors using HTTP status codes.
* Test API endpoints using Swagger UI.
* Use Git and GitHub to manage a software project.

I also learned that different parts of a backend application have different responsibilities. The routes handle requests, schemas validate data, models describe the database, and repositories handle database operations.

---

## Challenges I Faced

One of the main challenges was changing my original terminal-based banking system into an API.

In the original project, I used `input()` to communicate with users. In an API, users send requests instead, so I had to learn a new way of handling input and validation.

Another challenge was connecting the application to MySQL and making sure that information was stored permanently.

I also learned how to introduce UUIDs as public identifiers while keeping the internal database IDs for relationships.

Working through these challenges helped me understand that building an application is not only about writing code that works. It is also about organizing the code, validating information, protecting private credentials, handling errors, and making the application understandable to other developers.

---

## Final Note

This project represents the progression of my original Python banking assignment into a more complete backend application.

What started as a simple banking program using Python classes has now been developed into a REST API using:

**Python + FastAPI + SQLAlchemy + MySQL + Pydantic + UUIDs + Git/GitHub**

The main goal was not only to make the banking operations work, but also to understand how the different parts of a backend application connect together.

