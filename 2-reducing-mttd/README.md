# 🧠 AI Test Drive – Cenário 2: Enriquecendo Incidentes com IA

## 🎯 Objetivo

Este exercício prático demonstra **como aplicar modelos de IA (LLMs)** para **enriquecer informações de incidentes** em sistemas de ITSM (ex: ServiceNow) e **reduzir o Mean Time To Detect (MTTD)**.
A proposta é **simples, interativa e lúdica**, permitindo explorar **diferentes prompts, modelos e pipelines de avaliação** com as ferramentas da **plataforma Red Hat**.

---

## 🧩 O que você vai aprender

* Como **preparar e explorar um dataset de incidentes** simulados.
* Como **usar LLMs para completar informações faltantes** em registros.
* Como **testar e comparar prompts e modelos** dentro do OpenShift AI.
* Como **avaliar resultados com métricas de qualidade** usando **TrustyAI** e **MLflow**.
* Como **estruturar um pipeline de experimentos reprodutível e rastreável**.

---

## 🧱 Estrutura do Repositório

```
ai-testdrive-scenario2/
├── README.md
├── data/
│   ├── incidents_raw.csv
│   ├── incidents_enriched_groundtruth.csv
│   └── prompts/
├── notebooks/
│   ├── 01_load_and_explore_dataset.ipynb
│   ├── 02_prompt_experiments.ipynb
│   ├── 03_llm_eval_with_trustyai.ipynb
│   ├── 04_mlflow_tracking.ipynb
│   └── 05_summary_and_results.ipynb
├── src/
│   ├── utils.py
│   ├── prompts.py
│   ├── evaluator.py
│   └── mlflow_tracking.py
└── requirements.txt
```

---

## 🧪 Fluxo de Execução

1. **Explorar o dataset** de incidentes incompletos.
2. **Aplicar diferentes prompts** para gerar versões enriquecidas via LLM.
3. **Comparar e avaliar** as respostas com base em precisão, clareza e consistência.
4. **Rastrear os resultados** com MLflow e TrustyAI.
5. **Discutir insights e boas práticas** de IA corporativa.

---

## 📚 Dataset – Synthetic IT Call Center Tickets

