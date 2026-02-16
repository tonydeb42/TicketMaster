from worker.worker import app
from langchain_google_genai import ChatGoogleGenerativeAI
import json

@app.task
def generate_answer(data):
    try:
        query,top_chunks = data
        print(f"Generating answer for query: {query}")
        prompt = f'''
        You are a **final decision engine** inside a production ticket-assignment RAG pipeline. Your job is to select the single best employee who can most confidently resolve the user’s issue based strictly on structured employee metadata.

        ### USER QUERY

        {query}

        ---

        ### TOP 5 CANDIDATE EMPLOYEE CHUNKS (JSON)

        {top_chunks}

        Each chunk represents one employee and must be treated strictly as structured factual data.

        ---

        ### TASK

        Select **ONE employee only** who is the strongest possible match for resolving the user’s issue.

        Evaluation priority:

        1. Direct alignment between the issue and **Problem domains handled**.
        2. Strong match between **Primary skills** and technologies/infrastructure in the query.
        3. Supporting relevance from **Secondary skills**.
        4. Appropriate **role/title and department** for handling such tickets.
        5. Experience years only as a tie-breaker if relevance is otherwise similar.

        ---

        ### STRICT DECISION REQUIREMENTS

        * Choose a candidate only if the metadata strongly indicates they can confidently handle the issue.
        * Prefer deep relevance over superficial keyword matches.
        * Ignore missing or irrelevant fields.
        * Never hallucinate capabilities not explicitly present.
        * Do not hedge or output multiple candidates.

        ---

        ### OUTPUT RULES (CRITICAL)

        * Output ONLY the selected employee as a **valid JSON string** (strict JSON serialization).
        * Use double quotes for all keys and values.
        * Output must be a single plain JSON string — **no Markdown, no code fences, no backticks**.
        * Preserve the original field names, values, and ordering exactly.
        * Do NOT include explanations, commentary, labels, confidence scores, or extra text.
        * Do NOT reformat or prettify beyond valid JSON serialization.

        ---

        This is a strict selection + JSON serialization task — not explanation, formatting, or analysis.

        '''
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.0)
        response = llm.invoke(prompt)
        if isinstance(response.content, str):
            selected_employee = json.loads(response.content)
        else:
            selected_employee = response.content
        print(f"Selected employee: {json.dumps(selected_employee, indent=2)}")
        return selected_employee

    except Exception as e:
        print(f"Generating answer failed: {e}")
        raise e

# selected_employee = {"Employee ID": "EMP074", "Email": "ishaan.chatterjee@example.com", "Role/title": "Software Engineer", "Primary skills": "AWS, Docker", "Department": "Engineering", "Secondary skills": "Redis, Pandas, Prometheus, Kafka", "Experience years": 2, "Problem domains handled": "Banking Systems", "Name": "Ishaan Chatterjee"} 
# top_chunks = [{'Department': 'Engineering', 'Role/title': 'Backend Developer', 'Primary skills': 'TensorFlow, Kubernetes, Java', 'Email': 'aditya.joshi@example.com', 'Secondary skills': 'NumPy, Kafka', 'Problem domains handled': 'Healthcare', 'Employee ID': 'EMP013', 'Name': 'Aditya Joshi', 'Experience years': 8}, {'Problem domains handled': 'EdTech', 'Role/title': 'Software Engineer', 'Secondary skills': 'Kafka, Pandas, Scikit-learn, Prometheus', 'Primary skills': 'React, Kubernetes, Spring Boot', 'Experience years': 2, 'Employee ID': 'EMP001', 'Name': 'Vivaan Sharma', 'Department': 'Engineering', 'Email': 'vivaan.sharma@example.com'}, {'Employee ID': 'EMP074', 'Email': 'ishaan.chatterjee@example.com', 'Role/title': 'Software Engineer', 'Primary skills': 'AWS, Docker', 'Department': 'Engineering', 'Secondary skills': 'Redis, Pandas, Prometheus, Kafka', 'Experience years': 2, 'Problem domains handled': 'Banking Systems', 'Name': 'Ishaan Chatterjee'}, {'Department': 'Engineering', 'Role/title': 'ML Engineer', 'Secondary skills': 'CI/CD, Pandas, GraphQL, Kafka', 'Name': 'Diya Chatterjee', 'Primary skills': 'AWS, React, Java', 'Employee ID': 'EMP011', 'Experience years': 11, 'Problem domains handled': 'Telecom', 'Email': 'diya.chatterjee@example.com'}, {'Department': 'Engineering', 'Role/title': 'Frontend Developer', 'Employee ID': 'EMP060', 'Problem domains handled': 'Cybersecurity', 'Primary skills': 'Terraform, Kubernetes', 'Experience years': 4, 'Name': 'Arjun Chatterjee', 'Secondary skills': 'ELK, CI/CD, Pandas, NumPy', 'Email': 'arjun.chatterjee@example.com'}]
# query = "Our Kubernetes deployment on AWS keeps failing after CI/CD runs, Kafka event pipeline latency has spiked, and Prometheus alerts show abnormal container restarts — need someone who understands microservices infra, cloud, and backend debugging."
# generate_answer((query,top_chunks))