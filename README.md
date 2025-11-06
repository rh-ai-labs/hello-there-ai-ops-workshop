# AI Test Drive: Workshop de IA para Operações de TI

**Workshop prático sobre aplicação de Inteligência Artificial em operações de TI, com foco em redução de MTTR (Mean Time To Resolve) e MTTD (Mean Time To Detect).**

---

## 🎯 Visão Geral

Este workshop apresenta uma série de exercícios práticos que demonstram como aplicar técnicas de IA para melhorar operações de TI, desde conceitos básicos até implementação de agentes autônomos.

**Público-alvo:** Profissionais de TI, analistas de negócios, gerentes de projeto (não necessariamente cientistas de dados)  
**Abordagem:** Educacional, passo a passo, com explicações claras de cada conceito

---

## 📚 Módulos do Workshop

### [HANDS-ON-1] IA 101 na Prática

**Objetivo:** Introdução aos conceitos fundamentais de IA e ferramentas básicas.

**Conteúdo:**
- Explicação do **OpenShift AI** e sua importância no ecossistema de IA empresarial
- Introdução ao **Jupyter Notebook** como ferramenta de desenvolvimento e experimentação
- Primeiro contato prático com notebooks através do exemplo clássico: **"Vai jogar tênis ou não?"** usando Decision Tree

**O que você vai aprender:**
- Como funciona o ambiente OpenShift AI
- Como criar e executar notebooks Jupyter
- Conceitos básicos de Machine Learning através de um exemplo prático e intuitivo

---

### [Módulo 2] Redução de MTTD: Avaliação e Geração de Close Notes com IA

**Objetivo:** Avaliar e gerar close notes (notas de encerramento) de alta qualidade para incidentes de TI usando diferentes métodos de avaliação com IA.

**Problema:** Close notes mal escritas dificultam a resolução futura de incidentes similares, aumentando o MTTD (Mean Time To Detect).

**Solução:** Workflow educativo que ensina a avaliar qualidade de close notes usando métodos progressivos:
1. Métricas simples (n-gram) como baseline
2. Similaridade semântica usando embeddings
3. Avaliação estruturada com LLM-as-a-Judge

**Notebooks:**
1. **01_load_and_explore_dataset.ipynb** - Carrega e explora dataset de incidentes
2. **02_create_ground_truth.ipynb** - Define e separa exemplos bons vs ruins
3. **03_ngram_comparisons.ipynb** - Testa se métricas simples funcionam
4. **04_semantics_analysis.ipynb** - Avalia similaridade semântica usando embeddings
5. **05_llm_as_judge_evaluation.ipynb** - Avaliação estruturada com múltiplos critérios usando LLM
6. **06_llm_generation_evaluation.ipynb** - Geração e avaliação de close notes (TODO)

**Conceitos-chave:**
- **Ground Truth:** Definição de qualidade para close notes
- **N-gram Metrics:** Métricas de sobreposição de palavras (baseline)
- **Semantic Similarity:** Comparação de significado usando embeddings
- **LLM-as-a-Judge:** Avaliação estruturada com critérios múltiplos

**Localização:** `2-reducing-mttd/`

---

### [Módulo 3] Redução de MTTR: Busca por Similaridade entre Incidentes

**Objetivo:** Demonstrar como identificar incidentes similares usando busca semântica para reduzir o MTTR (Mean Time To Resolve).

**Problema:** Dado um conjunto de incidentes históricos, queremos identificar incidentes similares ao atual para:
- Sugerir resoluções anteriores
- Identificar padrões recorrentes de falha
- Reduzir o tempo de resolução (MTTR)

**Cenários:**

**CENÁRIO_A:** Utilizar um LLM e RAG genéricos
- ❌ RAG não retorna informações com precisão
- ❌ Resultados vagos e inconsistentes

**CENÁRIO_B:** Utilizar modelo + embeddings + técnicas efetivas de RAG
- ✅ Busca por semântica usando embeddings
- ✅ RAG mais preciso e eficiente
- ✅ Resultados relevantes e acionáveis

**O que você vai aprender:**
- Conceito de busca por semântica
- Como embeddings melhoram a precisão do RAG
- Técnicas para tornar o RAG mais eficiente
- Como aplicar isso na prática para reduzir MTTR

---

### [Módulo 4] Análise Preditiva: Identificando Mudanças que Geram Incidentes

**Objetivo:** Demonstrar como um modelo pode aprender a avaliar alterações em código, configuração ou infraestrutura e estimar o risco de cada mudança gerar um incidente.

**Problema:** Mudanças em sistemas (commits, PRs, deploys) podem causar incidentes. Como identificar mudanças de alto risco antes que causem problemas?

**Solução:** Modelo que aprende com histórico de mudanças e seus resultados (geraram ou não incidentes) para "enriquecer" cada nova mudança com:
- **Tags de risco:** "baixo", "médio", "alto"
- **Justificativas:** Explicação do nível de risco atribuído

**Conceitos introduzidos:**
- **Tagging automático:** LLM analisa mudança e atribui nível de risco
- **LLM-as-a-Judge:** Segundo modelo avalia se a classificação faz sentido
- **Fine-tuning supervisionado:** Modelo pequeno (3B-7B) ajustado com dataset de mudanças e incidentes
- **CPT + SFT:** Continual Pre-Training + Supervised Fine-Tuning (processo da Meta)
- **RHLF / RLAIF:** Reinforcement Learning from Human/AI Feedback

**Cenários:**

**CENÁRIO_A:** LLM genérico sem contexto adicional
- ❌ Tagging vago ou inconsistente
- ❌ Classificação ruim de níveis de risco
- ❌ Explicações pouco claras

