# Module 1: Introduction to Decision Trees with Play Tennis

**Project:** AI Test Drive – Workshop de IA para Operações de TI  
**Goal:** Learn the fundamentals of machine learning through an intuitive decision tree example

---

## 📋 Overview

This module introduces you to **machine learning** and **decision trees** through a fun, relatable example: predicting whether to play tennis based on weather conditions. You'll learn the core concepts that form the foundation for all AI/ML work, including how to prepare data, train a model, and evaluate its performance.

**Target Audience:** IT professionals, business analysts, project managers (not data scientists)  
**Approach:** Educational, step-by-step, with clear explanations of each concept  
**Prerequisites:** Basic Python knowledge, familiarity with pandas (we'll explain as we go)

**Why this matters:**
- Decision trees are intuitive and easy to understand
- The concepts you learn here apply to all machine learning projects
- This foundation is essential for understanding more advanced AI techniques
- The same approach can be used for IT operations problems (classifying incidents, predicting failures, etc.)

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

2. **OpenShift AI or Jupyter Notebook**
   ```bash
   # If using Jupyter locally
   jupyter notebook
   
   # If using OpenShift AI, access through the web interface
   ```

3. **Required Python Packages**
   - `pandas` - Data manipulation
   - `numpy` - Numerical operations
   - `scikit-learn` - Machine learning library
   - `matplotlib` - Visualization (optional, for tree visualization)
   - `pydotplus` - Tree visualization (optional)

### Running the Notebook

Execute the notebook in order:
1. `notebooks/01_introduction_to_decision_trees.ipynb`

**Note:** This is a single-notebook module designed as an introduction. Later modules will have multiple notebooks building on each other.

---

## 📚 Notebook Sequence

### Notebook 01: Introduction to Decision Trees ✅

**What it does:**
- Introduces machine learning concepts through a relatable example
- Loads and explores the Play Tennis dataset
- Prepares data for machine learning (encoding categorical variables)
- Trains a decision tree classifier
- Evaluates model performance using accuracy and other metrics
- Visualizes the decision tree to understand how it makes predictions

**Key Learning Points:**
- What machine learning is and why it matters
- How decision trees work (asking questions to make decisions)
- The importance of data preparation
- How to train and evaluate a model
- How to interpret model results

**Outputs:**
- Trained decision tree model
- Model evaluation metrics (accuracy, confusion matrix, classification report)
- Visualized decision tree

**Time Estimate:** 30-45 minutes

---

## 🔑 Key Concepts

### Machine Learning (ML)

**What it is:** A way for computers to learn patterns from data without being explicitly programmed for every scenario.

**Think of it like:** Teaching a child to recognize cats by showing them many cat pictures, rather than describing every possible cat feature. The child learns the pattern.

**Why it matters:** In IT operations, we can't write rules for every possible incident. ML learns patterns from historical data to help predict and classify new situations.

### Decision Trees

**What it is:** A simple, visual way to make decisions by asking a series of yes/no questions.

**Think of it like:** A flowchart or a game of "20 Questions" - you ask questions that narrow down the possibilities until you reach an answer.

**Example:**
- "Is it sunny?" → Yes → "Is it windy?" → No → "Play tennis!"
- "Is it sunny?" → No → "Is it raining?" → Yes → "Don't play tennis"

**Why it matters:** Decision trees are:
- Easy to understand (you can see exactly how decisions are made)
- Don't require complex math
- Work well with categorical data (like weather conditions)
- Form the basis for more advanced algorithms (Random Forests, Gradient Boosting)

### OpenShift AI

**What it is:** Red Hat's platform for building, training, and deploying AI/ML models in enterprise environments.

**Think of it like:** A complete workshop for AI projects - it provides:
- **Jupyter Notebooks** (like this one) for experimentation
- **Compute resources** for training models
- **Model serving** capabilities for production
- **Integration** with your existing IT infrastructure

**Why we're using it:** OpenShift AI gives you a professional, enterprise-ready environment to learn and experiment with AI, just like you'd use in real IT operations.

### Data Preparation

**What it is:** Converting raw data into a format that machine learning algorithms can understand.

**Think of it like:** Organizing ingredients before cooking - you need everything in the right form and ready to use.

**Why it matters:** ML algorithms work with numbers, not text. We need to convert categories (like "Sunny", "Rainy") into numbers (like 0, 1, 2) so the algorithm can process them.

### Model Training

**What it is:** Teaching the algorithm to recognize patterns by showing it examples.

**Think of it like:** Teaching a student with practice problems - you show them examples, they learn the pattern, then they can solve new problems.

**Why it matters:** The model needs to see examples to learn. The more relevant examples, the better it learns.

### Model Evaluation

**What it is:** Testing how well the model performs on new data it hasn't seen before.

**Think of it like:** Testing a student with new questions they haven't practiced - this shows if they really learned or just memorized.

**Why it matters:** We need to know if the model can make good predictions on new situations, not just repeat what it saw during training.

---

## 📊 Project Structure

```
1-ai-fundamentals/
├── README.md              # This file
├── notebooks/            # Jupyter notebooks
│   └── 01_introduction_to_decision_trees.ipynb
├── data/                 # Datasets
│   └── play_tennis.csv
└── src/                  # Source code modules (for future use)
    └── __init__.py
```

---

## 📈 Current Status

**Completed:**
- ✅ Notebook 01: Introduction to Decision Trees (structure ready, content refactoring in progress)

**In Progress:**
- 🔄 Content refactoring to align with workshop guidelines

---

## 🛠️ Dependencies

**Core Libraries:**
- `pandas>=2.0.0` - Data manipulation and analysis
- `numpy>=1.24.0` - Numerical operations
- `scikit-learn>=1.3.0` - Machine learning algorithms and utilities
- `matplotlib>=3.7.0` - Basic plotting (optional)
- `pydotplus>=2.0.2` - Decision tree visualization (optional)

**Jupyter:**
- `jupyter>=1.0.0` - Notebook environment
- `notebook>=7.0.0` - Jupyter notebook interface

**Installation:**
```bash
pip install pandas numpy scikit-learn matplotlib pydotplus jupyter notebook
```

---

## 💼 How This Applies to IT Operations

The same decision tree approach can be used for:

- **Classifying incidents:** 
  - "Is it a network issue?" → "Is it affecting multiple users?" → "Priority: High"
  
- **Predicting failures:**
  - "Is CPU usage high?" → "Is memory usage high?" → "Risk: Critical"
  
- **Routing tickets:**
  - "Is it a software issue?" → "Is it user-reported?" → "Route to: Support Team A"

- **Risk assessment:**
  - "Is it a production system?" → "Is it during business hours?" → "Risk Level: Medium"

**The pattern is the same:** Ask questions, narrow down possibilities, make a decision based on patterns learned from historical data.

---

## 📝 Notes

- **Educational focus:** This module is designed for learning, not production use
- **Simple example:** The "Play Tennis" dataset is intentionally small and simple to focus on concepts
- **Real-world complexity:** Production ML models use much larger datasets and more sophisticated techniques (covered in later modules)
- **OpenShift AI:** If you're using OpenShift AI, you'll have access to more compute resources and enterprise features

---

## 🎯 Next Steps

After completing this module, you'll be ready for:

- **Module 2:** `2-ai-rag/` - Learn how to use RAG and semantic search to find similar incidents
- **Module 3:** `3-ai-evaluation/` - Learn how to evaluate and improve AI outputs using multiple evaluation methods

**Related Resources:**
- [Scikit-learn Decision Trees Documentation](https://scikit-learn.org/stable/modules/tree.html)
- [OpenShift AI Documentation](https://access.redhat.com/documentation/en-us/red_hat_openshift_ai)
- [Pandas Documentation](https://pandas.pydata.org/docs/)

---

## 🤝 Contributing

When working on this module:
1. Follow the [workshop guidelines](../GUIDELINES.md)
2. Maintain the educational, beginner-friendly approach
3. Keep explanations clear and use analogies
4. Test all code cells end-to-end
5. Update this README if adding new content

---

**Last Updated:** December 2024

