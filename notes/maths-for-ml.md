# Maths for ML — taught so far

Every maths idea used in a lesson must be in this file first (`CLAUDE.md` §1.2 C).
One entry per idea: plain sentence, one number example, why ML needs it.
Status: **taught**, **partly taught**, or **not yet taught**.

---

## Square — taught

A number multiplied by itself.
`3 × 3 = 9`, `(−3) × (−3) = 9`. The sign disappears.

Why ML needs it: the loss is the error squared. The square makes +3 and −3 count as equally
wrong, makes "no error" (0) the lowest possible value, and makes big errors cost much more
than small ones (error 2 → 4, error 10 → 100).

## Absolute value — partly taught

The size of a number with the sign removed. Written `|x|`.
`|+3| = 3`, `|−3| = 3`. Unlike the square, big numbers are not made bigger: `|10| = 10`.

Why ML needs it: it is a possible loss. Its slope is always +1 or −1, so its gradient knows
which way to move but not how far. Steps never get smaller near the answer.

## Slope — taught (by measuring)

How much one thing changes when you move another thing a little. You measure it by nudging:
move the input a tiny step, see how much the output changed, divide.

Example, loss = error²: at error 4, the loss is 16. At error 4.001, it is 16.008. The
change, 0.008, divided by the nudge, 0.001, gives about **8**.

Why ML needs it: **the gradient is the slope of the loss**, measured with respect to one
weight. Its sign says which way is downhill; its size says how steep.
Script: `code/block-00/slope_by_two_points.py`.

## The slope of error² is 2 × error — taught (measured, not proved)

Measured by nudging, see the table below. The "2" is not a choice; it comes from the square.

```
error   slope of error²
1       2
3       6
4       8
10      20
```

Then the weight: when the weight moves by 1, the prediction moves by the input, so the
error moves by the input. So the slope of the loss for one weight is
`2 × (error) × (input)`.

**This is a shortcut for one loss only.** Change the loss and the shortcut changes. The
meaning — slope of the loss — never changes.

## Squaring a sum — taught 2026-10-07

`(a + b)² = a² + (2 × a × b) + b²`. Check: `(4 + 0.02)² = 16 + 0.16 + 0.0004 = 16.1604`.

Why ML needs it: it is the only algebra needed to derive the gradient of error².

## d-notation — taught 2026-10-07

`d(loss) / d(weight)` means (change in loss) ÷ (change in weight) for a very tiny step. It is
the measured slope, written as a symbol. `d` = "a tiny change in".

Derivation of the gradient of error² for one weight, done with him:
nudge weight by h → error grows by (input × h) → new loss = error² + (2 × error × input × h)
+ (input × h)² → subtract old loss, divide by h → (2 × error × input) + (input² × h) → h tiny
→ **2 × error × input**. At weight 0.5, input 20, error 4, h = 0.001 the leftover is 0.4,
which is why the measurement gave 160.4.

## Mean and median — not yet taught

Will be needed for "squared error aims at the average, absolute error at the median".
Teach with numbers before using either word.

## Derivative — not yet taught as a word

It is the formal name for the slope found by nudging with a smaller and smaller nudge. Do not
use the word until it is taught from the slope entry above.

## Chain rule — not yet taught

Needed for backpropagation. Teach from nudging: if A moves B, and B moves C, then how much C
moves is how much B moves times how much C moves per unit of B.
