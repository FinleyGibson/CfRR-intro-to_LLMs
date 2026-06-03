# Neural Network Scalar Equations

Each unit is computed individually — no matrix notation.

## Notation

| Symbol | Meaning |
|---|---|
| $x_i$ | The $i$-th input |
| $w^{(l)}_{j,i}$ | Scalar weight from unit $i$ in layer $l-1$ to unit $j$ in layer $l$ |
| $b^{(l)}_j$ | Bias of unit $j$ in layer $l$ |
| $h^{(l)}_j$ | Activation of unit $j$ in hidden layer $l$ |
| $\hat{y}_k$ | The $k$-th output |
| $\sigma(\cdot)$ | Activation function (e.g. ReLU, sigmoid) |

---

## Diagram 1 — Simple Network (2 → 3 → 3 → 2)

**Layer 1** — input to first hidden layer:

$$\begin{aligned}
h^{(1)}_1 &= \sigma\!\left(w^{(1)}_{1,1}\,x_1 + w^{(1)}_{1,2}\,x_2 + b^{(1)}_1\right) \\[6pt]
h^{(1)}_2 &= \sigma\!\left(w^{(1)}_{2,1}\,x_1 + w^{(1)}_{2,2}\,x_2 + b^{(1)}_2\right) \\[6pt]
h^{(1)}_3 &= \sigma\!\left(w^{(1)}_{3,1}\,x_1 + w^{(1)}_{3,2}\,x_2 + b^{(1)}_3\right)
\end{aligned}$$

**Layer 2** — first to second hidden layer:

$$\begin{aligned}
h^{(2)}_1 &= \sigma\!\left(w^{(2)}_{1,1}\,h^{(1)}_1 + w^{(2)}_{1,2}\,h^{(1)}_2 + w^{(2)}_{1,3}\,h^{(1)}_3 + b^{(2)}_1\right) \\[6pt]
h^{(2)}_2 &= \sigma\!\left(w^{(2)}_{2,1}\,h^{(1)}_1 + w^{(2)}_{2,2}\,h^{(1)}_2 + w^{(2)}_{2,3}\,h^{(1)}_3 + b^{(2)}_2\right) \\[6pt]
h^{(2)}_3 &= \sigma\!\left(w^{(2)}_{3,1}\,h^{(1)}_1 + w^{(2)}_{3,2}\,h^{(1)}_2 + w^{(2)}_{3,3}\,h^{(1)}_3 + b^{(2)}_3\right)
\end{aligned}$$

**Output layer:**

$$\begin{aligned}
\hat{y}_1 &= w^{(3)}_{1,1}\,h^{(2)}_1 + w^{(3)}_{1,2}\,h^{(2)}_2 + w^{(3)}_{1,3}\,h^{(2)}_3 + b^{(3)}_1 \\[6pt]
\hat{y}_2 &= w^{(3)}_{2,1}\,h^{(2)}_1 + w^{(3)}_{2,2}\,h^{(2)}_2 + w^{(3)}_{2,3}\,h^{(2)}_3 + b^{(3)}_2
\end{aligned}$$

---

## Diagram 2 — Deep Network (2 → 3 × 5 → 2)

**Layer 1** — same structure as Diagram 1:

$$\begin{aligned}
h^{(1)}_1 &= \sigma\!\left(w^{(1)}_{1,1}\,x_1 + w^{(1)}_{1,2}\,x_2 + b^{(1)}_1\right) \\[6pt]
h^{(1)}_2 &= \sigma\!\left(w^{(1)}_{2,1}\,x_1 + w^{(1)}_{2,2}\,x_2 + b^{(1)}_2\right) \\[6pt]
h^{(1)}_3 &= \sigma\!\left(w^{(1)}_{3,1}\,x_1 + w^{(1)}_{3,2}\,x_2 + b^{(1)}_3\right)
\end{aligned}$$

**Layers 2–5** — the same pattern repeats for $l = 2, \ldots, 5$:

$$\begin{aligned}
h^{(l)}_1 &= \sigma\!\left(w^{(l)}_{1,1}\,h^{(l-1)}_1 + w^{(l)}_{1,2}\,h^{(l-1)}_2 + w^{(l)}_{1,3}\,h^{(l-1)}_3 + b^{(l)}_1\right) \\[6pt]
h^{(l)}_2 &= \sigma\!\left(w^{(l)}_{2,1}\,h^{(l-1)}_1 + w^{(l)}_{2,2}\,h^{(l-1)}_2 + w^{(l)}_{2,3}\,h^{(l-1)}_3 + b^{(l)}_2\right) \\[6pt]
h^{(l)}_3 &= \sigma\!\left(w^{(l)}_{3,1}\,h^{(l-1)}_1 + w^{(l)}_{3,2}\,h^{(l-1)}_2 + w^{(l)}_{3,3}\,h^{(l-1)}_3 + b^{(l)}_3\right)
\end{aligned}$$

**Output layer:**

$$\begin{aligned}
\hat{y}_1 &= w^{(6)}_{1,1}\,h^{(5)}_1 + w^{(6)}_{1,2}\,h^{(5)}_2 + w^{(6)}_{1,3}\,h^{(5)}_3 + b^{(6)}_1 \\[6pt]
\hat{y}_2 &= w^{(6)}_{2,1}\,h^{(5)}_1 + w^{(6)}_{2,2}\,h^{(5)}_2 + w^{(6)}_{2,3}\,h^{(5)}_3 + b^{(6)}_2
\end{aligned}$$

---

## Diagram 3 — Wide & Deep Network (4 → 5 × 5 → 2)

**Layer 1** — 4 inputs feeding into 5 hidden units:

$$\begin{aligned}
h^{(1)}_1 &= \sigma\!\left(w^{(1)}_{1,1}\,x_1 + w^{(1)}_{1,2}\,x_2 + w^{(1)}_{1,3}\,x_3 + w^{(1)}_{1,4}\,x_4 + b^{(1)}_1\right) \\[4pt]
&\vdots \\[4pt]
h^{(1)}_5 &= \sigma\!\left(w^{(1)}_{5,1}\,x_1 + w^{(1)}_{5,2}\,x_2 + w^{(1)}_{5,3}\,x_3 + w^{(1)}_{5,4}\,x_4 + b^{(1)}_5\right)
\end{aligned}$$

**Layers 2–5** — repeated for $l = 2, \ldots, 5$, each unit receives 5 inputs:

$$\begin{aligned}
h^{(l)}_1 &= \sigma\!\left(w^{(l)}_{1,1}\,h^{(l-1)}_1 + \cdots + w^{(l)}_{1,5}\,h^{(l-1)}_5 + b^{(l)}_1\right) \\[4pt]
&\vdots \\[4pt]
h^{(l)}_5 &= \sigma\!\left(w^{(l)}_{5,1}\,h^{(l-1)}_1 + \cdots + w^{(l)}_{5,5}\,h^{(l-1)}_5 + b^{(l)}_5\right)
\end{aligned}$$

**Output layer:**

$$\begin{aligned}
\hat{y}_1 &= w^{(6)}_{1,1}\,h^{(5)}_1 + \cdots + w^{(6)}_{1,5}\,h^{(5)}_5 + b^{(6)}_1 \\[6pt]
\hat{y}_2 &= w^{(6)}_{2,1}\,h^{(5)}_1 + \cdots + w^{(6)}_{2,5}\,h^{(5)}_5 + b^{(6)}_2
\end{aligned}$$
