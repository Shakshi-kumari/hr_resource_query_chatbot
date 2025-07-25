import os
import json
import re
from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from backend.rag.utils import create_employee_text, format_response_message

DATA_PATH = os.path.join(os.path.dirname(__file__), '../data/employees.json')
with open(DATA_PATH, 'r') as f:
    employees = json.load(f)["employees"]

MODEL_NAME = 'all-MiniLM-L6-v2'
model = SentenceTransformer(MODEL_NAME)

embeddings = model.encode([create_employee_text(e) for e in employees])

EXPERIENCE_REGEX = {
    "min": [r"(\d+)\+?\s*years?", r"at least (\d+)\s*years?", r"more than (\d+)\s*years?", r"minimum (\d+)\s*years?"],
    "max": [r"less than (\d+)\s*years?", r"under (\d+)\s*years?", r"below (\d+)\s*years?"]
}

SKILL_CATEGORIES = {
    "backend": ["python", "java", "node.js", "c#", ".net", "flask", "django", "spring", "express"],
    "frontend": ["react", "vue", "angular", "typescript", "javascript"],
    "cloud": ["aws", "azure", "gcp"],
    "devops": ["docker", "kubernetes", "terraform", "devops"],
    "data": ["mongodb", "postgresql", "mysql", "sql", "pandas"],
    "ml": ["machine learning", "ai", "data science", "tensorflow", "pytorch", "nlp", "deep learning"],
    "mobile": ["mobile", "ios", "android", "react native", "flutter"],
    "other": ["firebase"]
}

def parse_experience(query):
    q = query.lower()
    for pattern in EXPERIENCE_REGEX["min"]:
        match = re.search(pattern, q)
        if match:
            return int(match.group(1)), ">="
    for pattern in EXPERIENCE_REGEX["max"]:
        match = re.search(pattern, q)
        if match:
            return int(match.group(1)), "<"
    return None, None

def parse_skills(query):
    q = query.lower()
    found = set()
    for group in SKILL_CATEGORIES.values():
        for skill in group:
            if skill in q:
                found.add(skill)
    return list(found)

def filter_candidates(candidates, min_exp=None, exp_op=None, skills=None):
    filtered = candidates
    if min_exp is not None and exp_op is not None:
        if exp_op == ">=":
            filtered = [c for c in filtered if c["experience_years"] >= min_exp]
        elif exp_op == "<":
            filtered = [c for c in filtered if c["experience_years"] < min_exp]
    if skills:
        filtered = [c for c in filtered if all(s in [sk.lower() for sk in c["skills"]] for s in skills)]
    return filtered

def augment_query_with_employees(query, employees):
    context = f"User query: {query}\n\nRelevant employees:\n"
    for emp in employees:
        context += f"- {emp['name']} ({emp['experience_years']} yrs): Skills: {', '.join(emp['skills'])}; Projects: {', '.join(emp['projects'])}; Availability: {emp['availability']}\n"
    return context

def generate_response(prompt: str, employees: list) -> str:
    return format_response_message(prompt, employees, model)

SIMILARITY_THRESHOLD = 0.2

def search_employees(query, top_k=10):
    query_emb = model.encode([query])
    similarities = cosine_similarity(query_emb, embeddings)[0]
    top_indices = np.argsort(similarities)[::-1][:top_k]
    results = [employees[i] for i in top_indices if similarities[i] > SIMILARITY_THRESHOLD]
    min_exp, exp_op = parse_experience(query)
    skills = parse_skills(query)
    results = filter_candidates(results, min_exp, exp_op, skills)
    return results[:5] 