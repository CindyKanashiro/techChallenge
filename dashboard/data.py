import pandas as pd
import requests
from os import getenv

API_URL = getenv('API_URL_FOR_STREAMLIT', "http://localhost:8000")


def get_request_logs_data(min_ts: float | None) -> pd.DataFrame:
    logs = fetch_request_logs(min_ts)
    logs["ts"] = (
        pd.to_datetime(logs["ts"], unit="s")
        .astype("datetime64[s]")
        .dt.tz_localize("UTC")
        .dt.tz_convert("America/Sao_Paulo")
    )
    logs["status_code_level"] = logs["status_code"] // 100
    logs["is_error"] = logs["status_code_level"] >= 4

    return logs


def get_app_logs_data(min_ts: None) -> pd.DataFrame:
    logs = fetch_app_logs(min_ts)
    logs["ts"] = (
        pd.to_datetime(logs["ts"], unit="s")
        .astype("datetime64[ns]")
        .dt.tz_localize("UTC")
        .dt.tz_convert("America/Sao_Paulo")
    )

    return logs


def fetch_request_stats(min_ts: float) -> dict:
    response = requests.get(
        f"{API_URL}/log/requests/stats", params={"min_timestamp": min_ts}
    )
    response.raise_for_status()
    return response.json()


def fetch_request_logs(min_ts: float | None) -> pd.DataFrame:
    response = requests.get(f"{API_URL}/log/requests", params={"min_timestamp": min_ts})
    response.raise_for_status()
    return pd.DataFrame(response.json())


def fetch_app_logs(min_ts: float | None) -> pd.DataFrame:
    response = requests.get(f"{API_URL}/log/app", params={"min_timestamp": min_ts})
    response.raise_for_status()
    return pd.DataFrame(response.json())
