from worker.worker import app
from dotenv import load_dotenv
import os
import redis
import json

load_dotenv()

REDIS_URL = os.getenv("REDIS_VECTOR_URL", "redis://localhost:6379/0")
INDEX_NAME = "employee_embeddings"


@app.task
def extract_metadata(query, department):
    try:
        print(f"Extracting metadata for '{department}'")

        redis_client = redis.from_url(REDIS_URL, decode_responses=True)

        q = f"@department:{department}"
        results = redis_client.ft(INDEX_NAME).search(q)

        primary_skills = set()
        secondary_skills = set()
        roles = set()

        for doc in results.docs:
            meta = json.loads(doc.metadata)

            ps = str(meta.get("Primary skills", "")).split(", ")
            ss = str(meta.get("Secondary skills", "")).split(", ")
            r = str(meta.get("Role/title", ""))

            primary_skills.update(ps)
            secondary_skills.update(ss)
            roles.add(r)

        primary_skills = ", ".join(s for s in primary_skills if s)
        secondary_skills = ", ".join(s for s in secondary_skills if s)
        roles = ", ".join(r for r in roles if r)

        print("Metadata extraction complete")

        return query, primary_skills, secondary_skills, department, roles

    except Exception as e:
        print(f"Error extracting metadata: {e}")
        raise e

# query = "Need to build a credit risk scoring model using historical loan data, experience with financial datasets required." 
# department = "Data Science" 
# query, primary_skills, secondary_skills, department, roles = extract_metadata(query,department) 
# print(primary_skills) 
# print(secondary_skills) 
# print(roles)