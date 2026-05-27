# Model Choice

## OpenAI

- Easy to use
- No free tier available

## Llama2

- Requires Nvidia GPU

## Google Colab

- Torch only compiled for CPU access.
- 12–16 GB VRAM per session
- Kinda works!

## Potential Options

### LoRa (Low-Rank Adaptation))

- Uses much less memory
- Trains faster
- Produces tiny adapter files (MBs instead of GBs)
- You can swap adapters to change behavior instantly

## TinyLlama

- Guide to fine-tuning [here](https://medium.com/@sudisabet/fine-tuning-a-lightweight-llm-on-your-laptop-a-practical-guide-using-lora-model-on-cpu-143ef5291b89)
- Combine with LoRA
