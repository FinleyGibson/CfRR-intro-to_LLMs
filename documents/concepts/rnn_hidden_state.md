# RNN Hidden State

The **hidden state** in an RNN is a **vector of numbers** (typically floating-point values) that serves as the "memory" of the network.

## Key Points

### 1. Shape

- It's a 1D vector, typically of size 128, 256, 512, etc.
- Example: if `hidden_size = 256`, then h₇ = [0.23, -0.45, 0.12, ..., 0.67] (256 numbers)

### 2. What it represents

- An **encoded summary** of everything the RNN has seen so far
- Not a copy of previous inputs, but a learned compressed representation
- The numbers don't directly correspond to specific words/characters—they're learned features

### 3. How it updates

At each time step:

```
h_new = tanh(W_h · h_old + W_x · x_current + b)
```

- Takes the previous hidden state (`h_old`)
- Combines it with the current input (`x_current`)  
- Passes through a non-linear activation (tanh)
- Produces a new hidden state (`h_new`)

Where:
- `W_h` is the weight matrix for the hidden state
- `W_x` is the weight matrix for the input
- `b` is a bias vector
- `·` represents matrix multiplication

### 4. Key property

- Same size at every time step (e.g., always 256 dimensions)
- Gets **overwritten/updated** at each step (doesn't grow)
- Information from early time steps can fade or be transformed as more inputs are processed

## Example

After processing "To be, or not to be", h₁₂ is a vector like `[0.12, -0.89, 0.45, ...]` that somehow encodes information about all those characters in a compressed form that helps predict what comes next.

## Visual Representation

In our diagrams:

- **Orange boxes** (h₇, h₈, h₉, etc.) represent these hidden state vectors
- **Orange arrows** show the flow of the hidden state from one time step to the next
- Each hidden state "remembers" context from all previous characters

## Why it matters

The hidden state is what allows RNNs to:
- Process sequences of any length
- Maintain context over time
- Make predictions based on history (not just the current input)

However, vanilla RNNs struggle with **long-term dependencies** because information in the hidden state can get "washed out" after many time steps. This is why variants like LSTMs and GRUs were developed—they have more sophisticated mechanisms for maintaining long-term memory.
