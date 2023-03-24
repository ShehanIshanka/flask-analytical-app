from datetime import datetime, date

from sqlalchemy import distinct, null, Date, cast
from sqlalchemy.sql import func
from sqlalchemy.orm import Session

from src.tables import Orders


def get_total_number_of_customers(
    session: Session, day: str = str(date.today())
) -> int:
    return len(
        session.query(Orders)
        .filter(Orders.customer_id != null())
        .filter(func.date(Orders.created_at) == day)
        .with_entities(distinct(Orders.customer_id))
        .all()
    )


def get_total_number_of_customers(
    session: Session, day: str = str(date.today())
) -> int:
    return len(
        session.query(Orders)
        .filter(Orders.customer_id != null())
        .filter(func.date(Orders.created_at) == day)
        .with_entities(distinct(Orders.customer_id))
        .all()
    )
