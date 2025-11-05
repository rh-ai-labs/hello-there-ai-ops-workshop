# 📊 Project Status Document

**Project:** AI Test Drive – Cenário 2: Enriquecendo Incidentes com IA  
**Last Updated:** December 2024  
**Status:** 🟡 In Progress

---

## 📋 Project Overview

**Goal:** Evaluate and generate high-quality close notes for IT incidents using AI.

**Workflow:** See `WORKFLOW.md` for detailed step-by-step process.

**Notebooks:**
1. **Notebook 01** - Data Loading and Exploration ✅
2. **Notebook 02** - Ground Truth Creation ✅
3. **Notebook 03** - N-gram Baseline Analysis ✅
4. **Notebook 04** - LLM-as-a-Judge Evaluation 🔴
5. **Notebook 05** - LLM Generation and Evaluation 🔴

---

## 🎯 Non-Functional Requirements

### Target Audience
- **Primary:** IT professionals, business analysts, project managers
- **Background:** Not data scientists, not familiar with ML/AI concepts
- **Knowledge level:** Basic understanding of IT incidents and documentation

### Notebook Requirements
- ✅ **Educational:** Every concept must be explained in simple terms
- ✅ **Step-by-step:** Clear explanations of what each step does and why
- ✅ **Visual:** Charts and visualizations with interpretation guides
- ✅ **Accessible:** Avoid jargon, explain acronyms, provide examples
- ✅ **Self-contained:** Each notebook should work independently
- ✅ **Readable:** Code comments explain what's happening

### Code Quality
- ✅ Simple, readable code over complex optimizations
- ✅ Clear variable names
- ✅ Inline comments explaining logic
- ✅ Error messages that are helpful and actionable

---

## ✅ What Has Been Completed

### 1. Project Foundation
- ✅ **Project structure** - Directory structure (`src/`, `notebooks/`, `data/`)
- ✅ **Dependencies** - Core libraries defined
- ✅ **Workflow documentation** - `WORKFLOW.md` created

### 2. Source Code Modules (`src/`)

#### ✅ `utils.py` - Utility Functions
- `load_incident_dataset()` - Loads dataset from Hugging Face
- `prepare_incident_for_enrichment()` - Prepares incident data
- `calculate_basic_stats()` - Computes dataset statistics
- `load_ground_truth_embeddings()` - Loads pre-computed embeddings
- `compute_semantic_similarity()` - Computes semantic similarity
- `find_most_similar_close_note()` - Finds similar close notes

#### ✅ `prompts.py` - Prompt Templates
- `get_base_enrichment_prompt()` - Basic enrichment prompt
- `get_structured_enrichment_prompt()` - JSON-structured output
- `get_minimal_enrichment_prompt()` - Minimal prompt variant
- `get_detailed_enrichment_prompt()` - Detailed prompt variant

#### ✅ `evaluator.py` - Evaluation Framework
- `IncidentEnrichmentEvaluator` class
- Embedding model: `BAAI/bge-m3` with FlagEmbedding fallback
- Semantic similarity computation
- ⚠️ **NOTE:** Some functions may need refactoring for Notebook 04/05

### 3. Notebooks

#### ✅ Notebook 01: `01_load_and_explore_dataset.ipynb` - **COMPLETE**
**Status:** ✅ Complete and ready

**What it does:**
- Loads incident dataset from Hugging Face
- Explores dataset structure and characteristics
- Visualizes distributions and patterns
- Prepares datasets for analysis

**Outputs:**
- `incidents_prepared.csv` - Prepared dataset
- `incidents_sample.csv` - Sample dataset

**Audience considerations:** ✅ Clear explanations, educational content

---

#### ✅ Notebook 02: `02_create_ground_truth.ipynb` - **COMPLETE**
**Status:** ✅ Complete and ready

**What it does:**
- Defines quality criteria for "good" close notes
- Filters high-quality close notes (info_score ≥ 0.8, poor_score ≤ 0.1)
- Excludes generic phrases
- Creates ground truth dataset with balanced sampling

**Outputs:**
- `reference_close_notes.csv` - Reference dataset (26 high-quality examples)
- `gt_close_notes_embeddings.npy` - Semantic embeddings (optional)
- `gt_close_notes_embeddings_metadata.pkl` - Embedding metadata

**Audience considerations:** ✅ Educational explanations included

**Note:** ⚠️ May need simplification review for non-technical audience

---

