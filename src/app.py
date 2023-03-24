import logging
import os
from datetime import date

from flask import Flask, jsonify, request, Response
from sqlalchemy import Engine
from sqlalchemy.orm import Session
from src.analytics import get_total_number_of_customers, get_total_number_of_items
from src.db import get_session, init_db, load_data


app = Flask(__name__)

try:
    # Initialize DB
    engine: Engine = init_db()
    # Load data from files if provided
    if os.getenv("DATA_DIR", ""):
        load_data(engine=engine, data_dir=os.environ["DATA_DIR"])

    session: Session = get_session(engine=engine)
except Exception as e:
    logging.exception("Database initialization failed")
    raise e


@app.route("/analytics", methods=["POST"])
def get_analytics() -> Response:
    day = request.get_json().get("day")
    if day is None:
        day = str(date.today())

    return jsonify(
        customers=get_total_number_of_customers(session=session, day=day),
        items=get_total_number_of_items(session=session, day=day),
    )


if __name__ == "__main__":
    app.run()
