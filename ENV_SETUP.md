# Environment Variables Setup

This project requires an OpenWeatherMap API key.

---

## 1️⃣ Create a `.env` File

In the project root (same folder as `docker-compose.yml`), create:

```
.env
```

Add:

```
OPENWEATHER_API_KEY=your_actual_api_key_here
```

Replace with your real API key.

---

## 2️⃣ Why This Is Needed

- `OPENWEATHER_API_KEY` → used in extract step
- `DB_*` variables → used by loader + dashboard
- Keeps secrets out of code

---

## 3️⃣ Make Sure `.env` Is Ignored

Add this to `.gitignore`:

```
.env
```

Never commit API keys.

---

## 4️⃣ Docker Uses These Automatically

Docker Compose reads `.env` automatically when you run:

```bash
docker compose up -d
```

Airflow and Dashboard containers receive the environment variables.

---

## 5️⃣ Verify Inside Container (Optional)

To confirm variable exists:

```bash
docker exec -it airflow_webserver env | grep OPENWEATHER
```
