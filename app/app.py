from pathlib import Path
from flask import Flask, render_template, request, jsonify
import chromadb
from sentence_transformers import SentenceTransformer

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "vector_db"
COLLECTION_NAME = "pantry_faq"

app = Flask(__name__)
model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path=str(DB_PATH))
collection = client.get_collection(COLLECTION_NAME)

def retrieve_answer(question: str):
    query_embedding = model.encode([question], normalize_embeddings=True).tolist()[0]

    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    docs = result["documents"][0]
    metas = result["metadatas"][0]
    distances = result["distances"][0]

    if not docs:
        return {
            "answer": "I could not find that information in the verified pantry reference data.",
            "source": None,
            "matches": []
        }

    # Minimal prototype behavior:
    # return the answer text from the best matching FAQ record.
    best_doc = docs[0]
    best_meta = metas[0]

    answer = best_doc.split("Answer:", 1)[-1].strip()

    return {
        "answer": answer,
        "source": best_meta.get("source"),
        "matches": [
            {
                "text": d,
                "source": m.get("source"),
                "distance": round(float(dist), 4)
            }
            for d, m, dist in zip(docs, metas, distances)
        ]
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/ask", methods=["POST"])
def ask():
    payload = request.get_json(silent=True) or {}
    question = str(payload.get("question", "")).strip()

    if not question:
        return jsonify({"error": "Please enter a question."}), 400

    return jsonify(retrieve_answer(question))

if __name__ == "__main__":
    app.run(debug=True)
