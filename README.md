```markdown
# 🔎 InsightLens — Evidence-Backed AI Intelligence

> An evidence-backed AI intelligence system that combines semantic retrieval, FAISS vector search, RAG, 4-bit quantized LLM inference, FastAPI, ngrok, and a custom Gradio interface.

---

## 🎓 Internship Project

This project was developed as part of the **Large Language Models (LLMs) Program** during the **Tips Hindawi Internship (August–October 2026)** at **Edrak for AI**.

---

# 👤 Participant

| Field | Value |
|---|---|
| **Full Name** | Ahmed Amr |
| **Project Name** | InsightLens — Evidence-Backed AI Intelligence |
| **GitHub Username** | aidev-ahmedamr |
| **Internship Batch** | August–October 2026 |
| **Training Program** | Large Language Models (LLMs) Program |
| **Organization** | Edrak for AI |
| **Internship** | Tips Hindawi |

---

# 📖 Project Overview

**InsightLens** is an evidence-backed AI intelligence system designed to analyze a user-provided topic using retrieved evidence rather than relying only on the language model's internal knowledge.

The system follows a Retrieval-Augmented Generation (RAG) architecture.

A user enters a topic through a custom Gradio interface. The system converts the topic into a semantic embedding, searches a FAISS vector index for the most relevant evidence, and passes the retrieved evidence to a quantized Mistral Nemo language model.

The LLM then generates a structured intelligence brief containing:

- Executive Summary
- Key Findings
- Supporting Signals
- Conflicting or Different Signals
- Risks / Opportunities
- Confidence Level
- Confidence Reason
- Evidence Used

The system is exposed through a FastAPI backend and made accessible externally using ngrok.

---

# 🎯 Project Objectives

The main objectives of InsightLens are:

- Build a complete Retrieval-Augmented Generation pipeline.
- Perform semantic search using sentence embeddings.
- Store and retrieve vectors efficiently using FAISS.
- Use retrieved evidence as the basis for LLM generation.
- Reduce hallucination by restricting the model to retrieved evidence.
- Use 4-bit quantization for memory-efficient LLM inference.
- Build an API using FastAPI.
- Expose the backend through ngrok.
- Create a custom user interface using Gradio.
- Present AI-generated intelligence in a structured and interpretable format.

---

# 🧠 Core Architecture

```text
                    ┌─────────────────────┐
                    │     User Topic      │
                    └──────────┬──────────┘
                               │
                               ▼
                 ┌──────────────────────────┐
                 │ Sentence Transformer     │
                 │ all-MiniLM-L6-v2         │
                 └────────────┬─────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   FAISS Index    │
                    │ Semantic Search   │
                    └────────┬─────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Top-K Evidence      │
                  │ Retrieved Documents  │
                  └──────────┬──────────┘
                             │
                             ▼
                ┌──────────────────────────┐
                │ Mistral Nemo Instruct    │
                │ 4-bit Quantized          │
                └────────────┬─────────────┘
                             │
                             ▼
                 ┌────────────────────────┐
                 │ Intelligence Brief     │
                 │ Structured Output      │
                 └────────────┬───────────┘
                              │
                              ▼
                     ┌────────────────┐
                     │    FastAPI     │
                     └───────┬────────┘
                             │
                             ▼
                        ┌──────────┐
                        │  ngrok   │
                        └────┬─────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Custom Gradio UI │
                    └──────────────────┘
