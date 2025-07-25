from pydantic import BaseModel
from typing import List

class Employee(BaseModel):
    id: int
    name: str
    gender: str
    skills: List[str]
    experience_years: int
    projects: List[str]
    availability: str
    specialization: str
    location: str 