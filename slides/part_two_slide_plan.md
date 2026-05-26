# Slide Plan: Part 2 — Getting More From LLMs

**Total slides:** ~16  
**Duration:** ~35 minutes of slides  
**Position:** After interactive session (notebooks 1–3), before fine-tuning demo  
**Format:** Each slide entry is `[Slide N] Title` followed by bullet points of content

> For detailed RAG & Hallucinations slide content, see `slides/rag_and_hallucinations.md`

---

## Section 1: Bridge & Overview (3 mins | ~2 slides)

**[Slide 1] Welcome Back**

- Quick recap of what the notebooks covered:
  - Tokenisation: text → tokens → IDs
  - Embeddings: tokens → meaningful vectors in high-dimensional space
  - Prompt engineering: crafting effective inputs for better outputs
- What's next: making LLMs reliable and specialised for your needs

**[Slide 2] Four Ways to Customise LLM Behaviour**

| Approach           | Complexity  | Changes the Model? |
| ------------------ | ----------- | ------------------ |
| Prompt Engineering | Low         | No                 |
| RAG                | Medium      | No                 |
| MCP Servers        | Medium–High | No                 |
| Fine-tuning        | High        | Yes                |

- You've just practised prompt engineering in Notebook 3
- This session: RAG, hallucinations, and fine-tuning

---

## Section 2: Hallucinations (5 mins | ~3 slides)

**[Slide 3] Hallucinations: A Critical Limitation**

- LLMs predict plausible text — not necessarily true text
- Confident, fluent, and wrong
- Common cases: fake citations, wrong dates, invented facts
- **Never trust LLM outputs blindly for critical tasks**

**[Slide 4] Types of Hallucination**

- **Factual**: model invents a fact not present in training data
- **Intrinsic**: model contradicts information in the provided context
- **Extrinsic**: model introduces information not present in the source
- Higher risk: specific facts, dates, citations, recent events
- Lower risk: creative writing, code syntax, well-known concepts

**[Slide 5] Mitigating Hallucinations**

- Use lower temperature (0.0–0.3) for factual tasks
- Provide context in the prompt: "Based on the following…"
- Ask for expressed uncertainty: "If you're not sure, say so"
- Verify critical information from authoritative sources
- Use retrieval augmentation → this is what RAG solves

---

## Section 3: RAG — Retrieval-Augmented Generation (10 mins | ~6 slides)

**[Slide 6] What is RAG?**

- **Retrieval-Augmented Generation**
- Combines: information retrieval + LLM generation
- Instead of relying on the model's training data memory...
- → Give it fresh, accurate information at query time
- Built directly on the embeddings you explored in Notebook 2

**[Slide 7] How RAG Works**

Without RAG:
- User question → LLM (training data only) → answer (may hallucinate)

With RAG:
1. Convert the question to an embedding
2. Search a vector database for similar document chunks
3. Retrieve the top-k most relevant chunks
4. Combine question + retrieved chunks in the prompt
5. LLM generates an answer grounded in the retrieved context

**[Slide 8] RAG Architecture**

- **Indexing phase** (one-time setup): documents → chunks → embeddings → vector DB
- **Query phase** (per request): question → embed → retrieve → prompt → answer
- _Diagram: two-phase architecture_
- Key point: the similarity search is exactly what Notebook 2 demonstrated

**[Slide 9] RAG Example: Company Knowledge Base**

- Documents in vector DB: employee handbook, IT policies, HR procedures
- User asks: "What's our work-from-home policy?"
- RAG retrieves the 3 most relevant policy chunks
- Prompt: "Answer based only on this context: [chunks]. Question: [user question]"
- LLM answers accurately from actual policy text — no hallucination

**[Slide 10] RAG vs Fine-Tuning**

| Aspect           | RAG                          | Fine-Tuning                  |
| ---------------- | ---------------------------- | ---------------------------- |
| Best for         | Factual Q&A, dynamic data    | Specific tasks, tone, format |
| Data updates     | Just add to vector DB        | Need to retrain              |
| Cost             | Low                          | High                         |
| Accuracy         | High (uses exact sources)    | Depends on training data     |
| Citations        | Easy                         | Hard                         |

- Best practice: often use both together

**[Slide 11] RAG Limitations**

- Retrieval failures: relevant info may not be retrieved if chunking is poor
- Context window limits: can only fit ~5–10 chunks per prompt
- Contradictory sources: retrieved docs may conflict with each other
- "Lost in the middle": LLMs attend more to start and end of context
- Fix: better chunking, hybrid search, metadata filtering, careful prompt structure

---

## Section 4: Fine-Tuning (5 mins | ~3 slides)

**[Slide 12] What is Fine-Tuning?**

- Train the model further on your own labelled data
- Changes the weights → model becomes specialised for your task
- Requires: curated dataset, compute, careful evaluation
- Result: a model that "speaks your domain"

**[Slide 13] LoRA: Parameter-Efficient Fine-Tuning**

- Training all weights is expensive (billions of parameters)
- LoRA: Low-Rank Adaptation — update only ~0.1% of weights
- Adds small trainable matrices alongside frozen model weights
- Near full-model performance at a fraction of the cost
- When to use: specific output format, domain expertise, consistent tone

**[Slide 14] Choosing Your Approach**

- Start with **prompt engineering** — cheapest, fastest, often enough
- Add **RAG** when you need up-to-date or proprietary information
- Use **fine-tuning** when you need consistent behaviour, style, or domain adaptation
- _We'll see fine-tuning in action in the demo now_

---

## Section 5: Wrap-Up (2 mins | ~2 slides)

**[Slide 15] What LLMs Are (and Aren't)**

- ✅ Excellent at: language tasks, summarisation, code, brainstorming
- ❌ Poor at: precise arithmetic, real-time information, guaranteed factual accuracy
- ❌ No persistent memory, no true reasoning (yet)
- ⚠️ Biases from training data propagate to outputs
- ⚠️ Privacy: never send sensitive data to a public API

**[Slide 16] Key Takeaways**

- LLMs predict plausible text — hallucinations are inherent, not a bug
- RAG grounds responses in real documents; it's built on embeddings (Notebook 2!)
- Fine-tuning specialises a model on your data and task
- Prompt engineering, RAG, and fine-tuning are complementary — not competing
- Always verify outputs; be especially careful with facts, dates, and citations

---

## Notes for Presenter

- **Slide 2**: use the overview table to orient attendees — make clear this whole second session flows from it
- **Slides 3–5**: keep brief; the goal is motivation for RAG, not an exhaustive taxonomy of hallucination types
- **Slide 8**: a simple two-phase diagram works well here; see `slides/rag_and_hallucinations.md` for a detailed ASCII version and additional examples
- **Slide 9**: the concrete example lands well — give it a moment, let it sink in
- **Slide 10**: the comparison table is the key decision framework for the audience to take away
- **Slides 12–14**: keep light; the demo follows immediately and will make this concrete
- **Slide 15**: don't skip even if running short — critical for responsible use
