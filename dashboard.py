import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://localhost:8000/api/v1"

st.title("📊 Dashboard - API Metrics")

# ====== Bloco 1: Métricas agregadas
summary = requests.get(f"{API_URL}/metrics").json()
st.metric("Total de Requisições", summary["total_requests"])
st.metric("Latência Média (ms)", round(summary["avg_latency"] * 1000, 2))

# ====== Bloco 2: Requisições detalhadas
st.subheader("📈 Histórico de chamadas recentes")

resp = requests.get(f"{API_URL}/metrics/detailed")
if resp.status_code == 200:
    data = resp.json()
    df = pd.DataFrame(data)

    # Converte timestamp
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["process_time_ms"] = df["process_time"] * 1000

    # Gráfico de linhas: latência ao longo do tempo
    fig = px.line(df.sort_values("timestamp"), x="timestamp", y="process_time_ms",
                  title="Tempo de resposta por chamada",
                  labels={"process_time_ms": "Latência (ms)"})
    st.plotly_chart(fig, use_container_width=True)

    # Gráfico de barras: requisições por método
    method_counts = df["method"].value_counts().reset_index()
    method_counts.columns = ["method", "count"]
    bar = px.bar(method_counts, x="method", y="count", title="Quantidade por método HTTP")
    st.plotly_chart(bar, use_container_width=True)

    # Mostrar tabela 
    st.dataframe(df[["timestamp", "method", "path", "status_code", "process_time_ms"]])
else:
    st.warning("Falha ao buscar dados detalhados.")
