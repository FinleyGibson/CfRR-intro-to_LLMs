# Prompt Engineering: Key Techniques Summary

This document summarizes the most important techniques used in prompt engineering for large language models.

---

## 1. Be Specific and Constrained
Clear prompts produce better outputs. Always define:
- Audience
- Task
- Format
- Tone
- Constraints

---

## 2. Role Prompting
Assign the model a role to shape its behavior.

Example: "You are a senior data analyst..."

---

## 3. Few-Shot Prompting
Provide examples of input-output pairs to guide behavior.

Useful for classification, formatting, and transformations.

---

## 4. Chain-of-Thought Prompting
Encourage step-by-step reasoning for complex tasks like math and logic.

---

## 5. Task Decomposition
Break complex tasks into smaller, manageable steps.

---

## 6. Structured Output Prompting
Request outputs in strict formats such as:
- JSON
- Tables
- Bullet lists

---

## 7. Retrieval-Augmented Prompting (RAG)
Provide external context to improve factual accuracy and reduce hallucinations.

---

## 8. Instruction Hierarchy
Organize instructions clearly and prioritize critical constraints.

---

## 9. Delimiters
Use clear separators (e.g., ``` or <<< >>>) to structure prompts and avoid confusion.

---

## 10. Self-Reflection / Critique
Ask the model to review and improve its own output.

---

## 11. Tool-Oriented Prompting
Encourage use of external tools (search, calculators, APIs) when needed.

---

## 12. Context Management
Keep prompts concise and relevant to stay within context limits.

---

## 13. Prompt Chaining
Break workflows into multiple prompts where outputs feed into the next step.

---

## 14. Constraint Prompting
Explicitly state what the model should NOT do (e.g., avoid hallucinations).

---

## 15. Iterative Refinement
Improve prompts through repeated testing and adjustment.

---

## 16. Meta-Prompting
Ask the model to improve or rewrite prompts for better performance.

---

## 17. Agentic Prompting
Design prompts for autonomous workflows with planning, execution, and verification steps.

---

## Golden Rules
- Be explicit
- Provide context
- Specify format
- Reduce ambiguity
- Use examples
- Break down tasks

---

## Most Important Techniques
1. Specific instructions
2. Structured outputs
3. Few-shot examples
4. Task decomposition
5. Retrieval/context injection
