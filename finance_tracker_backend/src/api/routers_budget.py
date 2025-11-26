from collections import defaultdict
from datetime import datetime
from typing import Dict, List

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.core.db import get_db
from src.core.security import get_current_user
from src.models.transaction import Transaction
from src.models.user import User
from src.schemas.budget import ByCategoryItem, Summary, TrendPoint

router = APIRouter(prefix="/budget", tags=["Budget"])


def _date_range_filters(query, start_date: datetime | None, end_date: datetime | None):
    if start_date is not None:
        query = query.filter(Transaction.date >= start_date)
    if end_date is not None:
        query = query.filter(Transaction.date <= end_date)
    return query


@router.get(
    "/summary",
    response_model=Summary,
    summary="Budget summary",
    description="Return total income, total expense, and balance for the specified period.",
)
def summary(
    start_date: datetime | None = Query(None, description="Start datetime inclusive (ISO)"),
    end_date: datetime | None = Query(None, description="End datetime inclusive (ISO)"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Summary:
    q = db.query(
        Transaction.type,
        func.coalesce(func.sum(Transaction.amount), 0),
    ).filter(Transaction.user_id == current_user.id)
    q = _date_range_filters(q, start_date, end_date)
    q = q.group_by(Transaction.type)

    totals: Dict[str, float] = {"income": 0.0, "expense": 0.0}
    for ttype, total in q.all():
        totals[str(ttype.value)] = float(total)

    balance = totals["income"] - totals["expense"]
    return Summary(total_income=totals["income"], total_expense=totals["expense"], balance=balance)


@router.get(
    "/by-category",
    response_model=List[ByCategoryItem],
    summary="Amounts by category",
    description="Aggregate amounts by category and type for the specified period.",
)
def by_category(
    start_date: datetime | None = Query(None),
    end_date: datetime | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[ByCategoryItem]:
    q = (
        db.query(
            Transaction.category,
            Transaction.type,
            func.coalesce(func.sum(Transaction.amount), 0),
        )
        .filter(Transaction.user_id == current_user.id)
    )
    q = _date_range_filters(q, start_date, end_date)
    q = q.group_by(Transaction.category, Transaction.type)

    results: List[ByCategoryItem] = []
    for category, ttype, total in q.all():
        results.append(
            ByCategoryItem(category=category, amount=float(total), type=ttype.value)
        )
    return results


@router.get(
    "/trend",
    response_model=List[TrendPoint],
    summary="Trend over time",
    description="Return periodized income and expense totals for trend charting.",
)
def trend(
    bucket: str = Query("month", pattern="^(day|week|month)$", description="Aggregation bucket"),
    start_date: datetime | None = Query(None),
    end_date: datetime | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[TrendPoint]:
    # Use SQLite compatible date truncation
    if bucket == "day":
        period_expr = func.strftime("%Y-%m-%d 00:00:00", Transaction.date)
    elif bucket == "week":
        period_expr = func.strftime("%Y-%W-1 00:00:00", Transaction.date)
    else:  # month
        period_expr = func.strftime("%Y-%m-01 00:00:00", Transaction.date)

    q = (
        db.query(
            period_expr.label("period_start"),
            Transaction.type,
            func.coalesce(func.sum(Transaction.amount), 0),
        )
        .filter(Transaction.user_id == current_user.id)
    )
    q = _date_range_filters(q, start_date, end_date)
    q = q.group_by("period_start", Transaction.type).order_by("period_start")

    buckets: Dict[str, Dict[str, float]] = defaultdict(lambda: {"income": 0.0, "expense": 0.0})
    for period_start, ttype, total in q.all():
        key = str(period_start)
        buckets[key][ttype.value] += float(total)

    points: List[TrendPoint] = []
    for k in sorted(buckets.keys()):
        # parse back into datetime for response
        period_dt = datetime.fromisoformat(k)
        points.append(
            TrendPoint(
                period_start=period_dt,
                income=buckets[k]["income"],
                expense=buckets[k]["expense"],
            )
        )
    return points
