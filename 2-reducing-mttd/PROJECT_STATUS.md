# 📊 Project Status Document

**Project:** AI Test Drive – Cenário 2: Enriquecendo Incidentes com IA  
**Last Updated:** November 2025  
**Status:** 🟡 In Progress

---

## ✅ What Has Been Completed

### 1. Project Foundation
- ✅ **Project structure** - Created basic directory structure (`src/`, `notebooks/`, `data/`)
- ✅ **requirements.txt** - Defined all dependencies including:
  - Core data science libraries (pandas, numpy, matplotlib, seaborn)
  - Hugging Face datasets and transformers
  - LangChain for LLM integration
  - MLflow for experiment tracking
  - Evaluation libraries (rouge-score, sentence-transformers)
- ✅ **.gitignore** - Python/Jupyter/ML project specific ignore patterns

### 2. Source Code Modules (`src/`)

#### ✅ `utils.py` - Utility Functions
- `load_incident_dataset()` - Loads dataset from Hugging Face with sampling support
- `prepare_incident_for_enrichment()` - Prepares incident data for LLM prompts
- `calculate_basic_stats()` - Computes dataset statistics
- `save_enriched_results()` - Saves results to CSV
- `load_ground_truth_embeddings()` - Loads pre-computed embeddings for ground truth
- `compute_semantic_similarity()` - Computes semantic similarity between two texts
- `find_most_similar_close_note()` - Finds most semantically similar close notes

#### ✅ `prompts.py` - Prompt Templates
- `get_base_enrichment_prompt()` - Basic enrichment prompt
- `get_structured_enrichment_prompt()` - JSON-structured output prompt
- `get_minimal_enrichment_prompt()` - Minimal prompt (Scenario A - general LLM)
- `get_detailed_enrichment_prompt()` - Detailed prompt (Scenario B - tuned LLM)
- `get_prompt_variants()` - Returns dictionary of all prompt variants

#### ✅ `evaluator.py` - Evaluation Framework
- `IncidentEnrichmentEvaluator` class with:
  - `evaluate_with_ground_truth()` - ROUGE scores and semantic similarity
  - `evaluate_json_structure()` - Validates JSON structure and required fields
  - `evaluate_specificity()` - Measures specificity (avoids vague statements)
  - `evaluate_actionability()` - Assesses actionability of resolution steps
  - `comprehensive_evaluation()` - Combines all metrics into overall quality score
  - **Embedding Model:** Uses `BAAI/bge-m3` with FlagEmbedding fallback support
  - Supports multilingual, multi-granularity embeddings (100+ languages, up to 8,192 tokens)

#### ✅ `mlflow_tracking.py` - Experiment Tracking
- `setup_mlflow()` - Configures MLflow experiment
- `log_incident_enrichment_run()` - Logs individual runs with metrics
- `log_comparison_run()` - Logs comparison between Scenario A and B
- `flatten_dict()` - Helper for nested dictionary logging
- `get_best_run()` - Retrieves best run based on metrics

### 3. Notebooks

#### ✅ `01_load_and_explore_dataset.ipynb` - **COMPLETE**
Comprehensive data exploration notebook with:
- Dataset loading from Hugging Face
- Basic dataset overview (structure, types, missing values)
- Dataset statistics calculation
- 9-panel visualization dashboard
- 4-panel content quality analysis
- Sample incident examination
- Data preparation for experiments
- Saves prepared datasets (`incidents_prepared.csv`, `incidents_sample.csv`)

#### ✅ `02_create_ground_truth.ipynb` - **COMPLETE**
Ground truth dataset creation notebook with:
- High-quality close notes filtering (info_score ≥ 0.8, poor_score ≤ 0.1)
- Generic phrase exclusion
- Balanced sampling across categories
- Ground truth dataset creation (`gt_close_notes.csv`)
- **Semantic Embeddings Analysis:**
  - Embedding generation using BGE-M3 model
  - Semantic similarity analysis within and between categories
  - t-SNE visualization for cluster analysis
  - Embeddings saved for future evaluation (`gt_close_notes_embeddings.npy`)
  - Metadata tracking (`gt_close_notes_embeddings_metadata.pkl`)

### 4. Dataset Understanding
- ✅ Dataset loaded and explored
- ✅ Understanding of actual columns:
  - Primary columns: `number`, `type`, `date`, `contact_type`, `short_description`, `content`, `category`, `subcategory`, `customer`, `resolved_at`, `close_notes`, `agent`, `reassigned_count`, `resolution_time`, `issue/request`, `software/system`, `assignment_group`, `info_score_close_notes`
  - Categories: SOFTWARE (dominant), ACCOUNT, PIV CARD, EMAIL, PRINTER, NETWORK
  - Subcategories: ERROR, MALFUNCTION, CONFIGURATION, INSTALLATION, ACCESS, etc.
  - Contact types: Email, Chat, Phone, Self-service
  - Types: Incident, Request

### 5. Ground Truth Dataset ✅ **COMPLETE**
- ✅ **Ground truth dataset created** (`data/gt_close_notes.csv`)
  - High-quality close notes filtered and validated
  - Balanced sampling across categories
  - 26 high-quality reference examples with metadata
- ✅ **Semantic embeddings generated**
  - Model: `BAAI/bge-m3` (multilingual, multi-granularity)
  - Semantic similarity analysis implemented
  - t-SNE visualization for cluster exploration
  - Embeddings saved for evaluation pipeline
