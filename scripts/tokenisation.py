from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("gpt2")

text = "Hello, how are you?"
tokens = tokenizer(text)

print(tokens["input_ids"])

print(tokenizer.decode(tokens["input_ids"]))
print()

for tok in tokens["input_ids"]:
    print(tok, "\t", tokenizer.decode(tok))


print("")
tokens = tokenizer("Counterfactual")
for tok in tokens["input_ids"]:
    print(tok, "\t", tokenizer.decode(tok))
