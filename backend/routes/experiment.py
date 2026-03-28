import uuid
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List
from sqlmodel import Session, select
from db.session import get_db
from db.models import Experiment, ExperimentRun, ExperimentOutput
from services.experiment_service import experiment_service

router = APIRouter()

class ExperimentInput(BaseModel):
    product_id: str
    created_by: str
    experiment_title: str
    experiment_type: str
    goal: str
    channel: str
    user_note: str

@router.post("/")
async def run_experiment_workflow(
    input_data: ExperimentInput,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    try:
        exp_id = str(uuid.uuid4())
        
        # Determine an integer user_id. Since created_by is a string, mapping to 1.
        user_id = 1 
        
        new_experiment = Experiment(
            id=exp_id,
            user_id=user_id,
            product_id=input_data.product_id,
            title=input_data.experiment_title,
            type=input_data.experiment_type,
            goal=input_data.goal,
            channel=input_data.channel,
            user_note=input_data.user_note,
            status="queued"
        )
        db.add(new_experiment)
        db.commit()
        
        # Process the experiment async
        background_tasks.add_task(
            experiment_service.process_experiment,
            experiment_id=exp_id
        )
        
        return {"experiment_id": exp_id, "status": "queued"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{experiment_id}")
async def get_experiment(experiment_id: str, db: Session = Depends(get_db)):
    experiment = db.exec(select(Experiment).where(Experiment.id == experiment_id)).first()
    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")
        
    run = db.exec(select(ExperimentRun).where(ExperimentRun.experiment_id == experiment_id)).first()
    outputs = db.exec(select(ExperimentOutput).where(ExperimentOutput.experiment_id == experiment_id)).all()
    
    run_dict = {}
    if run and run.plan_json:
        import json
        try:
            run_dict = json.loads(run.plan_json)
        except:
            run_dict = run.plan_json

    return {
        "experiment": experiment,
        "run": run_dict,
        "outputs": outputs
    }
