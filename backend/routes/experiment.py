from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel import Session
from db.session import get_db
from services.experiment_service import experiment_service

router = APIRouter()

class ExperimentInput(BaseModel):
    steer_text: str
    growth_objective: str

@router.post("/")
async def run_experiment_workflow(
    input_data: ExperimentInput, 
    db: Session = Depends(get_db)
):
    try:
        await experiment_service.process_experiment(
            db=db, 
            steer_text=input_data.steer_text, 
            growth_objective=input_data.growth_objective
        )
        return {"status": "success", "message": "Experiment processed and sent to ADK server."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
