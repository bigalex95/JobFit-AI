# models.py
# Pydantic models for JobFit-AI

from pydantic import BaseModel

class Resume(BaseModel):
    name: str
    email: str
    skills: list[str]

class JobDescription(BaseModel):
    title: str
    requirements: list[str]
