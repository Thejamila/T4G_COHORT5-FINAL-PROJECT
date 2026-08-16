"""
This file holds the interest calculation logic that used to live inside
my original SavingsAccount.apply_interest() method.

Because we now store savings accounts as rows in the same 'accounts'
table (not a separate table), this file works with an Account object
instead of a SavingsAccount object - but the math is identical to
my original class.
"""

from models.banking_account import Account, AccountType


def calculate_interest(account: Account) -> float:
    """Work out how much interest an account should earn, without adding it yet."""
    if account.account_type != AccountType.savings or not account.interest_rate:
        raise ValueError(
            "Interest can only be calculated for a savings account with a rate set."
        )
    return account.balance * (account.interest_rate / 100)


def apply_interest(account: Account) -> Account:
    """Actually add the interest to the account's balance."""
    interest = calculate_interest(account)
    account.balance += interest
    return account
