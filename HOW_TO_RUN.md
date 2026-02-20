# How to Run the Project

## 1️⃣ Start All Services (Docker)

From project root (where `docker-compose.yml` exists):

```bash
docker compose up -d --build
```

This starts:

- Postgres
- pgAdmin
- Airflow (webserver + scheduler)
- DQ Dashboard

---

## 2️⃣ Access Services

| Service | URL |
|---|---|
| Airflow UI | http://localhost:8080 |
| Streamlit DQ Dashboard | http://localhost:8501 |
| pgAdmin | http://localhost:8085 |

---

## 3️⃣ Trigger the Pipeline

1. Open Airflow UI
2. Enable DAG: `weather_nb_daily_pipeline`
3. Click **Trigger DAG**

Pipeline order:

```
extract → transform → load → dq
```

---

## 4️⃣ Stop the Project

```bash
docker compose down
```

---

## 5️⃣ Reset Everything (Optional Clean Start)

> ⚠️ This deletes database data.

```bash
docker compose down -v
docker compose up -d --build
```