**CENÁRIO_B:** LLM com exemplos rotulados + LLM-as-a-Judge
- ✅ Respostas mais consistentes e justificadas
- ✅ Aproxima-se do processo CPT + SFT
- ✅ Melhor precisão e explicabilidade

**CENÁRIO_C:** Modelo fine-tuned com histórico real
- ✅ Resultados mais precisos e coerentes
- ✅ Prioriza mudanças realmente críticas
- ✅ Reduz ruído e falsos positivos

**O que você vai aprender:**
- Como aplicar análise preditiva para prevenir incidentes
- Técnicas de fine-tuning para modelos de linguagem
- Processo de LLM-as-a-Judge para validação
- Simulação de processos de IA assistida para RCA (Root Cause Analysis)

---

### [Módulo 5] Agentes Autônomos: Integrando Análise + Ação

**Objetivo:** Construir um agente que consiga tomar ações no contexto de operações de TI para remediar o ambiente automaticamente.

**Problema:** Análises e recomendações são úteis, mas ainda requerem ação manual. Como automatizar a remediação?

**Solução:** Agente autônomo que:
- Analisa o estado do ambiente
- Identifica problemas e oportunidades de melhoria
- Toma ações corretivas automaticamente
- Aprende com resultados das ações

**O que você vai aprender:**
- Conceitos de agentes autônomos
- Como integrar análise com ação
- Framework para construção de agentes
- Técnicas de feedback e aprendizado contínuo

---

## 🚀 Quick Start

### Pré-requisitos

1. **Python Environment**
   ```bash
   # Usando uv (recomendado)
   uv sync
   
   # Ou usando pip
   pip install -r requirements.txt
   ```

2. **Ollama (para LLM-as-a-Judge)**
   ```bash
   # Instalar Ollama: https://ollama.ai
   # Iniciar servidor
   ollama serve
   
   # Baixar modelo
   ollama pull llama3.2:3b
   ```

3. **Jupyter Notebook**
   ```bash
   jupyter notebook
   ```

### Estrutura do Repositório

```
hello-there-ai-ops-workshop/
├── 2-reducing-mttd/          # Módulo 2: Redução de MTTD
│   ├── notebooks/            # Notebooks do módulo
│   ├── data/                  # Datasets gerados
│   ├── src/                   # Código fonte
│   └── README.md              # Documentação do módulo
├── docs/                      # Documentação geral
├── scripts/                   # Scripts auxiliares
├── pyproject.toml            # Dependências do projeto
└── README.md                  # Este arquivo
```

---

## 🛠️ Tecnologias Utilizadas

**Core:**
- Python 3.11+
- Jupyter Notebooks
- Pandas, NumPy
- Matplotlib, Seaborn

**IA/ML:**
- **Unitxt** - Framework de avaliação (n-gram metrics, LLM-as-a-Judge)
- **Sentence Transformers** - Modelos de embeddings
- **Ollama** - Servidor local de LLM
- **OpenShift AI** - Plataforma de IA empresarial

**Avaliação:**
- ROUGE (via Unitxt)
- BLEU (via Unitxt)
- Métricas customizadas

---

## 📊 Status dos Módulos

| Módulo | Status | Descrição |
|--------|--------|-----------|
| HANDS-ON-1 | ✅ | IA 101 na Prática |
| Módulo 2 | ✅ | Redução de MTTD - Avaliação de Close Notes |
| Módulo 3 | 🔴 | Redução de MTTR - Busca por Similaridade |
| Módulo 4 | 🔴 | Análise Preditiva - Risco de Mudanças |
| Módulo 5 | 🔴 | Agentes Autônomos - Análise + Ação |

**Legenda:**
- ✅ Completo
- 🟡 Em progresso
- 🔴 Planejado

---

## 🎓 Conceitos-Chave do Workshop

### Métricas de Operações de TI
- **MTTR (Mean Time To Resolve):** Tempo médio para resolver um incidente
- **MTTD (Mean Time To Detect):** Tempo médio para detectar um incidente

### Técnicas de IA
- **Embeddings:** Representações matemáticas de texto que capturam significado
- **RAG (Retrieval-Augmented Generation):** Técnica que combina busca e geração
- **LLM-as-a-Judge:** Uso de LLM para avaliação estruturada
- **Fine-tuning:** Ajuste de modelos pré-treinados para tarefas específicas
- **Agentes Autônomos:** Sistemas que tomam decisões e ações automaticamente

### Métodos de Avaliação
- **N-gram Metrics:** Métricas de sobreposição de palavras (ROUGE, BLEU)
- **Semantic Similarity:** Comparação de significado usando embeddings
- **Structured Evaluation:** Avaliação com múltiplos critérios usando LLM

---

## 📝 Notas Importantes

- **Cache folders** (`inference_engine_cache/`) são ignorados pelo git (ver `.gitignore`)
- **Arquivos de dados** em `data/` são gerados pelos notebooks
- **Foco educacional:** Todos os notebooks incluem explicações para público não técnico
- **Execução local:** Os exercícios podem ser executados localmente usando Ollama

---

## 🔗 Links Úteis

- [OpenShift AI Documentation](https://docs.redhat.com/en/openshift-ai)
- [Ollama](https://ollama.ai)
- [Unitxt Documentation](https://unitxt.ai)
- [Jupyter Notebooks](https://jupyter.org)

---

## 📧 Contato e Suporte

Para dúvidas ou sugestões sobre o workshop, consulte a documentação de cada módulo ou entre em contato com a equipe do projeto.

---

**Última Atualização:** Dezembro 2024

