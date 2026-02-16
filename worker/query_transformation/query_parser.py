from worker.worker import app
from langchain_google_genai import ChatGoogleGenerativeAI

@app.task
def query_parser(data):
    try:
        query,primary_skills,secondary_skills,department, roles = data
        print(f"Received query for embedding transformation: '{query}'")

        prompt = f'''
        You convert a user issue query into a structured employee-search string optimized for semantic embedding retrieval.

         Strict rules:

         1. Output must be ONE SINGLE LINE STRING ONLY.
            No explanation, no extra text, no markdown.

         2. Early rejection rule (highest priority):

            If you cannot confidently identify at least one relevant primary skill OR at least one relevant secondary skill from the provided lists, output exactly:

            no data

            * Do not output anything else in that case.
            * Do not attempt role assignment if skills cannot be determined.

         3. Never invent or infer:

            * Employee ID
            * Name
            * Email
            * Experience years

            These must NEVER appear in output.

         4. Skills extraction rules:

            * Only use skills present in the provided skill lists.
            * Select only clearly relevant skills.
            * Preserve original spelling and capitalization exactly.
            * Do NOT infer loosely related tools unless explicitly mentioned or strongly implied.

         5. Role/title rules:

            * You will receive allowed roles for the department.
            * Select a role only if strongly supported by the query.
            * If uncertain, omit the role entirely.
            * Never create new roles.

         6. Noise-reduction rule (critical for embeddings):

            * Include ONLY fields that contain confirmed information.
            * Completely OMIT empty or unknown fields.
            * Do NOT output placeholders, blank labels, or unused schema fields.

         7. Output formatting rules:

            * Format fields as: `Field: value`
            * Separate multiple fields with comma + space.
            * Keep concise wording optimized for semantic similarity search.
            * Output must remain a single line.

         ---

         Example 1

         INPUT

         QUERY:
         CI/CD deployment failing and Kubernetes pods restarting

         DEPARTMENT:
         Engineering

         PRIMARY SKILLS LIST:
         Kubernetes, Docker, Terraform

         SECONDARY SKILLS LIST:
         Prometheus, ELK

         POSSIBLE ROLES:
         Software Engineer, DevOps Engineer

         OUTPUT

         Department: Engineering, Role/title: DevOps Engineer, Primary skills: Kubernetes, Docker, Terraform, Secondary skills: Prometheus, ELK

         ---

         Example 2 (Reject case)

         INPUT

         QUERY:
         Need clarification on reimbursement policy

         DEPARTMENT:
         Engineering

         PRIMARY SKILLS LIST:
         Java, Spring Boot

         SECONDARY SKILLS LIST:
         SQL

         POSSIBLE ROLES:
         Software Engineer, DevOps Engineer

         OUTPUT

         no data

         ---

         QUERY:
         {query}

         DEPARTMENT:
         {department}

         PRIMARY SKILLS LIST:
         {primary_skills}

         SECONDARY SKILLS LIST:
         {secondary_skills}

         POSSIBLE ROLES:
         {roles}

        '''
     
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.0)
        response = llm.invoke(prompt)

        return department,query,response.content
    except Exception as e:
        print(f"Error in query to embedding transformation: {e}")
        raise e
    

# response = "Department: Cloud Ops, Role/title: Data Scientist, Primary skills: R, Python, SQL, Secondary skills: Pandas, ggplot2"    

# query = "Need to build a credit risk scoring model using historical loan data, experience with financial datasets required."

# primary_skills = "PowerBI, R, SQL, Python, Tableau"

# secondary_skills = "Pandas, ggplot2, PowerBI, Tableau, Shiny, Excel"

# department = "Cloud Ops"

# roles = "Data Scientist, Data Analyst"

# data = (query,primary_skills,secondary_skills,department,roles)
# result = query_parser(data)    
# print(result[2])