```

---

# ✨ Key Features

## 🔎 Semantic Retrieval

The system uses sentence embeddings to represent documents and user queries in a shared semantic vector space.

This allows the system to retrieve documents based on meaning rather than exact keyword matching.

---

## ⚡ FAISS Vector Search

FAISS is used to store the document embeddings and perform efficient similarity search.

The system uses normalized embeddings and inner-product similarity.

The top relevant documents are retrieved for every user query.

---

## 🧠 Retrieval-Augmented Generation

Instead of directly asking the language model to answer the user's topic, InsightLens first retrieves relevant evidence.

The retrieved evidence is then inserted into the LLM prompt.

This allows the generation process to be grounded in the retrieved information.

---

## 🤖 Quantized Mistral Nemo

The project uses:

```text
mistralai/Mistral-Nemo-Instruct-2407
```

The model is loaded using 4-bit quantization through BitsAndBytes.

This significantly reduces memory requirements compared with full-precision inference.

---

## 🛡️ Evidence-Grounded Prompting

The model is instructed to:

1. Use only retrieved evidence.
2. Avoid inventing facts.
3. Distinguish evidence from interpretation.
4. Reference evidence numbers.
5. Clearly indicate insufficient evidence.
6. Treat similarity scores as relevance indicators rather than proof of truth.

---

# 📊 Dataset

The project uses the **AG News** dataset.

The dataset contains categorized news articles covering four major news categories.

For the project pipeline, a subset of:

```text
5,000 documents
```

is used to build the semantic retrieval index.

Each document contains:

- News article text
- Category label
- Document identifier

---

# 🧩 Models

## Embedding Model

```text
sentence-transformers/all-MiniLM-L6-v2
```

Purpose:

- Convert documents into numerical embeddings.
- Convert user queries into embeddings.
- Enable semantic similarity search.

---

## Language Model

```text
mistralai/Mistral-Nemo-Instruct-2407
```

Purpose:

- Analyze retrieved evidence.
- Generate structured intelligence briefs.
- Produce evidence-grounded natural language output.

---

# 🗂️ System Components

The project consists of several main components.

### 1. Dataset Loading

The AG News dataset is loaded using the Hugging Face Datasets library.

---

### 2. Document Embeddings

Each document is converted into a dense vector representation using:

```text
all-MiniLM-L6-v2
```

---

### 3. FAISS Index

The generated embeddings are inserted into a FAISS index.

```text
IndexFlatIP
```

is used for similarity search.

---

### 4. Evidence Retrieval

For each query:

```text
User Topic
     ↓
Query Embedding
     ↓
FAISS Search
     ↓
Top 5 Documents
```

The system retrieves the five most semantically relevant documents.

---

### 5. LLM Analysis

The retrieved evidence is provided to Mistral Nemo together with a structured prompt.

The model generates the final intelligence brief.

---

### 6. FastAPI Backend

The model pipeline is exposed through an HTTP API.

Main endpoint:

```text
POST /intelligence
```

---

### 7. ngrok

ngrok creates a public HTTPS tunnel to the local FastAPI server running on port:

```text
8000
```

---

### 8. Gradio Interface

A custom Gradio interface allows users to interact with the system without directly interacting with the API.

---

# 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Hugging Face Datasets | Dataset loading |
| Sentence Transformers | Semantic embeddings |
| FAISS | Vector similarity search |
| PyTorch | Deep learning framework |
| Transformers | LLM loading and inference |
| BitsAndBytes | 4-bit quantization |
| Mistral Nemo | Language model |
| FastAPI | Backend API |
| Uvicorn | API server |
| ngrok | Public API tunnel |
| Requests | HTTP communication |
| Gradio | User interface |
| NumPy | Numerical operations |
| Jupyter / Kaggle | Development environment |

---

# ⚙️ Installation

## 1. Clone the repository

```bash
git clone https://github.com/aidev-ahmedamr/InsightLens.git
cd InsightLens
```

---

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

If a requirements file is not available, install the main dependencies:

```bash
pip install gradio requests
```

---

# 📦 Requirements

A typical backend environment requires:

```text
transformers
accelerate
bitsandbytes
sentence-transformers
faiss-cpu
datasets
torch
fastapi
uvicorn
pyngrok
requests
gradio
```

---

# 🚀 Running the Project

The AI backend is designed to run in a GPU-enabled environment such as Kaggle.

The local computer runs the Gradio interface.

---

## Step 1 — Start the Kaggle Backend

Run the notebook cells that:

1. Install dependencies.
2. Load AG News.
3. Create document embeddings.
4. Build the FAISS index.
5. Load Mistral Nemo.
6. Configure 4-bit quantization.
7. Create the retrieval pipeline.
8. Create the FastAPI API.
9. Start FastAPI.
10. Create the ngrok tunnel.

The backend runs on:

```text
http://localhost:8000
```

---

# 🔌 API

## Health Check

```http
GET /
```

Example response:

```json
{
  "project": "InsightLens",
  "status": "online",
  "message": "Evidence-Backed AI Intelligence API"
}
```

---

## Health Endpoint

```http
GET /health
```

Example response:

```json
{
  "status": "healthy"
}
```

---

## Intelligence Endpoint

```http
POST /intelligence
```

Request:

```json
{
  "topic": "Artificial intelligence is transforming the technology industry."
}
```

Authorization:

```text
Bearer secret123
```

Example:

```http
Authorization: Bearer secret123
```

---

# 🔐 API Authentication

The backend uses a simple Bearer token for API authentication.

Example:

```text
Authorization: Bearer secret123
```

For a production system, the API key should be stored using environment variables or a secure secrets manager instead of being hard-coded.

---

# 🌐 ngrok Configuration

After starting FastAPI, ngrok generates a public HTTPS URL similar to:

```text
https://example.ngrok-free.dev
```

The Gradio application uses this URL to communicate with the remote backend.

Inside:

```text
app.py
```

set:

```python
NGROK_URL = "https://YOUR-NGROK-URL.ngrok-free.dev"
```

Do not add:

```text
/intelligence
```

to the `NGROK_URL` variable.

The application automatically adds:

```text
/intelligence
```

when sending the request.

---

# 🖥️ Running the Local Interface

After configuring the ngrok URL:

```bash
python app.py
```

The Gradio interface will automatically open in the browser.

If necessary, the terminal will display the local Gradio URL.

---

# 🔄 End-to-End Workflow

```text
User
  │
  │ Topic
  ▼
