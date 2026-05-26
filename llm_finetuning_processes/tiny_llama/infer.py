import copy

import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

# Load tokenizer
model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(model_id)


# Inference helper
def generate_response(model, prompt, max_new_tokens=150):
    inputs = tokenizer(prompt, return_tensors="pt", padding=True)
    input_ids = inputs["input_ids"]
    attention_mask = inputs["attention_mask"]

    with torch.no_grad():
        output = model.generate(
            input_ids=input_ids,
            attention_mask=attention_mask,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.eos_token_id,
        )

    full_output = tokenizer.decode(output[0], skip_special_tokens=True)

    # Return only the assistant's reply
    if "<|assistant|>" in full_output:
        response = full_output.split("<|assistant|>\n")[1].strip()
    else:
        response = full_output.strip()

    return response


# Prompt
instruction = "Summarize how a combustion engine works."
prompt = f"<|user|>\n{instruction}\n<|assistant|>\n"

# Load base model once
base_model = AutoModelForCausalLM.from_pretrained(model_id)

# Wrap a deep copy with the LoRA adapter — avoids reading model.safetensors twice
lora_model = PeftModel.from_pretrained(copy.deepcopy(base_model), "./tinyllama-yoda/checkpoint-30")

# Generate responses
base_response = generate_response(base_model, prompt)
lora_response = generate_response(lora_model, prompt)

# Print results
print("=== Base Model Response ===")
print("Question: ", instruction)
print("Response: ", base_response)
print("\n=== LoRA-Finetuned Model Response ===")
print("Question: ", instruction)
print("Response: ", lora_response)

lora_model.print_trainable_parameters()
