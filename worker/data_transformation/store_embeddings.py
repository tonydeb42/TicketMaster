from worker.worker import app
import uuid
import numpy as np
import os
import redis
from redis.commands.search.field import VectorField, TextField
from redis.commands.search.index_definition import IndexDefinition, IndexType
from dotenv import load_dotenv
import json

load_dotenv()

REDIS_URL = os.getenv("REDIS_VECTOR_URL", "redis://localhost:6379/2")
INDEX_NAME = "employee_embeddings"

@app.task
def store_embeddings(data):
    try:
        embeddings,texts,metadata = data
        print(f"Storing {len(embeddings)} embeddings in ChromaDB...")

        redis_client = redis.from_url(REDIS_URL, decode_responses=False)

        try:
            redis_client.ft(INDEX_NAME).info()
        except:
            schema = (
                TextField("text"),
                TextField("department"),
                TextField("metadata"),
                VectorField(
                    "embedding",
                    "HNSW",
                    {
                        "TYPE": "FLOAT32",
                        "DIM": len(embeddings[0]),
                        "DISTANCE_METRIC": "COSINE"
                    },
                ),
            )
            redis_client.ft(INDEX_NAME).create_index(
                schema,
                definition=IndexDefinition(prefix=["emp:"], index_type=IndexType.HASH),
            )

        pipe = redis_client.pipeline()
        for emb, txt, meta in zip(embeddings, texts, metadata):
            key = f"emp:{uuid.uuid4()}"
            pipe.hset(
                key,
                mapping={
                    "embedding": np.array(emb, dtype=np.float32).tobytes(),
                    "text": txt,
                    "department": meta.get("Department", ""),
                    "metadata": json.dumps(meta),
                },
            )
        pipe.execute()

        return f"Stored {len(texts)} embeddings successfully." 
    except Exception as e:
        print(f"Error storing embeddings: {e}")
        raise e