Gradio Interface
  │
  │ HTTP POST
  ▼
ngrok
  │
  ▼
FastAPI
  │
  ▼
Query Embedding
  │
  ▼
FAISS Semantic Search
  │
  ▼
Top-K Evidence
  │
  ▼
Mistral Nemo
  │
  ▼
Structured Intelligence Brief
  │
  ▼
FastAPI Response
  │
  ▼
Gradio Interface
```

---

# 🧪 Example Input

```text
Artificial intelligence is transforming the technology industry.
```

Other possible topics:

```text
The growth of artificial intelligence in business.
```

```text
The impact of technology on the global economy.
```

```text
The role of AI in modern technology.
```

---

# 📋 Example Output Structure

The generated response follows this structure:

```text
EXECUTIVE SUMMARY:

A concise evidence-grounded summary.

KEY FINDINGS:

- Finding 1 [Evidence 1]
- Finding 2 [Evidence 3]
- Finding 3 [Evidence 5]

SUPPORTING SIGNALS:

- Signal 1 [Evidence 2]
- Signal 2 [Evidence 4]

CONFLICTING OR DIFFERENT SIGNALS:

- Signal 1 [Evidence 3]

RISKS / OPPORTUNITIES:

- Risk or opportunity 1
- Risk or opportunity 2

CONFIDENCE:

Medium

CONFIDENCE REASON:

Explanation based on the retrieved evidence.

EVIDENCE USED:

- Evidence 1: Document ID X
- Evidence 2: Document ID Y
- Evidence 3: Document ID Z
```

---

# 📈 Retrieval Process

For every user query, InsightLens performs the following:

```text
1. Receive topic
       ↓
2. Generate query embedding
       ↓
3. Search FAISS
       ↓
4. Retrieve top 5 documents
       ↓
5. Construct evidence-grounded prompt
       ↓
6. Generate intelligence brief
       ↓
7. Return evidence + analysis
```

---

# 🎯 Why RAG?

A normal LLM-based application may generate an answer directly from the model.

InsightLens instead follows:

```text
Query
 ↓
Retrieve Evidence
 ↓
Analyze Evidence
 ↓
