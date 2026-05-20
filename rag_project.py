import os
import time
import faiss
import numpy as np
import nltk
from flask import Flask, request, render_template, jsonify
app = Flask(__name__)
from google import genai
from google.genai import types
from huggingface_hub import InferenceClient
from nltk.tokenize import sent_tokenize


# ==========================================================
# HARD-CODED TOKENS
# ==========================================================

GEMINI_API_KEY = ""
HF_TOKEN = ""


# ==========================================================
# CONFIGURATION
# ==========================================================

DATA_FOLDER = "data"

# Hugging Face cloud embedding model
HF_EMBEDDING_MODEL = "ibm-granite/granite-embedding-97m-multilingual-r2"

# You can also try:
# HF_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Gemini cloud LLM 
# gemini-3-flash-preview
GEMINI_MODEL = "gemini-2.5-flash"

TOP_K = 5

# Start with 1 to avoid connection problems.
# Later you can try 4 or 8.
BATCH_SIZE = 4


# ==========================================================
# CLIENTS
# ==========================================================

gemini_client = genai.Client(api_key=GEMINI_API_KEY)

hf_client = InferenceClient(
    provider="hf-inference",
    api_key=HF_TOKEN
)


# ==========================================================
# NLTK SETUP
# ==========================================================

def setup_nltk():
    nltk.download("punkt", quiet=True)
    nltk.download("punkt_tab", quiet=True)


# ==========================================================
# LOAD DOCUMENTS
# ==========================================================
def load_documents(folder=DATA_FOLDER):
    """
    Load .txt files from the data folder and split them into structured text chunks.
    """

    if not os.path.exists(folder):
        raise FileNotFoundError(
            f"Folder '{folder}' does not exist. Create it and put .txt files inside."
        )

    chunks = []

    for file_name in os.listdir(folder):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder, file_name)

            with open(file_path, "r", encoding="utf-8") as file:
                text = file.read()

            # פיצול הקובץ לפי שורות / פסקאות
            paragraphs = text.split("\n")
            current_category = ""

            for paragraph in paragraphs:
                paragraph = paragraph.strip()
                
                # התעלמות משורות ריקות או מכותרת הקובץ הראשית
                if not paragraph or paragraph.startswith("==="):
                    continue
                    
                # זיהוי ושמירה של הקטגוריה הנוכחית כהקשר (Context)
                if paragraph.startswith("[CATEGORY:"):
                    current_category = paragraph
                    continue
                    
                # שמירת התוכן יחד עם הקטגוריה שלו (רק אם יש בו תוכן משמעותי)
                if len(paragraph) > 20:
                    # אם נמצאה קטגוריה, נצמיד אותה לתחילת הצ'אנק
                    if current_category:
                        full_chunk = f"{current_category}\n{paragraph}"
                    else:
                        full_chunk = paragraph
                        
                    chunks.append(full_chunk)

    if not chunks:
        raise ValueError(
            f"No text found. Make sure the '{folder}' folder contains .txt files."
        )

    print(f"Loaded {len(chunks)} text chunks.")
    return chunks



# ==========================================================
# HUGGING FACE CLOUD EMBEDDINGS
# ==========================================================
def normalize_embedding_output(raw_output, expected_count):
    """
    גרסה חסינה ואוניברסלית: מבטיחה המרה חלקה ל-Numpy דו-ממדי (expected_count x dimension).
    מונעת קריסות שרת לחלוטין כאשר השאילתה מוגשת בעברית או מכילה ריבוי טוקנים.
    """
    arr = np.array(raw_output, dtype="float32")

    # מקרה 1: וקטור בודד שטוח (למשל עבור השאלה של המשתמש)
    if arr.ndim == 1:
        arr = arr.reshape(1, -1)

    # מקרה 2: מערך דו-ממדי
    elif arr.ndim == 2:
        if arr.shape[0] == expected_count:
            pass
        elif expected_count == 1:
            arr = arr.mean(axis=0, keepdims=True)
        else:
            # במקום לזרוק שגיאה, נתאים ידנית למבנה הנדרש במקרה של סטייה בענן
            arr = arr.reshape(expected_count, -1)

    # מקרה 3: מערך תלת-ממדי (נפוץ מאוד בשאילתות בעברית בגלל פיצול טוקנים בענן)
    elif arr.ndim == 3:
        arr = arr.mean(axis=1)
        if expected_count == 1 and arr.ndim == 2 and arr.shape[0] > 1:
            arr = arr.mean(axis=0, keepdims=True)

    else:
        # גיבוי למניעת קריסת השרת
        arr = arr.reshape(expected_count, -1)

    # בדיקת בטיחות סופית להבטחת תאימות מלאה ל-FAISS
    if arr.shape[0] != expected_count:
        arr = arr.reshape(expected_count, -1)

    return arr.astype("float32")


def hf_feature_extraction_with_retries(inputs, expected_count, max_retries=5):
    """
    Calls Hugging Face cloud embedding model with retries.

    inputs can be:
    - string
    - list of strings
    """

    for attempt in range(1, max_retries + 1):
        try:
            result = hf_client.feature_extraction(
                inputs,
                model=HF_EMBEDDING_MODEL
            )

            embeddings = normalize_embedding_output(
                raw_output=result,
                expected_count=expected_count
            )

            return embeddings

        except Exception as e:
            print(f"Hugging Face embedding failed. Attempt {attempt}/{max_retries}")
            print("Error:", e)

            if attempt == max_retries:
                raise

            wait_seconds = attempt * 3
            print(f"Retrying in {wait_seconds} seconds...")
            time.sleep(wait_seconds)


