# LLM Recipe Generation Workflow

```mermaid
graph TD
    A[User Request LLM]:::accent0
    B[1. Planning / Decomposition]:::accent1
    C[2. Step Executor Loop]:::accent2
    D[3. Context Memory Update]:::accent3
    E[Final Structured Recipe<br/>+ step-by-step instructions]:::accent4
    
    A --> B
    B --> |→ Ingredients<br/>→ Ordered Steps| C
    C --> |LLM runs each step alone| D
    D --> |Previous steps accumulated| E
```

## Workflow Steps

1. **User Request (LLM)** - Initial user input requesting a recipe
2. **Planning / Decomposition** - LLM breaks down the request into:
   - Ingredients needed
   - Ordered steps to follow
3. **Step Executor Loop** - LLM processes each step individually
4. **Context Memory Update** - Previous steps are accumulated in memory
5. **Final Output** - Structured recipe with complete step-by-step instructions
