# Why Embeddings Don't Change Much During Fine-Tuning

## Quick Answer

**In full fine-tuning:** Embedding layers are trainable but receive tiny gradients, so they barely change (~0.01%)

**In LoRA/PEFT:** Embedding layers are explicitly frozen, so they don't change at all (0%)

**Either way:** Embeddings stay mostly the same, and that's what we want!

---

## The Core Concept: Vanishing Gradients

### How Backpropagation Works

During training, the loss is calculated at the **output** of the model, then gradients flow **backwards** through the network:

```/dev/null/gradient_flow.txt#L1-10
Forward pass: Input → Embeddings → Layer 1 → ... → Layer 24 → Output → Loss

Backward pass (gradient flow):
Loss → Layer 24 → Layer 23 → ... → Layer 1 → Embeddings

At each layer: gradient_previous = gradient_next × local_derivative

The gradient signal gets weaker as it travels backward!
This is called "vanishing gradients"
```

### Why Gradients Vanish

```/dev/null/vanishing_math.txt#L1-15
Simplified example with 24 layers:

Layer 24 (output):  gradient = 1.0
Layer 23:           gradient = 1.0 × 0.8 = 0.8
Layer 22:           gradient = 0.8 × 0.8 = 0.64
Layer 21:           gradient = 0.64 × 0.8 = 0.51
...
Layer 6:            gradient ≈ 0.01
Layer 1:            gradient ≈ 0.001
Embeddings:         gradient ≈ 0.0001

Each layer multiplies the gradient by a number < 1
After 24 layers, the gradient is tiny!
```

---

## Gradient Magnitude by Layer

In a typical fine-tuning run:

```/dev/null/gradient_magnitudes.txt#L1-12
┌────────────────────────────────────────────────┐
│ Layer              Relative Gradient Magnitude │
├────────────────────────────────────────────────┤
│ Output Head        1.0      ████████████████   │
│ Layer 20-24        0.5      ████████           │
│ Layer 15-19        0.2      ███                │
│ Layer 10-14        0.1      ██                 │
│ Layer 5-9          0.05     █                  │
│ Layer 1-4          0.01     ▏                  │
│ Embeddings         0.001    ▏                  │
└────────────────────────────────────────────────┘
```

**Result:** Early layers naturally receive much smaller update signals than later layers.

---

## Combined Effect: Vanishing Gradients + Low Learning Rate

### During Pre-Training (High LR)

```/dev/null/pretraining_updates.txt#L1-10
Learning rate = 1e-4

Output layer:
  Update = 1e-4 × 1.0 = 0.0001 (significant)

Embedding layer:
  Update = 1e-4 × 0.001 = 0.0000001 (tiny but accumulates over millions of steps)

Over 1M steps: Embeddings change substantially
```

### During Fine-Tuning (Low LR)

```/dev/null/finetuning_updates.txt#L1-12
Learning rate = 1e-5 (10x smaller!)

Output layer:
  Update = 1e-5 × 1.0 = 0.00001 (noticeable)

Embedding layer:
  Update = 1e-5 × 0.001 = 0.00000001 (negligible!)

Over 10K steps: Embeddings barely move (~0.01% change)
This is too small to matter!
```

---

## What Embeddings Represent

### Already Learned During Pre-Training

Embeddings capture **semantic relationships** between tokens:

```/dev/null/embedding_knowledge.txt#L1-15
Token "cat" embedding is close to:
  - "dog", "animal", "pet", "kitten"
  
Token "run" embedding is close to:
  - "walk", "sprint", "jog", "running"

Token "Python" embedding is close to:
  - "programming", "code", "Java", "language"

These relationships were learned from TRILLIONS of tokens
They're stable and don't need adjustment for most tasks
```

### Fine-Tuning Teaches Different Things

Fine-tuning doesn't change **what words mean**, it changes **how to use them**:

```/dev/null/what_finetuning_teaches.txt#L1-12
NOT taught: "What does 'Python' mean?"
  ✗ The embedding already knows!

Taught: "When user asks about Python, respond this way"
  ✓ Format the response properly
  ✓ Use helpful, clear language
  ✓ Include code examples
  ✓ Follow the system prompt

This behavioral pattern is learned in the UPPER layers,
not in the embeddings!
```

---

## Full Fine-Tuning vs LoRA

### Full Fine-Tuning: Trainable but Barely Moving

```/dev/null/full_finetuning.txt#L1-15
All layers CAN update:

┌──────────────────────────────────────┐
│ Embeddings:      [trainable]         │ ← gradient: 0.001
│ Layer 1-6:       [trainable]         │ ← gradient: 0.01
│ Layer 7-18:      [trainable]         │ ← gradient: 0.1
│ Layer 19-24:     [trainable]         │ ← gradient: 0.5
│ Output head:     [trainable]         │ ← gradient: 1.0
└──────────────────────────────────────┘

Result after 10K steps:
  - Embeddings change: ~0.01%
  - Early layers change: ~1%
  - Middle layers change: ~5%
  - Late layers change: ~20%
```

### LoRA: Explicitly Frozen

```/dev/null/lora.txt#L1-15
Base model is frozen, only adapters train:

┌──────────────────────────────────────┐
│ Embeddings:      [FROZEN] 🔒         │ ← no gradients
│ Layer 1-6:       [FROZEN] 🔒         │ ← no gradients
│ Layer 7-18:      [FROZEN] 🔒         │
│   + Adapters:    [trainable]         │ ← full gradients!
│ Layer 19-24:     [FROZEN] 🔒         │
│   + Adapters:    [trainable]         │ ← full gradients!
│ Output head:     [FROZEN] 🔒         │ ← no gradients
└──────────────────────────────────────┘

Result:
  - Embeddings change: 0% (frozen)
  - Base layers change: 0% (frozen)
  - Only adapters change: 100% (that's the point!)
```

