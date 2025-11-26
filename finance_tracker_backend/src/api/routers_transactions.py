from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from src.core.db import get_db
from src.core.security import get_current_user
from src.models.transaction import Transaction as TransactionModel
from src.models.user import User
from src.repositories import transaction_repo
from src.schemas.common import Paginated
from src.schemas.transaction import (
    TransactionCreate,
    TransactionListFilters,
    TransactionRead,
    TransactionUpdate,
)

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post(
    "",
    response_model=TransactionRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create transaction",
    description="Create a new income or expense transaction.",
)
def create_transaction(
    payload: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TransactionRead:
    txn = transaction_repo.create(db, user_id=current_user.id, data=payload)
    return TransactionRead.model_validate(txn)


@router.get(
    "/{txn_id}",
    response_model=TransactionRead,
    summary="Get transaction by id",
    description="Retrieve a transaction by its id, if it belongs to the authenticated user.",
)
def get_transaction(
    txn_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TransactionRead:
    txn = transaction_repo.get(db, txn_id)
    if not txn or txn.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return TransactionRead.model_validate(txn)


@router.patch(
    "/{txn_id}",
    response_model=TransactionRead,
    summary="Update transaction",
    description="Update fields on an existing transaction.",
)
def update_transaction(
    txn_id: int,
    payload: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> TransactionRead:
    txn: Optional[TransactionModel] = transaction_repo.get(db, txn_id)
    if not txn or txn.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Transaction not found")
    updated = transaction_repo.update(db, txn, data=payload)
    return TransactionRead.model_validate(updated)


@router.delete(
    "/{txn_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete transaction",
    description="Delete an existing transaction.",
)
def delete_transaction(
    txn_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> None:
    txn: Optional[TransactionModel] = transaction_repo.get(db, txn_id)
    if not txn or txn.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Transaction not found")
    transaction_repo.delete(db, txn)
    return None


@router.get(
    "",
    response_model=Paginated[TransactionRead],
    summary="List transactions",
    description="List transactions with optional filters and pagination. Items are sorted by date desc then id desc.",
)
def list_transactions(
    page: int = Query(1, ge=1, description="Page number starting from 1"),
    per_page: int = Query(20, ge=1, le=200, description="Items per page, max 200"),
    start_date: Optional[str] = Query(None, description="ISO start datetime inclusive"),
    end_date: Optional[str] = Query(None, description="ISO end datetime inclusive"),
    type: Optional[str] = Query(None, description="income or expense"),
    category: Optional[str] = Query(None, description="Category name filter"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Paginated[TransactionRead]:
    # Build filters
    filters = TransactionListFilters.model_validate(
        {
            "start_date": start_date,
            "end_date": end_date,
            "type": type,
            "category": category,
        }
    )
    items, total = transaction_repo.list_paginated(
        db, user_id=current_user.id, page=page, per_page=per_page, filters=filters
    )
    return Paginated[TransactionRead](
        items=[TransactionRead.model_validate(i) for i in items],
        total=total,
        page=page,
        per_page=per_page,
    )
