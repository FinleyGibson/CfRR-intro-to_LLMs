# Slide Plan

## To Cover

### Hook

- What is an LLM?
    - What does it do?

### Origins of LLMs

- Machine learning
    - What problem are we trying to solve?
- Neural Networks
    - What is the structure
        - Structure overview
        - Setting of weights
        - Generalisation
    - What is the training process actually doing?
        - Loss function
            - Mathematical definition of how well it has done
        - Differentiation
            - Loss function must be differentiable
    - Why is this hard?
        - Need a lot of data
        - Need labelled data
        - Expensive
- Recurrent Neural Networks
    - Next word/letter prediction

### Current LLMs

- Main changes
    - Architecture changes
        - Transformer architecture
        - Allowed greater parallelisation
    - Massive data/complexity increase
        - ChatGPT
- Important components
    - Tokenization
    - Embeddings
    - Attention
- Training Process
    - Next-token prediction
        - Autoregressive generation
    - Some Loss function
- Prompts
    - System prompt - Instructions given to the model before the conversation begins, used to set its behaviour, tone, or persona (e.g. "You are a helpful assistant that only answers questions about cooking")
    - User prompt - The message the user sends to the model
- Context Window
    - The maximum amount of text (measured in tokens) the model can "see" at once
    - Everything outside this window is invisible to the model - it has no memory beyond it
- Conversation History
    - LLMs have no built-in memory between turns - each response is generated from scratch
    - LLMs are "stateless"
    - The illusion of memory is created by passing the full conversation history back to the model with every new message, within the context window

#### What can we do to build

### Getting More Out of an LLM

| Approach           | Complexity  | Changes the model? |
| ------------------ | ----------- | ------------------ |
| Prompt Engineering | Low         | No                 |
| RAG                | Medium      | No                 |
| MCP Servers        | Medium-High | No                 |
| Fine-tuning        | High        | Yes                |

Stateless
`     [
      { "role": "system",    "content": "You are a helpful assistant." },
      { "role": "user",      "content": "What is the capital of France?" },
      { "role": "assistant", "content": "The capital of France is Paris." },
      { "role": "user",      "content": "What about Germany?" }
    ]
    `

    ## Points of Clarity

### Tokenization

- Turns text into something an LLM can process efficiently.

### Embeddings

- Trained during the LLM training
- Context based embeddings

### Attention

- Allows the model to move information, encoded in one embedding into another,

### Context Window

### System vs User Prompt