- ✅ **Embedding utilities**
  - Support for FlagEmbedding fallback
  - Functions for loading and using pre-computed embeddings
  - Semantic similarity computation functions

---

## 🚧 Next Steps - Implementation Roadmap

### 🎯 Phase 1: Ground Truth Creation ✅ **COMPLETE**

#### ✅ Step 1: Criar o Ground Truth de `close_notes` - **COMPLETED**

**Status:** ✅ Implementado e concluído

**Entregas:**
- ✅ Notebook `02_create_ground_truth.ipynb` criado e funcional
- ✅ Ground truth dataset `data/gt_close_notes.csv` criado (26 exemplos de alta qualidade)
- ✅ Embeddings semânticos gerados usando BGE-M3
- ✅ Análise de similaridade semântica implementada
- ✅ Visualização t-SNE para exploração de clusters
- ✅ Arquivos de embeddings salvos para uso futuro:
  - `data/gt_close_notes_embeddings.npy` (embeddings array)
  - `data/gt_close_notes_embeddings_metadata.pkl` (metadados)

**Características do Dataset:**
- Filtros aplicados: `info_score_close_notes` ≥ 0.8, `info_score_poor_close_notes` ≤ 0.1
- Exclusão de frases genéricas
- Amostragem balanceada por categoria
- Metadados incluídos: category, subcategory, contact_type, info_score

**Modelo de Embedding:**
- Modelo: `BAAI/bge-m3`
- Suporte multilíngue (100+ idiomas)
- Multi-granularidade (frases a documentos longos)
- Fallback para FlagEmbedding se necessário

---

### 🎯 Phase 2: N-gram Baseline Analysis

#### 📋 Step 2: Baseline N-gram Comparison (gt_close_notes × incident_descriptions)

**Objetivo:** Realizar uma análise exploratória para testar se métricas n-gram são úteis para avaliar qualidade de close notes.

**Contexto:**
1. Temos um dataset de incidentes com descrições originais (`content`)
2. Extraímos close notes de alta qualidade para servir como referência (`close_notes_ref`)
3. Objetivo final: Avaliar close notes (existentes ou geradas por LLM) contra essas referências

**Hipótese:** Descrições de incidentes e close notes usam linguagem muito diferente, tornando métricas n-gram menos úteis para avaliação.

**Teste:** Comparar close notes de ground truth vs descrições de incidentes usando métricas n-gram.

**Resultado Esperado:** Se os scores n-gram forem muito baixos (0.1-0.3), confirma que descrições de incidentes e close notes usam vocabulário diferente, validando que devemos usar **LLM-as-a-Judge** (avaliação semântica) em vez de n-grams para a avaliação principal.

**Por que usar Unitxt?**

✅ **Padronização**: Framework padronizado para avaliação de modelos  
✅ **Eficiência**: Métricas pré-implementadas e otimizadas  
✅ **Escalabilidade**: Processamento eficiente de grandes volumes  
✅ **Manutenibilidade**: Menos código customizado para manter  
✅ **Reprodutibilidade**: Resultados consistentes e comparáveis

**Abordagem:** Usar Unitxt para realizar comparações n-gram entre:
- **Ground Truth Dataset**: `data/gt_close_notes.csv` (contém `close_notes_ref`)
- **Incidents Dataset**: `data/incidents_prepared.csv` (contém `content` - descrições de problemas)

**Nota:** Esta comparação é um **teste de baseline**. A avaliação real será feita na Phase 4 usando LLM-as-a-Judge, que compara close notes contra close notes usando critérios semânticos.

**Etapas:**

1. **Preparar datasets para Unitxt:**
   - Carregar `gt_close_notes.csv` com campo `close_notes_ref`
   - Carregar `incidents_prepared.csv` com campo `content`
   - Estruturar dados no formato esperado pelo Unitxt

2. **Configurar métricas n-gram no Unitxt:**
   - ROUGE-1, ROUGE-2, ROUGE-L, ROUGE-Lsum (n-gram overlap)

3. **Executar comparações:**
   - Para cada par (ground truth close note, incident description)
   - Calcular métricas n-gram usando Unitxt
   - Agregar resultados por categoria/subcategoria

4. **Analisar resultados e concluir:**
   - Gerar visualizações de distribuição de scores
   - Identificar padrões por categoria
   - **Conclusão:** Se scores são baixos, confirma hipótese e valida uso de LLM-as-a-Judge

**Deliverable:** 
- Notebook `notebooks/03_ngram_comparisons.ipynb` usando Unitxt
- Métricas n-gram comparando `close_notes_ref` vs `content`
- Visualizações e análise de resultados
- Conclusão sobre relevância de n-grams para avaliação

**Notebook:** ✅ Criado `notebooks/03_ngram_comparisons.ipynb` usando Unitxt

**Dependencies:** 
- ✅ `data/gt_close_notes.csv` (do Step 1) - **COMPLETE**
- ✅ `data/incidents_prepared.csv` - **COMPLETE**
- ✅ Unitxt instalado (`unitxt>=1.0.0`) - **COMPLETE**
- ✅ Configuração Unitxt para n-gram metrics - **COMPLETE**

**Status:** ✅ **COMPLETE** - Notebook criado e funcional

---

### 🎯 Phase 3: Semantic Baseline Analysis (Optional)

#### 📋 Step 3: Baseline Semantic Comparison (gt_close_notes × incident_descriptions)

**Status:** 🟡 **OPTIONAL** - Pode ser pulado se Phase 2 já confirmar que métricas tradicionais não são adequadas

