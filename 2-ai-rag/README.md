# Module 2: Reducing MTTR with Semantic Search

**Project:** AI Test Drive – Workshop de IA para Operações de TI  
**Goal:** Demonstrate how to identify similar incidents using semantic search to reduce MTTR (Mean Time To Resolve)

---

## 📋 Overview

This module demonstrates how to use **RAG (Retrieval-Augmented Generation)** with LlamaStack to find similar incidents from historical data. By leveraging semantic search, you can quickly identify past incidents with similar problems and their solutions, significantly reducing the time needed to resolve new incidents.

**Target Audience:** IT professionals, business analysts, project managers (not data scientists)  
**Approach:** Educational, step-by-step, with clear explanations of each concept

**Why this matters:**
- **Problem:** When a new incident occurs, finding similar past incidents manually is time-consuming
- **Solution:** Semantic search automatically finds relevant incidents based on meaning, not just keywords
- **Impact:** Reduces MTTR by quickly surfacing relevant solutions and patterns
- **Real-world application:** This same approach can be used for knowledge bases, documentation search, and incident management systems

---

## 🚀 Quick Start

### Prerequisites

1. **Python Environment**
   ```bash
   # Using uv (recommended)
   uv sync
   
   # Or using pip
   pip install -r requirements.txt
   ```

2. **LlamaStack Server**
   - LlamaStack server running (see main README or OpenShift deployment docs)
   - Can be running locally (`http://localhost:8321`) or on OpenShift

3. **Ollama (for local inference)**
   ```bash
   # Install Ollama: https://ollama.ai
   # Start server
   ollama serve
   
   # Pull model
   ollama pull llama3.2:3b
   ```

4. **Jupyter Notebook**
   ```bash
   jupyter notebook
   ```

### Running the Notebooks

Execute notebooks in order:
1. `notebooks/01_simple_rag_llama_stack_chromadb.ipynb` - Build a basic RAG system
2. `notebooks/02_multifield_rag_llama_stack_chromadb.ipynb` - Enhance RAG with multi-field indexing

---

## 📚 Notebook Sequence

### Notebook 01: Simple RAG with LlamaStack ✅

**What it does:**
- Introduces RAG (Retrieval-Augmented Generation) concepts
- Loads IT call center ticket dataset
- Creates a vector database (ChromaDB) for semantic search
- Indexes documents using LlamaStack's RAG tool
- Performs semantic search queries to find similar incidents
- Uses retrieved context to answer questions about incidents

**Key Learning Points:**
- What RAG is and why it's useful for IT operations
- How vector databases enable semantic search
- How to index documents for retrieval
- How to query and retrieve relevant information
- How to use retrieved context to answer questions

**Outputs:**
- Vector database with indexed incident tickets
- Example queries demonstrating semantic search capabilities

**Time Estimate:** 45-60 minutes

---

### Notebook 02: Multi-Field RAG ✅

**What it does:**
- Extends simple RAG with multi-field document indexing
- Combines multiple ticket fields (`short_description`, `content`, `close_notes`) for richer context
- Demonstrates why multi-field RAG outperforms single-field RAG
- Shows practical examples where multi-field indexing improves retrieval quality

**Key Learning Points:**
- Why combining multiple fields improves search quality
- How to structure documents for better retrieval
- When multi-field RAG is especially powerful
- How to preserve metadata for filtering

**Outputs:**
- Enhanced vector database with multi-field documents
- Comparison examples showing single-field vs multi-field results

**Time Estimate:** 45-60 minutes

---

## 🔑 Key Concepts

### RAG (Retrieval-Augmented Generation)

**What it is:** A technique that combines information retrieval with language generation. Instead of relying solely on the model's training data, RAG retrieves relevant documents from a knowledge base and uses them as context for generating answers.

**Think of it like:** A librarian who first searches the library catalog (retrieval) and then reads relevant books (context) before answering your question (generation).

**Why it matters:** 
- Provides up-to-date information (not limited to training data)
- Can cite sources (retrieved documents)
- Reduces hallucinations by grounding answers in retrieved content
- Perfect for IT operations where you need to search through historical incidents

### Semantic Search

**What it is:** A search method that understands the meaning of queries and documents, not just matching keywords.

**Think of it like:** Traditional search finds "car" when you search for "car", but semantic search also finds "automobile", "vehicle", or "toyota" because it understands they're related concepts.

**Why it matters:**
- Finds relevant results even when exact keywords don't match
- Understands synonyms and related concepts
- Better for natural language queries
- Essential for finding similar incidents with different wording

### Vector Databases

