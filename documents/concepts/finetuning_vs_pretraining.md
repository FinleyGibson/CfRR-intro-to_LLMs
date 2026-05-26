# Fine-Tuning vs Pre-Training: Understanding the Differences

## Overview

Fine-tuning and pre-training both use the same fundamental algorithm (gradient descent with backpropagation), but they differ dramatically in how that algorithm is applied. Understanding these differences is crucial for working effectively with LLMs.

---

## TL;DR - Key Differences

| Aspect | Pre-training | Fine-tuning |
|--------|-------------|-------------|
| **Learning rate** | 1e-4 (high) | 1e-5 to 1e-6 (10-100x lower!) |
| **Duration** | Weeks to months | Hours to days |
| **Data volume** | Trillions of tokens | Millions to billions |
| **Data type** | Raw text (unlabeled) | Curated instruction-response pairs |
| **Cost** | $1M - $100M | $100 - $100K |
| **Hardware** | 1000s of GPUs | 1-10 GPUs |
| **Epochs** | 1 (one pass through data) | 1-5 |
| **Overfitting risk** | Low | High |
| **Goal** | Learn language | Learn specific behavior/task |

**The Big Picture:** Pre-training teaches the model *language*. Fine-tuning teaches it how to *use* that language for specific tasks.

---

## 1. Learning Rate (MUCH Lower for Fine-Tuning)

### Pre-training:
- **Learning rate:** ~1e-4 to 1e-3 (relatively high)
- **Why:** Starting from random weights, need significant updates to learn patterns

### Fine-tuning:
- **Learning rate:** ~1e-5 to 1e-6 (10-100x smaller!)
- **Why:** Model already understands language; just needs gentle adjustments
- **Critical:** Learning rates are **cranked DOWN, not up!**

```/dev/null/learning_rates.txt#L1-8
Pre-training: lr = 0.0001  ←  Big steps
Fine-tuning:  lr = 0.00001 ←  Tiny, careful steps

Analogy:
Pre-training = Sculpting a statue from a block of marble
Fine-tuning   = Polishing and adding fine details

Using high LR during fine-tuning → Catastrophic forgetting!
```

### What is Catastrophic Forgetting?

When you use too high a learning rate during fine-tuning:
- Model "forgets" general knowledge from pre-training
- Only remembers the narrow fine-tuning examples
- Loses capabilities on tasks outside the fine-tuning set

```/dev/null/forgetting.txt#L1-8
Example:
Pre-trained model: Can write code, answer questions, translate, etc.

After aggressive fine-tuning on customer support data:
✓ Great at customer support responses
✗ Forgets how to write code
✗ Forgets general knowledge
✗ Only knows customer support patterns
```

**Solution:** Use low learning rates to make gentle updates that preserve existing knowledge while adding new capabilities.

---

## 2. Training Duration (MUCH Shorter for Fine-Tuning)

### Pre-training:
- **Duration:** Weeks to months of continuous training
- **Tokens seen:** Trillions (GPT-3: ~300B, GPT-4: estimated 10T+)
- **Cost:** Millions to hundreds of millions of dollars
- **Hardware:** Thousands of GPUs/TPUs running in parallel

### Fine-tuning:
- **Duration:** Hours to days
- **Tokens seen:** Millions to low billions
- **Cost:** $100 to $100,000 depending on approach
- **Hardware:** 1-10 GPUs often sufficient

```/dev/null/scale_comparison.txt#L1-12
Pre-training GPT-3:
├─ ~300 billion tokens
├─ ~10,000 A100 GPUs
├─ ~$4-12 million in compute costs
├─ Several months of training
└─ One pass through the dataset

Instruction fine-tuning (full):
├─ ~100 million tokens
├─ 8 A100 GPUs
├─ ~$10k-50k in compute
├─ Days of training
└─ 1-3 epochs
```

---

## 3. Data (Completely Different)

### Pre-training Data:

**Type:** Raw, unlabeled text from the internet

**Sources:**
- Wikipedia articles
- Books (fiction, non-fiction, textbooks)
- Web pages (Common Crawl - billions of pages)
- GitHub code repositories
- Academic papers
- News articles
- Social media (filtered)

**Characteristics:**
- ✅ Massive volume (TB to PB)
- ✅ Diverse topics and styles
- ⚠️ Mixed quality
- ⚠️ Contains errors, biases, outdated info
- No human annotation

**Goal:** Learn general patterns of language, world knowledge, reasoning

```/dev/null/pretraining_example.txt#L1-6
Raw text from Wikipedia:
"The Eiffel Tower was built in 1889 by Gustave Eiffel. It stands 
324 meters tall and was initially criticized by Parisian artists..."

Model learns:
- Grammar and syntax
- Facts about the world
- How to continue coherent text
```

