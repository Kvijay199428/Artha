from fastapi import APIRouter
from app.api.v1 import auth, company, units, items, parties, invoices, master, orders, returns, quotations, boq, estimates, gst, adjustments, documents

api_router = APIRouter(prefix="/v1")
api_router.include_router(auth.router)
api_router.include_router(company.router)
api_router.include_router(units.router)
api_router.include_router(items.router)
api_router.include_router(parties.router)
api_router.include_router(invoices.router)
api_router.include_router(master.router)
api_router.include_router(orders.router)
api_router.include_router(returns.router)
api_router.include_router(quotations.router)
api_router.include_router(boq.router)
api_router.include_router(estimates.router)
api_router.include_router(gst.router)
api_router.include_router(adjustments.router)
api_router.include_router(documents.router)
