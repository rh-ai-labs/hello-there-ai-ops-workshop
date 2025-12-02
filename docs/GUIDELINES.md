# Workshop Guidelines: Red Hat AI Family Workshop

**Design Philosophy:** Apple Genius Bar Tutorial + IDEO Experience Design

This document defines the standards and guidelines for creating workshop content that feels polished, intuitive, and delightful—like learning at an Apple Genius Bar with IDEO's human-centered design approach.

---

## 🎯 Core Principles

### 1. **Clarity Over Cleverness**
- Every concept should be explainable to a non-technical audience
- Use analogies and real-world examples liberally
- Avoid jargon unless absolutely necessary (and always explain it)

### 2. **Progressive Disclosure**
- Start simple, build complexity gradually
- Each notebook should build on the previous one
- Never assume prior knowledge—always provide context

### 3. **Delightful Discovery**
- Make learning feel like exploration, not instruction
- Use visual elements (emojis, diagrams, charts) to guide attention
- Celebrate small wins and "aha!" moments

### 4. **Empathy First**
- Understand the user's mental model
- Anticipate confusion points and address them proactively
- Provide multiple ways to understand the same concept

### 5. **Consistency is King**
- Follow the same structure across all notebooks
- Use consistent terminology and naming conventions
- Maintain visual consistency (colors, fonts, spacing)

---

## 📁 Repository Structure

### Standard Module Structure

```
{N}-{module-name}/
├── README.md              # Module overview and quick start
├── notebooks/             # All Jupyter notebooks (numbered sequentially)
│   ├── 01_{topic}.ipynb
│   ├── 02_{topic}.ipynb
│   └── ...
├── src/                   # Reusable Python modules
│   ├── __init__.py
│   ├── utils.py          # Utility functions
│   └── {module_specific}.py
├── data/                  # Datasets and generated artifacts
│   ├── raw/              # Original datasets (if applicable)
│   ├── processed/        # Processed/intermediate data
│   └── outputs/          # Final outputs from notebooks
└── assets/               # Images, diagrams, reference materials (optional)
```

### Naming Conventions

**Folders:**
- Format: `{number}-{kebab-case-name}`
- Examples: `1-ai-fundamentals`, `2-ai-rag`, `3-ai-evaluation`, `4-ai-agents`, `5-ai-fine-tuning`
- Numbers indicate sequence/order
- Use descriptive, action-oriented names

**Notebooks:**
- Format: `{number:02d}_{descriptive-name}.ipynb`
- Examples: `01_load_and_explore_dataset.ipynb`, `02_create_ground_truth.ipynb`
- Always zero-pad numbers (01, 02, not 1, 2)
- Use snake_case for file names
- Names should clearly indicate what the notebook does

**Python Modules:**
- Format: `{descriptive_name}.py`
- Use snake_case
- Names should be self-documenting
- Group related functions in the same module

**Data Files:**
- Format: `{descriptive_name}.{ext}`
- Use snake_case
- Include version or date if files are versioned
- Examples: `incidents_prepared.csv`, `reference_close_notes.csv`

---

## 📓 Notebook Structure

### Standard Notebook Template

Every notebook should follow this structure:

```markdown
# Notebook {NN}: {Descriptive Title}

## 🎯 What is This Notebook About?

[2-3 paragraphs explaining the notebook's purpose]
- What we'll do (bullet points)
- Why this matters
- How it connects to previous notebooks

---

## 📚 Key Concepts Explained

### Concept 1: {Name}
**What it is:** [Simple definition]
**Why it matters:** [Relevance to the task]
**Think of it like:** [Analogy or real-world example]

### Concept 2: {Name}
[Same structure]

---

## 🎯 Learning Objectives

By the end of this notebook, you will:
- ✅ Objective 1
- ✅ Objective 2
- ✅ Objective 3

---

## ⚠️ Prerequisites

- [ ] Completed Notebook {NN-1}: {Previous Topic}
- [ ] Have {tool/service} running
- [ ] Installed required packages

---

## 📋 Step-by-Step Guide

### Step 1: {Action Name}

**What we're doing:** [Brief explanation]
**Why:** [Reason for this step]
**What to expect:** [Expected outcome]

[Code cell]

**What happened:** [Explanation of results]
**Key takeaway:** [Important insight]

---

### Step 2: {Action Name}

[Same structure]

---

## 🎓 Key Takeaways

- **Takeaway 1:** [Insight]
- **Takeaway 2:** [Insight]
- **Takeaway 3:** [Insight]

---

## 🔗 Next Steps

- **Next notebook:** `{NN+1}_{next_topic}.ipynb` - {What comes next}
- **Related concepts:** [Links to relevant documentation]

---

## 💡 Additional Resources

- [Resource 1](link)
- [Resource 2](link)
```

