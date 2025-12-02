# Module 5: Predictive Analysis - Fine-tuning for Risk Assessment

**Project:** AI Test Drive – Workshop de IA para Operações de TI  
**Goal:** Demonstrate how to fine-tune a language model to assess changes and estimate the risk of each change generating an incident

---

## 📋 Overview

This module demonstrates how to fine-tune a language model using **LoRA (Low-Rank Adaptation)** for a specific IT operations task: extracting structured fields from incident tickets. The fine-tuned model learns to analyze ticket descriptions and automatically extract key information like category, subcategory, assignment group, and other metadata.

**Target Audience:** IT professionals, business analysts, project managers (not data scientists)  
**Approach:** Educational, step-by-step, with clear explanations of each concept

**Why this matters:**
- **Problem:** Changes in systems (commits, PRs, deploys) can cause incidents. How do we identify high-risk changes before they cause problems?
- **Solution:** A fine-tuned model that learns from historical changes and their outcomes to enrich each new change with risk tags and justifications
- **Impact:** Enables proactive risk assessment and prevents incidents before they occur
- **Real-world application:** This same approach can be used for change risk assessment, incident prediction, and automated ticket classification

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

2. **Hugging Face Account**
   - Create account at https://huggingface.co
   - Login: `huggingface-cli login`
   - Required for downloading models and uploading fine-tuned adapters

3. **GPU (Optional but Recommended)**
   - Fine-tuning is much faster on GPU
   - Works on CPU but will be slower
   - Minimum 8GB GPU memory recommended

4. **Jupyter Notebook**
   ```bash
   jupyter notebook
   ```

### Running the Notebooks

Execute notebooks in order:
1. `notebooks/01_fine_tune_dataset.ipynb` - Prepare dataset for fine-tuning
2. `notebooks/02_upload_fine_tune_model.ipynb` - Fine-tune model using LoRA
3. `notebooks/03_test_fine_tuned_model.ipynb` - Test the fine-tuned model

---

## 📚 Notebook Sequence

### Notebook 01: Prepare Fine-tuning Dataset ✅

**What it does:**
- Loads IT call center ticket dataset
- Prepares data in the format required for fine-tuning (JSONL with messages)
- Creates training examples with structured input/output pairs
- Generates dataset file for fine-tuning

**Key Learning Points:**
- How to structure data for fine-tuning
- Format required by Hugging Face Transformers
- Creating input/output pairs for supervised learning

**Outputs:**
- `finetune_multioutput_small.jsonl` - Training dataset in JSONL format

**Time Estimate:** 15-20 minutes

---

### Notebook 02: Fine-tune Model with LoRA ✅

**What it does:**
- Loads base model (Qwen2.5-3B-Instruct)
- Configures LoRA (Low-Rank Adaptation) for efficient fine-tuning
- Prepares and tokenizes the training dataset
- Trains the model using SFTTrainer
- Saves the LoRA adapter

**Key Learning Points:**
- What LoRA is and why it's efficient
- How to configure fine-tuning parameters
- How to format data for training
- How to monitor training progress

**Outputs:**
- `qwen2.5-lora/` - Directory containing the trained LoRA adapter

**Time Estimate:** 30-60 minutes (depends on GPU availability and dataset size)

---

### Notebook 03: Test Fine-tuned Model ✅

**What it does:**
- Loads the base model and fine-tuned LoRA adapter
- Tests the model with example tickets
- Evaluates extraction quality
- Demonstrates how to use the fine-tuned model for inference

**Key Learning Points:**
- How to load and use a fine-tuned model
- How to format inputs for inference
- How to parse and validate model outputs
- Evaluating model performance

**Outputs:**
- Test results showing model performance
- Examples of structured field extraction

**Time Estimate:** 20-30 minutes

---

## 🔑 Key Concepts

### Fine-tuning

**What it is:** The process of adapting a pre-trained language model to a specific task by training it on task-specific data.

**Think of it like:** Taking a general-purpose assistant who knows many languages and teaching them specialized vocabulary for your specific domain (like IT operations).

**Why it matters:**
- Pre-trained models are general-purpose but may not understand your specific domain
- Fine-tuning adapts the model to your use case
- Much faster and cheaper than training from scratch
- Improves accuracy for domain-specific tasks

### LoRA (Low-Rank Adaptation)

**What it is:** An efficient fine-tuning technique that trains only a small fraction of the model's parameters (typically < 1%) by adding low-rank matrices to attention layers.

**Think of it like:** Instead of retraining the entire model (like rewriting a whole book), LoRA adds small "sticky notes" (adapters) with new information to specific pages.

**Why it matters:**
- **Efficiency:** Uses much less memory and compute
- **Speed:** Trains faster than full fine-tuning
- **Flexibility:** Can train multiple adapters for different tasks
- **Quality:** Maintains model quality while being efficient

**Key Benefits:**
- Reduces memory usage by 3-10x
- Trains 2-5x faster
- Can train on consumer GPUs
- Easy to switch between different fine-tuned versions

### Supervised Fine-Tuning (SFT)

**What it is:** Training a model on labeled examples where you provide both the input and the desired output.

**Think of it like:** Teaching by example - you show the model "when you see this input, produce this output" repeatedly until it learns the pattern.