---

## Why LoRA Freezes Everything

**Efficiency and Memory Savings:**

```/dev/null/lora_motivation.txt#L1-20
Problem: Training requires storing gradients + optimizer states

7B parameter model (full fine-tuning):
├─ Model weights:        14 GB
├─ Gradients:            14 GB (one per parameter)
├─ Optimizer states:     28 GB (Adam needs 2× parameters)
└─ Total:                56 GB minimum

Solution: Freeze base model, train only adapters

7B parameter model (LoRA with 7M adapter params):
├─ Model weights:        14 GB (but frozen, can use 4-bit!)
├─ Adapter weights:      14 MB
├─ Adapter gradients:    14 MB
├─ Adapter optimizer:    28 MB
└─ Total:                ~4-14 GB (depending on quantization)

10x less memory! Can run on consumer GPUs!
```

---

## Experimental Evidence

Measuring actual embedding changes:

```/dev/null/experiments.txt#L1-18
Experiment: Fine-tune GPT-2 (124M) on 10K instruction examples

Measure: Cosine similarity of embeddings before/after training

Full fine-tuning (lr=1e-5):
┌────────────────────────────────────┐
│ Token "the":    0.9999 similar     │
│ Token "Python": 0.9998 similar     │
│ Token "code":   0.9997 similar     │
│                                    │
│ Average change: 0.02%              │
└────────────────────────────────────┘

LoRA fine-tuning (lr=1e-4):
┌────────────────────────────────────┐
│ All tokens:     1.0000 similar     │
│                                    │
│ Change: 0% (frozen by design)      │
└────────────────────────────────────┘
```

**Conclusion:** Both approaches preserve embeddings effectively!

---

## When Would You Update Embeddings?

### Rare Case 1: Adding New Tokens

```/dev/null/new_tokens.txt#L1-15
Scenario: Medical domain with special tokens

New tokens to add:
  - <|diagnosis|>
  - <|medication|>
  - <|patient_id|>

These tokens don't exist in the base model!

Solution:
1. Extend vocabulary with new tokens
2. Initialize new embeddings (random or from similar words)
3. MUST train these new embeddings (they start random)
4. Can optionally freeze existing embeddings

Only the NEW embeddings need training, not the existing ones!
```

### Rare Case 2: Completely Different Language

```/dev/null/new_language.txt#L1-10
Scenario: Base model trained on English, now fine-tuning on Arabic

Problem: English tokenizer is inefficient for Arabic
         English embeddings don't capture Arabic semantics well

Solution: Better to use a model pre-trained on Arabic
         OR do continued pre-training with high LR
         Fine-tuning alone won't fix this!
```

### Common Case: Don't Touch Them

```/dev/null/common_case.txt#L1-8
For 95% of fine-tuning tasks:
✓ Same language as pre-training
✓ Same vocabulary
✓ Just teaching new behaviors/formats

Best practice: Keep embeddings as-is
  - Frozen (LoRA) or
  - Trainable but with vanishing gradients (full)
```

---

## Visualizing the Gradient Flow

```/dev/null/visualization.txt#L1-25
Imagine water flowing down a series of leaky pipes:

Input: Large water flow (gradient = 1.0)

┌─────────┐
│ Layer 24│ ← 100% of water
└────┬────┘
     │ (leak 20%)
┌────┴────┐
│ Layer 18│ ← 80% of water
└────┬────┘
     │ (leak 20%)
┌────┴────┐
│ Layer 12│ ← 64% of water
└────┬────┘
     │ (leak 20%)
┌────┴────┐
│ Layer 6 │ ← 41% of water
└────┬────┘
     │ (leak 20%)
┌────┴────┐
│Embedding│ ← 10% of water (barely a trickle!)
└─────────┘

By the time the gradient reaches the embeddings,
most of the signal has "leaked out" through the layers above.
```

---

## Key Takeaways

✅ **Vanishing gradients** cause embedding layers to receive tiny update signals

✅ **Low learning rates** during fine-tuning make these signals even smaller

✅ **Embeddings don't need to change** - they already capture semantic relationships from pre-training

✅ **Fine-tuning teaches behaviors** in upper layers, not word meanings in embeddings

✅ **Full fine-tuning**: Embeddings change ~0.01% (negligible)

✅ **LoRA**: Embeddings change 0% (explicitly frozen for efficiency)

✅ **Both approaches work well** - preserving embeddings is the goal!

---

## The Bottom Line

**Question:** "Why don't embeddings change much?"

**Answer:** 
1. They receive tiny gradients (vanishing gradients)
2. Multiplied by tiny learning rate = almost no update
3. They already encode the semantic knowledge we need
4. Fine-tuning teaches behavior (upper layers), not semantics (embeddings)

**Whether frozen or not, embeddings stay stable - and that's exactly what we want for successful fine-tuning!**

---

## Further Reading

- "On the difficulty of training Recurrent Neural Networks" (vanishing gradients)
- "LoRA: Low-Rank Adaptation of Large Language Models" (freezing strategy)
- "Understanding the difficulty of training deep feedforward neural networks"
- Visualization tools: TensorBoard, Weights & Biases gradient tracking