**Objetivo:** Comparar o texto de referência (`close_notes_ref` do ground truth dataset) com os textos de incidentes (`content` do incidents dataset) usando métricas de similaridade semântica como análise complementar.

**Princípio:** Usar embeddings semânticos para medir similaridade de significado entre textos, capturando relações que métricas n-gram não conseguem capturar.

**Nota:** Similar à Phase 2, esta é uma análise de baseline. Se Phase 2 já confirmar que métricas tradicionais não são adequadas, esta fase pode ser opcional. A avaliação principal será feita na Phase 4 usando LLM-as-a-Judge.

**Por que usar Unitxt?**

✅ **Padronização**: Framework padronizado para avaliação de modelos  
✅ **Eficiência**: Métricas de similaridade semântica pré-implementadas  
✅ **Escalabilidade**: Processamento eficiente de grandes volumes  
✅ **Manutenibilidade**: Menos código customizado para manter  
✅ **Reprodutibilidade**: Resultados consistentes e comparáveis

**Abordagem:** Usar Unitxt para realizar comparações semânticas entre:
- **Ground Truth Dataset**: `data/gt_close_notes.csv` (contém `close_notes_ref`)
- **Incidents Dataset**: `data/incidents_prepared.csv` (contém `content`)

**Etapas:**

1. **Preparar datasets para Unitxt:**
   - Carregar `gt_close_notes.csv` com campo `close_notes_ref`
   - Carregar `incidents_prepared.csv` com campo `content`
   - Estruturar dados no formato esperado pelo Unitxt

2. **Configurar métricas semânticas no Unitxt:**
   - Cosine similarity usando embeddings (sentence-transformers)
   - Semantic similarity scores
   - Opcionalmente usar embeddings pré-computados (`gt_close_notes_embeddings.npy`)

3. **Executar comparações semânticas:**
   - Para cada par (ground truth close note, incident description)
   - Calcular similaridade semântica usando Unitxt
   - Comparar com métricas n-gram da Phase 2
   - Agregar resultados por categoria/subcategoria

4. **Analisar resultados:**
   - Gerar visualizações de distribuição de scores semânticos
   - Comparar com scores n-gram (Phase 2)
   - Identificar padrões por categoria
   - Conclusão sobre relevância de métricas semânticas

**Deliverable:** 
- Notebook `notebooks/04_semantic_comparisons.ipynb` usando Unitxt (opcional)
- Métricas de similaridade semântica comparando `close_notes_ref` vs `content`
- Visualizações e análise comparativa com Phase 2

**Notebook:** 🟡 Criar `notebooks/04_semantic_comparisons.ipynb` usando Unitxt (opcional)

**Dependencies:** 
- ✅ `data/gt_close_notes.csv` (do Step 1) - **COMPLETE**
- ✅ `data/gt_close_notes_embeddings.npy` (opcional) - **COMPLETE**
- ✅ `data/incidents_prepared.csv` - **COMPLETE**
- ✅ Unitxt instalado (`unitxt>=1.0.0`) - **COMPLETE**
- ✅ Sentence-transformers/BGE-M3 para embeddings - **COMPLETE**
- 🔴 Configuração Unitxt para semantic similarity metrics - **OPTIONAL**

**Referência:** Unitxt documentation for semantic similarity metrics

---                                | Description                                                                            | Example of “Good” (Score 5)                                                                              |
| ---------------------------------------- | -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| **Incident Coverage**                    | Does the generated note cover the same core problem and context as the reference note? | Mentions the same issue (e.g., “Google Workspace crashing when saving files”) and troubleshooting scope. |
| **Technical Steps & Resolution Actions** | Are the main diagnostic or corrective steps included and technically sound?            | Lists actions such as “cleared cache,” “reinstalled software,” or “updated drivers.”                     |
| **Accuracy of Facts**                    | Does it avoid adding or changing facts not present in the reference note?              | No new systems, error codes, or users invented.                                                          |
| **Customer/System Context**              | Does it correctly reference the affected system, user, or service?                     | Correctly identifies the impacted system (e.g., “Epson ET-2760 printer”) and user role.                  |
| **Clarity & Structure**                  | Is the note logically structured (problem → action → result)?                          | Uses concise sentences, chronological order, and readable formatting.                                    |
| **Resolution Summary / Conclusion**      | Does it clearly describe the outcome and confirm resolution or escalation?             | Ends with “Issue resolved and verified with user” or equivalent closure statement.                       |

Each dimension is rated from **0 to 5**, where 5 = excellent alignment, 0 = completely incorrect.

---

## 🧩 Step 2 — Judge Prompt Template

The evaluation LLM (judge) must follow a **structured JSON output**, ensuring consistency and automation.
This is the reusable prompt you’ll give to the evaluator model:

---

