import logging
import os
from datetime import date

from flask import Flask, jsonify, request, Response
from sqlalchemy import Engine
from sqlalchemy.orm import Session
from src.analytics import get_order_analytics, OrderAnalytics
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

    payload: OrderAnalytics = get_order_analytics(session=session, day=day)
    return jsonify(payload._asdict())


if __name__ == "__main__":
    app.run()
