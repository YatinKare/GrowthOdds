import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class CompanyInfo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    industry: str

class Experiment(SQLModel, table=True):
    __tablename__ = "experiments"
    id: str = Field(primary_key=True)
    user_id: int
    product_id: Optional[str] = None
    title: str
    type: str
    goal: str
    channel: str
    user_note: Optional[str] = None
    status: str = "queued"
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now(datetime.timezone.utc))

class ExperimentRun(SQLModel, table=True):
    __tablename__ = "experiment_runs"
    id: str = Field(primary_key=True)
    experiment_id: str = Field(foreign_key="experiments.id")
    status: str
    plan_json: Optional[str] = None
    started_at: Optional[datetime.datetime] = None
    completed_at: Optional[datetime.datetime] = None

class ExperimentOutput(SQLModel, table=True):
    __tablename__ = "experiment_outputs"
    id: str = Field(primary_key=True)
    experiment_id: str = Field(foreign_key="experiments.id")
    kind: str
    label: str
    content: str
