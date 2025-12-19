#  CredResolve Expense Sharing Backend

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95-green)
![SQLAlchemy](https://img.shields.io/badge/Database-SQLite-lightgrey)

A scalable backend system for splitting expenses between users and groups. This project implements advanced features like **Exact & Percent splits** and uses a **Greedy Algorithm** to simplify debt settlements (minimizing total transactions).

---

## Key Features

* **User & Group Management**: seamless creation and retrieval.
* **Expense Splitting**:
    * `EQUAL`: Split equally among all members.
    * `EXACT`: Specify exact amounts for each user.
    * `PERCENT`: Split by percentage share.
* **Debt Simplification**: An optimized algorithm to resolve debts. Instead of `A->B` and `B->C`, the system resolves `A->C` directly.
* **Data Validation**: Powered by Pydantic schemas.

---

##  Project Structure

```bash
src/
├── routers/
│   ├── users.py       # User management endpoints
│   ├── groups.py      # Group creation & Balance logic
│   └── expenses.py    # Expense adding logic
├── services/
│   └── expense_service.py  # Core business logic for splits
├── models.py          # Database Tables (SQLAlchemy)
├── schemas.py         # Pydantic Data Models
├── database.py        # DB Connection setup
└── main.py            # Entry point


## Why This Approach Stands Out

### 1. Architectural Scalability
Instead of a monolithic design, I implemented a **Service-Repository Pattern**. By decoupling the business logic (`services/`) from the API layer (`routers/`), the codebase remains modular, testable, and easier to maintain as the application grows.

### 2. Algorithmic Efficiency
The core challenge of expense sharing is minimizing the number of transactions. I implemented a **Greedy Graph Simplification Algorithm** that:
* Calculates net balances for all users.
* Separates users into distinct heaps of Debtors and Creditors.
* Iteratively settles the largest debts first.
This reduces the complexity of settlement from $O(N^2)$ (everyone pays everyone) to near $O(N)$ (direct settlements).

### 3. Type Safety & Validation
Leveraging **Pydantic** and **Python Type Hints**, the system enforces strict data validation at the entry level. This ensures that invalid states (e.g., splits not summing to the total amount) are caught immediately, preventing database corruption.