> **System Prompt:**
> You are an expert in IT Service Management and incident documentation.
> Your task is to evaluate how accurately and completely a *generated close note* describes the resolution of an incident, compared to a *reference note*.
>
> Compare the following texts:
>
> * **Reference (ground truth) close note:**
>   {close_notes_ref}
>
> * **Generated close note:**
>   {close_notes_pred}
>
> Evaluate the generated note according to the following criteria.
> For each, assign a **score from 0 to 5** and include a one-sentence explanation.
>
> 1. **Incident coverage (0–5)** — Does it address the same issue and context?
> 2. **Technical steps & resolution actions (0–5)** — Are the main diagnostic and corrective actions consistent and complete?
> 3. **Accuracy of facts (0–5)** — Does it avoid inventing systems, errors, or results?
> 4. **Customer/system context (0–5)** — Does it correctly reference the affected service, device, or user?
> 5. **Clarity & structure (0–5)** — Is it readable, logically ordered, and professionally written?
> 6. **Resolution summary (0–5)** — Does it clearly describe the outcome or confirmation of resolution?
>
> Then compute:
>
> * `"general_score"` — the average of the six scores
> * `"general_score_explanation"` — a brief summary of your overall judgment
>
> Return the evaluation as valid JSON only:
>
> ```json
> {
>   "check_incident_coverage": 5,
>   "check_incident_coverage_explanation": "...",
>   "check_technical_steps": 5,
>   "check_technical_steps_explanation": "...",
>   "check_accuracy_of_facts": 5,
>   "check_accuracy_of_facts_explanation": "...",
>   "check_customer_context": 5,
>   "check_customer_context_explanation": "...",
>   "check_clarity_structure": 4,
>   "check_clarity_structure_explanation": "...",
>   "check_resolution_summary": 5,
>   "check_resolution_summary_explanation": "...",
>   "general_score": 4.83,
>   "general_score_explanation": "The generated close note accurately covers the same incident, includes consistent troubleshooting steps, and provides a clear resolution summary with no invented facts."
> }
> ```

---

## 🧮 Step 3 — Scoring Standards

| Score             | Interpretation                                                    | Example                                                             |
| ----------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| **5 (Excellent)** | Fully accurate and complete; aligns perfectly with the reference. | Mentions identical issue, actions, and outcome in a structured way. |
| **4 (Good)**      | Mostly accurate with minor omissions or paraphrasing.             | Slightly simplified version but conveys same meaning.               |
| **3 (Adequate)**  | Covers the main idea but misses important details.                | Omits one or two troubleshooting steps.                             |
| **2 (Weak)**      | Only partially correct; vague or incomplete.                      | Describes the issue but not the fix.                                |
| **1 (Poor)**      | Misleading or incorrect content.                                  | Introduces wrong system or incorrect result.                        |
| **0 (Invalid)**   | Completely unrelated or hallucinated.                             | Talks about something entirely different.                           |

---

## 🔍 Step 4 — How to Run the Evaluation

1. **Select dataset:** use incident records for which we have:
   - *Reference* close note (`close_notes_ref` from ground truth)
   - *Close note to evaluate* (`close_notes` from dataset, or LLM-generated)
   
   **Note:** Each incident has different context, so we match by category/similarity or use same incident pairs where available.

2. **Send each pair** (`close_notes_ref`, `close_notes_to_evaluate`) through the judge prompt.
3. **Collect JSON outputs** for all samples.
4. **Aggregate scores** across all dimensions and samples:

   * Mean score per dimension;
   * Mean `general_score`;
   * Distribution of low scores (to detect weak generations).

This can be done as a batch notebook or automated evaluation job.

**Challenges & Solutions:**
- **Challenge:** Each incident has different context → different close notes expected
- **Solution:** Match by category/subcategory, or use semantic similarity to find similar incidents
- **Solution:** Provide context (incident description) to judge for better evaluation

---

## 📊 Step 5 — Interpreting Results

* **High-performing models** should achieve:

  * `general_score ≥ 4.0`
  * No dimension consistently below 3.5.

* **Low-performing prompts/models** typically show:

  * Low “technical steps” or “accuracy of facts” scores;
  * Inconsistent coverage or missing conclusions.

Use these scores to rank:

* Prompt templates;
* Model versions (generic vs. fine-tuned);
* Post-processing strategies (structured outputs vs. free text).

---

## 🔗 Step 6 — Integrating with Langfuse & MLflow

### **Langfuse**

* Log every evaluation as a trace:

  * `input` = reference note + generated note,
  * `output` = JSON with judge scores,
  * Tags for each dimension and score (e.g., `check_technical_steps=4`).
* Build dashboards to track score evolution over prompt versions.

### **MLflow**

* Log:

  * `general_score_mean` per experiment,
  * All six sub-scores as metrics,
  * Associated prompt/model identifiers.
* Use these logs to correlate **model quality vs. cost vs. runtime**.

---

## ✅ Deliverables Checklist

By the end of the LLM-as-a-Judge setup, you should have:

* [ ] **Evaluation schema** (the six ITSM-specific dimensions)
* [ ] **Reference dataset (`gt_close_notes.csv`)**
* [ ] **Judge prompt template (structured JSON)**
* [ ] **Scoring scale (0–5)** documented

**Usando Llama Stack `/scoring` API:**

- Criar scoring function customizada para LLM-as-a-Judge
- Configurar prompt de avaliação com critérios específicos
- Usar `/scoring` API para executar avaliações em batch
- Obter scores estruturados e explicações qualitativas

**Critérios de avaliação recomendados:**

1. **Cobertura de tópico** – O texto cobre os mesmos aspectos do problema?
2. **Uso de dados do cliente** – Contém as informações corretas sobre o contexto?
3. **Fatos de suporte** – Inclui os mesmos fatos ou passos de resolução?
4. **Ausência de invenções** – Evita criar informações inexistentes?
5. **Estrutura e clareza** – Está bem organizado e compreensível?
6. **Conclusão** – Apresenta fechamento adequado e explicativo?

