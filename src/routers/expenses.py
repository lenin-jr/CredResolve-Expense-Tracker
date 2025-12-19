from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database
from ..services import expense_service

router = APIRouter(prefix="/expenses", tags=["Expenses"])
get_db = database.get_db

@router.post("/", response_model=schemas.ExpenseResponse)
def add_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    # Call the service layer we created in Step 7
    return expense_service.create_expense(db, expense)