from worker.worker import app
import pandas as pd
from sentence_transformers import SentenceTransformer
from pathlib import Path

@app.task
def create_embeddings(file_path):
    try:
        print(f"Creating embeddings for file: {file_path}")
        df = pd.read_csv(file_path)

        texts = []
        metadata = []
        for _, row in df.iterrows():
                texts.append(", ".join(f"{col}: {val}" for col, val in row.items()))
                metadata.append(row.to_dict())

        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        embeddings = model.encode(texts, show_progress_bar=True, batch_size=50)
        embeddings = embeddings.tolist()

        file = Path(file_path)
        if file.exists():
            file.unlink()
        print(f"Processed {len(df)} rows and created embeddings.")
        return embeddings,texts,metadata
    except Exception as e:
        print(f"Error creating embeddings: {e}")
        raise e