**Sistema de pontuação:**
- Cada critério pontuado de 0 a 5
- Score geral calculado com base na média ponderada
- Incluir explicações qualitativas para cada critério
- Configurar via scoring function no Llama Stack

**Resultados esperados:**
- **Respostas boas** → score médio entre 4 e 5
- **Respostas medianas ou vagas** → score entre 2,5 e 3,5
- **Respostas ruins ou inventadas** → score < 2,5

**Benefícios:**
- Análise reprodutível, rápida e escalável
- Feedback instantâneo durante a iteração de prompts
- Integração nativa com Llama Stack e outros componentes
- Pode ser integrada com Langfuse e MLflow para rastrear resultados

**Mitigação de vieses:**
- **Position swapping**: Trocar posições de referência e resultado para contrarrestar viés de posição
- **Few-shot prompting**: Adicionar exemplos ao scoring function para calibrar avaliador
- **Awareness**: Estar ciente de que LLMs podem preferir texto gerado por LLM sobre texto humano

**Deliverable:** 
- Scoring function para LLM-as-a-Judge no Llama Stack
- Notebook demonstrando uso do `/scoring` API
- Integração com pipeline de avaliação existente

**Notebook:** Criar `notebooks/04_llm_as_judge_evaluation.ipynb` usando Llama Stack `/scoring` API

**Dependencies:**
- Llama Stack configurado (Phase 2)
- LLM integration (ver Step 5)
- `data/gt_close_notes.csv`

---

### 🎯 Phase 4: LLM-as-a-Judge Evaluation ⭐ **MAIN EVALUATION METHOD**

#### 📋 Step 4: LLM-as-a-Judge Evaluation

**Objetivo:** Usar um modelo de linguagem como avaliador automático para comparar **close notes** (existentes ou geradas por LLM) com **close notes de referência** (ground truth), substituindo (ou complementando) revisões humanas.

**Este é o método de avaliação principal** que será usado para avaliar qualidade de close notes, superando as limitações das métricas n-gram e semânticas (Phase 2 e 3).

**Princípio:** O LLM é instruído a comparar dois textos de close notes: o gerado/avaliado e o de referência (ground truth). Ele analisa o quanto o texto avaliado cobre os mesmos pontos, é claro, completo e não inventa informações.

**Comparação:**
- **Referência**: Close notes de ground truth (`close_notes_ref`)
- **Avaliado**: Close notes existentes (`close_notes` do dataset) ou geradas por LLM

**Nota:** Diferente das Phases 2 e 3, aqui comparamos **close notes vs close notes**, não close notes vs descrições de incidentes.

## 🎯 Objective

Evaluate how well a model-generated *close_note* summarizes and documents the resolution of an IT incident, compared to a *reference (ground truth)* close note.

The goal is to measure:

* **Accuracy** — Are the steps and facts consistent with the reference?
* **Completeness** — Does the note include all essential resolution details?
* **Clarity** — Is the note written in a clear, professional IT support style?

This approach uses an **LLM as a structured evaluator ("judge")** to produce **quantitative (scores)** and **qualitative (explanations)** feedback — replicating the *SumUp* benchmark method, but focused on ITSM workflows.

---

## ⚙️ Step 1 — Define Evaluation Dimensions for ITSM Context

Each generated *close_note* is assessed along **six concrete quality dimensions** relevant to incident and service management documentation:

| Dimension                                | Description                                                                            | Example of "Good" (Score 5)                                                                              |
| ---------------------------------------- | -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| **Incident Coverage**                    | Does the generated note cover the same core problem and context as the reference note? | Mentions the same issue (e.g., "Google Workspace crashing when saving files") and troubleshooting scope. |
| **Technical Steps & Resolution Actions** | Are the main diagnostic or corrective steps included and technically sound?            | Lists actions such as "cleared cache," "reinstalled software," or "updated drivers."                     |
| **Accuracy of Facts**                    | Does it avoid adding or changing facts not present in the reference note?              | No new systems, error codes, or users invented.                                                          |
| **Customer/System Context**              | Does it correctly reference the affected system, user, or service?                     | Correctly identifies the impacted system (e.g., "Epson ET-2760 printer") and user role.                  |
| **Clarity & Structure**                  | Is the note logically structured (problem → action → result)?                          | Uses concise sentences, chronological order, and readable formatting.                                    |
| **Resolution Summary / Conclusion**      | Does it clearly describe the outcome and confirm resolution or escalation?             | Ends with "Issue resolved and verified with user" or equivalent closure statement.                       |

Each dimension is rated from **0 to 5**, where 5 = excellent alignment, 0 = completely incorrect.

---

## 🧩 Step 2 — Judge Prompt Template

The evaluation LLM (judge) must follow a **structured JSON output**, ensuring consistency and automation.
This is the reusable prompt you'll give to the evaluator model:

---

