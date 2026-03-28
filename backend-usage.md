# Backend Usage Guide

This guide explains how to start the backend services, test the experiment pipeline, and stop the services.

## 1. Starting the Services

You need two terminal windows to run the API and the ADK Agent locally.

**Terminal 1: ADK Agent Server**
```bash
cd agents
uvx --from google-adk adk api_server --port 8001
```

**Terminal 2: FastAPI Backend**
```bash
cd backend
uv run main.py
```

---

## 2. Testing the Pipeline

Once both services are running, you can submit an experiment. The backend will queue it and process it asynchronously.

**Submit an Experiment (POST)**
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/experiment/" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": "prod_123",
    "created_by": "user_123",
    "experiment_title": "Competitor comparison post",
    "experiment_type": "social_post",
    "goal": "increase signups",
    "channel": "x",
    "user_note": "focus on simpler UX"
}'
```

The response will look like this:
```json
{"experiment_id":"<YOUR-UUID-HERE>","status":"queued"}
```

**View the Results (GET)**
Wait about 10-15 seconds for the Google ADK to generate results, then poll the GET endpoint using your UUID.

```bash
curl -X GET "http://127.0.0.1:8000/api/v1/experiment/<YOUR-UUID-HERE>" | json_pp
```
*(If you do not have `json_pp` or `jq`, you can just paste the URL in your browser).*

---

## 3. Stopping the Services

When you're done, you can stop the services by pressing `Ctrl+C` in each of your open terminal windows.

If processes get stuck in the background, you can find and kill them:

```bash
# Find PIDs
sudo lsof -i :8000
sudo lsof -i :8001

# Kill them
kill -9 <PID>
```
