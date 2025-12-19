from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, database
import heapq

router = APIRouter(prefix="/groups", tags=["Groups"])
get_db = database.get_db

@router.post("/", response_model=schemas.GroupResponse)
def create_group(group: schemas.GroupCreate, db: Session = Depends(get_db)):
    # 1. Fetch the users to make sure they exist
    members = db.query(models.User).filter(models.User.id.in_(group.member_ids)).all()
    
    # 2. Validation: Did we find all the users?
    if len(members) != len(group.member_ids):
        raise HTTPException(status_code=400, detail="One or more user IDs not found")

    # 3. Create the Group and add members
    new_group = models.Group(name=group.name)
    new_group.members = members
    
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return new_group

@router.get("/", response_model=List[schemas.GroupResponse])
def read_groups(db: Session = Depends(get_db)):
    return db.query(models.Group).all()
@router.get("/{group_id}/balances")
def get_group_balances(group_id: int, db: Session = Depends(get_db)):
    # 1. Fetch expenses
    expenses = db.query(models.Expense).filter(models.Expense.group_id == group_id).all()
    
    # 2. Calculate Net Balances
    balances = {}
    for expense in expenses:
        # Payer gets credit (+)
        balances[expense.payer_id] = balances.get(expense.payer_id, 0.0) + expense.amount
        
        # Everyone in the split gets debt (-)
        for split in expense.splits:
            balances[split.user_id] = balances.get(split.user_id, 0.0) - split.amount_owed
            # Remove that amount from payer's "credit" to balance the equation
            balances[expense.payer_id] -= split.amount_owed

    # 3. Separate into Debtors (-) and Creditors (+)
    debtors = []
    creditors = []
    
    for uid, amount in balances.items():
        amount = round(amount, 2)
        if amount < -0.01:
            debtors.append({"id": uid, "amount": amount})
        elif amount > 0.01:
            creditors.append({"id": uid, "amount": amount})
            
    # 4. Greedy Matching Algorithm (Simplification)
    transactions = []
    
    # Sort by amount magnitude
    debtors.sort(key=lambda x: x["amount"])
    creditors.sort(key=lambda x: x["amount"], reverse=True)
    
    i = 0 
    j = 0 
    
    while i < len(debtors) and j < len(creditors):
        debtor = debtors[i]
        creditor = creditors[j]
        
        # The amount to settle is the minimum of what's owed or what's needed
        amount = min(abs(debtor["amount"]), creditor["amount"])
        
        # Record the transaction
        transactions.append(f"User {debtor['id']} pays User {creditor['id']}: {amount}")
        
        # Adjust remaining balances
        debtor["amount"] += amount
        creditor["amount"] -= amount
        
        # Move pointers if settled
        if abs(debtor["amount"]) < 0.01:
            i += 1
        if creditor["amount"] < 0.01:
            j += 1
            
    if not transactions:
        return ["All settled up!"]
        
    return transactions