### Fine-tuning Data:

**Type:** Carefully curated, labeled instruction-response pairs

**Format:**
```/dev/null/finetuning_example.txt#L1-20
Example 1 - Instruction following:
{
  "instruction": "Translate to French: Hello, how are you?",
  "output": "Bonjour, comment allez-vous?"
}

Example 2 - Chat format:
<|im_start|>system
You are a helpful assistant.<|im_end|>
<|im_start|>user
What is 2+2?<|im_end|>
<|im_start|>assistant
2+2 equals 4.<|im_end|>

Example 3 - Domain-specific:
{
  "input": "Patient reports headache and fever",
  "output": "Recommend: Check temperature, assess severity, 
            consider common causes (viral infection, dehydration)..."
}
```

**Characteristics:**
- ✅ High quality, human-reviewed
- ✅ Specific format/structure
- ✅ Teaches desired behaviors
- ⚠️ Smaller volume (1K to 100M examples)
- Often created by human labelers or experts

**Goal:** Teach specific behaviors, formats, or domain expertise

---

## 4. Objective Function (Similar but Different)

### Both Use Next-Token Prediction

The fundamental task is the same: predict the next token given previous tokens.

```/dev/null/next_token.txt#L1-4
Input:  "The capital of France is"
Target: " Paris"

Loss: Cross-entropy between prediction and target
```

### But Applied Differently:

**Pre-training:**
- Calculate loss on **every token** in the sequence
- No special treatment for different parts
- Goal: Model the probability of all text

```/dev/null/pretraining_loss.txt#L1-5
Sequence: "The Eiffel Tower was built in 1889"

Calculate loss on:
"The" → "Eiffel" → "Tower" → "was" → "built" → "in" → "1889"
(Every single token)
```

**Fine-tuning (Instruction Tuning):**
- Often **mask the loss** on the input/prompt
- Only calculate loss on the desired output
- Focus learning on generating good responses

```/dev/null/finetuning_loss.txt#L1-10
Sequence:
<|im_start|>user: What is Python?<|im_end|>
<|im_start|>assistant: Python is a programming language<|im_end|>

Calculate loss ONLY on:
"Python" → "is" → "a" → "programming" → "language"

Ignore loss on the user prompt!

Why? We want to learn to GENERATE good responses,
not memorize prompts.
```

This loss masking helps the model:
- Focus on output quality
- Not waste capacity memorizing input patterns
- Learn the instruction-following behavior more efficiently

---

## 5. What Gets Updated? (Parameter-Efficient Options)

### Pre-training:
- **Always update ALL parameters**
- No choice here - starting from scratch
- For a 7B model: update all 7 billion parameters

### Fine-tuning Options:

#### **Option A: Full Fine-Tuning**

Update all parameters (same as pre-training, but with lower LR):

```/dev/null/full_finetuning.txt#L1-6
7B parameter model:
├─ Update all 7,000,000,000 parameters
├─ Requires ~28GB GPU memory (fp32) or ~14GB (fp16)
├─ Higher cost
├─ Maximum flexibility
└─ Risk of overfitting on small datasets
```

#### **Option B: Parameter-Efficient Fine-Tuning (PEFT)**

Only update a small subset of parameters:

**LoRA (Low-Rank Adaptation):**
```/dev/null/lora.txt#L1-8
Add small "adapter" matrices to attention layers:

Original weight: W (frozen)
LoRA update: W + (B × A)
  where B and A are small matrices

Result:
├─ Update only ~7-70M parameters (0.1-1% of total!)
├─ Requires ~4-6GB GPU memory
├─ Much cheaper
└─ Almost as effective as full fine-tuning
```

**QLoRA (Quantized LoRA):**
```/dev/null/qlora.txt#L1-5
LoRA + Quantization:
├─ Reduce base model to 4-bit precision
├─ Fine-tune LoRA adapters in higher precision
├─ Requires ~3-4GB GPU memory
└─ Can fine-tune 13B models on consumer GPUs!
```

**This is what you'll see in today's demo!**

---

## 6. Risk of Overfitting (MUCH Higher in Fine-Tuning)

### Pre-training:
- **Data:** Trillions of tokens
- **Diversity:** Extremely varied content
- **Risk:** Very low - hard to memorize that much data
- **Strategy:** More epochs generally = better (until compute budget runs out)

### Fine-tuning:
- **Data:** Thousands to millions of examples
- **Diversity:** Often narrow domain
- **Risk:** Very high - easy to memorize small datasets
- **Strategy:** Usually just 1-3 epochs, careful validation

