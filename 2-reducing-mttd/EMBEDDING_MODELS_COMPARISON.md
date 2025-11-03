# Embedding Models Comparison for IT Incident Close Notes

## 🎯 Use Case Requirements
- **Domain**: IT Service Management (ITSM) / Technical support documentation
- **Task**: Semantic similarity comparison between close notes
- **Text Type**: Technical documentation with IT terminology, troubleshooting steps, resolutions
- **Key Requirements**:
  - High semantic similarity accuracy
  - Understanding of technical terminology
  - Fast inference (for batch processing)
  - Local deployment (open-source, no API costs)

---

## 📊 Recommended Models (Ranked by Performance)

### 🥇 **Top Recommendation: `BGE-base-en-v1.5` or `BGE-small-en-v1.5`**

**Why it's best:**
- ✅ **State-of-the-art performance** on MTEB (Massive Text Embedding Benchmark)
- ✅ **Specifically designed for semantic search** and similarity tasks
- ✅ **Good balance** between accuracy and speed
- ✅ **Small model** (109MB) available for faster inference
- ✅ **Strong performance** on technical/documentation text

**Model Card:**
- **BGE-small-en-v1.5**: `BAAI/bge-small-en-v1.5` - 109MB, 384 dimensions
- **BGE-base-en-v1.5**: `BAAI/bge-base-en-v1.5` - 438MB, 768 dimensions

**Installation:**
```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('BAAI/bge-small-en-v1.5')
# or for better accuracy (larger):
model = SentenceTransformer('BAAI/bge-base-en-v1.5')
```

---

### 🥈 **Alternative: `all-mpnet-base-v2` (Better accuracy than MiniLM)**

**Why consider it:**
- ✅ **Better accuracy** than all-MiniLM-L6-v2 (currently used)
- ✅ **Proven performance** on semantic similarity tasks
- ✅ **Good for technical text** understanding
- ⚠️ **Slower** than MiniLM (2-3x slower inference)

**Model Card:**
- Model: `sentence-transformers/all-mpnet-base-v2`
- Size: ~420MB, 768 dimensions

---

### 🥉 **Current Model: `all-MiniLM-L6-v2` (Speed optimized)**

**Why it's used:**
- ✅ **Very fast** inference (best for large batches)
- ✅ **Lightweight** (80MB)
- ✅ **Good baseline** performance
- ⚠️ **Lower accuracy** than BGE or MPNet models

**Model Card:**
- Model: `sentence-transformers/all-MiniLM-L6-v2`
- Size: ~80MB, 384 dimensions

---

### 🌟 **For Maximum Accuracy: `e5-large-v2` or `NV-Embed-v2`**

**When to use:**
- Highest accuracy requirements
- Computational resources available
- Processing time less critical

**Options:**
- `intfloat/e5-large-v2`: 560MB, 1024 dimensions
- `NV-Embed-v2`: NVIDIA's latest (requires API or specialized setup)

---

## 📈 Performance Comparison

| Model | Size | Dims | Speed | Accuracy | Best For |
|-------|------|------|-------|----------|----------|
| **all-MiniLM-L6-v2** | 80MB | 384 | ⚡⚡⚡ Very Fast | ⭐⭐⭐ Good | Large batches, speed priority |
| **all-mpnet-base-v2** | 420MB | 768 | ⚡⚡ Fast | ⭐⭐⭐⭐ Very Good | Balanced speed/accuracy |
| **BGE-small-en-v1.5** | 109MB | 384 | ⚡⚡⚡ Very Fast | ⭐⭐⭐⭐ Very Good | **RECOMMENDED** - Best balance |
| **BGE-base-en-v1.5** | 438MB | 768 | ⚡⚡ Fast | ⭐⭐⭐⭐⭐ Excellent | High accuracy needs |
| **e5-large-v2** | 560MB | 1024 | ⚡ Slower | ⭐⭐⭐⭐⭐ Excellent | Maximum accuracy |

*Speed ratings are relative to MiniLM. Accuracy based on MTEB benchmarks.*

---

## 💡 Recommendation for This Project

### **Primary Choice: `BGE-small-en-v1.5`**
```python
model = SentenceTransformer('BAAI/bge-small-en-v1.5')
```

**Rationale:**
1. **Better accuracy** than current MiniLM while maintaining fast inference
2. **Optimized for semantic similarity** tasks (our exact use case)
3. **Small footprint** - only slightly larger than MiniLM
4. **Active development** - BAAI models are well-maintained
5. **Excellent MTEB scores** for retrieval and similarity tasks

### **Alternative if accuracy is critical: `BGE-base-en-v1.5`**
For maximum quality when processing time allows.

---

## 🔧 Implementation Suggestion

Update the notebook to support model selection:

```python
# Model selection based on priority
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'BAAI/bge-small-en-v1.5')

MODELS = {
    'fast': 'sentence-transformers/all-MiniLM-L6-v2',        # Current
    'balanced': 'BAAI/bge-small-en-v1.5',                   # Recommended
    'accurate': 'BAAI/bge-base-en-v1.5',                    # Higher accuracy
    'reference': 'sentence-transformers/all-mpnet-base-v2'  # Proven alternative
}

model = SentenceTransformer(MODELS.get('balanced', EMBEDDING_MODEL))
```

---

## 📚 References

- **MTEB Leaderboard**: https://huggingface.co/spaces/mteb/leaderboard
- **BGE Models**: https://huggingface.co/BAAI/bge-small-en-v1.5
- **Sentence Transformers**: https://www.sbert.net/

---

## ⚠️ Migration Note

If switching from `all-MiniLM-L6-v2` to `BGE-small-en-v1.5`:
- Embeddings will be **384 dimensions** (same as MiniLM) ✅
- **Higher semantic similarity** scores expected ✅  
- **Slightly slower** (~10-15% slower) but still very fast ⚠️
- **Need to regenerate** embeddings for consistency ⚠️