def embed_texts_with_huggingface(texts, batch_size=BATCH_SIZE):
    """
    Creates document embeddings using Hugging Face cloud inference.
    """

    all_embeddings = []
    total_batches = (len(texts) + batch_size - 1) // batch_size

    for start in range(0, len(texts), batch_size):
        batch = texts[start:start + batch_size]

        current_batch = start // batch_size + 1
        print(f"Embedding batch {current_batch}/{total_batches}...")

        embeddings = hf_feature_extraction_with_retries(
            inputs=batch,
            expected_count=len(batch)
        )

        all_embeddings.append(embeddings)

    final_embeddings = np.vstack(all_embeddings).astype("float32")
    print("Final embeddings:", final_embeddings)
    print(f"Created document embeddings. Shape: {final_embeddings.shape}")

    return final_embeddings


def embed_query_with_huggingface(query):
    """
    Creates one query embedding using Hugging Face cloud inference.
    """

    embedding = hf_feature_extraction_with_retries(
        inputs=query,
        expected_count=1
    )

    return embedding.astype("float32")


# ==========================================================
# FAISS VECTOR SEARCH
# ==========================================================

def create_faiss_index(embeddings):
    """
    Creates FAISS index.

    We normalize vectors and use inner product.
    This behaves like cosine similarity.
    """

    faiss.normalize_L2(embeddings)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)

    print(f"FAISS index created with {index.ntotal} vectors.")

    return index


def retrieve(query, index, chunks, k=TOP_K):
    """
    Embeds the user question with Hugging Face and searches FAISS.
    """

    query_embedding = embed_query_with_huggingface(query)

    faiss.normalize_L2(query_embedding)

    scores, indexes = index.search(query_embedding, k)

    print("\nFAISS scores:", scores)
    print("FAISS indexes:", indexes)

    retrieved_chunks = []

    for idx in indexes[0]:
        if idx != -1:
            retrieved_chunks.append(chunks[idx])

    return retrieved_chunks


# ==========================================================
# GEMINI LLM
# ==========================================================

def ask_gemini(context, question):
    """
    Gemini is the LLM.
    Hugging Face is only used for embeddings.
    """

    prompt = f"""
You are Mitzie AI, a helpful and professional RAG assistant specialized in Ministry of Defense regulations.
Your job is to answer the user's question by combining, summarizing, and synthesizing information from the provided context.

Rules:
1. Answer the question using the provided context as your primary source of truth.
2. If the context does not contain enough information to answer the question, state clearly what is missing, but answer whatever is available in the context.
3. Be flexible: Summarize, connect, and synthesize information from different paragraphs if it helps provide a complete and holistic answer.
4. Keep the answer factual, objective, simple, and clear.
5. Do not invent any new facts, brackets, or numbers that are not explicitly written in the context.

Context:
{context}

Question:
{question}

Answer:
"""

    response = gemini_client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.3,
            max_output_tokens=500,
            thinking_config=types.ThinkingConfig(
                thinking_budget=0
            )
        )
    )

    return response.text.strip()


# ==========================================================
# FKASK APP
# ==========================================================

# משתנים גלובליים חדשים כדי לשמור את המאגר בזיכרון של השרת
GLOBAL_CHUNKS = []
GLOBAL_INDEX = None

@app.before_request
def initialize_rag_system():
    """
    רץ פעם אחת אוטומטית כשהשרת עולה.
    טוען את המסמכים ובונה את אינדקס ה-FAISS בזיכרון.
    """
    global GLOBAL_CHUNKS, GLOBAL_INDEX
    if GLOBAL_INDEX is None:
        print("\n--- [Flask] Building FAISS Knowledge Base ---")
        setup_nltk()
        GLOBAL_CHUNKS = load_documents(DATA_FOLDER)
        document_embeddings = embed_texts_with_huggingface(GLOBAL_CHUNKS)
        GLOBAL_INDEX = create_faiss_index(document_embeddings)
        print("--- [Flask] RAG System is Web Ready! ---")


@app.route("/")
def home():
    """מציג למשתמש את ממשק האינטרנט (דף ה-HTML)"""
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    """
    נקודת הקצה (API) שמקבלת את השאלה מהדפדפן,
    מפעילה את ה-retrieve ואת ה-LLM, ומחזירה תשובה.
    """
    global GLOBAL_CHUNKS, GLOBAL_INDEX
    
    # קבלת השאלה שנשלחה מהאתר
    data = request.get_json() or {}
    question = data.get("question", "").strip()

    # טיפול במקרה קצה: שאילתה ריקה
    if not question:
        return jsonify({"error": "אנא הקלד שאלה תקינה."}), 400

    try:
        # 1. שליפת פסקאות מ-FAISS (הפונקציה המקורית שלך)
        top_chunks = retrieve(
            query=question,
            index=GLOBAL_INDEX,
            chunks=GLOBAL_CHUNKS,
            k=TOP_K
        )
        
        context = "\n".join(top_chunks)
        
        # 2. יצירת תשובה מעוגנת בנתונים מ-Gemini (הפונקציה המקורית שלך)
        answer = ask_gemini(context, question)
        
        # החזרת המידע כ-JSON לדפדפן
        return jsonify({
            "answer": answer,
            "sources": top_chunks
        })
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "אירעה שגיאה בעיבוד הנתונים."}), 500


if __name__ == "__main__":
    # use_reloader=False מונע מ-Flask להפעיל את תהליך האתחול פעמיים
    app.run(debug=True, port=5000, use_reloader=False)
