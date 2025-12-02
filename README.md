# AI Test Drive: Workshop de IA para Operações de TI

**Workshop prático sobre aplicação de Inteligência Artificial em operações de TI, com foco em redução de MTTR (Mean Time To Resolve) e MTTD (Mean Time To Detect).**

---

## 🎯 Visão Geral

Este workshop apresenta uma série de exercícios práticos que demonstram como aplicar técnicas de IA para melhorar operações de TI, desde conceitos básicos até implementação de agentes autônomos.

**Público-alvo:** Profissionais de TI, analistas de negócios, gerentes de projeto (não necessariamente cientistas de dados)  
**Abordagem:** Educacional, passo a passo, com explicações claras de cada conceito

---

## 📖 Guidelines for Contributors

This workshop follows design principles inspired by **Apple Genius Bar tutorials** and **IDEO's human-centered design approach**. 

**For contributors creating new modules or notebooks:**
- 📘 **[Complete Guidelines](./GUIDELINES.md)** - Comprehensive standards for structure, writing style, and quality
- 📋 **[Quick Reference](./GUIDELINES_QUICK_REFERENCE.md)** - Cheat sheet for common patterns and checklists

**Key principles:**
- **Clarity over cleverness** - Explain concepts simply, use analogies
- **Progressive disclosure** - Build complexity gradually
- **Delightful discovery** - Make learning feel like exploration
- **Empathy first** - Anticipate confusion, address it proactively
- **Consistency is king** - Follow established patterns

---

## 📚 Módulos do Workshop

### 1. IA 101 na Prática

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

### 2. Avaliação e Geração de Close Notes com IA

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

### 3. Redução de MTTR: Busca por Similaridade entre Incidentes

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

**Notebooks:**
1. **01_simple_rag_llama_stack_chromadb.ipynb** - Construção de um sistema RAG básico
2. **02_multifield_rag_llama_stack_chromadb.ipynb** - RAG aprimorado com indexação multi-campo

**Conceitos-chave:**
- **RAG (Retrieval-Augmented Generation):** Combina recuperação de informações com geração de texto
- **Busca Semântica:** Busca baseada em significado, não apenas palavras-chave
- **Vector Databases:** Bancos de dados que armazenam documentos como vetores para busca rápida
- **Multi-Field RAG:** Combina múltiplos campos de documentos para melhor recuperação

**O que você vai aprender:**
- Conceito de busca por semântica
- Como embeddings melhoram a precisão do RAG
- Técnicas para tornar o RAG mais eficiente
- Como aplicar isso na prática para reduzir MTTR

**Localização:** `3-rag/`

---

### 4. Análise Preditiva: Identificando Mudanças que Geram Incidentes

**Objetivo:** Demonstrar como um modelo pode aprender a avaliar alterações em código, configuração ou infraestrutura e estimar o risco de cada mudança gerar um incidente.

**Problema:** Mudanças em sistemas (commits, PRs, deploys) podem causar incidentes. Como identificar mudanças de alto risco antes que causem problemas?

**Solução:** Modelo que aprende com histórico de mudanças e seus resultados (geraram ou não incidentes) para "enriquecer" cada nova mudança com:
- **Tags de risco:** "baixo", "médio", "alto"
- **Justificativas:** Explicação do nível de risco atribuído

**Notebooks:**
1. **01_fine_tune_dataset.ipynb** - Preparação do dataset para fine-tuning
2. **02_upload_fine_tune_model.ipynb** - Fine-tuning do modelo usando LoRA
3. **03_test_fine_tuned_model.ipynb** - Teste do modelo fine-tuned

**Conceitos introduzidos:**
- **Fine-tuning:** Adaptação de um modelo pré-treinado para uma tarefa específica
- **LoRA (Low-Rank Adaptation):** Técnica eficiente de fine-tuning que treina apenas uma pequena fração dos parâmetros
- **Supervised Fine-Tuning (SFT):** Treinamento supervisionado com exemplos rotulados
- **Structured Output Extraction:** Extração de campos estruturados de texto não estruturado
- **Tagging automático:** LLM analisa mudança e atribui nível de risco
- **LLM-as-a-Judge:** Segundo modelo avalia se a classificação faz sentido

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

**Localização:** `4-predictive-analysis/`

---

### 5. Agentes Autônomos: Integrando Análise + Ação

**Objetivo:** Construir um agente que consiga tomar ações no contexto de operações de TI para remediar o ambiente automaticamente.

**Problema:** Análises e recomendações são úteis, mas ainda requerem ação manual. Como automatizar a remediação?

**Solução:** Agente autônomo que:
- Analisa o estado do ambiente
- Identifica problemas e oportunidades de melhoria
- Toma ações corretivas automaticamente
- Aprende com resultados das ações

**Notebooks:**
1. **01_introduction_to_agents.ipynb** - Introdução aos conceitos de agentes autônomos
2. **02_building_simple_agent.ipynb** - Construção de um agente simples com ferramentas e memória
3. **03_llamastack_core_features.ipynb** - Recursos principais do LlamaStack: Chat e RAG
4. **04_mcp_tools.ipynb** - Protocolo MCP (Model Context Protocol) e criação de ferramentas customizadas
5. **05_safety_shields.ipynb** - Implementação de escudos de segurança e moderação de conteúdo
6. **06_multi_metric_evaluation.ipynb** - Avaliação de agentes usando múltiplas métricas incluindo LLM-as-a-Judge

**Conceitos-chave:**
- **Agentes Autônomos:** Sistemas que podem raciocinar, planejar e agir
- **Ferramentas (Tools):** Funções que agentes podem chamar para interagir com o mundo
- **Memória:** Memória de curto e longo prazo para agentes
- **MCP (Model Context Protocol):** Protocolo padronizado para integração de ferramentas
- **Safety Shields:** Moderação de conteúdo e verificações de segurança
- **Avaliação Multi-métrica:** Avaliação de agentes usando múltiplos critérios

**O que você vai aprender:**
- Conceitos de agentes autônomos
- Como integrar análise com ação
- Framework para construção de agentes
- Técnicas de feedback e aprendizado contínuo
- Como criar ferramentas customizadas usando MCP
- Implementação de segurança e moderação de conteúdo
- Métodos de avaliação de agentes

**Localização:** `5-autonomous-agents/`

---
