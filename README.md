# Mitzie AI - Ministry of Defense Rights Navigator

Welcome to Mitzie AI, a full-stack Retrieval-Augmented Generation (RAG) web application engineered to help users navigate and maximize their rights, benefits, and rehabilitation procedures within the Israeli Ministry of Defense.

Instead of forcing users to sift through complex, dense official regulatory documents, Mitzie AI allows them to ask questions in plain Hebrew and receive factual, objective, and fully sourced answers instantly.

---

## Project Architecture & RAG Pipeline

The application is built using a clean, modern RAG pipeline designed to minimize hallucinations and guarantee data grounding:

1. User Query: The user inputs a question in Hebrew through a clean web interface.
2. Semantic Retrieval: The system embeds the query and searches a local vector database to find the top 5 most relevant legal text chunks.
3. Context Injection: The retrieved official text blocks are injected into a strict system prompt.
4. Grounded Generation: Gemini LLM synthesizes the final response based only on the provided context, complete with source-matching indicators in the UI.

---

## Knowledge Base & Chunking Strategy

### 1. Data Source & Preprocessing
The system relies on a curated, accurate dataset of official Ministry of Defense regulations and protocols stored as text files inside the data directory.

### 2. Custom Category-Aware Chunking
To prevent the loss of crucial structural context during retrieval, a smart chunking strategy was developed in Python:
* Files are parsed by paragraphs.
* The system dynamically detects specific metadata tags such as [CATEGORY: ...].
* When text is split into chunks, the relevant category header is automatically prepended to the top of that specific chunk. This ensures that even if a paragraph is retrieved standalone, the model always knows exactly which legal category or protocol it belongs to.

### 3. Embedding Model
We utilize the cloud-based ibm-granite/granite-embedding-97m-multilingual-r2 model via Hugging Face. This model provides superior semantic understanding of multi-token Hebrew queries, mapping them into a high-dimensional vector space.

### 4. FAISS Vector Indexing
Vectors are normalized using L2 normalization, and indexed using a flat Inner Product index (faiss.IndexFlatIP). This architecture effectively transforms the database search into a highly efficient Cosine Similarity calculation.

---

## Tech Stack

* Backend: Python, Flask (Micro-framework)
* Vector Database: FAISS (Facebook AI Similarity Search)
* Embedding Engine: Hugging Face Inference API
* Large Language Model: Google Gemini 2.5 Flash (google-genai SDK)
* Frontend: Clean HTML5, CSS3 (including a custom layout and dynamic loading animations), and Vanilla JavaScript (Asynchronous Fetch API).

---

## Edge Cases & Error Handling

Mitzie AI is engineered with robust production-grade error handling:
* Empty Queries: The frontend prevents empty submissions, displaying an intuitive warning message.
* API Resiliency: Embedding requests include an exponential backoff retry loop (max_retries=5) to handle temporary cloud connection hiccups seamlessly.
* Token Splitting Issues: A universal multi-dimensional array reshaping function (normalize_embedding_output) handles unexpected 3D array variations common when tokenizing Hebrew text in the cloud, completely preventing server-side crashes.
* Strict Anchoring: If the vector database returns empty or irrelevant texts, the system prompt explicitly forbids the LLM from inventing figures or brackets, forcing it to state exactly what information is missing.
