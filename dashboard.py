import os
import pandas as pd
import psycopg2
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
}

st.set_page_config(page_title="Mundial 2026 - Dashboard", layout="wide")


@st.cache_data(ttl=300)
def load_matches():
    conn = psycopg2.connect(**DB_CONFIG)
    df = pd.read_sql("SELECT * FROM matches ORDER BY utc_date", conn)
    conn.close()
    return df


df = load_matches()

st.title("⚽ Dashboard - FIFA World Cup 2026")
st.markdown("Datos extraídos automáticamente vía pipeline ETL (Airflow + PostgreSQL)")

# --- Métricas destacadas ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de partidos", len(df))
finished = df[df["status"] == "FINISHED"]
col2.metric("Partidos finalizados", len(finished))
total_goals = (finished["home_score"] + finished["away_score"]).sum()
col3.metric("Goles totales", int(total_goals))
avg_goals = (finished["home_score"] + finished["away_score"]).mean()
col4.metric("Promedio de goles/partido", f"{avg_goals:.2f}")

st.divider()

# --- Filtros ---
st.sidebar.header("Filtros")
stages = st.sidebar.multiselect(
    "Fase del torneo", options=df["stage"].unique(), default=df["stage"].unique()
)
status_filter = st.sidebar.multiselect(
    "Estado", options=df["status"].unique(), default=df["status"].unique()
)

filtered_df = df[df["stage"].isin(stages) & df["status"].isin(status_filter)]

# --- Ranking de goles por equipo ---
st.subheader("🥅 Ranking de goles por equipo")

home_goals = finished.groupby("home_team")["home_score"].sum()
away_goals = finished.groupby("away_team")["away_score"].sum()
total_by_team = (home_goals.add(away_goals, fill_value=0)
                  .sort_values(ascending=False)
                  .head(15)
                  .reset_index())
total_by_team.columns = ["team", "goals"]

fig_goals = px.bar(
    total_by_team, x="goals", y="team", orientation="h",
    title="Top 15 equipos por goles anotados",
    color="goals", color_continuous_scale="Blues"
)
fig_goals.update_layout(yaxis={"categoryorder": "total ascending"})
st.plotly_chart(fig_goals, use_container_width=True)

# --- Partidos por fase ---
st.subheader("📊 Partidos por fase del torneo")
stage_counts = df["stage"].value_counts().reset_index()
stage_counts.columns = ["stage", "count"]
fig_stage = px.pie(stage_counts, names="stage", values="count", title="Distribución de partidos por fase")
st.plotly_chart(fig_stage, use_container_width=True)

# --- Tabla de partidos ---
st.subheader("📋 Detalle de partidos")
st.dataframe(
    filtered_df[["utc_date", "stage", "group", "home_team", "away_team",
                 "home_score", "away_score", "status"]],
    use_container_width=True,
    hide_index=True,
)