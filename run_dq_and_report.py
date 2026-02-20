import json
import os
from datetime import datetime, timezone, date

import pandas as pd
from sqlalchemy import create_engine, text


DB_USER = "root"
DB_PASS = "root"
DB_HOST = "postgres"
DB_PORT = "5432"
DB_NAME = "weatherdb"

engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

RUN_ID = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
TODAY = date.today()  # local date is fine for daily run

CHECKS = [
    # Null checks (count null rows)
    ("null_temp", """
        SELECT COUNT(*)::float AS metric
        FROM weather_nb
        WHERE temp_c IS NULL;
    """, "metric == 0"),

    ("null_humidity", """
        SELECT COUNT(*)::float AS metric
        FROM weather_nb
        WHERE humidity_pct IS NULL;
    """, "metric == 0"),

    ("null_pressure", """
        SELECT COUNT(*)::float AS metric
        FROM weather_nb
        WHERE pressure_hpa IS NULL;
    """, "metric == 0"),

    # Range checks (count out-of-range rows)
    ("temp_range", """
        SELECT COUNT(*)::float AS metric
        FROM weather_nb
        WHERE temp_c IS NOT NULL AND (temp_c < -50 OR temp_c > 60);
    """, "metric == 0"),

    ("humidity_range", """
        SELECT COUNT(*)::float AS metric
        FROM weather_nb
        WHERE humidity_pct IS NOT NULL AND (humidity_pct < 0 OR humidity_pct > 100);
    """, "metric == 0"),

    ("pressure_range", """
        SELECT COUNT(*)::float AS metric
        FROM weather_nb
        WHERE pressure_hpa IS NOT NULL AND (pressure_hpa < 900 OR pressure_hpa > 1100);
    """, "metric == 0"),

    # Duplicate check (count extra rows beyond unique pairs)
    ("duplicates_city_time", """
        SELECT COALESCE(SUM(cnt - 1), 0)::float AS metric
        FROM (
          SELECT city, observed_at_utc, COUNT(*) AS cnt
          FROM weather_nb
          WHERE city IS NOT NULL AND observed_at_utc IS NOT NULL
          GROUP BY city, observed_at_utc
          HAVING COUNT(*) > 1
        ) t;
    """, "metric == 0"),

    # Freshness check for today's data (Did we load today’s data?”)
    ("freshness_today", """
        SELECT CASE
  WHEN COUNT(*) > 0 THEN 0
  ELSE 1
END::float AS metric
FROM weather_nb
WHERE observed_at_utc IS NOT NULL
  AND observed_at_utc::date = CURRENT_DATE
    """, "metric == 0"),
]

def eval_rule(rule: str, metric: float) -> bool:
    # rules are simple strings like "metric == 0"
    return eval(rule, {"metric": metric})

results = []
with engine.begin() as conn:
    for check_name, sql, rule in CHECKS:
        metric = conn.execute(text(sql)).scalar()
        metric = float(metric) if metric is not None else float("nan")
        passed = eval_rule(rule, metric)
        status = "PASS" if passed else "FAIL"

        msg = "ok" if passed else f"check failed, metric={metric}"
        results.append({
            "run_id": RUN_ID,
            "check_name": check_name,
            "status": status,
            "metric_value": metric,
            "message": msg
        })

    # insert results into dq_results
    conn.execute(
        text("""
          INSERT INTO dq_results (run_id, check_name, status, metric_value, message)
          VALUES (:run_id, :check_name, :status, :metric_value, :message)
        """),
        results
    )

# Create a daily report file
os.makedirs("reports", exist_ok=True)

passed = sum(1 for r in results if r["status"] == "PASS")
failed = sum(1 for r in results if r["status"] == "FAIL")

report = {
    "run_id": RUN_ID,
    "run_date": str(TODAY),
    "total_checks": len(results),
    "passed": passed,
    "failed": failed,
    "failures": [r for r in results if r["status"] == "FAIL"]
}

report_path = f"reports/dq_report_{TODAY}.json"
with open(report_path, "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2)

print("Saved report:", report_path)
print("Checks:", len(results), "| Passed:", passed, "| Failed:", failed)
