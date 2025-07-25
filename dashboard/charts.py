import pandas as pd
import plotly.express as px
import streamlit as st


def render_request_metrics_panel(
    total_requests: int, successful_requests: int, failed_requests: int
):
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Requests", total_requests, border=True)
    col2.metric("Successful Requests", successful_requests, border=True)
    col3.metric("Failed Requests", failed_requests, border=True)


def render_request_timeline_chart(data: pd.DataFrame):
    chart = px.line(
        data,
        x="ts",
        y="size",
        markers=True,
        labels={"ts": "Date/Time", "size": "Requests"},
    )

    st.plotly_chart(chart, use_container_width=True)


def render_failed_requests_information(data: pd.DataFrame):
    data = (
        data.loc[
            data["is_error"], ["ts", "path", "client_addr", "method", "status_code"]
        ]
        .copy()
        .rename(
            columns={
                "ts": "Date/Time",
                "path": "Path",
                "client_addr": "Client Address",
                "method": "HTTP Method",
                "status_code": "Status Code",
            }
        )
    )
    st.dataframe(data, hide_index=True)


def render_application_logs(data: pd.DataFrame):
    st.dataframe(
        data[["ts", "message", "filename", "lineno", "logger", "level"]].rename(
            columns={
                "ts": "Date/Time",
                "message": "Message",
                "filename": "File",
                "lineno": "Line",
                "logger": "Logger",
                "level": "Log Type",
            }
        ),
        hide_index=True,
    )
