# 📊 Project Status Document

**Project:** AI Test Drive – Cenário 2: Enriquecendo Incidentes com IA  
**Last Updated:** December 2024 (Notebook 05 complete)  
**Status:** 🟡 In Progress

---

## 📋 Project Overview

**Goal:** Evaluate and generate high-quality close notes for IT incidents using AI.

**Workflow:** See `WORKFLOW.md` for detailed step-by-step process.

**Notebooks:**
1. **Notebook 01** - Data Loading and Exploration ✅
2. **Notebook 02** - Ground Truth Creation ✅
3. **Notebook 03** - N-gram Baseline Analysis ✅
4. **Notebook 04** - Embeddings and Semantics Analysis ✅
5. **Notebook 05** - LLM-as-a-Judge Evaluation 🔴
6. **Notebook 06** - LLM Generation and Evaluation 🔴

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
- Defines quality criteria for "good" close notes (with examples)
- Filters high-quality close notes (info_score ≥ 0.8, poor_score ≤ 0.1)
- Excludes generic phrases
- Creates ground truth dataset with balanced sampling
- **Separates dataset into two groups:**
  - Reference Dataset (high-quality examples)
  - Other Incidents Dataset (remaining incidents for comparison)
- **Optional embeddings generation:** Processes ALL incidents to validate quality scores
- **Validation:** Checks if incidents with similar quality scores are semantically closer

**Outputs:**
- `reference_close_notes.csv` - Reference dataset (high-quality examples)
- `other_incidents.csv` - Other incidents dataset (remaining incidents)
- `gt_close_notes_embeddings.npy` - Semantic embeddings for all incidents (optional)
- `gt_close_notes_embeddings_metadata.pkl` - Embedding metadata (optional)

**Key Features:**
- ✅ Extensive educational content explaining each step
- ✅ Clear separation of good vs remaining samples
- ✅ Semantic validation of quality scores
- ✅ t-SNE visualization showing all incidents colored by quality score

**Audience considerations:** ✅ Complete educational explanations included, ready for non-technical audience

---

#### ✅ Notebook 03: `03_ngram_comparisons.ipynb` - **COMPLETE**
**Status:** ✅ Complete and ready

**What it does:**
- Creates pairs from same incident: (content, close_notes) for both datasets
- Compares Reference Dataset (good close notes) vs Other Incidents Dataset (bad/regular close notes) using n-gram metrics
- **Tests hypothesis:** Can n-grams distinguish between good and bad close notes?
- Visualizes comparison between good and bad close notes

**Outputs:**
- `ngram_comparison_results.csv` - Comparison results
- Visualizations comparing good vs bad close notes

**Audience considerations:** ✅ Extensive educational content, concept explanations

**Hypothesis Test:** 
- **Hypothesis:** N-grams are NOT useful for evaluating/differentiating between good and bad close notes
- **Test:** Compare n-gram scores from reference (good) vs other incidents (bad)
- **Expected:** If scores are similar, confirms n-grams cannot distinguish quality → proceed to LLM-as-a-Judge

---

## 🚧 Next Steps - Implementation Roadmap

### 🔴 Critical Path (Must Have)

#### ✅ Notebook 04: Embeddings and Semantics Analysis - **COMPLETE**

**Objective:** Analyze semantic similarity between close notes using embeddings to understand how meaning relates to quality.

**Status:** ✅ **COMPLETE**

**What it does:**
1. **Generate embeddings** - Creates semantic embeddings for:
   - Reference dataset close notes (good examples)
   - Other incidents close notes (bad/regular examples)
   - Uses BGE-M3 embedding model (BAAI/bge-m3) via Sentence-Transformers

2. **Compare semantic similarity** - Calculates:
   - Within-group similarity (good vs good, bad vs bad)
   - Between-group similarity (good vs bad)
   - Category-aware similarity analysis (within same category)

3. **Visualize and analyze** - Creates visualizations:
   - t-SNE plots showing semantic space with category color-coding
   - Quality distinction via marker shapes (circles = good, squares = bad/regular)
   - Category breakdown summary

4. **Validate quality scores** - Analyzes:
   - Whether good close notes cluster together semantically
   - Whether semantic similarity can distinguish quality
   - Category-specific patterns

