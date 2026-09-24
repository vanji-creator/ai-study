# Why a stack of layers needs a non-linear rule between them.
#
# Three data points that no straight line can pass through:
#     input 1 -> 1,  input 2 -> 4,  input 3 -> 9
#
# Run: python3 code/block-00/why_non_linearity.py

input_values = [1, 2, 3]
actual_values = [1, 4, 9]


def gaps_between(values):
    """The difference from each value to the next. Constant gaps mean a straight line."""
    return [round(values[index + 1] - values[index], 6)
            for index in range(len(values) - 1)]


# ---------------------------------------------------------------------------
# Part 1.  One stage cannot fit the data. Not "not yet" - cannot.
# ---------------------------------------------------------------------------

print("Part 1 - one weight and one bias, solved from the first two rows")
print()
weight = (actual_values[1] - actual_values[0]) / (input_values[1] - input_values[0])
bias = actual_values[0] - weight * input_values[0]
print(f"  weight = {weight}, bias = {bias}")
print()
print(f"{'input':>7} {'actual':>8} {'predicted':>11} {'error':>8}")
print("-" * 36)
for input_value, actual in zip(input_values, actual_values):
    predicted = weight * input_value + bias
    print(f"{input_value:>7} {actual:>8} {predicted:>11.2f} {predicted - actual:>8.2f}")
print()
print("  Rows 1 and 2 fit exactly. Row 3 is out by 2, and no other weight and bias")
print("  do better on all three at once - the three points are not on a line.")
print()
print()

# ---------------------------------------------------------------------------
# Part 2.  Two stages, no rule in between. It collapses into one stage.
# ---------------------------------------------------------------------------

print("Part 2 - two stages chained, nothing in between")
print()

def two_stages_plain(input_value, weight1, bias1, weight2, bias2):
    hidden = (weight1 * input_value) + bias1
    return (weight2 * hidden) + bias2


for weight1, bias1, weight2, bias2 in [(2, 1, 3, 5), (0.5, -4, 10, 2), (7, 3, -2, 9)]:
    predictions = [two_stages_plain(i, weight1, bias1, weight2, bias2)
                   for i in input_values]
    collapsed_weight = weight2 * weight1
    collapsed_bias = (weight2 * bias1) + bias2
    print(f"  weight1 {weight1:>5}, bias1 {bias1:>5}, "
          f"weight2 {weight2:>5}, bias2 {bias2:>5}")
    print(f"    predictions {predictions}   gaps {gaps_between(predictions)}")
    print(f"    same as ONE stage with weight {collapsed_weight}, bias {collapsed_bias}: "
          f"{[collapsed_weight * i + collapsed_bias for i in input_values]}")
    print()

print("  The gaps are always constant, whatever the four parameters are. Four knobs,")
print("  two stages, and still a straight line. The stages multiply into one:")
print()
print("      predicted = (weight2 x ((weight1 x input) + bias1)) + bias2")
print("                = ((weight2 x weight1) x input) + ((weight2 x bias1) + bias2)")
print("                   \\______ one number ______/     \\______ one number ______/")
print()
print()

# ---------------------------------------------------------------------------
# Part 3.  Put one rule between the stages: negatives become zero.
# ---------------------------------------------------------------------------

def relu(value):
    """The whole rule: if it is negative, it becomes 0. Otherwise leave it alone."""
    return value if value > 0 else 0.0


def two_stages_with_rule(input_value, weight1, bias1, weight2, bias2):
    hidden = (weight1 * input_value) + bias1
    hidden = relu(hidden)
    return (weight2 * hidden) + bias2


print("Part 3 - the same two stages, with the rule in between")
print()
for weight1, bias1, weight2, bias2 in [(1, -2, 1, 0), (1, -1, 1, 0), (1, 0, 1, 0)]:
    predictions = [two_stages_with_rule(i, weight1, bias1, weight2, bias2)
                   for i in input_values]
    print(f"  weight1 {weight1:>4}, bias1 {bias1:>4}  ->  predictions {predictions}   "
          f"gaps {gaps_between(predictions)}")

print()
print("  The gaps are no longer constant, so it is no longer a straight line.")
print("  And look at bias1: it decides WHERE the flat part ends and the climb starts.")
print("  The position of the bend is a learned parameter.")
print()
print()

# ---------------------------------------------------------------------------
# Part 4.  Enough bends fit the data exactly. Hand-chosen here, learned in practice.
# ---------------------------------------------------------------------------

print("Part 4 - three bends, added together, hitting all three points exactly")
print()

# Each unit is: relu((1 x input) + its own bias), then scaled by its own weight.
# Chosen by hand so that the three points land on 1, 4 and 9.
units = [(0.0, 1.0), (-1.0, 2.0), (-2.0, 2.0)]   # (bias1, weight2) for each unit

print("  three units, each one relu((1 x input) + bias1) scaled by weight2:")
for bias1, weight2 in units:
    print(f"    bias1 {bias1:>5}, weight2 {weight2:>5}")
print()
print(f"{'input':>7} {'actual':>8} {'predicted':>11}")
print("-" * 28)
for input_value, actual in zip(input_values, actual_values):
    predicted = sum(weight2 * relu((1 * input_value) + bias1)
                    for bias1, weight2 in units)
    print(f"{input_value:>7} {actual:>8} {predicted:>11.2f}")

print()
print("  Exact. Nobody had to know the data was squares. Three bends, placed by")
print("  three biases, scaled by three weights - all of them ordinary parameters")
print("  that gradient descent can find.")
print()
print("  One more thing, for the next topic: the rule's own gradient is either 1")
print("  (the value was positive, so it passed straight through) or 0 (the value was")
print("  negative, so it was blocked). Nothing in between. That matters for backprop.")
