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

**Hypothesis:** Low n-gram scores confirm that incident descriptions and close notes use different language, validating that n-grams aren't suitable for evaluation.

**Output:**
- N-gram comparison results
- Visualization comparing both datasets
- Conclusion: N-grams are not suitable → proceed to LLM-as-a-Judge

---

## Notebook 4: LLM-as-a-Judge Evaluation

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
   - Find similar ground truth reference (by category/similarity)
   - Send pair to LLM judge: (reference, close_note_to_evaluate)
   - Get structured scores (0-5) with explanations

3. **Aggregate results** - Analyze scores across all evaluated close notes

**Output:**
- Evaluation scores for each close note
- Comparison: existing close notes vs ground truth
- Insights about quality differences

---

## Notebook 5: LLM Generation and Evaluation

**Objective:** Generate close notes for new incidents and evaluate them.

**Steps:**
1. **Provide new incident** - Input: incident description (`content`)

2. **Generate resolution** - Use LLM to generate:
   - Resolution steps
   - Troubleshooting actions
   - Technical details

3. **Generate close notes** - Use LLM to create professional close notes from incident + resolution

4. **Evaluate generated close notes** - Use two methods:
   - **Semantic similarity** - Compare embeddings with ground truth references
   - **LLM-as-a-Judge** - Evaluate against ground truth using structured criteria

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
1. **N-gram (Baseline)** - Tests if word overlap is useful (not suitable)
2. **Semantic Similarity** - Compares meaning using embeddings
3. **LLM-as-a-Judge** - Structured evaluation with multiple criteria (main method)

**Why This Approach:**
- Each incident has different context → need semantic evaluation, not just word matching
- LLM-as-a-Judge provides explainable scores with reasoning
- Scalable evaluation without human labeling
- Can handle variations in language and structure

---

## 🎯 Success Criteria

- Ground truth dataset created with high-quality examples
- Baseline analysis confirms n-grams aren't suitable
- LLM-as-a-Judge provides consistent, explainable evaluations
- Generated close notes achieve high scores (≥4.0) on evaluation criteria
- Demonstrated improvement over generic LLM outputs