**Fonte:**
[🔗 Hugging Face – KameronB/synthetic-it-callcenter-tickets](https://huggingface.co/datasets/KameronB/synthetic-it-callcenter-tickets)

Este dataset contém **tickets sintéticos de um call center de TI**, simulando incidentes e requisições em sistemas corporativos (como ServiceNow).
Ele é ideal para demonstrar tarefas de **classificação, enriquecimento e correlação de incidentes** usando modelos de linguagem.

---

### 🧾 Estrutura dos Dados

Cada registro representa um ticket (incidente ou requisição).
Abaixo estão as colunas principais — úteis para os exercícios de enriquecimento e análise de similaridade:

| Coluna                        | Tipo       | Descrição                                                              |
| ----------------------------- | ---------- | ---------------------------------------------------------------------- |
| `number`                      | `string`   | Identificador único do ticket (ex: INC0048604, TASK0049212).           |
| `date`                        | `datetime` | Data/hora de abertura do chamado.                                      |
| `contact_type`                | `string`   | Canal de contato (Chat, Email, Phone, Portal).                         |
| `short_description`           | `string`   | Resumo breve do problema ou solicitação.                               |
| `content`                     | `string`   | Texto completo da descrição do ticket — usado como input do LLM.       |
| `category`                    | `string`   | Categoria principal (SOFTWARE, HARDWARE, NETWORK, etc.).               |
| `subcategory`                 | `string`   | Subcategoria mais específica (INSTALLATION, ERROR, PERFORMANCE, etc.). |
| `customer`                    | `string`   | Nome do solicitante (sintético).                                       |
| `resolved_at`                 | `datetime` | Data/hora de resolução.                                                |
| `close_notes`                 | `string`   | Texto do fechamento do ticket (usado como “resposta verdadeira”).      |
| `agent`                       | `string`   | Nome do atendente responsável (sintético).                             |
| `reassigned_count`            | `int`      | Número de reatribuições entre equipes.                                 |
| `resolution_time`             | `float`    | Tempo total de resolução (em minutos).                                 |
| `issue/request`               | `string`   | Tipo de demanda (Incident / Request).                                  |
| `software/system`             | `string`   | Sistema ou aplicação afetada.                                          |
| `assignment_group`            | `string`   | Grupo responsável pelo atendimento.                                    |
| `info_score_close_notes`      | `float`    | Indicador da qualidade informacional das notas de fechamento.          |
| `info_score_poor_close_notes` | `float`    | Indicador da falta de informações úteis.                               |

> 💡 **Dica:** as colunas `content` e `close_notes` são as mais importantes para o cenário de *enriquecimento de incidentes*, pois representam o antes/depois da atuação do LLM.

---

### 🧩 Exemplo de Registro

| Campo                 | Valor                                                                                                                                 |
| --------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| **number**            | `INC0048604`                                                                                                                          |
| **date**              | `3/27/2021 10:09`                                                                                                                     |
| **contact_type**      | `Email`                                                                                                                               |
| **short_description** | `ZTrend crashes unexpectedly when saving files`                                                                                       |
| **content**           | `User reports ZTrend crashes unexpectedly when attempting to save files. Performed initial diagnostics...`                            |
| **category**          | `SOFTWARE`                                                                                                                            |
| **subcategory**       | `ERROR`                                                                                                                               |
| **close_notes**       | `Performed diagnostics and identified corrupted config files. Cleared cache, reinstalled app, and restored defaults. Issue resolved.` |
| **agent**             | `Watson, Samuel`                                                                                                                      |
| **resolution_time**   | `876.01` minutes                                                                                                                      |

---

### ⚙️ Como carregar o dataset no notebook

```python
from datasets import load_dataset

dataset = load_dataset("KameronB/synthetic-it-callcenter-tickets")
df = dataset["train"].to_pandas()

df.head()
```

Para reduzir a carga durante o teste, você pode usar uma amostra pequena:

```python
df = df.sample(200, random_state=42)
```

Perfeito 👌 — o **Langfuse** é parte essencial do stack moderno de observabilidade e rastreabilidade de LLMs, então ele deve aparecer junto das demais ferramentas de monitoramento e experimentação.
Aqui está a versão atualizada da seção “⚙️ Ferramentas Envolvidas”, já com **Langfuse** incluído e descrito de forma alinhada com as demais tecnologias da Red Hat AI stack:

---

## ⚙️ Ferramentas Envolvidas

* 🧠 **OpenShift AI** – ambiente unificado para desenvolvimento, execução e gestão de notebooks, modelos e pipelines de IA, com escalabilidade e segurança corporativa.
* 🧩 **TrustyAI** – conjunto de ferramentas para **avaliação de qualidade, fairness, explicabilidade e confiabilidade** de modelos de IA, integrável com o ecossistema Red Hat.
* 📈 **MLflow** – plataforma para **rastreamento e comparação de experimentos**, versionamento de modelos e monitoramento de métricas de performance durante o ciclo de vida da IA.
* 🧾 **Langfuse** – ferramenta de **observabilidade e tracing de LLMs**, utilizada para:

  * registrar e visualizar prompts, respostas e tempos de execução;
  * comparar desempenho entre diferentes versões de prompts e modelos;
  * integrar métricas de qualidade (ex.: *factual consistency*, *latência*, *custo*) com o pipeline de MLflow;
  * gerar dashboards de uso e impacto das aplicações baseadas em IA.
* 📦 **LangChain / Hugging Face** – bibliotecas para **integração, orquestração e execução de modelos de linguagem (LLMs)** e manipulação de datasets públicos, incluindo o *Synthetic IT Call Center Tickets*.

---

## 💡 Valor Demonstrado

Este exercício mostra, de forma prática, como **um modelo pequeno e governado** pode superar um **LLM genérico** em precisão e custo — destacando a **força do ecossistema Red Hat AI** em **controle, auditabilidade e eficiência**.

