CREATE TABLE IF NOT EXISTS dq_results (
    run_id TEXT,
    check_name TEXT,
    status TEXT,                    -- PASS / FAIL
    metric_value DOUBLE PRECISION,
    message TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);


CREATE DATABASE airflow_db;