> **System Prompt:**
> You are an expert in IT Service Management and incident documentation.
> Your task is to evaluate how accurately and completely a *generated close note* describes the resolution of an incident, compared to a *reference note*.
>
> Compare the following texts:
>
> * **Reference (ground truth) close note:**
>   {close_notes_ref}
>
> * **Generated close note:**
>   {close_notes_pred}
>
> Evaluate the generated note according to the following criteria.
> For each, assign a **score from 0 to 5** and include a one-sentence explanation.
>
> 1. **Incident coverage (0–5)** — Does it address the same issue and context?
> 2. **Technical steps & resolution actions (0–5)** — Are the main diagnostic and corrective actions consistent and complete?
> 3. **Accuracy of facts (0–5)** — Does it avoid inventing systems, errors, or results?
> 4. **Customer/system context (0–5)** — Does it correctly reference the affected service, device, or user?
> 5. **Clarity & structure (0–5)** — Is it readable, logically ordered, and professionally written?
> 6. **Resolution summary (0–5)** — Does it clearly describe the outcome or confirmation of resolution?
>
> Then compute:
>
> * `"general_score"` — the average of the six scores
> * `"general_score_explanation"` — a brief summary of your overall judgment
>
> Return the evaluation as valid JSON only:
>
> ```json
> {
>   "check_incident_coverage": 5,
>   "check_incident_coverage_explanation": "...",
>   "check_technical_steps": 5,
>   "check_technical_steps_explanation": "...",
>   "check_accuracy_of_facts": 5,
>   "check_accuracy_of_facts_explanation": "...",
>   "check_customer_context": 5,
>   "check_customer_context_explanation": "...",
>   "check_clarity_structure": 4,
>   "check_clarity_structure_explanation": "...",
>   "check_resolution_summary": 5,
>   "check_resolution_summary_explanation": "...",
>   "general_score": 4.83,
>   "general_score_explanation": "The generated close note accurately covers the same incident, includes consistent troubleshooting steps, and provides a clear resolution summary with no invented facts."
> }
> ```
>
> ---
>
> ## 🧮 Step 3 — Scoring Standards
>
> | Score             | Interpretation                                                    | Example                                                             |
> | ----------------- | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
> | **5 (Excellent)** | Fully accurate and complete; aligns perfectly with the reference. | Mentions identical issue, actions, and outcome in a structured way. |
> | **4 (Good)**      | Mostly accurate with minor omissions or paraphrasing.             | Slightly simplified version but conveys same meaning.               |
> | **3 (Adequate)**  | Covers the main idea but misses important details.                | Omits one or two troubleshooting steps.                             |
> | **2 (Weak)**      | Only partially correct; vague or incomplete.                      | Describes the issue but not the fix.                                |
> | **1 (Poor)**      | Misleading or incorrect content.                                  | Introduces wrong system or incorrect result.                        |
> | **0 (Invalid)**   | Completely unrelated or hallucinated.                             | Talks about something entirely different.                           |
>
> ---
>
> ## 🔍 Step 4 — How to Run the Evaluation
>
> 1. **Select dataset:** use the same incident records for which both a *reference* and *generated* close note exist.
> 2. **Send each pair** (`close_notes_ref`, `close_notes_pred`) through the judge prompt.
> 3. **Collect JSON outputs** for all samples.
> 4. **Aggregate scores** across all dimensions and samples:
>
>    * Mean score per dimension;
>    * Mean `general_score`;
>    * Distribution of low scores (to detect weak generations).
>
> This can be done as a batch notebook or automated evaluation job.

**Implementação:**

- Usar LangChain para orquestração de chamadas LLM
- Integrar com Ollama ou outros providers LLM
- Processar avaliações em batch
- Armazenar resultados para análise
- **Estrutura de avaliação:**
  - Para cada close note a avaliar:
    1. Encontrar close note de referência similar (por categoria ou similaridade semântica)
    2. Opcionalmente incluir contexto do incident (`content`) para melhor avaliação
    3. Enviar par (referência, avaliado) para LLM judge
    4. Obter scores estruturados (JSON) com explicações

**Mitigação de Vieses:**
- **Position swapping**: Trocar posições de referência e resultado para contrarrestar viés de posição
- **Few-shot prompting**: Adicionar exemplos ao prompt para calibrar avaliador
- **Context awareness**: Incluir descrição do incident para melhor contexto

**Deliverable:** 
- Notebook `notebooks/05_llm_as_judge_evaluation.ipynb`
- Módulo `src/llm_judge.py` com implementação do judge
- Integração com pipeline de avaliação existente
- Métricas agregadas e visualizações
- Exemplos de boas e ruins gerações com scores correspondentes

**Notebook:** 🔴 Criar `notebooks/05_llm_as_judge_evaluation.ipynb`

**Dependencies:**
- ✅ `data/gt_close_notes.csv` - **COMPLETE**
- ✅ LangChain instalado - **COMPLETE**
- 🔴 LLM integration (Ollama ou outro provider) - **NEEDED**
- 🔴 LLM Client implementation (Phase 6) - **NEEDED**

---

### 🎯 Phase 5: Observability Integration

#### 📋 Step 5: Integração com Langfuse

**Objetivo:** Centralizar os logs de prompts, respostas, métricas e julgamentos dos modelos.

**O que monitorar:**

- Cada chamada de modelo (prompt → resposta)
- Tempo de execução e custo
- Score de avaliação (semântica ou via LLM-as-a-judge)
- Histórico de versões de prompts e modelos
- Comparação entre diferentes configurações

**Como usar na prática:**

1. **Registrar automaticamente cada iteração:**
   - Cada chamada de prompt/modelo
   - Cada resultado de avaliação
   - Métricas de desempenho

2. **Visualizar e comparar outputs:**
   - Painel Langfuse para análise visual
   - Comparação lado a lado de diferentes prompts/modelos
   - Análise de tendências ao longo do tempo

3. **Integrar com MLflow:**
   - Manter coerência entre rastreamento técnico (ML) e observabilidade semântica (LLM)
   - MLflow para métricas técnicas
   - Langfuse para qualidade textual e semântica

**Resultado:** Observabilidade completa do pipeline de IA: técnica (métricas) + semântica (qualidade textual)

