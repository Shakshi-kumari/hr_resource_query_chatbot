import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="HR Resource Query Chatbot", page_icon="🤖", layout="wide")

with st.sidebar:
    st.markdown("### 👋 Hi HRs!")
    st.write("Welcome to your assistant for employee skill, project & experience queries.")
    if st.button("Start New Chat 🔄"):
        st.session_state["messages"] = []
        st.session_state["search_skill"] = ""
        st.session_state["search_min_experience"] = 0
        st.session_state["search_available"] = False

st.title("HR Resource Query Chatbot 👥")

st.markdown("""
**Try asking:**
- I need someone experienced with machine learning for a healthcare project
- List female engineers with at least 4 years of experience
- Who has worked on insurance or finance projects?
- Candidates with more than 5 years of experience
""")

st.markdown("---")
st.header("🔎 Employee Search")
with st.form("employee_search_form"):
    col1, col2, col3 = st.columns([2, 1, 2])
    with col1:
        skill = st.text_input("Skill (e.g., Python, React, AWS)", key="search_skill")
    with col2:
        min_experience = st.number_input("Min Years", min_value=0, step=1, key="search_min_experience")
    with col3:
        available = st.checkbox("Only available", key="search_available")
    search_submitted = st.form_submit_button("Search Employees")

search_results = None
if search_submitted:
    params = {}
    if skill:
        params["skill"] = skill
    if min_experience:
        params["min_experience"] = int(min_experience)
    if available:
        params["available"] = True
    try:
        resp = requests.get(f"{API_URL}/employees/search", params=params)
        if resp.status_code == 200:
            search_results = resp.json()
        else:
            st.error(f"Search error: {resp.text}")
    except Exception as e:
        st.error(f"Error connecting to backend: {str(e)}")

if search_results is not None:
    if len(search_results) == 0:
        st.info("No employees found matching your criteria.")
    else:
        st.markdown(f"**Found {len(search_results)} employees:**")
        st.dataframe(search_results)

if "messages" not in st.session_state:
    st.session_state.messages = []

query = st.chat_input("Ask about employee skills, experience, or projects...")

if query:
    st.session_state.messages.append({"role": "user", "content": query})
    with st.spinner("Thinking..."):
        try:
            response = requests.post(f"{API_URL}/chat", json={"query": query})
            if response.status_code == 200:
                result = response.json()
                st.session_state.messages.append({"role": "assistant", "content": result["response"]})
            else:
                st.error(f"Error: {response.text}")
        except Exception as e:
            st.error(f"Error connecting to backend: {str(e)}")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
