from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def create_employee_text(employee):
    """Create a searchable text representation of an employee."""
    return (
        f"{employee['name']} is a {employee['specialization']} based in {employee['location']} with {employee['experience_years']} years of experience. "
        f"Their skills include {', '.join(employee['skills'])} and they have worked on projects like {', '.join(employee['projects'])}. "
        f"Current status: {employee['availability']}"
    )

def get_pronoun(gender):
    if gender.lower() == "female":
        return "She"
    elif gender.lower() == "male":
        return "He"
    else:
        return "They"

def find_relevant_project(projects, query, model=None):
    if not projects:
        return "various projects"
    if model is not None:
        project_embeddings = model.encode(projects)
        query_embedding = model.encode([query])
        similarities = cosine_similarity(query_embedding, project_embeddings)[0]
        best_idx = int(np.argmax(similarities))
        return projects[best_idx]

    query_lower = query.lower()
    stopwords = {"the", "and", "for", "with", "user", "more", "than", "of", "in", "on", "to", "a", "an", "is", "are"}
    keywords = [word for word in query_lower.split() if len(word) > 3 and word not in stopwords]
    best_project = None
    best_score = 0
    for project in projects:
        score = sum(1 for keyword in keywords if keyword in project.lower())
        if score > best_score:
            best_score = score
            best_project = project
    if best_project:
        return best_project
    for project in projects:
        for keyword in query_lower.split():
            if keyword in project.lower():
                return project
    return projects[0]

def polished_candidate_bullet(emp, query, model=None):
    pronoun = get_pronoun(emp.get('gender', 'other'))
    relevant_project = find_relevant_project(emp['projects'], query, model)
    skills = ', '.join(emp['skills'])
    return (
        f"- **{emp['name']}** would be perfect for this role. "
        f"{pronoun} has {emp['experience_years']} years of experience in {emp['specialization'].lower()} and "
        f"notably worked on the '{relevant_project}' project. "
        f"{pronoun} is skilled in {skills}. "
        f"{pronoun} is currently {emp['availability']}."
    )

def format_response_message(query, employees, model=None):
    if not employees:
        return "I couldn't find any employees matching your criteria."
    intro = f"Based on your requirements ({query}), I found {len(employees)} excellent candidate{'s' if len(employees) > 1 else ''}: \n"
    bullets = ""
    for emp in employees:
        bullets += polished_candidate_bullet(emp, query, model) + "\n"
    closing = (
        "\nWould you like more details about their experience, specific projects, or check their availability for meetings?"
    )
    return intro + bullets + closing 