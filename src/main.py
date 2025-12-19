from fastapi import FastAPI
from .database import engine
from . import models
from .routers import users, groups, expenses  # <--- UPDATE THIS IMPORT

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="CredResolve Expense Tracker")

app.include_router(users.router)
app.include_router(groups.router)
app.include_router(expenses.router)   # <--- ADD THIS LINE

@app.get("/")
def health_check():
    return {"status": "running", "message": "System is live"}