**What it is:** A database that stores documents as vectors (arrays of numbers) representing their meaning. Similar documents have similar vectors, enabling fast similarity search.

**Think of it like:** A map where similar concepts are placed close together. To find similar items, you just look at nearby locations on the map.

**Why it matters:**
- Enables fast semantic search (milliseconds vs seconds)
- Scales to millions of documents
- Works with embeddings from language models
- Foundation for modern RAG systems

### Embeddings

**What it is:** Numerical representations of text that capture semantic meaning. Similar texts have similar embeddings.

**Think of it like:** A fingerprint for text - texts with similar meanings have similar "fingerprints" (embeddings).

**Why it matters:**
- Converts text into numbers that computers can compare
- Enables semantic similarity calculations
- Powers vector databases and semantic search
- Generated by specialized embedding models

### Multi-Field RAG

**What it is:** A RAG approach that combines multiple fields from documents (e.g., problem description + solution) into a single searchable representation.

**Think of it like:** Instead of searching only book titles, you search through titles, summaries, and chapter contents together for better results.

**Why it matters:**
- Captures complete context (problem + solution)
- Improves retrieval quality for complex queries
- Enables pattern recognition across document lifecycle
- Better for IT incidents where you need both problem and resolution

---

## 📊 Project Structure

```
2-ai-rag/
├── README.md              # This file
├── notebooks/             # Jupyter notebooks
│   ├── 01_simple_rag_llama_stack_chromadb.ipynb
│   └── 02_multifield_rag_llama_stack_chromadb.ipynb
├── data/                  # Datasets
│   └── synthetic-it-call-center-tickets.csv
└── src/                   # Source code modules
    └── __init__.py
```

---

## 📈 Current Status

**Completed:**
- ✅ Notebook 01: Simple RAG with LlamaStack
- ✅ Notebook 02: Multi-Field RAG

**In Progress:**
- 🔄 Refactoring notebooks to align with workshop guidelines

---

## 🛠️ Dependencies

**Core Libraries:**
- `pandas>=2.0.0` - Data manipulation
- `numpy>=1.24.0` - Numerical operations
- `jupyter>=1.0.0` - Notebook environment

**AI/ML Libraries:**
- `llama-stack-client>=0.3.1` - LlamaStack Python client
- `python-dotenv>=1.0.0` - Environment variable management

**Optional:**
- `termcolor>=2.3.0` - Colored terminal output
- `huggingface-hub>=0.20.0` - Access to Hugging Face datasets

**Installation:**
```bash
pip install pandas numpy jupyter llama-stack-client python-dotenv termcolor huggingface-hub
```

---

## 💼 How This Applies to IT Operations

The RAG approach demonstrated here can be used for:

- **Incident Resolution:**
  - "Find similar incidents to this one" → Get past solutions
  - "What was the resolution for memory-related crashes?" → Retrieve relevant close notes
  
- **Knowledge Base Search:**
  - Search through documentation, runbooks, and procedures
  - Find relevant information even with different wording
  
- **Pattern Recognition:**
  - Identify recurring problems across incidents
  - Discover common root causes and solutions
  
- **Root Cause Analysis:**
  - Find incidents with similar symptoms
  - Learn from past diagnostic approaches

**The pattern is the same:** Index historical data → Query semantically → Retrieve relevant context → Use context to answer questions or suggest solutions.

---

## 📝 Notes

- **Dataset:** Uses synthetic IT call center tickets for demonstration
- **Vector Database:** ChromaDB is used as the vector store (can be replaced with other providers)
- **Embedding Model:** Uses `nomic-embed-text-v1.5` for generating embeddings
- **Educational focus:** This module focuses on concepts and techniques, not production deployment
- **LlamaStack:** Requires LlamaStack server running (local or OpenShift)

---

## 🎯 Next Steps

After completing this module, you'll be ready for:

- **Module 3:** `3-ai-evaluation/` - Learn how to evaluate AI outputs using multiple evaluation methods
- **Module 4:** `4-ai-agents/` - Build autonomous agents that can take actions based on RAG results

**Related Resources:**
- [LlamaStack Documentation](https://github.com/llamastack/llamastack)
- [ChromaDB Documentation](https://www.trychroma.com/)
- [RAG Best Practices](https://www.pinecone.io/learn/retrieval-augmented-generation/)

---

## 🤝 Contributing

When working on this module:
1. Follow the [workshop guidelines](../docs/GUIDELINES.md)
2. Maintain the educational, beginner-friendly approach
3. Keep explanations clear and use analogies
4. Test all code cells end-to-end
5. Update this README if adding new content

---

**Last Updated:** December 2024

