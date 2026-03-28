from typing import List, Optional
from sqlmodel import Field, SQLModel, Relationship

class CompanyInfo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    industry: str

class Experiment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: str
    outcome: str
    company_id: int = Field(foreign_key="companyinfo.id")
