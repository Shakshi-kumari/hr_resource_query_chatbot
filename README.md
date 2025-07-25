# HR Resource Query Chatbot

## Overview
The HR Resource Query Chatbot is an intelligent assistant designed to help HR teams quickly find employees for projects and resource allocation using natural language queries. Leveraging modern NLP and retrieval techniques, the chatbot can answer questions like:
- "I need someone experienced with machine learning for a healthcare project"
- "List female engineers with at least 4 years of experience"
- "Who has worked on insurance or finance projects?"
- "Candidates with more than 5 years of experience"

The system uses a Retrieval-Augmented Generation (RAG) pipeline with semantic search and template-based natural language responses.

---

## Features
- 🔍 **Semantic Search:** Finds the most relevant employees using embeddings and cosine similarity.
- 🧑‍💻 **Natural Language Queries:** Supports flexible, human-like queries about skills, experience, and projects.
- 📝 **Context-Aware Responses:** Generates narrative, assignment-style recommendations for HR.
- 🗂️ **Rich Employee Profiles & Transformer-based Search:** Includes name, skills, gender, experience, projects, specialization, location, and availability. Uses SentenceTransformers for semantic matching.
- ⚡ **FastAPI Backend:** REST API for chat and employee search.
- 💬 **Modern Streamlit Frontend:** Clean chat UI with full-width input and real-time responses.
- ✅ **Error Handling:** User-friendly error messages and robust backend validation.
- 🔝 **Top 5 Results:** Only the most relevant candidates are shown for each query.

---

## Architecture

- **Frontend:** Streamlit app for chat and results display.
- **Backend:** FastAPI app with `/chat` and `/employees/search` endpoints.
- **RAG Pipeline:** Semantic search (MiniLM), filtering, and template-based response generation.
- **Data Layer:** JSON file with 15+ realistic employee profiles.

---

## Setup & Installation

### **1. Clone the repository:**
```bash
git clone https://github.com/Shakshi-kumari/hr_resource_query_chatbot.git
cd hr_resource_query_chatbot
```

### **2. Create and activate a virtual environment:**

#### **Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

#### **Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### **3. Install dependencies:**
```bash
pip install -r requirements.txt
```

### **4. Start the backend (FastAPI):**
```bash
uvicorn backend.main:app --reload
```

### **5. Start the frontend (Streamlit):**
```bash
streamlit run frontend/app.py
```

### **6. Open your browser:**
- Frontend: [http://localhost:8501](http://localhost:8501)
- Backend docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## API Documentation

### **POST /chat**
- **Description:** Submit a natural language query and get recommended employees.
- **Request Example:**
  ```json
  {
    "query": "Find Python developers with 3+ years experience"
  }
  ```
- **Response Example:**
  ```json
  {
    "response": "Based on your requirements (Find Python developers with 3+ years experience), I found 2 excellent candidates: ...",
    "employees": [
      {
        "id": 1,
        "name": "Alice Johnson",
        "gender": "female",
        "skills": ["Python", "React", "AWS"],
        "experience_years": 5,
        "projects": ["E-commerce Platform", "Healthcare Dashboard"],
        "availability": "available",
        "specialization": "Full Stack Development",
        "location": "New York"
      }
    ]
  }
  ```

### **GET /employees/search**
- **Description:** Search employees by skill, experience, and availability.
- **Query Parameters:** `skill`, `min_experience`, `available`
- **Example:** `/employees/search?skill=Python&min_experience=3&available=true`

---

## AI Development Process

- **AI Coding Assistants Used:**
  - **ChatGPT:** Used for architecture planning.
  - **Cursor AI:**
    1. Used for error handling, debugging, and code refactoring (backend and frontend).
    2. Used for designing the frontend and implementing filtering features.
    3. Helped debug and optimize the RAG pipeline.
    4. Provided suggestions for user experience improvements and filtering logic.
- **How AI Helped:**
  - Generating Employee Data
  - Helped debug and optimize the RAG pipeline.
  - Error handling and debugging.
  - Assisted in designing a clean, modular architecture.
  - Provided suggestions for user experience improvements and filtering logic.

---

## Technical Decisions

- **Why Open-Source Models:**
  - Chose SentenceTransformers (MiniLM) for embeddings due to ease of use, speed, and no API key required.
- **No LLM/Cloud API:**
  - Used semantic search + template-based generation for cost, privacy, and simplicity.
- **Performance vs. Cost vs. Privacy:**
  - All processing is local, no data leaves your machine.
  - FastAPI and Streamlit provide fast, interactive experience.

---

## Future Improvements

- **Real Data Set:** Integrate the system with a real-world HR database or import actual employee data to enable live, production-ready deployments and more realistic recommendations.
- **Multi-language support:** Extend the chatbot to understand and respond to queries in multiple languages, making it accessible to global HR teams and diverse workforces.
- **Fast response/fix:** Further optimize backend and frontend code to ensure instant responses, minimize latency, and provide a seamless user experience even under heavy load.
- **Performance optimization:** Profile and optimize the RAG pipeline, embedding computation, and API calls to handle larger datasets and more concurrent users efficiently.
- **User authentication:** Implement secure user authentication..
- **Advanced analytics and reporting:** Add detailed analytics and reporting features to help HR teams track resource allocation, employee skills, and project history for better decision-making.

---

## Demo

- **Live Demo:** https://drive.google.com/file/d/1q_rVUSnAfyIVtTPBxfpmydGBiDN-GFAS/view?usp=sharing