### Cell Organization

**Markdown Cells:**
1. **Introduction Cell** - Title, overview, learning objectives
2. **Concept Explanation Cells** - Before introducing new concepts
3. **Section Headers** - Before each major step
4. **Transition Cells** - Between steps, explaining connections
5. **Summary Cells** - Key takeaways, next steps

**Code Cells:**
1. **Import Cell** - All imports at the top
2. **Setup Cell** - Configuration, paths, initial setup
3. **Action Cells** - One logical action per cell
4. **Visualization Cells** - Separate from computation
5. **Cleanup Cells** - Save outputs, finalize results

**Best Practices:**
- Keep code cells focused (one concept per cell)
- Add markdown cells before code cells to explain what's coming
- Add markdown cells after code cells to explain what happened
- Use cell outputs to show results, not just print statements

---

## ✍️ Writing Style Guide

### Tone and Voice

**Use:**
- ✅ Friendly, conversational tone
- ✅ Second person ("you", "we")
- ✅ Active voice ("We'll load the data" not "The data will be loaded")
- ✅ Short, clear sentences
- ✅ Questions to engage the reader ("Why does this matter?")

**Avoid:**
- ❌ Academic or overly formal language
- ❌ Passive voice
- ❌ Long, complex sentences
- ❌ Assumptions about prior knowledge
- ❌ Jargon without explanation

### Language Patterns

**Introductions:**
- "Welcome! This notebook will..."
- "In this notebook, we'll explore..."
- "Think of this like..."

**Explanations:**
- "What this means is..."
- "In simple terms..."
- "Think of it like..."
- "Here's why this matters..."

**Transitions:**
- "Now that we've [done X], let's [do Y]"
- "This connects to what we learned in..."
- "Before we move on, let's understand..."

**Summaries:**
- "What we learned:"
- "Key takeaway:"
- "Remember:"

### Emoji Usage

Use emojis strategically to:
- Guide attention (🎯 for objectives, ⚠️ for warnings)
- Add visual interest (📚 for concepts, 💡 for tips)
- Create visual hierarchy
- Make content scannable

**Standard Emojis:**
- 🎯 Objectives and goals
- 📚 Concepts and explanations
- ⚠️ Warnings and prerequisites
- ✅ Completed tasks or checkpoints
- 🔗 Links and references
- 💡 Tips and insights
- 📊 Data and visualizations
- 🚀 Quick starts
- 🎓 Learning and takeaways
- 🔍 Exploration and investigation

**Guidelines:**
- Use emojis consistently across notebooks
- Don't overuse (1-2 per section max)
- Use them in headers, not body text
- Maintain consistency (same emoji = same meaning)

---

## 🎨 Visual Design Principles

### Typography Hierarchy

