import httpx
from typing import Any, Dict, List
from sqlmodel import Session, select
from db.models import CompanyInfo, Experiment

# Configuration for the external ADK FastAPI server
ADK_SERVER_URL = "http://localhost:8001/process-experiment"

class ExperimentService:
    async def process_experiment(self, db: Session, steer_text: str, growth_objective: str) -> None:
        # 1. Fetch Company Info (assuming one company for now)
        company_info = db.exec(select(CompanyInfo)).first()
        company_data = company_info.model_dump() if company_info else {}

        # 2. Fetch Past Experiments
        experiments = db.exec(select(Experiment)).all()
        experiments_data = [exp.model_dump() for exp in experiments]

        # 3. Combine into one JSON object
        payload = {
            "steer_text": steer_text,
            "growth_objective": growth_objective,
            "company_info": company_data,
            "past_experiments": experiments_data
        }

        # 4. Make API call to the ADK FastAPI server
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(ADK_SERVER_URL, json=payload)
                response.raise_for_status()
                # Assuming no output is needed as per request
            except httpx.HTTPStatusError as e:
                print(f"Error calling ADK server: {e}")
                raise e
            except Exception as e:
                print(f"Unexpected error: {e}")
                raise e

experiment_service = ExperimentService()
