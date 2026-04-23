from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import RecurringExpense, Expense, FrequencyEnum
import logging

logger = logging.getLogger(__name__)

def generate_recurring_expenses():
    """Generate recurring expenses that are due today"""
    db = SessionLocal()
    try:
        today = date.today()
        active_recurring = db.query(RecurringExpense).filter(
            RecurringExpense.is_active == True
        ).all()

        for recurring in active_recurring:
            expense = recurring.expense
            last_execution = recurring.last_execution_date

            should_execute = False

            if last_execution is None:
                should_execute = True
            elif recurring.frequency == FrequencyEnum.WEEKLY:
                should_execute = today >= last_execution + timedelta(weeks=1)
            elif recurring.frequency == FrequencyEnum.MONTHLY:
                should_execute = today >= last_execution + relativedelta(months=1)
            elif recurring.frequency == FrequencyEnum.YEARLY:
                should_execute = today >= last_execution + relativedelta(years=1)

            if should_execute:
                # Créer une nouvelle dépense basée sur le template
                new_expense = Expense(
                    user_id=expense.user_id,
                    category_id=expense.category_id,
                    title=expense.title,
                    amount=expense.amount,
                    date=today,
                    note=f"Auto-generated: {expense.note}" if expense.note else "Auto-generated",
                    is_recurring=False
                )
                db.add(new_expense)

                # Mettre à jour la dernière exécution
                recurring.last_execution_date = today

                logger.info(f"Generated recurring expense: {recurring.recurring_id} for user {recurring.user_id}")

        db.commit()
        logger.info("Recurring expenses generation completed")

    except Exception as e:
        logger.error(f"Error generating recurring expenses: {e}")
        db.rollback()
    finally:
        db.close()

def start_scheduler():
    """Start background scheduler for recurring expenses"""
    try:
        from apscheduler.schedulers.background import BackgroundScheduler
        from apscheduler.triggers.cron import CronTrigger

        scheduler = BackgroundScheduler()
        # Run at 1:00 AM every day
        scheduler.add_job(
            generate_recurring_expenses,
            CronTrigger(hour=1, minute=0),
            id='recurring_expenses',
            name='Generate recurring expenses'
        )
        scheduler.start()
        logger.info("Scheduler started for recurring expenses")
        return scheduler
    except ImportError:
        logger.warning("APScheduler not installed, recurring expenses won't be auto-generated")
        return None
