from fastapi import APIRouter

from routes.customers import router as customers_router
from routes.accounts import router as accounts_router
from routes.transactions import router as transactions_router

# This bundles all the separate route files into one, so main.py
# only has to plug in ONE thing to get every URL in the app.
api_router = APIRouter()
api_router.include_router(customers_router)
api_router.include_router(accounts_router)
api_router.include_router(transactions_router)