#### ✅ Notebook 03: `03_ngram_comparisons.ipynb` - **COMPLETE**
**Status:** ✅ Complete and ready

**What it does:**
- Creates pairs from same incident: (content, close_notes)
- Compares Ground Truth pairs vs Incidents pairs using n-gram metrics
- Tests hypothesis: Do incident descriptions and close notes use different language?
- Visualizes comparison between datasets

**Outputs:**
- `ngram_comparison_results.csv` - Comparison results
- Visualizations comparing both datasets

**Audience considerations:** ✅ Extensive educational content, concept explanations

**Hypothesis Test:** Confirms n-grams are not suitable → proceed to LLM-as-a-Judge

---

## 🚧 Next Steps - Implementation Roadmap

### 🔴 Critical Path (Must Have)

#### 📋 Notebook 04: LLM-as-a-Judge Evaluation

**Objective:** Evaluate close notes quality using LLM as an automated judge with structured criteria.

**Status:** 🔴 **TO DO**

**What it needs to do:**
1. **Set up evaluation criteria** - 6 quality dimensions (0-5 scores):
   - Topic coverage
   - Profile data accuracy  
   - Supporting facts
   - No invented facts
   - Text structure
   - Conclusion quality

2. **Compare close notes** - For each close note to evaluate:
   - Find similar ground truth reference (by category/similarity)
   - Send pair to LLM judge: (reference, close_note_to_evaluate)
   - Include incident context (`content`) for better evaluation
   - Get structured JSON scores with explanations

3. **Aggregate and visualize results** - Analyze scores across all evaluated close notes

**Deliverables:**
- Notebook `notebooks/04_llm_as_judge_evaluation.ipynb`
- Module `src/llm_judge.py` (if needed)
- Evaluation results with scores and explanations

**Dependencies:**
- ✅ `data/reference_close_notes.csv` - **COMPLETE**
- 🔴 LLM integration (Ollama or other provider) - **NEEDED**
- 🔴 LLM Client implementation - **NEEDED**

**Non-functional requirements:**
- Explain what LLM-as-a-Judge means in simple terms
- Show examples of good vs bad close notes with scores
- Explain each evaluation criterion clearly
- Provide interpretation guides for scores

**Bias mitigation:**
- Position swapping (swap reference and evaluated positions)
- Few-shot prompting (add examples to calibrate judge)
- Context awareness (include incident description)

---

#### 📋 Notebook 05: LLM Generation and Evaluation

**Objective:** Generate close notes for new incidents and evaluate them.

**Status:** 🔴 **TO DO**

**What it needs to do:**
1. **Provide new incident** - Input: incident description (`content`)

2. **Generate resolution** - Use LLM to generate:
   - Resolution steps
   - Troubleshooting actions
   - Technical details

3. **Generate close notes** - Use LLM to create professional close notes from incident + resolution

4. **Evaluate generated close notes** - Use two methods:
   - **Semantic similarity** - Compare embeddings with ground truth references
   - **LLM-as-a-Judge** - Evaluate against ground truth using structured criteria (from Notebook 04)

**Deliverables:**
- Notebook `notebooks/05_llm_generation_evaluation.ipynb`
- Generated close notes for sample incidents
- Evaluation scores (semantic + LLM judge)
- Quality assessment and recommendations

**Dependencies:**
- ✅ `data/reference_close_notes.csv` - **COMPLETE**
- 🔴 Notebook 04 (LLM-as-a-Judge) - **NEEDED**
- 🔴 LLM Client implementation - **NEEDED**

**Non-functional requirements:**
- Show step-by-step: incident → resolution → close notes
- Explain how LLM generates each part
- Compare generated vs reference close notes
- Explain evaluation scores in context

---

### 🟡 Optional / Future Work

#### Phase 3: Semantic Baseline Analysis (Optional)
- Similar to Notebook 03 but using semantic similarity
- Can be skipped if Notebook 03 already confirms traditional metrics aren't suitable
- Status: 🟡 **OPTIONAL**

---

## 🔧 Things That Need Refactoring

### Source Code Modules

#### ⚠️ `src/mlflow_tracking.py` - **NOT USED**
- **Status:** Legacy code, not used in current workflow
- **Action:** Remove or mark as deprecated
- **Reason:** Not using MLflow for tracking

#### ⚠️ `src/evaluator.py` - **NEEDS REVIEW**
- **Status:** Contains evaluation functions that may overlap with Notebook 04/05
- **Action:** Review and refactor to align with LLM-as-a-Judge approach
- **Consider:** Keep only functions used by notebooks, remove unused code

