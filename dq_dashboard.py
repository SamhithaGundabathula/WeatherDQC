import os
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine

st.set_page_config(page_title="Weather DQ Dashboard", layout="wide")
st.title("Weather Pipeline — Daily DQ Dashboard")

DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "root")
DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "weatherdb")

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

dq = pd.read_sql("""
SELECT run_id, check_name, status, metric_value, message, created_at
FROM dq_results
ORDER BY created_at DESC
LIMIT 500;
""", engine)

if dq.empty:
    st.info("No dq_results found yet. Trigger the Airflow DAG once.")
    st.stop()

latest_run = dq["run_id"].iloc[0]
latest = dq[dq["run_id"] == latest_run].copy()

passed = int((latest["status"] == "PASS").sum())
failed = int((latest["status"] == "FAIL").sum())
total = int(len(latest))

c1, c2, c3 = st.columns(3)
c1.metric("Run ID", latest_run)
c2.metric("Checks Passed", passed)
c3.metric("Checks Failed", failed)

st.caption(f"Total checks: {total}")

st.subheader("Failures (latest run)")
fails = latest[latest["status"] == "FAIL"]
if fails.empty:
    st.success("No failures ✅")
else:
    st.error("Failures found ❌")
    st.dataframe(fails, use_container_width=True)

st.subheader("All recent DQ results")
st.dataframe(dq, use_container_width=True)