**Deliverables:**
- ✅ Notebook `notebooks/04_semantics_analysis.ipynb` - **COMPLETE**
- ✅ Embeddings for all close notes - **GENERATED**
- ✅ Semantic similarity analysis results - **COMPLETE**
- ✅ Visualizations showing semantic relationships - **COMPLETE**
- ✅ Category-aware visualization with color-coding - **COMPLETE**

**Key Features:**
- Educational explanations of embeddings and semantic similarity
- Category color-coding in t-SNE visualization
- Quality distinction via marker shapes (○ circles = good, □ squares = bad/regular)
- Category breakdown summary showing distribution
- Analysis of alternative embedding models and strategies

**Dependencies:**
- ✅ `data/reference_close_notes.csv` - **COMPLETE**
- ✅ `data/other_incidents.csv` - **COMPLETE**
- ✅ Embedding models (BGE-M3, Sentence-Transformers) - **AVAILABLE**

**Non-functional requirements:** ✅ **MET**
- ✅ Explains embeddings and semantic similarity in simple terms
- ✅ Shows how embeddings capture meaning (not just words)
- ✅ Explains why semantic similarity matters for evaluation
- ✅ Provides interpretation guides for similarity scores and visualizations

---

#### 📋 Notebook 05: LLM-as-a-Judge Evaluation

**Objective:** Evaluate close notes quality using LLM as an automated judge with structured criteria.

**Status:** ✅ **COMPLETE**

**What it does:**
1. **Set up evaluation criteria** - 5 quality dimensions:
   - Informativeness - Does it provide useful information?
   - Specificity - Does it include specific details?
   - Completeness - Does it cover all key aspects?
   - No Generic Statements - Does it avoid generic phrases?
   - Clarity - Is it well-written and clear?

2. **Evaluate close notes** - For each close note:
   - Load from reference dataset (good) and other incidents dataset (bad)
   - Include incident context (`content` field) for better evaluation
   - Evaluate against all 5 criteria using LLM-as-a-Judge
   - Get scores (0.0-1.0) and reasoning for each criterion

3. **Compare and visualize results** - Analyze scores across all evaluated close notes:
   - Compare good vs bad close notes
   - Visualize score distributions
   - Show criterion-by-criterion differences
   - Display detailed results with reasoning

**Deliverables:**
- ✅ Notebook `notebooks/05_llm_as_judge_evaluation.ipynb` - **COMPLETE**
- ✅ Test scripts: `scripts/test_llm_as_judge_ollama.py`, `scripts/test_simple_criteria.py` - **COMPLETE**
- ✅ Evaluation framework using Unitxt + Ollama - **COMPLETE**

**Dependencies:**
- ✅ `data/reference_close_notes.csv` - **COMPLETE**
- ✅ `data/other_incidents.csv` - **COMPLETE**
- ✅ Notebook 04 (Semantics Analysis) - **COMPLETE**
- ✅ LLM integration (Ollama) - **COMPLETE**
- ✅ Unitxt LLM-as-a-Judge implementation - **COMPLETE**

**Non-functional requirements:** ✅ **MET**
- ✅ Explains what LLM-as-a-Judge means in simple terms
- ✅ Shows examples of good vs bad close notes with scores
- ✅ Explains each evaluation criterion clearly
- ✅ Provides interpretation guides for scores
- ✅ Educational content throughout for non-technical audience

**Key Features:**
- Uses Unitxt's `LLMJudgeDirect` with `CrossProviderInferenceEngine` (Ollama)
- 5 custom criteria tailored for close notes evaluation
- Includes incident context for better evaluation
- Displays detailed reasoning for each score
- Visualizations comparing good vs bad close notes
- Average score calculation across all criteria

**Next Review:** After Notebook 06 completion

---

#### 📋 Notebook 06: LLM Generation and Evaluation

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
   - **Semantic similarity** - Compare embeddings with ground truth references (from Notebook 04)
   - **LLM-as-a-Judge** - Evaluate against ground truth using structured criteria (from Notebook 05)

**Deliverables:**
- Notebook `notebooks/06_llm_generation_evaluation.ipynb`
- Generated close notes for sample incidents
- Evaluation scores (semantic + LLM judge)
- Quality assessment and recommendations

**Dependencies:**
- ✅ `data/reference_close_notes.csv` - **COMPLETE**
- ✅ Notebook 04 (Semantics Analysis) - **COMPLETE** (for semantic evaluation)
- 🔴 Notebook 05 (LLM-as-a-Judge) - **NEEDED** (for structured evaluation)
- 🔴 LLM Client implementation - **NEEDED**

