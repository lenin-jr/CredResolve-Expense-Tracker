from sqlalchemy.orm import Session
from fastapi import HTTPException
from .. import models, schemas

def create_expense(db: Session, expense_data: schemas.ExpenseCreate):
    # 1. Create the Main Expense Record
    new_expense = models.Expense(
        description=expense_data.description,
        amount=expense_data.amount,
        split_type=expense_data.split_type,
        payer_id=expense_data.payer_id,
        group_id=expense_data.group_id
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    # 2. Calculate Splits based on Type
    final_splits = []
    
    if expense_data.split_type == "EQUAL":
        # Logic: Total / Number of People
        # We assume the expense involves ALL group members for simplicity here
        group = db.query(models.Group).filter(models.Group.id == expense_data.group_id).first()
        if not group or not group.members:
            raise HTTPException(status_code=400, detail="Group has no members")
            
        split_amount = round(expense_data.amount / len(group.members), 2)
        
        for member in group.members:
            # Don't create a debt record for the person who paid!
            if member.id != expense_data.payer_id:
                split = models.ExpenseSplit(
                    expense_id=new_expense.id,
                    user_id=member.id,
                    amount_owed=split_amount
                )
                final_splits.append(split)

    elif expense_data.split_type == "EXACT":
        # Validate that the total matches
        total_share = sum(s.amount for s in expense_data.splits)
        if total_share != expense_data.amount:
             raise HTTPException(status_code=400, detail="Splits do not equal total amount")
        
        for s in expense_data.splits:
            if s.user_id != expense_data.payer_id:
                split = models.ExpenseSplit(
                    expense_id=new_expense.id,
                    user_id=s.user_id,
                    amount_owed=s.amount
                )
                final_splits.append(split)

    # 3. Save all splits to DB
    db.add_all(final_splits)
    db.commit()
    
    return new_expense