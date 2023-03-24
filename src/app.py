import os, logging
from flask import Flask, jsonify
from sqlalchemy import Engine
from sqlalchemy.orm import Session

from src.analytics import get_total_number_of_customers
from src.db import init_db, load_data, get_session
from src.tables import Orders

app = Flask(__name__)
try:
    engine: Engine = init_db()
    if os.getenv("DATA_DIR", ""):
        load_data(engine=engine, data_dir="./data")
    load_data(engine=engine, data_dir="./data")

    session: Session = get_session(engine=engine)
except Exception as e:
    logging.exception("Database initialization failed")
    raise e


@app.route("/")
def hello_world():
    return jsonify(customers=get_total_number_of_customers(session, "2019-08-01"))


if __name__ == "__main__":

    print(get_total_number_of_customers(session, "2019-08-01"))

    # app.run()
