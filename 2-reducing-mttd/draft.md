1 - Deploying LLM on OpenShift AI
2 - Introduces vLLM
3 - Access the LLM
4 - Discuss Prompt Platform Engineering (langfuse, mlflow)
5 - Multiple Prompts
6 - Evaluate and score
(BLEU, ROUGE)
-----


Perfeito — o **Cenário 2 (“Enriquecer as informações sobre um incidente para reduzir o MTTD”)** já tem uma boa estrutura, mas dá para deixá-lo mais completo e didático, com passos claros, objetivos técnicos e de negócio.
Aqui vai uma proposta detalhada:

---





-----
To evaluate the quality of LLM responses in your project, consider these concise methods:

Ground Truth Comparison: Create a reference dataset from verified medical sources. Use semantic similarity metrics (e.g., cosine similarity with Sentence Transformers) to score precision and novelty.

Specificity and Relevance: Score responses based on specificity (e.g., "IV saline" vs. "drink water") and direct relevance to symptoms using rule-based keywords or a fine-tuned model.

Medical Model Scoring: Use fine-tuned LLMs (e.g., PubMed GPT) to evaluate correctness and actionability with prompts like: "Rate the specificity of this treatment on a scale of 1-10."

Diversity and Uniqueness: Apply clustering or TF-IDF to flag repetitive, generalized responses and prioritize unique, actionable insights.

Precision and Recall: Create high-precision rules for penalizing broad results while maintaining recall for less common but valid recommendations.

Human Evaluation: Engage medical experts to label responses and refine automated scoring.

Tools: Sentence Transformers, BERT, PubMedBERT, clustering (e.g., k-Means), metrics like BLEU and F1.

Scoring Framework:

Specificity (40%)

Accuracy (30%)

Relevance (20%)

Uniqueness (10%)

1. Define “precise”
Specific: Refers to a distinct medical condition or treatment.

Evidence-based: Matches guidelines or literature.

Actionable: Gives clear next steps, not vague advice.

2. Scoring Methods
Embedding-based novelty: Compare outputs to a corpus of common/general advice using cosine similarity; low similarity = more unique.

LLM-as-judge: Use a second LLM to rate each symptom-action pair (1–5) for specificity and precision.

Reference-based: Curate a small set of expert-verified symptom → root cause/treatment examples to benchmark outputs.

3. Hybrid Approach
Combine embeddings, LLM ratings, and reference comparisons to produce a final score.

Filter outputs below a threshold to remove platitudes.

Generation metrics	
Retrieval metrics

 

Faithfulness

How factually accurate the generated answer is

 

Context precision

The signal to noise ratio of retrieved context

 

Answer relevancy

How relevant is the generated answer to the question

 

Context recall

Can it retrieve all relevant information required to answer the question

This is the core distinction between LLM product evals and benchmarks. Benchmarks are like school exams — they measure general skills. LLM product evals are more like job performance reviews. They check if the system excels in the specific task it was "hired" for, and that depends on the job and tools you’re working with.

LLM Product Evaluation	LLM Model Evaluation
Focus	Ensuring accurate, safe outputs for a specific task.	Comparing capabilities of different LLMs.
Scope	Testing the LLM-powered system (with prompt chains, guardrails, integrations, etc).	Testing the LLM itself through direct prompts.
Evaluation data	Custom, scenario-based datasets.	General benchmark datasets.
Evaluation scenario	Iterative testing from development to production.	Periodic checks with new model releases.
Example task	Assessing a support chatbot’s accuracy.	Choosing the best LLM for math problems.

Here’s a quick breakdown of common matching methods:

Method	Description	Example
Exact Match	Check if the response exactly matches the expected output (True/False).	Confirm a certain text is correctly classified as “spam”.
Word or Item Match	Check if the response includes specific words or items, regardless of full phrasing (True/False).	Verify that “Paris” appears in answers about France’s capital.
JSON match	Match key-value pairs in structured JSON outputs, ignoring order (True/False).	Verify that all ingredients extracted from a recipe match a known list.
Semantic Similarity	Measure similarity using embeddings to compare meanings. (E.g., cosine similarity).	Match “reject” and “decline” as similar responses.
N-gram overlap	Measure overlap between generated and reference text (E.g. BLEU, ROUGE, METEOR scores).	Compare word sequence overlap between two sets of translations or summaries.
LLM-as-a-judge	Prompt an LLM to evaluate correctness (Returns label or score).	Check that the response maintains a certain style and level of detail.