```/dev/null/overfitting_signs.txt#L1-12
Common mistake:
"My training loss keeps going down, let me train longer!"

Signs of overfitting:
✗ Training loss ↓ but validation loss ↑
✗ Model outputs memorized training examples verbatim
✗ Poor performance on similar-but-different inputs
✗ Loss of general capabilities

Result:
- Model becomes expert on training data
- Performs worse on real-world tasks
- "Overfitted specialist" instead of "general expert"

Best practice: Early stopping based on validation loss
```

### Example of Overfitting:

```/dev/null/overfit_example.txt#L1-15
Training data (100 customer support examples):
Q: "My internet is down"
A: "Have you tried restarting your router?"

After 1 epoch:
✓ Model learns the pattern
✓ Responds appropriately to variations

After 10 epochs (overfitting):
Q: "My internet is down"
A: "Have you tried restarting your router?"  ← Memorized exactly

Q: "My WiFi isn't working"  
A: [Generic response or confused] ← Can't generalize!
```

---

## 7. The Complete Training Pipeline

Modern LLMs go through multiple training stages, each building on the previous:

```/dev/null/pipeline.txt#L1-30
┌──────────────────────────────────────────────────────────────┐
│ 1. PRE-TRAINING (Foundation)                                 │
├──────────────────────────────────────────────────────────────┤
│ Data:          Trillions of tokens (web, books, code)        │
│ Duration:      Months                                        │
│ Cost:          $1M - $100M                                   │
│ Learning rate: 1e-4, with cosine decay                       │
│ Hardware:      1000s of GPUs                                 │
│ Output:        Base model (e.g., GPT-4-base, Llama-2-base)   │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│ 2. INSTRUCTION FINE-TUNING (Supervised)                      │
├──────────────────────────────────────────────────────────────┤
│ Data:          ~100M tokens (instruction-response pairs)     │
│ Duration:      Days                                          │
│ Cost:          $10K - $100K                                  │
│ Learning rate: 1e-5 to 1e-6                                  │
│ Hardware:      8-64 GPUs                                     │
│ Output:        Instruction-following model                   │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│ 3. RLHF (Reinforcement Learning from Human Feedback)         │
├──────────────────────────────────────────────────────────────┤
│ Train reward model on human preference rankings             │
│ Use PPO/DPO to optimize model against reward                │
│ Duration:      Days to weeks                                 │
│ Cost:          $10K - $50K                                   │
│ Learning rate: 1e-6 (even smaller!)                          │
│ Output:        Chat model (e.g., GPT-4, ChatGPT, Claude)     │
└──────────────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────────────┐
│ 4. YOUR FINE-TUNING (Domain-specific customization)          │
├──────────────────────────────────────────────────────────────┤
│ Data:          1K - 1M examples                              │
│ Duration:      Hours                                         │
│ Cost:          $100 - $1K (with LoRA)                        │
│ Learning rate: 1e-5 to 1e-4                                  │
│ Hardware:      1 GPU (consumer-grade possible with QLoRA)    │
│ Output:        Your custom model!                            │
└──────────────────────────────────────────────────────────────┘
```

Each stage:
- Builds on the previous one
- Uses progressively smaller datasets
- Uses progressively lower learning rates
- Has progressively more specific objectives
- Requires progressively higher quality data

---

## 8. The Algorithm: Same but Different

### What's the SAME:

Both pre-training and fine-tuning use:
- ✅ Gradient descent optimization (usually Adam or AdamW)
- ✅ Backpropagation
- ✅ Cross-entropy loss for next-token prediction
- ✅ Mini-batch training
- ✅ Learning rate schedules (warmup + decay)
- ✅ Dropout and regularization

### What's DIFFERENT:

```/dev/null/process_comparison.txt#L1-28
═══════════════════════════════════════════════════════════
PRE-TRAINING PROCESS:
═══════════════════════════════════════════════════════════
1. Initialize weights randomly (or from smaller model)
2. Load massive dataset (TB of raw text)
3. For millions of steps:
   ├─ Sample random sequence (2048-4096 tokens)
   ├─ Forward pass: predict next tokens
   ├─ Calculate loss on ALL tokens
   ├─ Backward pass: compute gradients
   ├─ Update ALL parameters with lr=1e-4
   ├─ No validation checking
   └─ Continue until compute budget exhausted
4. Save final checkpoint

Result: Model that can predict/generate text

═══════════════════════════════════════════════════════════
FINE-TUNING PROCESS:
═══════════════════════════════════════════════════════════
1. Load pre-trained weights (transfer learning!)
2. Load small, curated dataset (GB of instruction pairs)
3. For thousands of steps:
   ├─ Sample instruction-response pair
   ├─ Forward pass: predict response tokens
   ├─ Calculate loss ONLY on response (mask prompt)
   ├─ Backward pass: compute gradients
   ├─ Update parameters (all or just adapters) with lr=1e-5
   ├─ Monitor validation loss carefully
   └─ Early stopping when validation plateaus
4. Save fine-tuned model/adapters

Result: Model that follows instructions in specific format
```

