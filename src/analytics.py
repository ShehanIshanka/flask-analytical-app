from sqlalchemy import distinct, null
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from src.tables import OrderLines, Orders


def get_total_number_of_customers(session: Session, day: str) -> int:
    """
    Get total number of customers for a given day.
    :param session: DB session
    :param day: Day
    :return: Total number of customers
    """

    return len(
        session.query(Orders)
        .filter(Orders.customer_id != null())
        .filter(func.date(Orders.created_at) == day)
        .with_entities(distinct(Orders.customer_id))
        .all()
    )


def get_total_number_of_items(session: Session, day: str) -> int:
    """
    Get total number of items purchased for a given day.
    :param session: DB session
    :param day: Day
    :return Total number of items purchased
    """

    subquery = (
        session.query(Orders).filter(func.date(Orders.created_at) == day).subquery()
    )
    result = (
        session.query(subquery)
        .outerjoin(OrderLines, subquery.c.id == OrderLines.order_id)
        .with_entities(OrderLines.quantity)
        .all()
    )
    return sum([r[0] for r in result])
