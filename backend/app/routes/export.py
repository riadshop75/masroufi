from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse, FileResponse
from sqlalchemy.orm import Session
from datetime import date
from io import BytesIO
from uuid import UUID
from app.database import get_db
from app.models import User, Expense
from app.dependencies import get_current_user
from app.utils.exporters import generate_csv, generate_pdf

router = APIRouter(prefix="/api/v1/export", tags=["export"])

def get_expenses_for_period(
    user: User,
    db: Session,
    month: int = None,
    year: int = None,
    category_id: UUID = None
):
    today = date.today()
    if month is None:
        month = today.month
    if year is None:
        year = today.year

    if month == 12:
        end_date = date(year + 1, 1, 1)
    else:
        end_date = date(year, month + 1, 1)

    start_date = date(year, month, 1)

    query = db.query(Expense).filter(
        Expense.user_id == user.user_id,
        Expense.date >= start_date,
        Expense.date < end_date
    )

    if category_id:
        query = query.filter(Expense.category_id == category_id)

    return query.order_by(Expense.date.desc()).all(), start_date, end_date

@router.get("/csv")
async def export_csv(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    month: int = Query(None),
    year: int = Query(None),
    category_id: UUID = Query(None)
):
    expenses, start_date, end_date = get_expenses_for_period(user, db, month, year, category_id)

    if not expenses:
        raise HTTPException(status_code=404, detail="No expenses found for this period")

    csv_content = generate_csv(expenses, user.name)

    filename = f"expenses_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv"

    return StreamingResponse(
        iter([csv_content]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.get("/pdf")
async def export_pdf(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    month: int = Query(None),
    year: int = Query(None),
    category_id: UUID = Query(None)
):
    expenses, start_date, end_date = get_expenses_for_period(user, db, month, year, category_id)

    if not expenses:
        raise HTTPException(status_code=404, detail="No expenses found for this period")

    pdf_content = generate_pdf(expenses, user.name, start_date, end_date)

    filename = f"expenses_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.pdf"

    return StreamingResponse(
        BytesIO(pdf_content),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
