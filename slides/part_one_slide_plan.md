# Slide Plan: Introduction to Large Language Models — Part 1

**Total slides:** ~22  
**Duration:** ~55 mins (10 min welcome + 45 min content)  
**Format:** Each slide entry is `[Slide N] Title` followed by bullet points of content

---

## Preamble: Welcome & Admin (~10 mins | ~5 slides)

**[Slide 1] Title Slide**

- Introduction to Large Language Models
- Coding for Reproducible Research
- Course Leader: Finley Gibson | Course Helper: Conor Crilly
- May 2026
- Collaborative doc: https://tinyurl.com/fd3cd22b
- Course sign-in sheet

**[Slide 2] Session Structure**

- Welcome and hello: 10 mins
- Intro slides: 45 mins
    - What is an LLM? / How did we get here? / Current LLMs
- Break: 10 mins
- Interactive session: 65 mins (3 notebooks)
- Break: 10 mins
- Second slides + fine-tuning demo + Q&A: 35 mins

**[Slide 3] Code of Conduct**

- Welcoming and supportive environment for all, regardless of background or identity
- Show courtesy and respect; be respectful of different viewpoints
- Gracefully accept constructive criticism
- Be patient with technical glitches
- No recording — protects the session and ensures GDPR compliance

**[Slide 4] Programme Funding**

- CfRR is supported by: IDSAI, Research Software Analytics Group, EPSRC RSE Fellowship, Reproducibility Leadership Team, and volunteer academics
- Please attend all sessions you register for and fill in the feedback form at the end

---

## [Slide 5] Part 1: What is an LLM? (~8 mins | ~2 slides)

**[Slide 6] Mentimeter: Discuss with Your Neighbour**

- What is an LLM and what does one do?
- Share your answers at: [Mentimeter link]

**[Slide 7] What is an LLM?**

- By the end of this section you will be able to:
    - Describe what an LLM does at a high level
    - Understand what it can and can't do
    - Know how to get the most out of one
- We'll unpick the components behind this apparent intelligence and understand the mechanism driving it all
- **Answer: An LLM predicts the next token in a sequence**

---

## Part 2: How Did We Get Here? (~15 mins | ~5 slides)

**[Slide 8] Traditional Programming vs Machine Learning**

- Algorithm: a computational set of instructions — Input → Algorithm → Output
- **Traditional approach**: write logic using domain knowledge
- **Machine learning approach**: supply data, apply no domain knowledge, let the machine find the pattern
- If we can express our problem mathematically, we can automate the tuning of parameters from data — without needing to define the rules by hand

**[Slide 9] Neural Networks: Mechanism**

- Nodes connected in layers (diagram)
- Each node: weighted sum of inputs passed through a nonlinear activation
- More parameters = longer equation = more expressive model
- Not just a straight line; not limited to two inputs
- Problem: hard to set exact weight values manually → need data and a training process

**[Slide 10] Problems with Neural Networks → Recurrent Neural Networks**

- **Fixed input size**: works well for images (known size), bad for variable-length text
- **Requires numbers**: text must be converted to a numeric form first
- **Solution — Recurrent Neural Networks (RNNs)**:
    - Process sequences one token at a time; each token gets a number
    - Hidden state carries context forward between steps
    - Natural fit for next-letter / next-word prediction
- **Problem with RNNs**: sequential processing is slow; vanishing gradients mean they lose long-range context

**[Slide 11] The Key Insight: Transformers**

- What if we could look at **all tokens at once?**
- And let each token attend to every other token?
- → **Transformer architecture** (2017: "Attention is All You Need", Vaswani et al.)
- Fully parallelisable → unlocks GPU-scale training on massive datasets

**[Slide 12] Part 2 Summary**

- If we can express our problem mathematically, we can solve it with enough data
- More parameters = more complex model = more data required
- To work with language, we need to express text numerically
- The Transformer solved the key bottlenecks of earlier approaches

---

## Part 3: Current LLMs (~20 mins | ~9 slides)

**[Slide 13] Scale Changed Everything**

- Parallelisation — unlocked by the Transformer — made training on vastly more data feasible
- GPT-1 (2018): 117M parameters
- GPT-2 (2019): 1.5B parameters
- GPT-3 (2020): 175B parameters
- ChatGPT (2022): GPT-3.5 + instruction fine-tuning → mainstream moment
- GPT-4, Claude, Llama, Gemini...
- More data + more parameters + better architecture = emergent capabilities