**Deliverable:** 
- Módulo `src/langfuse_tracking.py` (similar ao `mlflow_tracking.py`)
- Integração nos notebooks de avaliação
- Instruções de configuração

**Dependencies:**
- Langfuse instalado (comentado em `requirements.txt`)
- LLM integration funcionando

---

### 🎯 Phase 6: LLM Integration

#### 📋 Step 6: Implementar LLM Client

**Objetivo:** Criar módulo para integração com modelos LLM (OpenShift AI, vLLM, ou outros).

**Requisitos:**

- Conectar a endpoints LLM (OpenShift AI, vLLM, ou outros)
- Suportar múltiplos tipos de modelo:
  - Scenario A: Modelo genérico grande (40B+)
  - Scenario B: Modelo menor ajustado (3B-7B)
- Usar LangChain para orquestração
- Tratar chamadas de API, error handling, retries
- Suportar saídas estruturadas (JSON) e não estruturadas
- Configurável via variáveis de ambiente

**Estrutura sugerida:**

```python
class LLMClient:
    def __init__(self, model_name, endpoint_url, api_key=None)
    def enrich_incident(self, prompt: str, temperature: float = 0.7) -> str
    def enrich_incident_structured(self, prompt: str) -> Dict
    def batch_enrich(self, prompts: List[str]) -> List[str]
```

**Deliverable:** `src/llm_client.py` com integração completa

**Dependencies:**
- LangChain (já em `requirements.txt`)
- Configuração de endpoints (ver Step 6)

---

### 🎯 Phase 7: Configuration & Environment

#### 📋 Step 7: Configuração de Ambiente

**Objetivo:** Facilitar configuração e deployment do projeto.

**Arquivos a criar:**

1. **`.env.example`** - Template para variáveis de ambiente:
   ```env
   # LLM Configuration
   LLM_ENDPOINT_URL_SCENARIO_A=https://...
   LLM_ENDPOINT_URL_SCENARIO_B=https://...
   LLM_API_KEY=...
   MODEL_NAME_SCENARIO_A=llama-2-40b
   MODEL_NAME_SCENARIO_B=llama-2-7b-tuned
   
   # MLflow Configuration
   MLFLOW_TRACKING_URI=http://localhost:5000
   
   # Langfuse Configuration
   LANGFUSE_SECRET_KEY=...
   LANGFUSE_PUBLIC_KEY=...
   LANGFUSE_HOST=https://cloud.langfuse.com
   
   # TrustyAI Configuration
   TRUSTYAI_ENDPOINT=...
   ```

2. **`config.py`** - Módulo de configuração centralizado:
   - Carregar variáveis de ambiente
   - Validação de configuração
   - Valores padrão

**Deliverable:** `.env.example` e `src/config.py`

---

### 🎯 Phase 8: TrustyAI Integration

#### 📋 Step 8: Integração com TrustyAI

**Objetivo:** Adicionar análises de fairness, explainability e bias detection usando TrustyAI.

**Funcionalidades:**

- **Fairness metrics** - Analisar diferenças de desempenho entre categorias
- **Explainability** - Explicar por que certos enriquecimentos têm scores mais altos
- **Bias detection** - Verificar diferenças sistemáticas entre grupos
- **Confidence scores** - Medir confiança nas avaliações

**Integração:**
- TrustyAI pode ser usado como parte do pipeline de avaliação
- Integrar análises de fairness e explainability nos processos de avaliação
- Usar resultados do TrustyAI como métricas adicionais

**Deliverable:** 
- Integração TrustyAI com pipeline de avaliação
- Notebook demonstrando uso combinado
- Atualizar `requirements.txt` (descomentar TrustyAI)
- Módulo `src/trustyai_integration.py` (se necessário)

**Dependencies:**
- TrustyAI disponível no ambiente
- Phases 2, 3, e 4 completas
- Configuração de endpoints

---

## 📋 Expected Deliverables (Final)

Ao final da implementação, os participantes terão:

1. ✅ **Dataset com ground truth de close_notes** (`data/gt_close_notes.csv`)
2. ✅ **Análise baseline n-gram** (Phase 2 usando Unitxt) - Validação de hipótese
3. 🟡 **Análise baseline semântica** (Phase 3 usando Unitxt) - Opcional
4. 🔴 **Camada de avaliação automatizada via LLM-as-a-Judge** (Phase 4) ⭐ **MAIN METHOD**
   - Avaliação estruturada com 6 critérios (0-5)
   - Comparação de close notes vs ground truth
   - Scores explicáveis com reasoning
5. 🔴 **Observabilidade e rastreabilidade** com Langfuse e MLflow
6. 🔴 **Capacidade de demonstrar** que um modelo menor e governado (ajustado e avaliado) produz resultados mais confiáveis, explicáveis e consistentes que um LLM genérico

---

## 📊 Implementation Priority

### 🔴 Critical Path (Must Have)
1. ✅ **Complete** - Notebook 01: Data exploration
2. ✅ **Complete** - Step 1: Create Ground Truth dataset
3. ✅ **Complete** - Phase 2: N-gram Baseline Analysis using Unitxt
   - ✅ Created `notebooks/03_ngram_comparisons.ipynb`
   - ✅ Implemented n-gram metrics (ROUGE) using Unitxt
   - ✅ Compare gt_close_notes × incident_descriptions (baseline test)
