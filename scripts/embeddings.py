import torch
from transformers import AutoModel, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModel.from_pretrained("gpt2")

text = "Hello, how are you?"

# Tokenize
inputs = tokenizer(text, return_tensors="pt")

# Get embeddings (no gradients needed)
with torch.no_grad():
    outputs = model(**inputs)

# Last hidden states = contextual embeddings
embeddings = outputs.last_hidden_state

print(embeddings.shape)  # (batch_size, sequence_length, hidden_size)
print(embeddings)