**Why it matters:**
- Most common fine-tuning approach
- Works well for structured tasks (like field extraction)
- Requires labeled data (input/output pairs)
- Foundation for more advanced techniques

### Structured Output Extraction

**What it is:** Training a model to extract specific fields from unstructured text and return them in a structured format (like JSON).

**Think of it like:** Teaching someone to read a ticket and fill out a form automatically, extracting specific information into labeled fields.

**Why it matters:**
- Converts unstructured text to structured data
- Enables automation of data entry tasks
- Improves consistency and accuracy
- Essential for IT operations automation

**Example:**
- **Input:** "User unable to login to company portal. Tried resetting password multiple times."
- **Output:** `{"category": "SOFTWARE", "subcategory": "ERROR", "assignment_group": "IT SUPPORT", ...}`

### Risk Assessment

**What it is:** Using a fine-tuned model to analyze changes (code, config, infrastructure) and estimate the risk of each change causing an incident.

**Think of it like:** Having an experienced engineer review every change and flag risky ones before deployment.

**Why it matters:**
- Prevents incidents before they occur
- Helps prioritize changes for review
- Provides explainable risk scores
- Enables proactive operations

---

## 📊 Project Structure

```
5-ai-fine-tuning/
├── README.md              # This file
├── notebooks/             # Jupyter notebooks
│   ├── 01_fine_tune_dataset.ipynb
│   ├── 02_upload_fine_tune_model.ipynb
│   └── 03_test_fine_tuned_model.ipynb
├── data/                  # Datasets
│   └── synthetic-it-call-center-tickets.csv
└── src/                   # Source code modules
    └── __init__.py
```

---

## 📈 Current Status

**Completed:**
- ✅ Notebook 01: Prepare Fine-tuning Dataset
- ✅ Notebook 02: Fine-tune Model with LoRA
- ✅ Notebook 03: Test Fine-tuned Model

**In Progress:**
- 🔄 Refactoring notebooks to align with workshop guidelines

---

## 🛠️ Dependencies

**Core Libraries:**
- `pandas>=2.0.0` - Data manipulation
- `numpy>=1.24.0` - Numerical operations
- `jupyter>=1.0.0` - Notebook environment

**AI/ML Libraries:**
- `transformers>=4.35.0` - Hugging Face Transformers (model loading, training)
- `peft>=0.6.0` - Parameter-Efficient Fine-Tuning (LoRA)
- `trl>=0.7.0` - Transformer Reinforcement Learning (SFTTrainer)
- `datasets>=2.14.0` - Hugging Face Datasets
- `torch>=2.0.0` - PyTorch (deep learning framework)
- `accelerate>=0.24.0` - Hugging Face Accelerate (training utilities)

**Optional:**
- `bitsandbytes>=0.41.0` - 8-bit optimizers (for GPU memory efficiency)
- `huggingface-hub>=0.20.0` - Hugging Face Hub integration

**Installation:**
```bash
pip install pandas numpy jupyter transformers peft trl datasets torch accelerate bitsandbytes huggingface-hub
```

**Note:** For GPU support, install PyTorch with CUDA:
```bash
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

---

## 💼 How This Applies to IT Operations

The fine-tuning approach demonstrated here can be used for:

- **Change Risk Assessment:**
  - Analyze code changes, PRs, and deployments
  - Assign risk levels (low, medium, high)
  - Provide justifications for risk scores
  - Flag high-risk changes for review
  
- **Incident Prediction:**
  - Predict which changes are likely to cause incidents
  - Identify patterns in historical failures
  - Prioritize monitoring and testing
  
- **Automated Ticket Classification:**
  - Extract structured fields from ticket descriptions
  - Route tickets to appropriate teams
  - Enrich tickets with metadata automatically
  
- **Root Cause Analysis:**
  - Analyze incident descriptions
  - Extract key information automatically
  - Identify common patterns

**The pattern is the same:** Prepare labeled data → Fine-tune model → Test and evaluate → Deploy for inference

---

## 📝 Notes

- **Dataset:** Uses synthetic IT call center tickets for demonstration
- **Base Model:** Qwen2.5-3B-Instruct (can be replaced with other models)
- **LoRA Configuration:** Uses rank=32, alpha=32 (can be adjusted)
- **Training:** Can be done on CPU but GPU is recommended
- **Educational focus:** This module focuses on concepts and techniques, not production deployment
- **Hugging Face:** Requires Hugging Face account for model access

---

## 🎯 Next Steps

After completing this module, you'll be ready for:

- **Advanced Fine-tuning:** Explore other techniques like QLoRA, full fine-tuning, or RLHF
- **Advanced Fine-tuning:** Explore other techniques like QLoRA, full fine-tuning, or RLHF

**Related Resources:**
- [Hugging Face Transformers Documentation](https://huggingface.co/docs/transformers)
- [PEFT (LoRA) Documentation](https://huggingface.co/docs/peft)
- [TRL Documentation](https://huggingface.co/docs/trl)
- [Fine-tuning Guide](https://huggingface.co/docs/transformers/training)

---

## 🤝 Contributing

When working on this module:
1. Follow the [workshop guidelines](../docs/GUIDELINES.md)
2. Maintain the educational, beginner-friendly approach
3. Keep explanations clear and use analogies
4. Test all code cells end-to-end
5. Update this README if adding new content

---

**Last Updated:** December 2024