#### ⚠️ `src/prompts.py` - **NEEDS REVIEW**
- **Status:** Contains prompt templates
- **Action:** Review if prompts align with Notebook 05 requirements
- **Consider:** May need new prompts for LLM-as-a-Judge and generation

#### ⚠️ `src/utils.py` - **GOOD, KEEP**
- **Status:** Contains useful utility functions
- **Action:** Keep, but ensure all functions are documented

---

## 📋 Expected Deliverables (Final)

At the end of implementation, participants will have:

1. ✅ **Ground truth dataset** (`data/reference_close_notes.csv`) - **COMPLETE**
2. ✅ **N-gram baseline analysis** (Notebook 03) - **COMPLETE**
3. 🔴 **LLM-as-a-Judge evaluation** (Notebook 04) - **TO DO**
   - Structured evaluation with 6 criteria (0-5 scores)
   - Comparison: existing close notes vs ground truth
   - Explainable scores with reasoning
4. 🔴 **LLM generation and evaluation** (Notebook 05) - **TO DO**
   - Generate close notes for new incidents
   - Evaluate using semantic similarity + LLM-as-a-Judge
   - Quality assessment and recommendations

---

## 🎯 Key Decisions

### ✅ Resolved
1. **Evaluation Framework:** Unitxt selected for n-gram metrics
2. **Ground Truth Approach:** Extract high-quality close notes as references
3. **Evaluation Method:** LLM-as-a-Judge as main evaluation (Notebook 04)
4. **Workflow:** 5 notebooks following clear progression

### 🔴 Pending
1. **LLM Integration:**
   - Which LLM provider? (Ollama, OpenShift AI, etc.)
   - Which model for LLM-as-a-Judge?
   - Which model for generating close notes?
   
2. **LLM Client Implementation:**
   - Create `src/llm_client.py` module
   - Support structured JSON outputs
   - Error handling and retries
   - Configuration via environment variables

---

## 📝 Current Approach Summary

### Data Structure
- **`content`** = Original incident description (input)
- **`close_notes`** = Existing close notes in dataset
- **`close_notes_ref`** = High-quality reference close notes (ground truth)
- **LLM Output** = Generated close notes from incident descriptions

### Evaluation Strategy

**Baseline (Notebook 03):**
- N-gram comparison: Tests if word overlap is useful
- Result: Low scores confirm n-grams aren't suitable
- Conclusion: Need semantic evaluation (LLM-as-a-Judge)

**Main Evaluation (Notebook 04):**
- LLM-as-a-Judge: Structured evaluation with 6 criteria
- Compares: close notes (existing/generated) vs ground truth references
- Provides: Scores (0-5) + explanations for each criterion

**Generation & Evaluation (Notebook 05):**
- Generate: Resolution + close notes for new incidents
- Evaluate: Semantic similarity + LLM-as-a-Judge
- Assess: Quality and provide recommendations

---

## 📊 Implementation Status

### ✅ Completed
- [x] Notebook 01: Data exploration
- [x] Notebook 02: Ground truth creation
- [x] Notebook 03: N-gram baseline analysis
- [x] Workflow documentation (`WORKFLOW.md`)

### 🔴 In Progress / Next
- [ ] Notebook 04: LLM-as-a-Judge evaluation
- [ ] Notebook 05: LLM generation and evaluation
- [ ] LLM Client implementation (`src/llm_client.py`)

### 🟡 Optional / Future
- [ ] Semantic baseline analysis (Notebook 03 alternative)
- [ ] Code cleanup and refactoring

---

## ⚠️ Items to Remove/Refactor

### Remove References To:
- ❌ **Langfuse** - Not using for observability
- ❌ **MLflow** - Not using for experiment tracking
- ❌ **Llama Stack** - Not using, replaced by Unitxt + direct LLM integration
- ❌ **TrustyAI** - Not in current scope

### Code Cleanup Needed:
- ⚠️ `src/mlflow_tracking.py` - Remove or deprecate
- ⚠️ Remove MLflow/Langfuse references from `requirements.txt` (if any)
- ⚠️ Update `src/evaluator.py` to align with Notebook 04/05 approach
- ⚠️ Review `src/prompts.py` for Notebook 05 compatibility

---

**Document Status:** ✅ Updated  
**Last Review:** December 2024  
**Next Review:** After Notebook 04 completion
