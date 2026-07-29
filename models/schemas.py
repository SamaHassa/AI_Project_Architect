from typing import List
from pydantic import BaseModel


class BasicInfo(BaseModel):
    project_name: str
    overview: str
    project_type: str
    target_users: str
    estimated_complexity: str
    
class Architecture(BaseModel):
    pattern: str
    reason: str
    mermaid_diagram: str

class Technology(BaseModel):
    category: str
    name: str
    reason: str

class Component(BaseModel):
    name: str
    purpose: str
    technologies: List[str]


class DatabaseTable(BaseModel):
    name: str
    fields: List[str]

class API(BaseModel):
    method: str
    endpoint: str
    description: str

class Requirement(BaseModel):
    title: str
    description: str


class Phase(BaseModel):
    phase: str
    duration: str
    tasks: List[str]


class Risk(BaseModel):
    risk: str
    mitigation: str

    
class ProjectBlueprint(BaseModel):

    basic_info: BasicInfo

    functional_requirements: List[Requirement]

    non_functional_requirements: List[Requirement]

    architecture: Architecture

    components: List[Component]

    data_flow: List[str]

    technology_stack: List[Technology]

    database_type: str

    database_tables: List[DatabaseTable]

    apis: List[API]

    folder_structure: str

    roadmap: List[Phase]

    risks: List[Risk]

    future_features: List[str]