from pathlib import Path
import sqlite3

from flask import Flask, render_template, request, jsonify
import chromadb
from sentence_transformers import SentenceTransformer


# Project paths and configuration
ROOT = Path(__file__).resolve().parents[1]

# ChromaDB database used by the AI assistant
DB_PATH = ROOT / "vector_db"

# SQLite database used for pantry user and volunteer signups
SIGNUP_DB_PATH = ROOT / "data" / "pantry_signups.db"

COLLECTION_NAME = "pantry_faq"


# Flask application
app = Flask(__name__)


# AI Assistant / ChromaDB setup
model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(
    path=str(DB_PATH)
)

collection = client.get_collection(
    COLLECTION_NAME
)


# SQLite signup database
def init_signup_db():
    with sqlite3.connect(SIGNUP_DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS signups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                signup_type TEXT NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                availability TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


# Create database/table when application starts
init_signup_db()


# AI Assistant retrieval function
def retrieve_answer(question: str):
    query_embedding = model.encode(
        [question],
        normalize_embeddings=True
    ).tolist()[0]

    result = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    docs = result["documents"][0]
    metas = result["metadatas"][0]
    distances = result["distances"][0]

    if not docs:
        return {
            "answer": (
                "I could not find that information in the "
                "verified pantry reference data."
            ),
            "source": None,
            "matches": []
        }

    # Use the best matching FAQ record
    best_doc = docs[0]
    best_meta = metas[0]

    answer = best_doc.split(
        "Answer:",
        1
    )[-1].strip()

    return {
        "answer": answer,
        "source": best_meta.get("source"),
        "matches": [
            {
                "text": document,
                "source": metadata.get("source"),
                "distance": round(float(distance), 4)
            }
            for document, metadata, distance in zip(
                docs,
                metas,
                distances
            )
        ]
    }


# Home page
@app.route("/")
def index():
    return render_template("index.html")


# AI Assistant API
@app.route("/api/ask", methods=["POST"])
def ask():
    payload = request.get_json(silent=True) or {}

    question = str(
        payload.get("question", "")
    ).strip()

    if not question:
        return jsonify({
            "error": "Please enter a question."
        }), 400

    return jsonify(
        retrieve_answer(question)
    )


# Pantry user / volunteer signup API
@app.route("/api/signup", methods=["POST"])
def signup():
    payload = request.get_json(silent=True) or {}

    signup_type = str(
        payload.get("signup_type", "")
    ).strip()

    name = str(
        payload.get("name", "")
    ).strip()

    email = str(
        payload.get("email", "")
    ).strip()

    phone = str(
        payload.get("phone", "")
    ).strip()

    availability = str(
        payload.get("availability", "")
    ).strip()

    # Validate signup type
    if signup_type not in {"pantry_user", "volunteer"}:
        return jsonify({
            "error": "Please select a valid signup type."
        }), 400

    # Name and email are required
    if not name or not email:
        return jsonify({
            "error": "Name and email are required."
        }), 400

    # Save signup to SQLite
    with sqlite3.connect(SIGNUP_DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO signups
            (
                signup_type,
                name,
                email,
                phone,
                availability
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                signup_type,
                name,
                email,
                phone,
                availability
            )
        )

        conn.commit()

    return jsonify({
        "message": "Signup submitted successfully.",
        "signup_type": signup_type
    })


# Run application
if __name__ == "__main__":
    app.run(debug=True)