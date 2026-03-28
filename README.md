# GrowthOdds

AI-powered marketing experiment generator for startups. Submit an experiment idea and get AI-generated marketing content based on past performance.

## How It Works

- User submits an experiment (title, goal, channel, notes)
- A Google ADK agent pipeline analyzes past experiments and generates optimized marketing content
- Results are stored and viewable in the dashboard

## Tech Stack

- **Frontend** -- SvelteKit, TypeScript
- **Backend** -- FastAPI, SQLModel, SQLite
- **Agents** -- Google ADK, Gemini 2.5 Flash

## Running Locally

- Start the ADK agent server:
  ```
  cd agents
  uvx --from google-adk adk api_server --port 8001
  ```
- Start the backend:
  ```
  cd backend
  uv run main.py
  ```
- Start the frontend:
  ```
  cd frontend/growthodds
  bun run dev
  ```
