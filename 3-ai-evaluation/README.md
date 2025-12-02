# Module 3: AI Evaluation - Close Notes Quality Assessment

**Project:** AI Test Drive – Cenário 2: Enriquecendo Incidentes com IA  
**Goal:** Evaluate and generate high-quality close notes for IT incidents using AI

---

## 📋 Overview

This project demonstrates how to use AI to evaluate and generate high-quality close notes for IT incidents. The workflow progresses through 6 notebooks, from data exploration to AI-powered evaluation and generation.

**Target Audience:** IT professionals, business analysts, project managers (not data scientists)  
**Approach:** Educational, step-by-step, with clear explanations of each concept

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

2. **Ollama (for LLM-as-a-Judge)**
   ```bash
   # Install Ollama: https://ollama.ai
   # Start server
   ollama serve
   
   # Pull model
   ollama pull llama3.2:3b
   ```

3. **Jupyter Notebook**
   ```bash
   jupyter notebook
   ```

### Running the Notebooks

Execute notebooks in order:
1. `01_load_and_explore_dataset.ipynb`
2. `02_create_ground_truth.ipynb`
3. `03_ngram_comparisons.ipynb`
4. `04_semantics_analysis.ipynb`
5. `05_llm_as_judge_evaluation.ipynb`
6. `06_llm_generation_evaluation.ipynb` (TODO)

---

## 📚 Notebook Sequence

### Notebook 01: Data Loading and Exploration ✅

**What it does:**
- Loads incident dataset from Hugging Face
- Explores dataset structure and characteristics
- Visualizes distributions and patterns

**Outputs:**
- `data/incidents_prepared.csv`
- `data/incidents_sample.csv`

---

### Notebook 02: Ground Truth Creation ✅

**What it does:**
- Defines quality criteria for "good" close notes
- Separates dataset into:
  - **Reference Dataset** (`reference_close_notes.csv`) - High-quality examples
  - **Other Incidents Dataset** (`other_incidents.csv`) - Standard examples
- Generates embeddings for all incidents to validate quality scores

**Outputs:**
- `data/reference_close_notes.csv`
- `data/other_incidents.csv`

---

### Notebook 03: N-gram Baseline Analysis ✅

**What it does:**
- Tests if n-gram metrics (word/phrase overlap) can distinguish good from bad close notes
- Compares n-gram scores between reference (good) and other (bad) datasets
- **Hypothesis:** N-grams are NOT useful for evaluating close note quality

**Key Finding:**
- N-gram scores are similar between good and bad close notes
- Confirms we need semantic evaluation instead

**Outputs:**
- N-gram comparison results and visualizations

---

### Notebook 04: Embeddings and Semantics Analysis ✅

**What it does:**
- Generates semantic embeddings for all close notes (BGE-M3 model)
- Calculates semantic similarity between good and bad close notes
- Visualizes semantic relationships using t-SNE
- Validates that quality scores correlate with semantic similarity

**Key Features:**
- Category color-coding in visualizations
- Quality distinction via marker shapes (○ good, □ bad/regular)
- Within-group and between-group similarity analysis

**Outputs:**
- Embeddings and similarity analysis
- t-SNE visualizations with category identification

---

### Notebook 05: LLM-as-a-Judge Evaluation ✅

**What it does:**
- Evaluates close notes using LLM as an automated judge
- Uses 5 evaluation criteria:
  1. **Informativeness** - Does it provide useful information?
  2. **Specificity** - Does it include specific details?
  3. **Completeness** - Does it cover all key aspects?
  4. **No Generic Statements** - Does it avoid generic phrases?
  5. **Clarity** - Is it well-written and clear?
- Compares good vs bad close notes
- Provides scores (0.0-1.0) and reasoning for each criterion

**Key Features:**
- Uses Unitxt + Ollama for local LLM evaluation
- Includes incident context for better assessment
- Detailed results with judge's reasoning
- Visualizations comparing score distributions

**Outputs:**
- Evaluation scores and reasoning
- Comparison analysis between good and bad close notes

---

### Notebook 06: LLM Generation and Evaluation 🔴 TODO

**What it will do:**
- Generate close notes for new incidents using LLM
- Evaluate generated close notes using:
  - Semantic similarity (from Notebook 04)
  - LLM-as-a-Judge (from Notebook 05)
- Provide quality assessment and recommendations

---

## 🔑 Key Concepts

### Ground Truth Dataset
High-quality close notes extracted from incidents that serve as reference examples for evaluation.

### Evaluation Methods

1. **N-gram (Baseline)** - Tests word overlap (not suitable for this use case)
2. **Semantic Similarity** - Compares meaning using embeddings (Notebook 04)
3. **LLM-as-a-Judge** - Structured evaluation with multiple criteria (Notebook 05, main method)

### LLM-as-a-Judge

Uses a Large Language Model (like Llama) to evaluate text quality based on structured criteria, similar to how a human judge would evaluate it.

**How it works:**
1. Define evaluation criteria (what to look for)
2. Provide close note and incident context to LLM
3. LLM assesses against each criterion
4. LLM selects an option (e.g., "Excellent", "Acceptable", "Bad")
5. Get score (0.0-1.0) and reasoning

**Why it matters:**
- Consistent evaluation (same criteria applied to all notes)
- Explainable scores (we know why a score was given)
- Scalable (can evaluate many notes automatically)

---

## 📊 Project Structure

```
3-ai-evaluation/
├── data/                    # Datasets (CSV files)
├── notebooks/               # Jupyter notebooks (01-06)
└── README.md              # This file
```

**Note:** Utility functions are defined directly in the notebooks where they're used, following the workshop's self-contained notebook approach.

---

## 📈 Current Status

**Completed:**
- ✅ Notebook 01: Data Loading and Exploration
- ✅ Notebook 02: Ground Truth Creation
- ✅ Notebook 03: N-gram Baseline Analysis
- ✅ Notebook 04: Embeddings and Semantics Analysis
- ✅ Notebook 05: LLM-as-a-Judge Evaluation

**In Progress:**
- 🔴 Notebook 06: LLM Generation and Evaluation

---

## 🛠️ Dependencies

**Core Libraries:**
- `pandas` - Data manipulation
- `numpy` - Numerical operations
- `matplotlib`, `seaborn` - Visualizations
- `jupyter` - Notebook environment

**AI/ML Libraries:**
- `unitxt` - Evaluation framework (n-gram metrics, LLM-as-a-Judge)
- `sentence-transformers` - Embedding models
- `ollama` - Local LLM serving

**Evaluation:**
- `rouge-score` - N-gram metrics (via Unitxt)
- `sacrebleu` - BLEU metric (via Unitxt)

---

## 📝 Notes

- **Cache folders** (`inference_engine_cache/`) are ignored by git (see `.gitignore`)
- **Data files** in `data/` directory are generated by notebooks
- **Educational focus:** All notebooks include explanations for non-technical audiences

---

## 🎯 Next Steps

1. Complete Notebook 06: LLM Generation and Evaluation
2. Test with real incident data
3. Refine evaluation criteria based on results
4. Optimize prompts for better close note generation

---

**Last Updated:** December 2024