---

## 9. Why Lower Learning Rates for Fine-Tuning?

Think of the model's knowledge as a landscape:

### Pre-training (High Learning Rate):

```/dev/null/pretraining_landscape.txt#L1-8
Starting point: Random noise, no knowledge
Goal: Find a good solution from scratch

[Random weights] --BIG STEPS--> [Language model]

Like: Hiking across a mountain range to find a valley
      Need big steps to cover ground quickly
      Don't care if you overshoot - you'll correct
```

### Fine-tuning (Low Learning Rate):

```/dev/null/finetuning_landscape.txt#L1-10
Starting point: Already in a good valley (pre-trained model)
Goal: Find a slightly better spot nearby

[Pre-trained] --tiny steps--> [Fine-tuned specialist]

Like: You're already in a nice valley
      Just need to find the best picnic spot
      Big steps would throw you over the cliff!
      Small steps keep you near the good solution
```

### What Happens with Wrong Learning Rate:

```/dev/null/wrong_lr.txt#L1-18
Too HIGH learning rate during fine-tuning:
┌────────────────────────────────────────┐
│ Model: "Oh, big updates? Must be       │
│        learning something completely   │
│        new! Let me change everything!" │
│                                        │
│ Result: Catastrophic forgetting        │
│ - Forgets general knowledge            │
│ - Loses capabilities                   │
│ - Overfits to fine-tuning data         │
└────────────────────────────────────────┘

Too LOW learning rate:
- Takes forever to train
- Might not converge
- Waste of compute resources

Just right (1e-5 to 1e-6):
- Preserves general knowledge
- Adds new capabilities
- Efficient training
```

---

## 10. Practical Implications

### When to Use What?

**Pre-training from scratch:**
- You have trillions of tokens of domain-specific data
- You need a completely custom vocabulary (e.g., new language)
- You have millions of dollars in compute budget
- Examples: Medical language in non-Latin script, specialized scientific notation

**Full fine-tuning:**
- You have 100K+ high-quality examples
- You need to significantly change model behavior
- You have access to multiple high-end GPUs
- Budget: $1K-$10K

**LoRA/PEFT fine-tuning:** ⭐ **Most common choice**
- You have 1K-100K examples
- You want to teach specific tasks/formats
- You have 1 consumer-grade GPU or cloud credits
- Budget: $100-$1K
- **This is what you'll do today!**

**Prompt engineering (no training):**
- You have <100 examples
- You just need slightly different outputs
- Zero budget for training
- Can provide examples in context window

---

## 11. Key Takeaways

### The Analogy:

```/dev/null/analogy.txt#L1-10
Pre-training = Learning a language from scratch
├─ Like: Child learning English over years
├─ Process: Exposure to millions of examples
├─ Result: General language capability
└─ Effort: Enormous

Fine-tuning = Learning a job using that language
├─ Like: Learning customer service scripts
├─ Process: Study specific examples and practice
├─ Result: Specialized skill within language
└─ Effort: Modest (days, not years)
```

### The Core Differences:

✅ **Same algorithm** (gradient descent + backpropagation)  
✅ **Different scale** (trillions vs millions of tokens)  
✅ **Different learning rates** (1e-4 vs 1e-5, cranked DOWN)  
✅ **Different data** (raw text vs instruction pairs)  
✅ **Different objectives** (general language vs specific behavior)  
✅ **Different risks** (hard to overfit vs easy to overfit)  

### Remember:

🎯 Pre-training teaches the model **language**  
🎯 Fine-tuning teaches the model **how to use language for specific tasks**  
🎯 Lower learning rates preserve existing knowledge while adding new skills  
🎯 PEFT methods (LoRA) make fine-tuning accessible to everyone  

---

## 12. Further Reading

**Papers:**
- "Attention Is All You Need" (Vaswani et al.) - The Transformer architecture
- "Language Models are Few-Shot Learners" (GPT-3 paper)
- "LoRA: Low-Rank Adaptation of Large Language Models"
- "QLoRA: Efficient Finetuning of Quantized LLMs"

**Resources:**
- Hugging Face PEFT library documentation
- Stanford CS224N lectures on transfer learning
- Sebastian Ruder's blog on transfer learning and fine-tuning

**Hands-On:**
- Today's fine-tuning demo!
- Hugging Face fine-tuning tutorial
- Google Colab notebooks for LoRA

---

## Try It Yourself!

After today's demo, experiment with fine-tuning on your own data. Start small (1K examples), use LoRA, and watch for overfitting. The best way to understand these concepts is to see them in action!