**[Slide 14] How an LLM Works: Overview**

- Architecture diagram: tokenisation → embeddings → transformer layers + attention → output probabilities
- Forward pass: text in, probability distribution over the next token out
- Within each transformer layer, **attention** allows every token to "look at" every other token — this is how the model understands context and relationships
- Everything is learned jointly to minimise next-token prediction loss
- All the apparent "intelligence" emerges from this one objective

**[Slide 15] Tokenisation**

- Text is split into tokens — not words
    - "unhappiness" → ["un", "happiness"] (2 tokens)
- Vocabulary of ~50,000 tokens (Byte-Pair Encoding algorithm)
- Why not characters? Sequences become too long. Why not words? Too many rare words.
- Token ≈ 0.75 words on average
- We will do some hands-on exploration of this later on.

**[Slide 16] Embeddings**

- Each token ID is mapped to a high-dimensional vector (~768–4096 dimensions)
- Vectors encode meaning: similar words cluster together in embedding space
- Learned during training alongside everything else
- Classic example: King − Man + Woman ≈ Queen
- _You'll visualise these in Notebook 2_

**[Slide 17] Putting It All Together**

- Revisit architecture diagram: tokenisation → embeddings → attention layers → output
- Transformer layers are stacked 12–96 times depending on model size
- Each layer refines the representation
- Early layers: syntax and structure. Later layers: semantics and reasoning.
- At inference: generate one token at a time, appending each to the input (autoregressive)

**[Slide 18] Statelessness**

- LLMs have no memory between calls
- Every API request must include the full conversation history:

```json
[
    { "role": "system", "content": "You are a helpful assistant." },
    { "role": "user", "content": "What is the capital of France?" },
    { "role": "assistant", "content": "The capital of France is Paris." },
    { "role": "user", "content": "What about Germany?" }
]
```

- Each call is independent — the "memory" is just the growing list you pass each time

**[Slide 19] Parameters**

- Parameters are the learned weights of the model — the numbers that encode everything it knows
- GPT-3: 175 billion parameters. Modern models: hundreds of billions to trillions.
- More parameters = more capacity to learn — but also more data, more compute, more cost to run
- You cannot change parameters through prompting — only fine-tuning modifies them

**[Slide 20] Context Window**

- The maximum number of tokens the model can see at once
- GPT-3.5: 4K tokens. GPT-4: 128K tokens. Gemini 1.5: 1M tokens.
- Everything outside the window is **invisible** to the model
- Implication: long conversations eventually drop early context
- Implication: pasting a full paper into a prompt may exceed the limit
- Implication: cost = prompt tokens + response tokens

---

## Part 4: Wrap-Up (~5 mins | ~2 slides)

> ℹ️ Hallucinations, RAG, fine-tuning, and capabilities/limitations are covered in the second presentation — see `slides/part_two_slide_plan.md`.

**[Slide 21] Key Takeaways**

- LLMs are trained on one task: predict the next token
- All apparent intelligence — language, reasoning, knowledge — emerges from this
- They are stateless: memory must be passed explicitly each time
- Context windows are finite: long inputs get cut off
- Prompting, RAG, and fine-tuning let you customise behaviour for your use case

**[Slide 22] What's Coming Next**

- Interactive session — 3 notebooks:
    - Notebook 1: Tokenisation explorer (15 mins)
    - Notebook 2: Embeddings visualisation (25 mins)
    - Notebook 3: Prompt engineering playground (25 mins)
- After break: RAG, hallucinations, fine-tuning slides + demo
- Questions welcome throughout!

---

## Notes for Presenter

- **Slide 6**: Mentimeter link goes here; give 2–3 mins for neighbour discussion before revealing Slide 7
- **Slide 14**: use the TikZ diagram from `diagrams/llm_architecture_nexttoken.pdf`
- **Slides 15–16**: keep technical detail light — the notebooks cover these hands-on; use as teasers
- **Slide 17**: revisit the architecture diagram and walk through it end-to-end now that all components have been introduced
- **Slide 18**: the JSON example is the clearest way to make statelessness concrete — give it a moment to land
- **Slide 22**: make the notebook structure and timings explicit so attendees know what to expect
