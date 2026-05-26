# RAG and Hallucinations: Critical Concepts for LLM Applications

**Duration:** 15 minutes  
**Position:** After interactive notebooks, before fine-tuning section

---

## Slide 1: Title Slide
**RAG & Hallucinations**  
**Making LLMs Reliable for Real-World Applications**

---

## Slide 2: The Problem - LLM Hallucinations

### What Are Hallucinations? 🤔

**Definition:** When an LLM generates information that sounds plausible but is factually incorrect or completely made up.

### Real Examples:

❌ **Fake citations**: "According to Smith et al. (2023)..." (paper doesn't exist)  
❌ **Wrong facts**: "The Eiffel Tower was built in 1889 by Gustav Klimt" (wrong architect!)  
❌ **Confident nonsense**: Making up API methods, historical events, or statistics  
❌ **Outdated info**: Knowledge cutoff means recent events are unknown

### Why This Happens:

- LLMs are trained to predict *plausible* text, not necessarily *true* text
- No built-in fact-checking or knowledge base
- Training data contains errors and biases
- Model fills gaps with statistically likely patterns

---

## Slide 3: Types of Hallucinations

### 1. **Factual Hallucinations**
```/dev/null/example.txt#L1-3
Q: "When did Python 3.15 release?"
A: "Python 3.15 was released in October 2023..."
   ❌ Python 3.15 doesn't exist (as of training cutoff)
```

### 2. **Intrinsic Hallucinations**
```/dev/null/example.txt#L1-4
Given context: "The study had 100 participants"
Q: "How many participants?"
A: "There were 250 participants in the study"
   ❌ Contradicts source material
```

### 3. **Extrinsic Hallucinations**
```/dev/null/example.txt#L1-3
Q: "Summarize this document about cats"
A: "The document discusses training techniques for dogs..."
   ❌ Introduces info not in source
```

---

## Slide 4: When Are Hallucinations Most Likely?

### High Risk Scenarios ⚠️

- ✗ Asking about very recent events (after training cutoff)
- ✗ Requesting specific facts/statistics/dates
- ✗ Asking for sources and citations
- ✗ Domain-specific technical questions outside training
- ✗ Long, complex documents where details matter
- ✗ Questions about people, places, or things with similar names

### Lower Risk Scenarios ✓

- ✓ Creative writing and brainstorming
- ✓ Code generation (syntax is deterministic)
- ✓ Explanation of well-known concepts
- ✓ Text transformation (summarization, translation)
- ✓ Pattern recognition tasks

---

## Slide 5: Mitigating Hallucinations - Best Practices

### 🛡️ Strategies:

1. **Use lower temperature** (0.0-0.3) for factual tasks
2. **Provide context** in the prompt (paste relevant info)
3. **Ask for uncertainty**: "If you're not sure, say so"
4. **Verify critical information** from authoritative sources
5. **Use retrieval augmentation** (coming up: RAG!)
6. **Fine-tune on domain-specific data** (later today)
7. **Implement human-in-the-loop** for high-stakes decisions

### Example Prompt Engineering:

❌ **Risky:** "What were the Q3 earnings for TechCorp?"

✅ **Better:** "Based on the following earnings report, what were Q3 earnings: [paste report]"

✅ **Best:** Use RAG to automatically retrieve the report, then ask LLM to extract

---

## Slide 6: Introduction to RAG

### What is RAG? 🔍

**Retrieval-Augmented Generation**

A technique that combines:
1. **Information Retrieval** (finding relevant documents)
2. **LLM Generation** (using those documents to answer)

### The Core Idea:

Instead of relying on the LLM's training data memory...  
→ Give it **fresh, accurate information** to work with!

---

## Slide 7: How RAG Works - The Pipeline

### Traditional LLM (Without RAG):
```/dev/null/traditional.txt#L1-4
User Question 
    ↓
LLM (relies on training data) 
    ↓
Answer (may hallucinate)
```

### RAG Pipeline:
```/dev/null/rag.txt#L1-10
User Question 
    ↓
1. Convert question to embedding
    ↓
2. Search vector database for relevant documents
    ↓
3. Retrieve top-k most similar documents
    ↓
4. Combine question + retrieved docs in prompt
    ↓
5. LLM generates answer grounded in provided context
    ↓
Answer (factually grounded)
```

---

## Slide 8: RAG Architecture Diagram

```/dev/null/diagram.txt#L1-25
┌─────────────────────────────────────────────────────────────┐
│                    INDEXING PHASE (One-time)                 │
└─────────────────────────────────────────────────────────────┘

Documents → Chunk into smaller pieces → Generate embeddings 
    ↓
Store in Vector Database (Pinecone, Weaviate, ChromaDB, etc.)


┌─────────────────────────────────────────────────────────────┐
│                   QUERY PHASE (Each request)                 │
└─────────────────────────────────────────────────────────────┘

User Question 
    ↓
Convert to embedding
    ↓
Similarity search in Vector DB ──→ Retrieve top 3-5 documents
    ↓
Construct prompt:
"Answer based on this context: [retrieved docs]
Question: [user question]"
    ↓
LLM generates grounded answer
    ↓
Return to user (optionally with citations)
```

**Key Point:** The embeddings you explored earlier are the foundation of RAG!

---

## Slide 9: RAG Example - Concrete Walkthrough

### Scenario: Company knowledge base chatbot

**Documents in Vector DB:**
- Employee handbook
- IT policies  
- HR procedures
- Recent announcements

**User Question:** "What's our work-from-home policy?"

**RAG Process:**

1. **Embed question** → [0.23, -0.45, 0.67, ...]

2. **Search vector DB** → Find similar document chunks:
   - "Remote Work Policy (Updated Jan 2024): Employees may work..."
   - "WFH Equipment Reimbursement: Company provides up to $500..."
   - "Hybrid Schedule Options: Teams can choose 2-3 days..."

3. **Construct prompt:**
```/dev/null/prompt.txt#L1-10
Context from company policies:
[Retrieved chunk 1]
[Retrieved chunk 2]
[Retrieved chunk 3]

Question: What's our work-from-home policy?

Please answer based ONLY on the context provided above.
```

4. **LLM responds** with accurate, up-to-date answer from actual policy docs!

---

## Slide 10: RAG vs Fine-Tuning - When to Use What?

| Aspect | RAG | Fine-Tuning |
|--------|-----|-------------|
| **Best for** | Factual Q&A, dynamic knowledge | Specific tasks, tone, format |
| **Data updates** | Just add to vector DB | Need to retrain model |
| **Cost** | Low (storage + retrieval) | High (compute for training) |
| **Speed** | Fast (retrieval + generation) | Fast (just generation) |
| **Accuracy** | High (uses exact sources) | Depends on training data |
| **Citations** | Easy (know which docs used) | Hard (knowledge baked in) |
| **Use case example** | Customer support KB | Code generation style |

**Best Practice:** Often use BOTH together!
- Fine-tune for domain language and format
- RAG for up-to-date facts and specific info

---

## Slide 11: Building a Simple RAG System

### Components You Need:

1. **Document Collection** 
   - PDFs, web pages, databases, etc.

2. **Embedding Model**
   - `sentence-transformers` (open source)
   - OpenAI `text-embedding-3-small`
   - Cohere embeddings

3. **Vector Database**
   - Simple: FAISS (local, free)
   - Production: Pinecone, Weaviate, Qdrant
   - Integrated: LangChain, LlamaIndex

4. **LLM**
   - GPT-4, Claude, Llama, etc.

5. **Orchestration** (optional but recommended)
   - LangChain
   - LlamaIndex
   - Haystack

---

## Slide 12: RAG Code Example (Simplified)

```intro_to_llms/example_rag.py#L1-30
from sentence_transformers import SentenceTransformer
import numpy as np

# 1. Index documents (one-time setup)
model = SentenceTransformer('all-MiniLM-L6-v2')

documents = [
    "Our WFH policy allows 3 days remote per week.",
    "Equipment budget is $500 per employee.",
    "All meetings must be hybrid-friendly with video."
]

doc_embeddings = model.encode(documents)

# 2. Query time
user_question = "Can I work from home?"
question_embedding = model.encode([user_question])

# 3. Find most similar documents
similarities = np.dot(doc_embeddings, question_embedding.T)
top_idx = similarities.argmax()
relevant_doc = documents[top_idx]

# 4. Construct prompt with context
prompt = f"""Answer based on this context:
{relevant_doc}

Question: {user_question}
"""

# 5. Send to LLM (pseudo-code)
answer = llm.generate(prompt)
# "Yes, our policy allows 3 days remote work per week."
```

---

## Slide 13: Advanced RAG Techniques

### Beyond Basic RAG:

1. **Hybrid Search**
   - Combine semantic (embedding) + keyword (BM25) search
   - Best of both worlds

2. **Re-ranking**
   - Retrieve 20 candidates, re-rank to top 3 most relevant
   - Cross-encoder models for better relevance

3. **Recursive Retrieval**
   - Retrieve → Generate → Retrieve again if needed
   - Multi-hop reasoning

4. **Query Expansion**
   - Rephrase question multiple ways
   - Retrieve for each variation

5. **Metadata Filtering**
   - "Only search documents from 2024"
   - "Only search HR department docs"

6. **Citation Tracking**
   - Track which chunks were used
   - Provide sources to users

---

## Slide 14: RAG Limitations & Challenges

### ⚠️ Watch Out For:

1. **Retrieval Failures**
   - Relevant info exists but isn't retrieved
   - Fix: Better chunking, hybrid search

2. **Context Window Limits**
   - Can only fit ~5-10 document chunks
   - Fix: Better filtering, summarization

3. **Contradictory Information**
   - Retrieved docs conflict with each other
   - Fix: Timestamp filtering, source ranking

4. **Computation Cost**
   - Every query requires embedding + search
   - Fix: Caching, efficient vector DB

5. **"Lost in the Middle" Problem**
   - LLMs focus on start/end of context, ignore middle
   - Fix: Put most relevant docs first and last

---

## Slide 15: RAG + Hallucinations - Summary

### 🎯 Key Takeaways:

**Hallucinations:**
✅ LLMs will make things up - it's inherent to how they work  
✅ Higher risk for facts, dates, citations, recent events  
✅ Lower temperature + verification helps  
✅ Never trust LLM outputs blindly for critical applications  

**RAG:**
✅ Grounds LLM responses in real documents  
✅ Enables up-to-date, accurate information retrieval  
✅ Built on embeddings (which you just learned!)  
✅ Production standard for Q&A and knowledge systems  
✅ Complements fine-tuning (not a replacement)  

**Together:**
→ RAG is the #1 technique to reduce hallucinations in production systems  
→ You now have the building blocks: embeddings (notebook 2) + LLMs  

---

## Slide 16: Try It Yourself - Next Steps

### 🚀 Resources to Explore:

**Tutorials:**
- LangChain RAG tutorial (free)
- LlamaIndex quickstart guide
- DeepLearning.AI: "LangChain for LLM Application Development"

**Tools:**
- ChromaDB (simplest vector DB for prototyping)
- FAISS (Facebook AI Similarity Search)
- Pinecone (managed vector DB)

**Projects:**
- Build a chatbot for your research papers
- Create a personal knowledge base from PDFs
- Company documentation search system

### Demo After Break:
We'll see RAG concepts in action during the fine-tuning section!

---

## Questions?

**Discussion Points:**
- Have you encountered hallucinations in LLMs you've used?
- What use cases can you think of for RAG in your research/work?
- When would fine-tuning be better than RAG?

---

**Next:** [15-minute break, then fine-tuning slides + demo]
