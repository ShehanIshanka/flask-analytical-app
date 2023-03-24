import mock
from mock.mock import call
from src.db import init_db


@mock.patch("os.makedirs")
@mock.patch("src.db.Base.metadata.create_all")
@mock.patch("src.db.create_engine", return_value="engine")
def test_init_db(mock_create_engine, mock_create_all, mock_makedirs) -> None:
    assert init_db() == "engine"

    assert mock_makedirs.mock_calls == [call("./app-data/db", exist_ok=True)]
    assert mock_create_engine.mock_calls == [call("sqlite:///app-data/db/data.db")]
    assert mock_create_all.mock_calls == [call("engine")]