**Non-functional requirements:**
- Show step-by-step: incident → resolution → close notes
- Explain how LLM generates each part
- Compare generated vs reference close notes
- Explain evaluation scores in context

---

### 🟡 Optional / Future Work

- Additional analysis and visualizations (as needed)
- Code cleanup and optimization

---

## 🔧 Things That Need Refactoring

### Source Code Modules

#### ⚠️ `src/mlflow_tracking.py` - **NOT USED**
- **Status:** Legacy code, not used in current workflow
- **Action:** Remove or mark as deprecated
- **Reason:** Not using MLflow for tracking

#### ⚠️ `src/evaluator.py` - **NEEDS REVIEW**
- **Status:** Contains evaluation functions that may overlap with Notebook 04/05/06
- **Action:** Review and refactor to align with semantics analysis and LLM-as-a-Judge approach
- **Consider:** Keep only functions used by notebooks, remove unused code

#### ⚠️ `src/prompts.py` - **NEEDS REVIEW**
- **Status:** Contains prompt templates
- **Action:** Review if prompts align with Notebook 06 requirements
- **Consider:** May need new prompts for LLM-as-a-Judge and generation

#### ⚠️ `src/utils.py` - **GOOD, KEEP**
- **Status:** Contains useful utility functions
- **Action:** Keep, but ensure all functions are documented

---

## 📋 Expected Deliverables (Final)

At the end of implementation, participants will have:

1. ✅ **Ground truth dataset** (`data/reference_close_notes.csv`) - **COMPLETE**
2. ✅ **N-gram baseline analysis** (Notebook 03) - **COMPLETE**
3. ✅ **Semantics analysis** (Notebook 04) - **COMPLETE**
   - ✅ Generate embeddings for all close notes
   - ✅ Analyze semantic similarity between good and bad close notes
   - ✅ Visualize semantic relationships with category color-coding
4. ✅ **LLM-as-a-Judge evaluation** (Notebook 05) - **COMPLETE**
   - Structured evaluation with 5 criteria (0.0-1.0 scores)
   - Comparison: existing close notes vs ground truth
   - Explainable scores with reasoning
   - Visualizations and detailed analysis
5. 🔴 **LLM generation and evaluation** (Notebook 06) - **TO DO**
   - Generate close notes for new incidents
   - Evaluate using semantic similarity + LLM-as-a-Judge
   - Quality assessment and recommendations

---

## 🎯 Key Decisions

### ✅ Resolved
1. **Evaluation Framework:** Unitxt selected for n-gram metrics
2. **Ground Truth Approach:** Extract high-quality close notes as references
3. **Evaluation Method:** Semantics analysis (Notebook 04) + LLM-as-a-Judge (Notebook 05)
4. **Workflow:** 6 notebooks following clear progression

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
- **`close_notes`** = Existing close notes in dataset (in `other_incidents.csv`)
- **`close_notes_ref`** = High-quality reference close notes (in `reference_close_notes.csv`)
- **LLM Output** = Generated close notes from incident descriptions

### Datasets Created
- **`reference_close_notes.csv`** - High-quality close notes (good samples) for evaluation
- **`other_incidents.csv`** - Remaining incidents (for comparison in Notebook 03)

### Evaluation Strategy

**Baseline (Notebook 03):**
- N-gram comparison: Tests if n-grams can distinguish good from bad close notes
- Method: Compare n-gram scores from reference dataset (good) vs other incidents dataset (bad)
- Result: If scores are similar, confirms n-grams cannot distinguish quality
- Conclusion: Need semantic evaluation which can evaluate meaning and quality

**Semantics Analysis (Notebook 04):**
- Embeddings: Generate semantic representations for all close notes
- Similarity: Compare good vs bad close notes in semantic space
- Validation: Check if semantic similarity correlates with quality scores
- Visualization: Show semantic relationships and clustering

**Main Evaluation (Notebook 05):**
- LLM-as-a-Judge: Structured evaluation with 6 criteria
- Compares: close notes (existing/generated) vs ground truth references
- Provides: Scores (0-5) + explanations for each criterion
- Uses: Semantic similarity from Notebook 04 to find similar references

