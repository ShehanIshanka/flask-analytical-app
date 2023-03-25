from typing import Dict, NamedTuple

from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from src.tables import Commissions, OrderLines, Orders, ProductPromotions, Promotions


class CommissionAnalytics(NamedTuple):
    promotions: Dict = {}
    total: float = 0.0
    order_average: float = 0.0


class OrderAnalytics(NamedTuple):
    customers: int = 0
    items: int = 0
    total_discount_amount: float = 0.0
    discount_rate_avg: float = 0.0
    order_total_avg: float = 0.0
    commissions: Dict = CommissionAnalytics()._asdict()


def get_order_analytics(session: Session, day: str) -> OrderAnalytics:
    """
    Get analytics payload for a given day.
    :param session: DB session
    :param day: Day
    :return Analytics payload for a given day
    """

    result = _get_db_results(session=session, day=day)

    total_customer_count = len(set([r[2] for r in result]))
    total_orders = len(set([r[0] for r in result]))
    total_items = sum([r[5] for r in result])
    total_discounts = sum([r[6] for r in result])
    total_discount_rates = sum([r[7] for r in result])
    total_amount = sum([r[8] for r in result])
    total_commission = sum([r[8] * r[10] for r in result])

    promotions = {}
    for r in result:
        if r[9] is not None:
            promotions[r[9]] = promotions.get(r[9], 0) + r[8]

    return OrderAnalytics(
        customers=total_customer_count,
        items=total_items,
        total_discount_amount=total_discounts,
        discount_rate_avg=total_discount_rates / total_orders if total_orders else 0.0,
        order_total_avg=total_amount / total_orders if total_orders else 0.0,
        commissions=CommissionAnalytics(
            promotions=promotions,
            total=total_commission,
            order_average=total_commission / total_orders if total_orders else 0.0,
        )._asdict(),
    )


def _get_db_results(session: Session, day: str) -> list:
    """
    Get order analytics data for a given day.
    :param session: DB session
    :param day: Day
    :return List of rows includes order_id,vendor_id,customer_id,product_id,product_price,quantity,discounted_amount,discount_rate,total_amount,promotion_id,rate  # noqa:  E501
    """
    orders_query = (
        session.query(Orders).filter(func.date(Orders.created_at) == day).subquery()
    )
    order_lines_query = (
        session.query(orders_query)
        .outerjoin(OrderLines, orders_query.c.id == OrderLines.order_id)
        .with_entities(
            OrderLines.order_id,
            orders_query.c.vendor_id,
            orders_query.c.customer_id,
            OrderLines.product_id,
            OrderLines.product_price,
            OrderLines.quantity,
            OrderLines.discounted_amount,
            OrderLines.discount_rate,
            OrderLines.total_amount,
        )
        .subquery()
    )

    product_promotions_query = (
        session.query(ProductPromotions)
        .filter(func.date(ProductPromotions.date) == day)
        .subquery()
    )
    promotions_query = (
        session.query(Promotions)
        .outerjoin(
            product_promotions_query,
            Promotions.id == product_promotions_query.c.promotion_id,
        )
        .with_entities(
            product_promotions_query.c.product_id,
            product_promotions_query.c.promotion_id,
        )
        .subquery()
    )
    commissions_query = (
        session.query(Commissions).filter(func.date(Commissions.date) == day).subquery()
    )

    order_details_query = (
        session.query(order_lines_query)
        .outerjoin(
            promotions_query,
            order_lines_query.c.product_id == promotions_query.c.product_id,
        )
        .with_entities(
            order_lines_query.c.order_id,
            order_lines_query.c.vendor_id,
            order_lines_query.c.customer_id,
            order_lines_query.c.product_id,
            order_lines_query.c.product_price,
            order_lines_query.c.quantity,
            order_lines_query.c.discounted_amount,
            order_lines_query.c.discount_rate,
            order_lines_query.c.total_amount,
            promotions_query.c.promotion_id,
        )
        .subquery()
    )

    final_query = (
        session.query(order_details_query)
        .outerjoin(
            commissions_query,
            order_details_query.c.vendor_id == commissions_query.c.vendor_id,
        )
        .with_entities(
            order_details_query.c.order_id,
            order_details_query.c.vendor_id,
            order_details_query.c.customer_id,
            order_details_query.c.product_id,
            order_details_query.c.product_price,
            order_details_query.c.quantity,
            order_details_query.c.discounted_amount,
            order_details_query.c.discount_rate,
            order_details_query.c.total_amount,
            order_details_query.c.promotion_id,
            commissions_query.c.rate,
        )
    )

    return final_query.all()