Generate Answer
```

This design helps improve transparency because the generated analysis is accompanied by the retrieved evidence used by the system.

---

# 🛡️ Hallucination Reduction Strategy

InsightLens uses several techniques to reduce unsupported generation:

### Evidence Restriction

The model is explicitly instructed to use only retrieved evidence.

### Evidence References

Important findings are associated with evidence identifiers.

### Insufficient Evidence Handling

The model is instructed to explicitly state when the retrieved evidence is insufficient.

### Similarity Interpretation

Similarity scores are treated as indicators of semantic relevance rather than proof that a statement is factually correct.

---

# 🎨 User Interface

The application includes:

- Dark modern interface
- Topic input
- Intelligence generation button
- Executive summary
- Key findings
- Supporting signals
- Conflicting signals
- Risks and opportunities
- Confidence assessment
- Retrieved evidence
- Similarity scores
- Evidence cards
- Retrieval statistics

---

# 📁 Project Structure

```text
InsightLens/
│
├── app.py
│
├── README.md
│
├── requirements.txt
│
├── .gitignore
│
└── notebooks/
    └── InsightLens_RAG.ipynb
```

---

# 📝 Recommended `.gitignore`

Create a file named:

```text
.gitignore
```

with:

```gitignore
__pycache__/
*.pyc
.ipynb_checkpoints/

.env
.env.*
*.key
*.pem

venv/
.venv/

.DS_Store

kaggle.json

*.log
```

Do not upload:

- API keys
- ngrok authentication tokens
- passwords
- private credentials
- large model files
- private datasets

---

# 📊 Results

The project successfully demonstrates an end-to-end RAG pipeline consisting of:

```text
5,000 indexed documents
        ↓
Semantic Embeddings
        ↓
FAISS Vector Search
        ↓
Top-5 Evidence Retrieval
        ↓
4-bit Quantized Mistral Nemo
        ↓
Structured Intelligence Brief
```

The system also demonstrates remote model serving through:

```text
Kaggle GPU
     ↓
FastAPI
     ↓
ngrok
     ↓
Local Gradio Interface
```

---

# 🔮 Future Improvements

Possible future improvements include:

- Replace AG News with domain-specific datasets.
- Add a larger document collection.
- Add metadata filtering.
- Add hybrid keyword + semantic search.
- Add reranking models.
- Add document upload functionality.
- Support PDFs and webpages.
- Add source citations.
- Add conversation memory.
- Add multi-query retrieval.
- Add query rewriting.
- Add evaluation metrics.
- Add retrieval precision and recall evaluation.
- Add production-grade authentication.
- Deploy the backend to a cloud GPU service.
- Store embeddings in a production vector database.
- Add monitoring and logging.

---

# 🧠 Learning Outcomes

Through this project, the following concepts were practiced:

### Large Language Models

- LLM inference
- Instruction prompting
- Structured generation

### Retrieval-Augmented Generation

- Embedding generation
- Semantic retrieval
- Evidence-grounded generation

### Vector Search

- FAISS
- Similarity search
- Normalized embeddings

### Model Optimization

- 4-bit quantization
- BitsAndBytes
- GPU inference

### Backend Development

- FastAPI
- REST API
- Authentication
- Uvicorn

### AI Application Development

- Gradio
- API integration
- Remote inference
- User interface design

---

# 📚 About the Internship

This project was developed during the:

**Tips Hindawi Internship — August–October 2026**

within the:

**Large Language Models (LLMs) Program**

at:

**Edrak for AI**

The project provided practical experience in building AI applications using modern LLM technologies, retrieval pipelines, model optimization, APIs, and user-facing interfaces.

---

# 👨‍💻 Author

**Ahmed Amr**

Computer Science Student — AI Specialization

Interested in:

- Machine Learning
- Deep Learning
- Generative AI
- Large Language Models
- Retrieval-Augmented Generation
- NLP
- Computer Vision
- AI Engineering

---

# 📄 License

This project is intended for educational and portfolio purposes.

You may modify and extend the project for learning and experimentation.
```