**Generation & Evaluation (Notebook 06):**
- Generate: Resolution + close notes for new incidents
- Evaluate: Semantic similarity (from Notebook 04) + LLM-as-a-Judge (from Notebook 05)
- Assess: Quality and provide recommendations

---

## 📊 Implementation Status

### ✅ Completed
- [x] Notebook 01: Data exploration
- [x] Notebook 02: Ground truth creation (refactored with educational content, saves two datasets, validates quality scores)
- [x] Notebook 03: N-gram baseline analysis
- [x] Workflow documentation (`WORKFLOW.md`)
- [x] Project status refactored (removed unused tools, aligned with workflow)

### 🔴 In Progress / Next
- [x] Notebook 04: Embeddings and Semantics Analysis ✅
- [ ] Notebook 05: LLM-as-a-Judge evaluation
- [ ] Notebook 06: LLM generation and evaluation
- [ ] LLM Client implementation (`src/llm_client.py`)

### 🟡 Optional / Future
- [ ] Code cleanup and refactoring
- [ ] Additional analysis and visualizations

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
- ⚠️ Update `src/evaluator.py` to align with Notebook 04/05/06 approach
- ⚠️ Review `src/prompts.py` for Notebook 06 compatibility

---

**Document Status:** ✅ Updated  
**Last Review:** December 2024  
**Next Review:** After Notebook 05 completion

---

## 📝 Recent Updates (December 2024)

### Notebook 02 Refactoring
- ✅ Added extensive educational content for non-technical audience
- ✅ Clarified dataset separation (Reference vs Other Incidents)
- ✅ Now saves two CSV files: `reference_close_notes.csv` and `other_incidents.csv`
- ✅ Updated embeddings to process ALL incidents (not just reference)
- ✅ Added validation: checks if similar quality scores = semantic similarity
- ✅ Updated t-SNE visualization to show all incidents with quality scores
- ✅ Fixed indentation errors in embeddings section
- ✅ All variable references updated (`gt_final` → `reference_final`)

### Notebook 03 Refactoring
- ✅ Updated hypothesis: Now tests if n-grams can distinguish good from bad close notes (not testing if descriptions vs close notes use different language)
- ✅ Clarified comparison: Reference Dataset (good) vs Other Incidents Dataset (bad)
- ✅ Updated interpretation: Focus on similarity of scores between good and bad (not just low scores)
- ✅ Updated visualization labels: "Reference (Good)" vs "Other Incidents (Bad)"
- ✅ Updated conclusion logic: Compares score differences to validate hypothesis
- ✅ Fixed dataset filename reference (`gt_close_notes.csv` → `reference_close_notes.csv`)

### Notebook 04 Completion
- ✅ Created comprehensive embeddings and semantics analysis notebook
- ✅ Generates embeddings for all close notes using BGE-M3 model
- ✅ Calculates semantic similarity (within-group and between-group)
- ✅ Category-aware similarity analysis
- ✅ t-SNE visualization with category color-coding
- ✅ Quality distinction via marker shapes (○ circles = good, □ squares = bad/regular)
- ✅ Category breakdown summary
- ✅ Educational content explaining embeddings and semantic similarity

### Notebook 05 Completion
- ✅ Created LLM-as-a-Judge evaluation notebook
- ✅ Implemented 5 custom evaluation criteria (Informativeness, Specificity, Completeness, No Generic Statements, Clarity)
- ✅ Integrated Unitxt LLM-as-a-Judge with Ollama (local LLM)
- ✅ Created test scripts: `test_llm_as_judge_ollama.py`, `test_simple_criteria.py`
- ✅ Evaluation includes incident context for better assessment
- ✅ Detailed results display with scores, options, and reasoning
- ✅ Visualizations comparing good vs bad close notes
- ✅ Educational content explaining LLM-as-a-Judge in simple terms
- ✅ Criterion-by-criterion comparison and interpretation guides
- ✅ Score extraction and analysis framework
- ✅ Comparison between reference (good) and other (bad) close notes

### Documentation Updates
- ✅ Created `WORKFLOW.md` - Simple workflow summary
- ✅ Refactored `PROJECT_STATUS.md` - Removed unused tools (Langfuse, MLflow, Llama Stack)
- ✅ Updated all filename references (`gt_close_notes.csv` → `reference_close_notes.csv`)
