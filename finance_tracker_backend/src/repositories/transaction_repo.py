from typing import List, Optional, Tuple

from sqlalchemy.orm import Session

from src.models.transaction import Transaction
from src.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionListFilters


# PUBLIC_INTERFACE
def create(db: Session, user_id: int, data: TransactionCreate) -> Transaction:
    """Create a new transaction for a user."""
    txn = Transaction(
        user_id=user_id,
        amount=data.amount,
        type=data.type,
        category=data.category,
        date=data.date,
        note=data.note,
    )
    db.add(txn)
    db.commit()
    db.refresh(txn)
    return txn


# PUBLIC_INTERFACE
def get(db: Session, txn_id: int) -> Optional[Transaction]:
    """Get a transaction by id."""
    return db.query(Transaction).filter(Transaction.id == txn_id).first()


# PUBLIC_INTERFACE
def update(db: Session, txn: Transaction, data: TransactionUpdate) -> Transaction:
    """Update transaction fields that are provided."""
    for field in ("amount", "type", "category", "date", "note"):
        value = getattr(data, field)
        if value is not None:
            setattr(txn, field, value)
    db.add(txn)
    db.commit()
    db.refresh(txn)
    return txn


# PUBLIC_INTERFACE
def delete(db: Session, txn: Transaction) -> None:
    """Delete a transaction."""
    db.delete(txn)
    db.commit()


def _apply_filters(query, user_id: int, filters: Optional[TransactionListFilters]):
    query = query.filter(Transaction.user_id == user_id)
    if filters:
        if filters.start_date is not None:
            query = query.filter(Transaction.date >= filters.start_date)
        if filters.end_date is not None:
            query = query.filter(Transaction.date <= filters.end_date)
        if filters.type is not None:
            query = query.filter(Transaction.type == filters.type)
        if filters.category:
            query = query.filter(Transaction.category == filters.category)
    return query


# PUBLIC_INTERFACE
def list_paginated(
    db: Session,
    user_id: int,
    page: int,
    per_page: int,
    filters: Optional[TransactionListFilters] = None,
) -> Tuple[List[Transaction], int]:
    """List transactions for a user with filters and pagination."""
    base_q = db.query(Transaction)
    filtered_q = _apply_filters(base_q, user_id, filters)

    total = filtered_q.count()
    items = (
        filtered_q.order_by(Transaction.date.desc(), Transaction.id.desc())
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )
    return items, total
