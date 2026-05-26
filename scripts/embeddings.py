from transformers import AutoModel, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("gpt2")
model = AutoModel.from_pretrained("gpt2")

text = "Hello, how are you?"

# Tokenize
# inputs contain the tokenized input and their attention mask
inputs = tokenizer(text, return_tensors="pt")

tokens = inputs["input_ids"]
print("Inputs: ", tokens)

# # Get embeddings (no gradients needed)
# with torch.no_grad():
#     outputs = model(**inputs)

# # Last hidden states = contextual embeddings
# embeddings = outputs.last_hidden_state

# print(embeddings.shape)  # (batch_size, sequence_length, hidden_size)
# print("Embeddings: ", embeddings)


# def euclidean_distance(emb1, emb2):
#     return torch.sqrt(torch.sum((emb1 - emb2) ** 2))

print("Done!")
