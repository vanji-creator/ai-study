# Self-study list

From 2026-10-09 the working method is: **Vikash studies the topics himself, then the tutor
verifies.** The tutor does not lecture unless he asks. Verification is by cold recall: he
writes or says the answer in his own words, the tutor marks it ✓ / ~ / ✗ / –, and every ✗ or
– becomes a card at box 1.

Resource titles come from search results, not from watching them. Check they are current.

---

## List 1 — finish Block 0 (the next step)

Topics:
1. Chain rule
2. Forward pass and backward pass
3. Backpropagation on a two-weight chain, by hand
4. Why backpropagation reuses work (and why nudging every weight is too slow)

Resources:
- StatQuest, "Neural Networks Part 2: Backpropagation Main Ideas", then "Backpropagation
  Details Part 1" and "Part 2".
- 3Blue1Brown, Neural Networks chapter 3, "Backpropagation, intuitively"; chapter 4,
  "Backpropagation calculus".

Verification: the Block 0 gate (`CLAUDE.md` §6). Worked example already in this repository:
two boxes, input 2, weight1 3, weight2 0.5, actual 4. Gradients −2 and −12.

## List 2 — maths gaps (before they are needed)

1. Mean and median
2. Derivative as slope (we already measured it by nudging)
3. Vectors and the dot product
4. Exponent and logarithm (needed for softmax and cross-entropy)
5. Basic probability

Resources: 3Blue1Brown "Essence of calculus" and "Essence of linear algebra" series;
StatQuest for mean/median and probability.

## List 3 — Block M, machine learning foundations

1. Train, validation and test sets
2. Data leakage; grouped splits (why Clikk was split by domain)
3. Underfitting and overfitting (bias and variance)
4. Regularisation: L2 weight decay, dropout, early stopping
5. Loss functions: squared error vs cross-entropy
6. Confusion matrix
7. Accuracy, precision, recall, F1, false-positive rate
8. ROC-AUC and PR-AUC
9. Class imbalance; choosing a threshold
10. Calibration
11. Cross-validation
12. Logistic regression
13. Decision trees, random forests, gradient boosting
14. k-nearest neighbours, k-means

Verification: Block M gate (`CLAUDE.md` §6).

## List 4 — Block 1 part 2, embeddings

1. What an embedding vector represents
2. Cosine similarity, dot product, Euclidean distance
3. Why normalising makes cosine and dot product equal
4. Dimensionality
5. Bi-encoder vs cross-encoder

Verification: Block 1 gate (`CLAUDE.md` §6).
