from pathlib import Path

import chromadb
import pandas as pd
from sentence_transformers import SentenceTransformer


# Project locations
ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "pantry_faq_clean.csv"
DB_PATH = ROOT / "vector_db"

COLLECTION_NAME = "pantry_faq"


def main():
    # Load cleaned pantry FAQ data
    df = pd.read_csv(DATA_PATH)

    documents = []
    metadatas = []
    ids = []

    # Each FAQ record is short, so each row is one chunk
    for _, row in df.iterrows():

        document = (
            f"Question: {row['question']}\n"
            f"Answer: {row['answer']}"
        )

        documents.append(document)

        metadatas.append({
            "category": str(row["category"]),
            "audience": str(row["audience"]),
            "source": str(row["source"])
        })

        ids.append(str(row["id"]))

    # Convert FAQ chunks into vector embeddings
    model = SentenceTransformer("all-MiniLM-L6-v2")

    embeddings = model.encode(
        documents,
        normalize_embeddings=True
    ).tolist()

    # Create persistent local Chroma vector database
    client = chromadb.PersistentClient(
        path=str(DB_PATH)
    )

    # Rebuild collection when script is run again
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={
            "description":
            "ISU School Street Food Pantry FAQ reference data"
        }
    )

    # Store FAQ chunks and vectors
    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(f"FAQ records processed: {len(documents)}")
    print(f"Vector database stored in: {DB_PATH}")


if __name__ == "__main__":
    main()
