from worker.worker import app
from sentence_transformers import SentenceTransformer
import redis
import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import numpy as np

load_dotenv()

REDIS_URL = os.getenv("REDIS_VECTOR_URL", "redis://localhost:6379/0")
INDEX_NAME = "employee_embeddings"

@app.task
def retrieve_chunks(data):
    try:
        department,query,parsed_data = data
        if parsed_data == 'no data':
            raise ValueError("No relevant skills identified. Please choose correct department or try reframing your query.")

        print(f"Received structured query for chunk retrieval: '{data}'")

        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        embeddings = model.encode(parsed_data, show_progress_bar=True).tolist()

        redis_client = redis.from_url(REDIS_URL, decode_responses=True)

        query_vec = np.array(embeddings, dtype=np.float32).tobytes()
        query = f'(@department:"{department}")=>[KNN 10 @embedding $vec AS score]'
        results = redis_client.ft("employee_embeddings").search(
            query,
            query_params={"vec": query_vec}
        )

        results = [
            json.dumps(json.loads(doc.metadata), ensure_ascii=False, indent=2)
            for doc in results.docs
        ]

        retrieved_chunks = "\n---CHUNK---\n".join(results)

        prompt = f'''
        You are an expert reranking engine inside a **production RAG ticket-assignment system**. Your job is to identify which employees are most suitable to handle a user’s issue based on structured employee metadata retrieved from a vector database.

        ### USER QUERY

        {query}


        ### RETRIEVED EMPLOYEE CHUNKS (JSON)

        {retrieved_chunks}

        Each chunk represents ONE employee and must be treated strictly as structured factual data (NOT narrative text). Typical fields may include:

        * Name
        * Employee ID
        * Email
        * Department
        * Role/title
        * Primary skills
        * Secondary skills
        * Experience years
        * Problem domains handled

        ---

        ### TASK

        1. Rank employees strictly by their likelihood of successfully handling the user’s issue.

        2. Ranking priorities (highest → lowest):

        **A. Core technical capability**

        * Primary skills matching technologies/platforms/concepts in the query.

        **B. Direct domain match**

        * Use “Problem domains handled” aligning with the issue.

        **C. Supporting capability**

        * Secondary skills reinforcing suitability.
        
        **D. Organizational relevance**

        * Department and role/title fit for the ticket category.

        **E. Experience (tie-breaker only)**

        * Use years of experience only if relevance is otherwise similar.

        3. Handle imperfect data robustly:

        * Ignore missing or irrelevant fields.
        * Never hallucinate attributes.
        * Do not penalize unrelated extra skills.
        * Focus strictly on capability to resolve the ticket.

        4. Prioritize precision over recall:

        * Strong matches only.
        * Avoid weak or speculative matches.

        ---

        ### OUTPUT RULES (STRICT)

        * Return ONLY the TOP 5 employee JSON chunks.
        * Reproduce each chunk EXACTLY as received.
        * Preserve formatting, field order, punctuation, and spacing.
        * Do NOT summarize, explain, justify, or rank numerically.
        * Do NOT output reasoning, commentary, labels, or headers.
        * If fewer than 5 chunks exist, return all unchanged.

        ---

        This is a strict reranking and extraction task — NOT generation, summarization, or analysis.
        '''

        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.0)
        response = llm.invoke(prompt)

        content = response.content.strip()
        if content.startswith("```"):
            content = content.split("\n", 1)[1] if "\n" in content else content[3:]
            if content.endswith("```"):
                content = content.rsplit("```", 1)[0]

        top_chunks = [
            json.loads(chunk.strip()) 
            for chunk in content.strip().split("\n---CHUNK---\n") 
            if chunk.strip()
        ]

        return query,top_chunks
    
    except Exception as e:
        print(f"Error in retrieving and reranking chunks: {e}")
        raise e




# response = "Department: Cloud Ops, Role/title: Data Scientist, Primary skills: R, Python, SQL, Secondary skills: Pandas, ggplot2"
# query,top_chunks = retrieve_chunks(("Data Science",
#                  "Need to build a credit risk scoring model using historical loan data, experience with financial datasets required.",
#                  response))
# print(top_chunks)
# retrieve_chunks(("Data Science",
#                  "Need to build a credit risk scoring model using historical loan data, experience with financial datasets required.",
#                  response))