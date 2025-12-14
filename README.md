Hummingbird Medical Chatbot (RAG)
Hummingbird embeddings • Llama-2-7B Chat (GGML) • LangChain • Chainlit • Runs on CPU

A local medical Q&A chatbot built with Retrieval-Augmented Generation (RAG). It uses a Sentence Transformers Hummingbird embedding model for semantic retrieval and a quantized Llama-2 7B Chat GGML model for response generation, grounded on The Gale Encyclopedia of Medicine (Vol. 1, 2nd Edition).


---

Why this project

Medical questions require reliable context. This chatbot reduces hallucinations by retrieving relevant passages from a medical reference before generating responses.

---
 Features

- Hummingbird embeddings for semantic search over medical text
- Local inference (CPU-only) using a quantized GGML Llama-2 7B Chat model
- RAG pipeline: PDF ingestion → chunking → embeddings → retrieval → grounded answers
- Chainlit web UI for interactive chat in the browser
- Easy to adapt to new PDFs or different embedding models

---

What it can do

- Answer questions about medical topics based on the encyclopedia content
- Summarize entries into short, readable explanations
- Generate medical text grounded in retrieved context (recommended with citations enabled)

Example prompts:
- “Explain asthma and common triggers.”
- “Summarize migraine symptoms and treatment options.”
- “What is hypertension? Explain it simply.”

---
 How it works (RAG overview)

1. Load the medical PDF
2. Split text into chunks
3. Compute vector embeddings with the Hummingbird model
4. Store embeddings in a vector index (e.g., FAISS/Chroma)
5. Retrieve the most relevant chunks for each question
6. Generate a response with the LLM using the retrieved context

---
 Requirements

Suggested minimum:

- OS: Linux / macOS / Windows
- CPU: Intel® Core™ i3 (or equivalent)
- RAM: 8 GB
- Disk: 7 GB free
- GPU: Not required (CPU-only)

---
 

