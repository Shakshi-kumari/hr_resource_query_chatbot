from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from backend.models.employee import Employee
import json
import os
from backend.rag.rag import search_employees, augment_query_with_employees, generate_response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'employees.json')
with open(DATA_PATH, 'r') as f:
    employees_data = json.load(f)["employees"]

@app.get("/employees/search", response_model=List[Employee])
def filter_employees(skill: str = None, min_experience: int = 0, available: bool = False):
    """Search employees by skill, experience, and availability."""
    results = []
    for emp in employees_data:
        if skill and skill not in emp["skills"]:
            continue
        if emp["experience_years"] < min_experience:
            continue
        if available and emp["availability"] != "available":
            continue
        results.append(emp)
    return results

@app.post("/chat")
def chat(query: dict):
    """Handle chat queries using RAG pipeline."""
    try:
        user_query = query.get("query", "")
        relevant_employees = search_employees(user_query, top_k=len(employees_data))
        response = generate_response(user_query, relevant_employees)
        return {"response": response, "employees": relevant_employees}
    except Exception as e:
        return {"response": f"Sorry, an error occurred while processing your request: {str(e)}", "employees": []} 