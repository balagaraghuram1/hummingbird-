Hummingbird Medical Chatbot (RAG)
Hummingbird embeddings + Llama-2-7B Chat (GGML) - LangChain - Chainlit - CPU-friendly

A local medical Q&A chatbot built with Retrieval-Augmented Generation (RAG). It uses a Sentence Transformers Hummingbird embedding model for semantic retrieval and a quantized Llama-2 7B Chat GGML model for response generation, grounded on The Gale Encyclopedia of Medicine (Vol. 1, 2nd Edition).

Medical disclaimer: This project is for educational and research purposes only. It is not medical advice and must not be used for diagnosis or treatment decisions. If you have urgent symptoms or a medical emergency, contact local emergency services or a qualified healthcare professional immediately.

Highlights
Hummingbird embeddings for high-quality semantic search over medical text

Local Llama-2 7B GGML inference (CPU-only, lightweight quantization)

RAG workflow: PDF ingestion → chunking → embeddings → retrieval → grounded generation

Chainlit UI for a fast, friendly chat experience in the browser

Easy to extend to new PDFs, new embedding models, and different vector stores

What it can do
Answer questions about medical topics based on the encyclopedia content

Summarize relevant sections into short, readable explanations

Generate medical text grounded in retrieved context (recommended with citations enabled)

Example prompts:

“Explain asthma and its common triggers.”

“Summarize migraine symptoms and typical treatments.”

“What is hypertension? Keep it simple.”

Architecture (RAG)
Load the PDF (Gale Encyclopedia)

Split text into chunks

Create vector embeddings using the Hummingbird model

Store embeddings in a vector index (FAISS/Chroma/etc.)

Retrieve top-
k
k relevant chunks for each user query

Generate an answer using Llama-2 conditioned on retrieved context

Models
1) Embeddings (Retrieval) — Hummingbird
This project uses a Sentence Transformers Hummingbird embedding model to encode:

Document chunks → vectors

User queries → vectors

Add your exact Hummingbird model ID (Hugging Face repo name) in the configuration/code so results are reproducible.

2) LLM (Generation) — Llama-2-7B Chat (GGML)
Recommended config from this repository:

File: llama-2-7b-chat.ggmlv3.q2_K.bin

Quantization: q2_K

Bits: 
2
2

Size: 
2.87
 GB
2.87 GB

Max RAM required: 
5.37
 GB
5.37 GB

System requirements
Suggested minimum:

OS: Linux / macOS / Windows

CPU: Intel® Core™ i3 (or equivalent)

RAM: 
8
 GB
8 GB

Disk: 
7
 GB
7 GB free

GPU: Not required (CPU-only)

Repository layout (typical)
text
.
├── data/
│   └── 71763-gale-encyclopedia-of-medicine.-vol.-1.-2nd-ed.pdf
├── models/
│   └── llama-2-7b-chat.ggmlv3.q2_K.bin
├── model.py
├── requirements.txt
└── README.md
Your repo may differ slightly—update paths to match your code.

Quickstart
1) Clone
bash
git clone https://github.com/ThisIs-Developer/Llama-2-GGML-Medical-Chatbot.git
cd Llama-2-GGML-Medical-Chatbot
2) Install dependencies
bash
pip install -r requirements.txt
3) Add the LLM model file
Download the GGML model and place it in your chosen directory (example):

text
models/llama-2-7b-chat.ggmlv3.q2_K.bin
Tip: avoid committing large binaries to git. Add this to .gitignore:

text
models/
*.bin
4) Run the app
bash
chainlit run model.py -w
Then open the local URL printed in the terminal (commonly http://localhost:8000).

Configuration (recommended)
If your code supports environment variables, this is a clean pattern:

MODEL_PATH → path to GGML model file

PDF_PATH → path to the Gale PDF

EMBEDDING_MODEL_NAME → Hummingbird model ID

CHUNK_SIZE → chunk length

CHUNK_OVERLAP → overlap tokens/characters

TOP_K → number of retrieved chunks

Create a .env (optional):

text
MODEL_PATH=models/llama-2-7b-chat.ggmlv3.q2_K.bin
PDF_PATH=data/71763-gale-encyclopedia-of-medicine.-vol.-1.-2nd-ed.pdf
EMBEDDING_MODEL_NAME=YOUR_HUMMINGBIRD_MODEL_ID_HERE
CHUNK_SIZE=1000
CHUNK_OVERLAP=150
TOP_K=4
Safety notes (medical domain)
Do not use this bot for diagnosis, prescriptions, or emergency triage

Add guardrails for high-risk prompts (e.g., self-harm, severe symptoms)

Prefer showing retrieved sources/snippets in responses

Evaluate grounding quality to reduce hallucinations

Roadmap
Source citations in the UI (show retrieved chunks + page numbers)

Re-ranking (cross-encoder) to improve retrieval precision

Multi-PDF ingestion and incremental indexing

Evaluation set (factuality + retrieval hit rate)

Config-driven pipeline (swap vector store / embedding model easily)

License & attribution
Llama 2 usage is governed by Meta’s license terms

Ensure you have the rights to use and redistribute the encyclopedia PDF

Add/check a project LICENSE file for your source code

Acknowledgements
Meta (Llama 2)

TheBloke (GGML model conversions)

LangChain, Chainlit, and Sentence Transformers communities
