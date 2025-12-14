Hummingbird Medical Chatbot (RAG) — Llama-2-7B GGML + LangChain + Chainlit
A local, CPU-friendly medical chatbot powered by a Sentence Transformers Hummingbird embedding model for retrieval and Llama-2 7B (GGML) for generation. It uses Retrieval-Augmented Generation (RAG) over The Gale Encyclopedia of Medicine (Vol. 1, 2nd Ed.) to answer medical questions, summarize entries, and generate medically themed text with grounded context.

⚠️ Disclaimer: This project is for educational and research purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider for medical concerns.

Key features
Semantic retrieval using the Hummingbird embeddings model (Sentence Transformers)

Local LLM inference (CPU-only) using quantized Llama-2 7B GGML

RAG pipeline with PDF chunking + similarity search for grounded answers

Chainlit UI for an interactive chat experience

Easy to extend to new PDFs, new embedding models, or different vector stores

Demo
Chat in your browser via Chainlit:

“What is diabetes mellitus?”

“Summarize symptoms, diagnosis, and treatment for migraine.”

“Explain hypertension in simple terms.”

Tip: Enable citations/snippets from retrieved chunks for better trust and debuggability.

Tech stack
Embeddings (Retrieval): Sentence Transformers (Hummingbird model)

LLM (Generation): Llama-2 7B Chat (GGML quantized)

Orchestration: LangChain

UI: Chainlit

Knowledge source: The Gale Encyclopedia of Medicine, Volume 1 (2nd Edition) PDF

LLM model details (Llama-2 GGML)
Configured to work with:

Name: llama-2-7b-chat.ggmlv3.q2_K.bin

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


Embeddings model (Hummingbird)
This chatbot uses a Sentence Transformers Hummingbird embedding model to convert:

PDF chunks → vectors

User queries → vectors

These vectors power similarity search to retrieve the best context before the LLM generates an answer.

Add your exact Hummingbird checkpoint name (Hugging Face ID) here to make runs reproducible.

Requirements
Minimum suggested machine:

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

GPU: Not required

Quickstart
1) Clone the repository
bash
git clone https://github.com/ThisIs-Developer/Llama-2-GGML-Medical-Chatbot.git
cd Llama-2-GGML-Medical-Chatbot
2) Install dependencies
bash
pip install -r requirements.txt
3) Add the Llama-2 GGML model
Download and place the model file where model.py expects it (example path):

text
models/llama-2-7b-chat.ggmlv3.q2_K.bin
4) Run the app
bash
chainlit run model.py -w
Open the printed local URL (usually http://localhost:8000).

How it works (RAG overview)
Load the Gale Encyclopedia PDF

Split into chunks

Embed chunks with the Hummingbird model

Store vectors in an index (FAISS/Chroma/etc.)

Retrieve top-matching chunks per question

Generate a grounded answer using Llama-2 + retrieved context

Safety notes (medical domain)
This bot does not provide medical diagnosis

Add emergency guidance rules for severe symptoms

Prefer showing sources/snippets and limiting speculative outputs

Evaluate grounding quality to reduce hallucinations

Roadmap
Show citations and retrieved passages in Chainlit

Add re-ranking for higher retrieval precision

Multi-document ingestion and indexing

Offline evaluation suite + safety checks

Config-driven setup (paths, chunk size, top-
k
k, embedding model)

License & attribution
Llama 2 is subject to Meta’s license and usage terms

Ensure you have rights to use/redistribute the encyclopedia PDF

Repository code license: add/check LICENSE
