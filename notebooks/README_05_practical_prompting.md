# 🎯 Practical Prompting Notebook - Quick Start Guide

## What This Notebook Does

Teaches the most useful prompt engineering techniques:
- 🌡️ **Temperature**: Control creativity vs consistency
- 📦 **JSON Output**: Extract structured data
- 🎓 **Few-Shot Learning**: Teach by example  
- 🧠 **Chain-of-Thought**: Better reasoning

**No torch library required!** Uses Hugging Face Inference API.

---

## 🚀 Quick Start (5 minutes)

### Step 1: Get Your Free API Key

1. Go to https://huggingface.co and sign up (free)
2. Go to https://huggingface.co/settings/tokens
3. Click **"New token"**
4. Give it a name (e.g., "notebook") and click **Create**
5. Copy the token (starts with `hf_`)

### Step 2: Set Your API Key

**Option A: Create `.env` file** (recommended)

In the `intro_to_llms` directory, create a file named `.env`:

```bash
HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxx
```

**Option B: Set environment variable**

```bash
export HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxx
```

### Step 3: Install Dependencies

```bash
pip install transformers requests python-dotenv
```

### Step 4: Run the Notebook

```bash
jupyter notebook notebooks/05_practical_prompting.ipynb
```

Or open it in VS Code / JupyterLab.

---

## 📖 What You'll Learn

### Part 1: Temperature
- Why temperature matters
- When to use low (0.0) vs high (1.5) temperature
- Factual vs creative task examples

### Part 2: JSON Output  
- Extract structured data from text
- Parse reviews, emails, documents
- Best practices for consistent output

### Part 3: Few-Shot Learning
- Teach models by showing examples
- Custom classification categories
- Text transformation tasks

### Part 4: Chain-of-Thought
- Improve reasoning with "Let's think step by step"
- Math and logic problems
- Multi-step analysis

### Part 5: Combining Techniques
- Real-world support ticket analysis
- JSON + Few-Shot + Chain-of-Thought
- Practice exercises

---

## 🔧 Troubleshooting

### "API Error: 401"
- Your API key is invalid or not set
- Check your `.env` file or environment variable
- Make sure the key starts with `hf_`

### "API Error: 503 - Model Loading"  
- Model is waking up (cold start)
- The notebook automatically waits and retries
- Usually takes 10-30 seconds

### Want to use local model instead?
In the notebook, change:
```python
llm = SimpleLLM(use_api=True)
```
to:
```python
llm = SimpleLLM(use_api=False, model="gpt2")
```

---

## 💡 Tips

1. **Start with low temperature (0.0-0.3)** for factual/structured tasks
2. **Use high temperature (0.7-1.5)** for creative tasks
3. **Combine techniques**: JSON + Few-Shot + Chain-of-Thought works great!
4. **Iterate on prompts**: Small changes can make big differences
5. **The API is free** but rate-limited - be patient between requests

**Enjoy learning! 🎉**
