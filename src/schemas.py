from pydantic import BaseModel
from typing import List, Optional

# --- User Schemas ---
class UserBase(BaseModel):
    name: str
    email: str
    mobile: str

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    
    class Config:
        from_attributes = True

# --- Group Schemas ---
class GroupCreate(BaseModel):
    name: str
    member_ids: List[int]

class GroupResponse(BaseModel):
    id: int
    name: str
    members: List[UserResponse]

    class Config:
        from_attributes = True

        # --- Expense Schemas ---
# This defines how we receive split data (e.g., User 2 owes $50)
class ExpenseSplitCreate(BaseModel):
    user_id: int
    amount: Optional[float] = None      # For EXACT split
    percentage: Optional[float] = None  # For PERCENT split

# This defines the main expense payload
class ExpenseCreate(BaseModel):
    description: str
    amount: float
    payer_id: int
    group_id: int
    split_type: str  # EQUAL, EXACT, or PERCENT
    splits: List[ExpenseSplitCreate] = []

class ExpenseResponse(BaseModel):
    id: int
    description: str
    amount: float
    
    class Config:
        from_attributes = True