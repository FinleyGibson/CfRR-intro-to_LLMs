# Neural Network Output Equations

## Notation

| Symbol          | Meaning                                                       |
| --------------- | ------------------------------------------------------------- |
| $x$             | Input vector                                                  |
| $W^{(l)}$       | Weight matrix for layer $l$                                   |
| $b^{(l)}$       | Bias vector for layer $l$                                     |
| $h^{(l)}$       | Hidden activation at layer $l$                                |
| $\hat{y}$       | Network output                                                |
| $\sigma(\cdot)$ | Activation function (e.g. ReLU, sigmoid) applied element-wise |

---

## Diagram 1 — Simple Network (2 → 3 → 3 → 2)

**Layer-by-layer:**

$$
h^{(1)} = \sigma\!\left(W^{(1)}\,x + b^{(1)}\right)
$$

$$
h^{(2)} = \sigma\!\left(W^{(2)}\,h^{(1)} + b^{(2)}\right)
$$

$$
\hat{y} = W^{(3)}\,h^{(2)} + b^{(3)}
$$

**Full composition:**

$$
\hat{y} = W^{(3)}\,\sigma\!\left(W^{(2)}\,\sigma\!\left(W^{(1)}\,x + b^{(1)}\right) + b^{(2)}\right) + b^{(3)}
$$

**Weight dimensions:**

| Parameter           | Shape                                      |
| ------------------- | ------------------------------------------ |
| $x$                 | $\mathbb{R}^{2}$                           |
| $W^{(1)},\ b^{(1)}$ | $\mathbb{R}^{3 \times 2},\ \mathbb{R}^{3}$ |
| $W^{(2)},\ b^{(2)}$ | $\mathbb{R}^{3 \times 3},\ \mathbb{R}^{3}$ |
| $W^{(3)},\ b^{(3)}$ | $\mathbb{R}^{2 \times 3},\ \mathbb{R}^{2}$ |

**Parameter count:**

| Layer              | Weights          | Biases | Subtotal |
| ------------------ | ---------------- | ------ | -------- |
| $W^{(1)}, b^{(1)}$ | $3 \times 2 = 6$ | $3$    | $9$      |
| $W^{(2)}, b^{(2)}$ | $3 \times 3 = 9$ | $3$    | $12$     |
| $W^{(3)}, b^{(3)}$ | $2 \times 3 = 6$ | $2$    | $8$      |
| **Total**          |                  |        | **29**   |

---

## Diagram 2 — Deep Network (2 → 3 × 5 → 2)

**Layer-by-layer:**

$$h^{(1)} = \sigma\!\left(W^{(1)}\,x + b^{(1)}\right)$$

$$h^{(l)} = \sigma\!\left(W^{(l)}\,h^{(l-1)} + b^{(l)}\right), \quad l = 2, \ldots, 5$$

$$\hat{y} = W^{(6)}\,h^{(5)} + b^{(6)}$$

**Full composition** (using $\cdots$ to compress the repeated hidden layers):

$$\hat{y} = W^{(6)}\,\sigma\!\left(W^{(5)}\,\sigma\!\left(\cdots\,\sigma\!\left(W^{(1)}\,x + b^{(1)}\right)\cdots\right) + b^{(5)}\right) + b^{(6)}$$

**Weight dimensions:**

| Parameter                          | Shape                                      |
| ---------------------------------- | ------------------------------------------ |
| $x$                                | $\mathbb{R}^{2}$                           |
| $W^{(1)},\ b^{(1)}$                | $\mathbb{R}^{3 \times 2},\ \mathbb{R}^{3}$ |
| $W^{(l)},\ b^{(l)},\ l=2,\ldots,5$ | $\mathbb{R}^{3 \times 3},\ \mathbb{R}^{3}$ |
| $W^{(6)},\ b^{(6)}$                | $\mathbb{R}^{2 \times 3},\ \mathbb{R}^{2}$ |

**Parameter count:**

| Layer                             | Weights                     | Biases       | Subtotal |
| --------------------------------- | --------------------------- | ------------ | -------- |
| $W^{(1)}, b^{(1)}$                | $3 \times 2 = 6$            | $3$          | $9$      |
| $W^{(l)}, b^{(l)},\ l=2,\ldots,5$ | $4 \times (3 \times 3 = 9)$ | $4 \times 3$ | $48$     |
| $W^{(6)}, b^{(6)}$                | $2 \times 3 = 6$            | $2$          | $8$      |
| **Total**                         |                             |              | **65**   |

---

## Diagram 3 — Wide & Deep Network (4 → 5 × 5 → 2)

The structure mirrors Diagram 2, but with a wider input ($x \in \mathbb{R}^4$) and wider hidden layers (5 units each).

**Layer-by-layer:**

$$h^{(1)} = \sigma\!\left(W^{(1)}\,x + b^{(1)}\right)$$

$$h^{(l)} = \sigma\!\left(W^{(l)}\,h^{(l-1)} + b^{(l)}\right), \quad l = 2, \ldots, 5$$

$$\hat{y} = W^{(6)}\,h^{(5)} + b^{(6)}$$

**Full composition:**

$$\hat{y} = W^{(6)}\,\sigma\!\left(W^{(5)}\,\sigma\!\left(\cdots\,\sigma\!\left(W^{(1)}\,x + b^{(1)}\right)\cdots\right) + b^{(5)}\right) + b^{(6)}$$

**Weight dimensions:**

| Parameter                          | Shape                                      |
| ---------------------------------- | ------------------------------------------ |
| $x$                                | $\mathbb{R}^{4}$                           |
| $W^{(1)},\ b^{(1)}$                | $\mathbb{R}^{5 \times 4},\ \mathbb{R}^{5}$ |
| $W^{(l)},\ b^{(l)},\ l=2,\ldots,5$ | $\mathbb{R}^{5 \times 5},\ \mathbb{R}^{5}$ |
| $W^{(6)},\ b^{(6)}$                | $\mathbb{R}^{2 \times 5},\ \mathbb{R}^{2}$ |

**Parameter count:**

| Layer                             | Weights                      | Biases       | Subtotal |
| --------------------------------- | ---------------------------- | ------------ | -------- |
| $W^{(1)}, b^{(1)}$                | $5 \times 4 = 20$            | $5$          | $25$     |
| $W^{(l)}, b^{(l)},\ l=2,\ldots,5$ | $4 \times (5 \times 5 = 25)$ | $4 \times 5$ | $120$    |
| $W^{(6)}, b^{(6)}$                | $2 \times 5 = 10$            | $2$          | $12$     |
| **Total**                         |                              |              | **157**  |
