## Model Optimisation

### Model Evals

- Eval: "Evaluations" that test model outputs to ensure they meet the style and content criteria of the task.

### RAG

- Retrieval-Augmented Generation (RAG) is a technique that combines retrieval and generation models to improve the quality of generated text. It works by first retrieving relevant documents from a large corpus using a retrieval model, and then using a generation model to generate text based on the retrieved documents.

### Supervised fine-tuning

1. Build your training dataset to determine what “good” looks like
2. Upload a training dataset containing example prompts and desired model output
3. Create a fine-tuning job for a base model using your training data
4. Evaluate your results using the fine-tuned model

#### Notes:

- The minimum number of examples you can provide for fine-tuning is 10.
- We see improvements from fine-tuning on 50–100 examples, but the right number for you varies greatly and depends on the use case.
- We recommend starting with 50 well-crafted demonstrations and evaluating the results
- If performance improves with 50 good examples, try adding examples to see further results. If 50 examples have no impact, rethink your task or prompt before adding training data.

### Large Model Distillation