1. **H1 (# Title)** - Notebook title
2. **H2 (## Section)** - Major sections
3. **H3 (### Subsection)** - Subsections
4. **H4 (#### Detail)** - Fine details (use sparingly)
5. **Bold** - Key terms, important concepts
6. **Italic** - Emphasis, alternative terms
7. **Code** - Technical terms, function names, file paths

### Code Formatting

**In Markdown:**
- Use backticks for: function names, variables, file paths, commands
- Use code blocks for: multi-line code examples
- Specify language: `python`, `bash`, `json`, etc.

**In Code Cells:**
- Follow PEP 8 style guide
- Add comments explaining "why", not "what"
- Use descriptive variable names
- Group related operations
- Add docstrings to functions

### Visualizations

**Principles:**
- Every chart should have a clear purpose
- Use color meaningfully (not just for decoration)
- Include titles, axis labels, legends
- Make charts readable (appropriate size, clear fonts)
- Use consistent color schemes across notebooks

**Best Practices:**
- Explain what the visualization shows before displaying it
- Explain insights after displaying it
- Use visualizations to tell a story
- Prefer simple, clear charts over complex ones

---

## 📖 Module README Structure

Every module should have a README.md following this structure:

```markdown
# Module {N}: {Module Title}

**Project:** {Project/Workshop Name}  
**Goal:** {One-sentence goal statement}

---

## 📋 Overview

[2-3 paragraphs explaining the module]
- What problem it solves
- What you'll learn
- Why it matters

**Target Audience:** {Who this is for}  
**Approach:** {Educational approach}

---

## 🚀 Quick Start

### Prerequisites

1. **{Requirement 1}**
   ```bash
   {command}
   ```

2. **{Requirement 2}**
   ```bash
   {command}
   ```

### Running the Notebooks

Execute notebooks in order:
1. `01_{topic}.ipynb`
2. `02_{topic}.ipynb`
3. ...

---

## 📚 Notebook Sequence

### Notebook 01: {Title} ✅

**What it does:**
- [Function 1]
- [Function 2]

**Outputs:**
- `{output_file_1}`
- `{output_file_2}`

---

### Notebook 02: {Title} ✅

[Same structure]

---

## 🔑 Key Concepts

### Concept 1: {Name}
[Brief explanation]

### Concept 2: {Name}
[Brief explanation]

---

## 📊 Project Structure

```
{module-name}/
├── notebooks/          # Jupyter notebooks
├── src/               # Source code modules
├── data/              # Datasets
└── README.md          # This file
```

---

## 📈 Current Status

**Completed:**
- ✅ Notebook 01: {Title}
- ✅ Notebook 02: {Title}

**In Progress:**
- 🔴 Notebook 03: {Title}

---

## 🛠️ Dependencies

**Core Libraries:**
- `{library}` - {Purpose}

**AI/ML Libraries:**
- `{library}` - {Purpose}

---

## 📝 Notes

- {Important note 1}
- {Important note 2}

---

## 🎯 Next Steps

1. {Next step 1}
2. {Next step 2}

---

**Last Updated:** {Date}
```

---

## 🔄 Workflow and Process

### Creating a New Module

1. **Plan the Journey**
   - Define learning objectives
   - Break into logical steps (notebooks)
   - Identify prerequisite knowledge
   - Plan the narrative arc

2. **Create Structure**
   - Create module folder: `{N}-{kebab-case-name}/`
   - Create subfolders: `notebooks/`, `src/`, `data/`
   - Create `README.md` with overview

3. **Build Notebooks Sequentially**
   - Start with `01_introduction.ipynb`
   - Build each notebook to completion before moving to next
   - Test each notebook end-to-end
   - Ensure outputs from one notebook feed into the next

4. **Write Documentation**
   - Update module README as you build
   - Document key concepts
   - Add troubleshooting tips

5. **Review and Refine**
   - Read through as a first-time user
   - Check for clarity, consistency
   - Test all code cells
   - Verify all links and references

### Creating a New Notebook

1. **Define Purpose**
   - What will the user learn?
   - What problem does it solve?
   - How does it connect to previous notebooks?

2. **Outline Structure**
   - List key concepts to explain
   - Plan the step-by-step flow
   - Identify where visualizations are needed
   - Plan the narrative arc

3. **Write Content**
   - Start with introduction and concepts
   - Add code cells with explanations
   - Add visualizations with context
   - End with takeaways and next steps

4. **Test and Refine**
   - Run all cells from top to bottom
   - Check outputs make sense
   - Verify explanations match results
   - Ensure smooth flow

---

## ✅ Quality Checklist

Before considering a notebook complete, verify:

### Content Quality
- [ ] Clear learning objectives stated upfront
- [ ] All concepts explained in simple terms
- [ ] Real-world analogies provided
- [ ] Smooth flow from one concept to next
- [ ] Key takeaways summarized at end

### Code Quality
- [ ] All code cells execute without errors
- [ ] Code follows PEP 8 style guide
- [ ] Comments explain "why", not "what"
- [ ] Variable names are descriptive
- [ ] Functions have docstrings

### User Experience
- [ ] Prerequisites clearly stated
- [ ] Expected outputs are explained
- [ ] Error messages are anticipated and addressed
- [ ] Next steps are clear
- [ ] Links and references work

### Visual Design
- [ ] Consistent emoji usage
- [ ] Clear typography hierarchy
- [ ] Visualizations are clear and labeled
- [ ] Consistent formatting throughout
- [ ] Code is properly formatted

### Documentation
- [ ] Module README is complete
- [ ] Notebook is listed in README
- [ ] Key concepts are documented
- [ ] Dependencies are listed
- [ ] Troubleshooting tips included

---

## 🎓 Teaching Philosophy

### The Apple Genius Bar Approach

**1. Start with Empathy**
- Understand where the user is coming from
- Acknowledge their current knowledge level
- Make them feel capable, not overwhelmed

**2. Show, Don't Just Tell**
- Demonstrate concepts with code
- Use visualizations to illustrate points
- Let users see results, not just read about them

**3. Build Confidence Gradually**
- Start with simple, achievable tasks
- Celebrate small wins
- Build complexity step by step

**4. Make It Personal**
- Use "you" and "we" language
- Connect concepts to their work
- Show real-world relevance

### The IDEO Design Approach

**1. Human-Centered**
- Design for the user's needs, not technical perfection
- Anticipate confusion and address it proactively
- Make the experience delightful, not just functional

**2. Iterative Refinement**
- Test with real users
- Refine based on feedback
- Continuously improve clarity

**3. Storytelling**
- Each notebook tells a story
- Build narrative tension (problem → solution)
- Create "aha!" moments

**4. Prototype and Test**
- Build notebooks incrementally
- Test each step
- Refine based on what works

---

## 📚 Reference Examples

### Excellent Notebook Patterns

**Pattern 1: Concept → Example → Practice**
1. Explain concept with analogy
2. Show simple example
3. Let user practice with guided exercise

**Pattern 2: Problem → Investigation → Solution**
1. Present a problem
2. Investigate why it happens
3. Show how to solve it
4. Explain why solution works

**Pattern 3: Simple → Complex → Application**
1. Start with simplest version
2. Add complexity gradually
3. Apply to real-world scenario

### Excellent Explanation Patterns

**The Analogy Pattern:**
"Think of [technical concept] like [familiar thing]. Just as [familiar thing] does [action], [technical concept] does [similar action]."

**The Why Pattern:**
"We do [action] because [reason]. This matters because [impact]."

**The What-Why-How Pattern:**
- **What:** [Definition]
- **Why:** [Relevance]
- **How:** [Mechanism]

---

## 🚫 Common Pitfalls to Avoid

### Content Pitfalls
- ❌ Assuming prior knowledge
- ❌ Skipping explanations because "it's obvious"
- ❌ Using jargon without explanation
- ❌ Making leaps in logic
- ❌ Forgetting to connect concepts

### Code Pitfalls
- ❌ Code without explanation
- ❌ Complex code without breaking it down
- ❌ Not explaining why code works
- ❌ Missing error handling
- ❌ Not showing expected outputs

### UX Pitfalls
- ❌ Unclear prerequisites
- ❌ Missing context for steps
- ❌ No clear next steps
- ❌ Broken links or references
- ❌ Inconsistent formatting

---

## 🔧 Tools and Resources

### Recommended Tools
- **Jupyter Notebook** - Primary development environment
- **JupyterLab** - Enhanced notebook interface
- **nbconvert** - Convert notebooks to other formats
- **nbstripout** - Clean notebook outputs for git
- **pandoc** - Convert markdown to other formats

### Useful Extensions
- **Jupyter Notebook Extensions** - Enhanced functionality
- **Code Formatters** - `black` for Python, `prettier` for markdown
- **Linters** - `flake8` for Python, `markdownlint` for markdown

### Reference Materials
- [Jupyter Notebook Best Practices](https://www.dataquest.io/blog/jupyter-notebook-tips-tricks-shortcuts/)
- [Markdown Guide](https://www.markdownguide.org/)
- [Python Style Guide (PEP 8)](https://pep8.org/)
- [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- [IDEO Design Kit](https://www.designkit.org/)

---

## 📝 Version History

- **v1.0** (2024-12) - Initial guidelines document

---

## 🤝 Contributing

When adding new content:
1. Follow these guidelines
2. Review the quality checklist
3. Test notebooks end-to-end
4. Update relevant README files
5. Get feedback from a first-time user

---

**Remember:** The goal is to create an experience that feels like learning from a patient, knowledgeable teacher who genuinely wants you to succeed. Every detail matters—from the emoji choice to the explanation of a single line of code. Make it delightful. Make it clear. Make it memorable.