4. 🟡 **Optional** - Phase 3: Semantic Baseline Analysis using Unitxt
   - 🟡 Create `notebooks/04_semantic_comparisons.ipynb` (optional)
   - 🟡 Implement semantic similarity metrics using Unitxt
   - 🟡 Compare gt_close_notes × incident_descriptions (optional baseline)
5. 🔴 **Next** - Phase 4: LLM-as-a-Judge Evaluation ⭐ **MAIN EVALUATION**
   - 🔴 Create `notebooks/05_llm_as_judge_evaluation.ipynb`
   - 🔴 Implement LLM judge for structured evaluation
   - 🔴 Compare close_notes (existing/LLM-generated) × gt_close_notes
   - 🔴 Implement 6 evaluation criteria with 0-5 scoring
6. 🔴 **Next** - Phase 6: Implement LLM Client (for generating close notes from incidents)

### 🟡 Important (Should Have)
7. 🟡 - Phase 5: Langfuse Integration
8. 🟡 - Phase 8: TrustyAI Integration
9. 🟡 - Phase 7: Environment Configuration

### 🟢 Nice to Have (Optional)
9. 🟢 - Unit tests
10. 🟢 - Integration tests
11. 🟢 - Comprehensive documentation

---

## 🎯 Key Decisions Needed

1. **Evaluation Framework**: ✅ **RESOLVED**
   - ✅ Unitxt selected as evaluation framework
   - ✅ Unitxt installed (`unitxt>=1.0.0`)
   - 🔴 **Next:** Configure Unitxt for n-gram and semantic metrics

2. **LLM Endpoints**: 🔴 **IN PROGRESS**
   - ✅ Ollama configured: `http://localhost:11434` (using llama3.2:3b model)
   - 🔴 **Next:** Determine if we need additional endpoints or can use Ollama for LLM-as-a-Judge
   - Note: Can use different Ollama models for different scenarios

3. **Model Selection**: 
   - For LLM-as-a-Judge: Which model to use as judge?
   - For generating close notes: Which models for Scenario A vs Scenario B?

4. **TrustyAI**: 
   - Is TrustyAI available in the environment?
   - Integration approach with evaluation pipeline?
   - What version and API should be used?

5. **Langfuse**: 
   - Will use cloud version or self-hosted?
   - API keys and configuration?
   - Integration with evaluation results?

---

## 📝 Notes

### Current Approach
- **`content`** = Original incident description (input to LLM)
- **`close_notes`** (in dataset) = Example close notes (can be used as reference)
- **LLM Output** = `close_notes` generated by the model from `content`

### Evaluation Strategy

**Fase de Baseline (Phase 2-3):**
1. **Phase 2: N-gram Comparisons** (ROUGE, BLEU) using Unitxt
   - **Objetivo:** Testar hipótese de que descrições de incidentes e close notes usam linguagem diferente
   - **Comparação:** Ground truth close notes vs incident descriptions
   - **Resultado esperado:** Scores baixos confirmam que n-grams não são adequados

2. **Phase 3: Semantic Comparisons** (embedding similarity) using Unitxt - **OPCIONAL**
   - **Objetivo:** Análise complementar de similaridade semântica
   - **Comparação:** Ground truth close notes vs incident descriptions
   - **Status:** Opcional se Phase 2 já confirmar que métricas tradicionais não são adequadas

**Fase de Avaliação Principal (Phase 4):**
3. **Phase 4: LLM-as-a-Judge** ⭐ **MAIN EVALUATION METHOD**
   - **Objetivo:** Avaliar qualidade de close notes usando critérios semânticos estruturados
   - **Comparação:** Close notes (existentes ou LLM-geradas) vs ground truth close notes
   - **Critérios:** Topic coverage, accuracy, facts, structure, conclusion
   - **Vantagem:** Avalia significado e qualidade, não apenas overlap de palavras
   - **Escalável:** Não requer labeling humano

**Fase de Integração:**
4. **TrustyAI Integration** - Fairness, explainability, bias detection

### Code Quality
- ✅ Good separation of concerns in `src/` modules
- ✅ Comprehensive evaluation framework (`evaluator.py` - será integrado com Unitxt)
- ✅ Well-structured prompt templates
- ⚠️ Missing error handling in some utility functions
- ⚠️ No logging framework (could use Python logging)

### **IMPORTANTE: Mudança de Abordagem**

**Por que usar Unitxt em vez de código customizado:**

1. **Framework Padronizado**: Unitxt fornece framework padronizado para avaliação
2. **Menos Código**: Não precisamos reimplementar funcionalidades já disponíveis
3. **Melhor Integração**: Facilita integração com outros componentes
4. **Manutenibilidade**: Menos código customizado = menos manutenção
5. **Escalabilidade**: Processamento otimizado para grandes volumes
6. **Reprodutibilidade**: Resultados consistentes e comparáveis

**O que manter do código atual:**
- `src/prompts.py` - Templates de prompts ainda são úteis
- `src/utils.py` - Funções utilitárias para preparação de dados
- `src/mlflow_tracking.py` - Tracking continua útil
- `src/evaluator.py` - Pode ser adaptado para usar Unitxt como backend

**O que melhorar/integrar:**
- `src/evaluator.py` - Integrar com Unitxt para métricas padronizadas
- Métricas customizadas - Usar Unitxt com métricas apropriadas
- Pipeline de avaliação - Usar Unitxt para execução padronizada

---

**Document Status:** ✅ Complete  
**Last Review:** December 2024  
**Next Review:** After Phase 1 completion
