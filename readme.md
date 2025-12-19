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
