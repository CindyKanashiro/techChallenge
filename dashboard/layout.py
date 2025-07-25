from dashboard.data import fetch_request_stats, get_request_logs_data, get_app_logs_data
from dashboard.charts import (
    render_request_metrics_panel,
    render_request_timeline_chart,
    render_application_logs,
    render_failed_requests_information,
)
from requests import RequestException
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta


def render_main_page():
    try:
        st.header("Books API: Status Board")

        time_range = st.selectbox(
            "Time Range",
            [
                "Last Hour",
                "Last 24 Hours",
                "Last 7 Days",
                "Last 30 Days",
                "Last 12 Months",
                "All Records",
            ],
            accept_new_options=False,
        )

        min_ts = _get_min_timestamp(time_range)
        # Painel com cards de métricas gerais sobre requisições
        request_stats = fetch_request_stats(min_ts)
        render_request_metrics_panel(**request_stats)

        # Visão detalhada
        request_logs = get_request_logs_data(min_ts)

        timeline_data = (
            _convert_logs_date(request_logs.copy(), time_range)
            .groupby(["ts", "is_error"], as_index=False)
            .size()
        )

        # Linha do tempo das requisições que deram certo
        st.subheader("Successful Requests over Time")
        render_request_timeline_chart(timeline_data.loc[~timeline_data["is_error"]])

        # Linha do tempo das requisições que deram erro
        st.subheader("Failed Requests over Time")
        render_request_timeline_chart(timeline_data.loc[timeline_data["is_error"]])

        # Tabela com detalhes dos erros de requisição
        st.subheader("Details of failed requests")
        render_failed_requests_information(request_logs)

        # Tabela com logs detalhados do funcionamento da aplicação
        app_logs = get_app_logs_data(min_ts)

        st.subheader("Application Logs")
        render_application_logs(app_logs)

    except RequestException:
        st.error(
            "Failed to properly communicate with the API. Please check the API server."
        )
        return


def _get_min_timestamp(time_range: str) -> float | None:
    now = datetime.now()
    if time_range == "Last Hour":
        return (now - timedelta(hours=1)).timestamp()
    if time_range == "Last 24 Hours":
        return (now - timedelta(hours=24)).timestamp()
    if time_range == "Last 7 Days":
        return (now - timedelta(days=7)).timestamp()
    if time_range == "Last 30 Days":
        return (now - timedelta(days=30)).timestamp()
    if time_range == "Last 12 Months":
        return (now - timedelta(days=365)).timestamp()

    return None


def _convert_logs_date(logs: pd.DataFrame, time_range: str) -> pd.DataFrame:
    if time_range == "Last 24 Hours":
        logs["ts"] = logs["ts"].dt.floor("h")
    if time_range in ("Last 7 Days", "Last 30 Days", "Last 12 Months", "All Records"):
        logs["ts"] = logs["ts"].dt.date

    return logs
