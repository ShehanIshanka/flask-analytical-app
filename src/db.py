import os

import pandas as pd
from sqlalchemy import create_engine, Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

Base = declarative_base()


def init_db() -> Engine:
    """
    Initialize the DB
    :return: None
    """
    db_dir: str = os.path.join("./app-data", "db")
    os.makedirs(db_dir, exist_ok=True)

    engine: Engine = create_engine("sqlite:///app-data/db/data.db")
    Base.metadata.create_all(engine)

    return engine


def load_data(engine: Engine, data_dir: str) -> None:
    """
    Load dat from csv files
    :param engine: DB engine
    :param data_dir: Data directory
    :return: None
    """
    tables = [
        "orders",
        "order_lines",
        "products",
        "promotions",
        "product_promotions",
        "commissions",
    ]

    for table in tables:
        df = pd.read_csv(f"{data_dir}/{table}.csv")
        df.to_sql(con=engine, index=False, name=table, if_exists="replace")


def get_session(engine: Engine) -> Session:
    """
    Retrieve DB session
    :param engine: DB Engine
    :return: DB Session
    """
    session = sessionmaker(bind=engine)
    return session()
