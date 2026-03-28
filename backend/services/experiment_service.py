import httpx
import json
import uuid
import datetime
from typing import Any, Dict, List
from sqlmodel import Session, select
from db.models import Experiment, ExperimentRun, ExperimentOutput
from db.session import engine
from config import ADK_SERVER_URL

class ExperimentService:
    def list_experiments(self, db: Session) -> List[Dict[str, Any]]:
        experiments = db.exec(
            select(Experiment).order_by(Experiment.created_at.desc())
        ).all()

        return [
            {
                "id": experiment.id,
                "title": experiment.title,
                "status": experiment.status,
                "created_at": experiment.created_at,
            }
            for experiment in experiments
        ]

    async def process_experiment(self, experiment_id: str) -> None:
        with Session(engine) as db:
            experiment = db.exec(select(Experiment).where(Experiment.id == experiment_id)).first()
            if not experiment:
                print(f"Error: Experiment {experiment_id} not found in DB.")
                return
            
            # Transition to running
            experiment.status = "running"
            db.commit()

            # Initialize Run
            run_id = str(uuid.uuid4())
            run = ExperimentRun(
                id=run_id,
                experiment_id=experiment_id,
                status="running",
                started_at=datetime.datetime.utcnow()
            )
            db.add(run)
            db.commit()

            # Setup contextual payloads
            product_mock = {
                "id": experiment.product_id,
                "name": "GrowthOdds",
                "tagline": "AI growth agent for startups",
                "url": "https://growthodds.app"
            }
            analytics_mock = {
                "visitors_7d": 42,
                "signups_7d": 3
            }

            # Build Agent Context 
            context_payload = {
                "experiment": {
                    "id": experiment.id,
                    "title": experiment.title,
                    "type": experiment.type,
                    "goal": experiment.goal,
                    "channel": experiment.channel,
                    "user_note": experiment.user_note
                },
                "product": product_mock,
                "analytics_summary": analytics_mock
            }
            
            try:
                # Call ADK Server
                async with httpx.AsyncClient(timeout=60.0) as client:
                    app_name = "generate_suggestions"
                    user_id_str = str(experiment.user_id)
                    
                    # 1. Create a session for the agent first
                    session_url = f"{ADK_SERVER_URL}/apps/{app_name}/users/{user_id_str}/sessions"
                    session_response = await client.post(session_url, json={})
                    session_response.raise_for_status()
                    session_data = session_response.json()
                    assigned_session_id = session_data.get("id")

                    try:
                        # 2. Re-map payload with correctly generated sessionId
                        adk_payload = {
                            "appName": app_name,
                            "userId": user_id_str,
                            "sessionId": assigned_session_id,
                            "newMessage": {
                                "role": "user",
                                "parts": [
                                    {"text": json.dumps(context_payload)}
                                ]
                            },
                            "streaming": False
                        }

                        # 3. Post to the actual run endpoint
                        run_url = f"{ADK_SERVER_URL}/run"
                        response = await client.post(run_url, json=adk_payload)
                        response.raise_for_status()
                        
                        # ADK Output Schema parse
                        adk_response = response.json()
                        
                        plan_data = {}
                        outputs_data = []

                        if isinstance(adk_response, list):
                            for item in adk_response:
                                author = item.get("author", "")
                                state_delta = item.get("actions", {}).get("stateDelta", {})
                                
                                if "past_experiements_reccomendations" in state_delta:
                                    plan_data["past_experiements_reccomendations"] = state_delta["past_experiements_reccomendations"]
                                    
                                if "post_content" in state_delta:
                                    outputs_data.append({
                                        "kind": "post",
                                        "label": author,
                                        "content": state_delta["post_content"]
                                    })

                        # Persist run parsing details
                        run.plan_json = json.dumps(plan_data)
                        run.status = "completed"
                        run.completed_at = datetime.datetime.utcnow()

                        for out in outputs_data:
                            db.add(ExperimentOutput(
                                id=str(uuid.uuid4()),
                                experiment_id=experiment_id,
                                kind=out.get("kind", ""),
                                label=out.get("label", ""),
                                content=out.get("content", "")
                            ))

                        experiment.status = "completed"
                        db.commit()

                    finally:
                        # 4. Clean up the ADK session to avoid memory bloat
                        if assigned_session_id:
                            try:
                                delete_url = f"{ADK_SERVER_URL}/apps/{app_name}/users/{user_id_str}/sessions/{assigned_session_id}"
                                await client.delete(delete_url)
                            except Exception as cleanup_err:
                                print(f"Warning: Failed to clean up ADK session {assigned_session_id}: {cleanup_err}")

            except Exception as e:
                print(f"Unexpected error interfacing with ADK: {e}")
                run.status = "failed"
                run.completed_at = datetime.datetime.utcnow()
                experiment.status = "failed"
                db.commit()

experiment_service = ExperimentService()