If you’re using LLMs for predictive tasks, which is often a component of larger LLM solutions, you can use classic ML quality metrics.

Task	Example metrics	Example use case
Classification	Accuracy, precision, recall, F1-score.	Spam detection: recall helps quantify whether all spam cases are caught.
Ranking	NDCG, Precision at K, Hit Rate, etc.	Retrieval in RAG: Hit Rate checks if at least one relevant result is retrieved for the query.

Without ground truth
Open-ended LLM evals
Reference-free evaluations: directly score the responses by chosen criteria.
However, obtaining ground truth answers isn’t always practical. For complex, open-ended tasks or multi-turn chats, it’s hard to define a single “right” response. And in production, there are no perfect references: you’re evaluating outputs as they come in. 

Instead of comparing outputs to a fixed answer, you can run reference-free LLM evaluations. They assess specific qualities of the output, like structure, tone, or meaning. 

One popular LLM evaluation method is using LLM-as-a-judge, where you use a language model to grade outputs based on a set rubric. For instance, an LLM judge might evaluate whether a chatbot response fully answers the question or whether the output maintains a consistent tone.

But it’s not the only option. Here’s a quick overview:

Method	Description	Example
LLM-as-a-Judge	Use an LLM with an evaluation prompt to assess custom properties.	Check if the response fully answers the question fully and does not contradict retrieved context.
ML models	Use specialized ML models to score input/output texts.	Verify that text is non-toxic and has a neutral or positive sentiment.
Semantic similarity	Measure text similarity using embeddings.	Track how similar the response is to the question as a proxy for relevance.
Regular expressions	Check for specific words, phrases, or patterns.	Monitor for mentions of competitor names or banned terms.
Format match	Validate structured formats like JSON, SQL, and XML.	Confirm the output is valid JSON and includes all required keys.
Text statistics	Measure properties like word count or symbols.	Ensure all generated summaries are single sentences.
These reference-free LLM evaluations can work both during iterative development (like when you refine outputs for tone or format) and for monitoring production performance.

While you don’t need to design and label a ground truth dataset in this case, you still need to put in some upfront work. This time, your focus is on:

curating a diverse set of test inputs and
fine-tuning the evaluators.
‍It takes some thought to narrow down and express assessment criteria. Once you set those, you may need to work on evaluators like LLM judges to align with your expectations.




[HANDS-ON-2] “Enriquecer as informações sobre um incidente para reduzir o MTTD (Mean Time To Detect).”
Exercício prático em que vamos demonstrar dois cenários. 
CENÁRIO_A → um LLM (40b, ou mais) é solicitado a enriquecer as informações de um incidente. Nesse cenário, o LLM é vago em alguns campos e também comete erros no seu relatório.
CENÁRIO_B → um LLM (3b ~ 7b) passou por um processo de ajuste (eval, guardrails, benchmarking, fairness, etc…) e demonstra um resultado preciso.

Como melhorar o cenário de uma IA que enriquece as informações sobre um incidente?
Definir um padrão que deve ser seguido pelo LLM para enriquecer as informações;
Avaliar e comparar os resultados entre cenários A e B;
Como medir os resultados dessa IA?
https://medium.com/inside-sumup/evaluating-the-performance-of-an-llm-application-that-generates-free-text-narratives-in-the-context-c402a0136518
Usando o modelo correto para isso
Ground Truth, LLM-as-judge, lm-eval, truty-ai, RHLF, RLAIF
https://www.reddit.com/r/deeplearning/comments/1hg76q9/methods_to_evaluate_quality_of_llm_response/
https://www.thoughtworks.com/en-br/insights/blog/generative-ai/how-to-evaluate-an-LLM-system
https://www.evidentlyai.com/llm-guide/llm-evaluation
Llama-Stack & TrustyAI
https://rh-aiservices-bu.github.io/llama-stack-tutorial/modules/advanced-04-eval.html 

