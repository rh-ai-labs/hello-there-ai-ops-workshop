# Guidelines Quick Reference

A cheat sheet for creating workshop content. For detailed guidelines, see [GUIDELINES.md](./GUIDELINES.md).

---

## 📁 Folder Structure

```
{N}-{module-name}/
├── README.md
├── notebooks/
│   ├── 01_{topic}.ipynb
│   └── 02_{topic}.ipynb
├── src/
│   ├── __init__.py
│   └── utils.py
└── data/
```

**Naming:**
- Folders: `{number}-{kebab-case}`
- Notebooks: `{NN}_{snake_case}.ipynb` (zero-padded)
- Python: `snake_case.py`
- Data: `snake_case.{ext}`

---

## 📓 Notebook Structure

### Required Sections (in order):

1. **Title & Overview** (`## 🎯 What is This Notebook About?`)
2. **Key Concepts** (`## 📚 Key Concepts Explained`)
3. **Learning Objectives** (`## 🎯 Learning Objectives`)
4. **Prerequisites** (`## ⚠️ Prerequisites`)
5. **Step-by-Step Guide** (`## 📋 Step-by-Step Guide`)
6. **Key Takeaways** (`## 🎓 Key Takeaways`)
7. **Next Steps** (`## 🔗 Next Steps`)

### Cell Organization:

```
[Markdown] Introduction
[Code] Imports
[Markdown] Concept explanation
[Code] Setup
[Markdown] Step header
[Code] Action
[Markdown] Explanation of results
[Markdown] Summary
```

---

## ✍️ Writing Style

### Tone
- ✅ Friendly, conversational
- ✅ Second person ("you", "we")
- ✅ Active voice
- ✅ Short sentences
- ❌ Jargon without explanation
- ❌ Passive voice
- ❌ Assumptions about knowledge

### Language Patterns

**Introducing:**
- "Welcome! This notebook will..."
- "In this notebook, we'll explore..."

**Explaining:**
- "What this means is..."
- "Think of it like..."
- "Here's why this matters..."

**Transitioning:**
- "Now that we've [X], let's [Y]"
- "This connects to what we learned..."

**Summarizing:**
- "What we learned:"
- "Key takeaway:"

---

## 🎨 Visual Elements

### Standard Emojis
- 🎯 Objectives
- 📚 Concepts
- ⚠️ Warnings
- ✅ Completed
- 🔗 Links
- 💡 Tips
- 📊 Data
- 🚀 Quick start
- 🎓 Takeaways
- 🔍 Exploration

### Typography
1. `#` - Notebook title
2. `##` - Major sections
3. `###` - Subsections
4. `**Bold**` - Key terms
5. `` `Code` `` - Technical terms

---

## ✅ Quality Checklist

### Content
- [ ] Learning objectives stated
- [ ] Concepts explained simply
- [ ] Analogies provided
- [ ] Smooth flow
- [ ] Takeaways summarized

### Code
- [ ] All cells execute
- [ ] PEP 8 compliant
- [ ] Comments explain "why"
- [ ] Descriptive names
- [ ] Docstrings present

### UX
- [ ] Prerequisites clear
- [ ] Outputs explained
- [ ] Errors anticipated
- [ ] Next steps clear
- [ ] Links work

### Visual
- [ ] Consistent emojis
- [ ] Clear hierarchy
- [ ] Charts labeled
- [ ] Consistent formatting

---

## 📖 Module README Template

```markdown
# Module {N}: {Title}

**Goal:** {One sentence}

## 📋 Overview
[2-3 paragraphs]

## 🚀 Quick Start
### Prerequisites
[Numbered list]

### Running Notebooks
[Ordered list]

## 📚 Notebook Sequence
### Notebook 01: {Title} ✅
**What it does:**
- [Function]

**Outputs:**
- [File]

## 🔑 Key Concepts
### Concept 1
[Brief explanation]

## 📊 Project Structure
[Tree diagram]

## 📈 Current Status
**Completed:** ✅
**In Progress:** 🔴

## 🛠️ Dependencies
[List with purposes]
```

---

## 🎓 Teaching Patterns

### Pattern 1: Concept → Example → Practice
1. Explain with analogy
2. Show simple example
3. Guided practice

### Pattern 2: Problem → Investigation → Solution
1. Present problem
2. Investigate
3. Solve
4. Explain why

### Pattern 3: Simple → Complex → Application
1. Simplest version
2. Add complexity
3. Real-world application

---

## 🚫 Common Pitfalls

**Content:**
- ❌ Assuming knowledge
- ❌ Skipping explanations
- ❌ Jargon without context
- ❌ Logic leaps

**Code:**
- ❌ Code without explanation
- ❌ Complex without breakdown
- ❌ Missing error handling

**UX:**
- ❌ Unclear prerequisites
- ❌ Missing context
- ❌ No next steps

---

## 💡 Quick Tips

1. **Start with "Why"** - Always explain why before what
2. **Use Analogies** - Connect to familiar concepts
3. **Show, Don't Tell** - Demonstrate with code
4. **Celebrate Wins** - Acknowledge progress
5. **Anticipate Confusion** - Address it proactively
6. **Test as First-Time User** - Read through fresh eyes
7. **Keep It Simple** - One concept per cell
8. **Tell a Story** - Build narrative arc

---

**Remember:** Make it delightful. Make it clear. Make it memorable.

