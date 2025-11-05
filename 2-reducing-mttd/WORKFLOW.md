# 📋 Project Workflow Summary

**Project:** AI Test Drive – Cenário 2: Enriquecendo Incidentes com IA  
**Goal:** Evaluate and generate high-quality close notes for IT incidents using AI

---

## Notebook 1: Data Loading and Exploration

**Objective:** Understand the incident dataset structure and characteristics.

**Steps:**
1. **Get the dataset** - Load incident data from source
2. **Explore the dataset** - Analyze structure, columns, distributions, and data quality

**Output:**
- `incidents_prepared.csv` - Prepared dataset ready for analysis
- `incidents_sample.csv` - Sample dataset for testing

---

## Notebook 2: Ground Truth Creation

**Objective:** Define and extract high-quality close notes that will serve as reference examples.

**Steps:**
1. **Define quality criteria** - Establish what makes a "good" close note
   - High information score
   - No generic phrases
   - Complete and clear documentation
   
2. **Separate datasets** - Split into two groups:
   - **Ground Truth Dataset** (`reference_close_notes.csv`) - High-quality reference close notes
   - **Incidents Dataset** - All other incidents (with existing close notes)

**Output:**
- `reference_close_notes.csv` - Reference dataset with high-quality close notes
- Semantic embeddings for ground truth (optional)

---

## Notebook 3: N-gram Baseline Analysis

**Objective:** Test if n-gram metrics (word/phrase overlap) are useful for evaluating close notes.

**Steps:**
1. **Create pairs from same incident** - For each incident, pair:
   - `content` (incident description) with `close_notes` (from same incident)
   
2. **Compare n-grams** - Calculate ROUGE scores for:
   - Ground Truth pairs: (content, close_notes_ref)
   - Incidents pairs: (content, close_notes)
   
3. **Compare results** - Analyze if both datasets show similar patterns

**Hypothesis:** N-grams are NOT useful for evaluating/differentiating between good and bad close notes. If scores are similar between good and bad, it confirms n-grams cannot distinguish quality.

**Output:**
- N-gram comparison results
- Visualization comparing both datasets
- Conclusion: N-grams are not suitable → proceed to Semantics Analysis (Notebook 04)

---

## Notebook 4: Embeddings and Semantics Analysis

**Objective:** Analyze semantic similarity between close notes using embeddings to understand how meaning relates to quality.

**Steps:**
1. **Generate embeddings** - Create semantic embeddings for:
   - Reference dataset close notes (good examples)
   - Other incidents close notes (bad/regular examples)
   - Use embedding model (e.g., BGE-M3, Sentence-Transformers)

2. **Compare semantic similarity** - For each close note:
   - Compare with reference close notes (same category/similar incidents)
   - Calculate cosine similarity scores
   - Analyze if good close notes cluster together semantically

3. **Visualize and analyze** - Create visualizations:
   - t-SNE or PCA plots showing semantic space
   - Similarity heatmaps
   - Distribution analysis of similarity scores

4. **Validate quality scores** - Check if:
   - Good close notes (high quality scores) are semantically closer to references
   - Bad close notes (low quality scores) are further from references
   - Semantic similarity correlates with quality

**Output:**
- Embeddings for all close notes
- Semantic similarity analysis results
- Visualizations showing semantic relationships
- Validation of quality scores using semantic similarity

---

## Notebook 5: LLM-as-a-Judge Evaluation

**Objective:** Evaluate close notes quality using LLM as an automated judge with structured criteria.

**Steps:**
1. **Set up evaluation criteria** - Define 6 quality dimensions:
   - Topic coverage
   - Profile data accuracy
   - Supporting facts
   - No invented facts
   - Text structure
   - Conclusion quality

2. **Compare close notes** - For each close note to evaluate:
   - Find similar ground truth reference (using semantic similarity from Notebook 04)
   - Send pair to LLM judge: (reference, close_note_to_evaluate)
   - Include incident context (`content`) for better evaluation
   - Get structured scores (0-5) with explanations

3. **Aggregate results** - Analyze scores across all evaluated close notes

**Output:**
- Evaluation scores for each close note
- Comparison: existing close notes vs ground truth
- Insights about quality differences
- Explainable scores with reasoning

---

## Notebook 6: LLM Generation and Evaluation

**Objective:** Generate close notes for new incidents and evaluate them.

**Steps:**
1. **Provide new incident** - Input: incident description (`content`)

2. **Generate resolution** - Use LLM to generate:
   - Resolution steps
   - Troubleshooting actions
   - Technical details

3. **Generate close notes** - Use LLM to create professional close notes from incident + resolution

4. **Evaluate generated close notes** - Use two methods:
   - **Semantic similarity** - Compare embeddings with ground truth references (from Notebook 04)
   - **LLM-as-a-Judge** - Evaluate against ground truth using structured criteria (from Notebook 05)

**Output:**
- Generated close notes for new incidents
- Evaluation scores (semantic + LLM judge)
- Quality assessment and recommendations

---

## 🔄 Overall Flow

```
Dataset → Explore → Create Ground Truth → Baseline Test (N-grams) 
                                              ↓
                                          (Low scores confirm)
                                              ↓
                                    Semantics Analysis (Embeddings)
                                              ↓
                                    LLM-as-a-Judge Evaluation
                                              ↓
                              Generate & Evaluate New Close Notes
```

---

## 📊 Key Concepts

**Ground Truth Dataset:**
- High-quality close notes extracted from incidents
- Serves as reference/template for evaluation
- Used to compare against other close notes (existing or generated)

**Evaluation Methods:**
1. **N-gram (Baseline)** - Tests if word overlap can distinguish good from bad (not suitable)
2. **Semantic Similarity** - Compares meaning using embeddings (Notebook 04)
3. **LLM-as-a-Judge** - Structured evaluation with multiple criteria (Notebook 05, main method)

**Why This Approach:**
- Each incident has different context → need semantic evaluation, not just word matching
- LLM-as-a-Judge provides explainable scores with reasoning
- Scalable evaluation without human labeling
- Can handle variations in language and structure

---

## 🎯 Success Criteria

- Ground truth dataset created with high-quality examples
- Baseline analysis confirms n-grams aren't suitable
- Semantics analysis shows good close notes cluster together semantically
- LLM-as-a-Judge provides consistent, explainable evaluations
- Generated close notes achieve high scores (≥4.0) on evaluation criteria
- Demonstrated improvement over generic LLM outputs

