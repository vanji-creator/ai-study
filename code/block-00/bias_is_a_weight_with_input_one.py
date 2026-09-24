# Why the bias gradient is "2 x 1 x error" while the weight gradient is "2 x input x error".
#
# Run: python3 code/block-00/bias_is_a_weight_with_input_one.py

def predict(weight, bias, input_value):
    return weight * input_value + bias


def loss_for(weight, bias, input_value, actual):
    error = predict(weight, bias, input_value) - actual
    return error ** 2


# ---------------------------------------------------------------------------
# Part 1.  INFLUENCE: move each parameter by 1, see how far the prediction moves.
# ---------------------------------------------------------------------------

print("Part 1 - how far does the prediction move when I move a parameter by 1?")
print()
print(f"{'input':>8} {'start':>10} {'weight +1':>12} {'moved by':>10} "
      f"{'bias +1':>10} {'moved by':>10}")
print("-" * 64)

for input_value in [1, 3, 10, 50]:
    starting_prediction = predict(weight=1, bias=1, input_value=input_value)
    after_weight_moved = predict(weight=2, bias=1, input_value=input_value)
    after_bias_moved = predict(weight=1, bias=2, input_value=input_value)
    print(f"{input_value:>8} {starting_prediction:>10} {after_weight_moved:>12} "
          f"{after_weight_moved - starting_prediction:>10} "
          f"{after_bias_moved:>10} {after_bias_moved - starting_prediction:>10}")

print()
print("  The weight's influence is the input. The bias's influence is 1, always.")
print("  That is the whole difference, and it is why we can write")
print("      predicted = weight * input + bias * 1")
print("  The bias is a weight whose input happens to be the constant 1.")
print()
print()

# ---------------------------------------------------------------------------
# Part 2.  Check the gradient formula by measuring the slope instead of trusting it.
#
#   claimed:  gradient = 2 * (that parameter's input) * error
#
#   measured: move the parameter by a tiny amount, see how much the loss changed,
#             divide by the amount moved.
# ---------------------------------------------------------------------------

WEIGHT, BIAS = 1.0, 1.0
NUDGE = 0.000001          # small enough that the measured slope is essentially exact

print("Part 2 - is that formula right? measure the slope and compare")
print()
print(f"{'input':>6} {'actual':>7} {'error':>8} "
      f"{'weight grad':>12} {'measured':>12}   "
      f"{'bias grad':>11} {'measured':>11}")
print("-" * 76)

for input_value, actual in [(1, 5), (3, 11), (10, 40), (50, 120)]:
    error = predict(WEIGHT, BIAS, input_value) - actual

    claimed_weight_gradient = 2 * input_value * error
    claimed_bias_gradient = 2 * 1 * error

    loss_here = loss_for(WEIGHT, BIAS, input_value, actual)
    measured_weight_gradient = (
        loss_for(WEIGHT + NUDGE, BIAS, input_value, actual) - loss_here) / NUDGE
    measured_bias_gradient = (
        loss_for(WEIGHT, BIAS + NUDGE, input_value, actual) - loss_here) / NUDGE

    print(f"{input_value:>6} {actual:>7} {error:>8.1f} "
          f"{claimed_weight_gradient:>12.1f} {measured_weight_gradient:>12.4f}   "
          f"{claimed_bias_gradient:>11.1f} {measured_bias_gradient:>11.4f}")

print()
print("  The formula and the measurement agree. Nothing was asserted.")
print()
print()

# ---------------------------------------------------------------------------
# Part 3.  What the bias buys you: a model without one is stuck through the origin.
# ---------------------------------------------------------------------------

print("Part 3 - what a model WITHOUT a bias cannot do")
print()

candidate_counts = [1, 3]
actual_times = [5, 11]          # this is 3 * input + 2, so it needs a bias of 2

print("  the data:   input 1 -> 5 seconds      input 3 -> 11 seconds")
print("  the truth:  predicted = 3 * input + 2")
print()
print("  Best possible one-parameter model (no bias), searched over many weights:")

best_weight, best_loss = None, None
weight_candidate = 0.0
while weight_candidate <= 6.0:
    total = sum((weight_candidate * input_value - actual) ** 2
                for input_value, actual in zip(candidate_counts, actual_times))
    if best_loss is None or total < best_loss:
        best_weight, best_loss = weight_candidate, total
    weight_candidate += 0.001

print(f"    best weight = {best_weight:.3f}   loss = {best_loss:.4f}   "
      f"-> cannot reach 0")
print(f"    it predicts {best_weight * 1:.2f} and {best_weight * 3:.2f} "
      f"for inputs 1 and 3, against 5 and 11")
print()
print("  With a bias, weight 3 and bias 2 give loss exactly "
      f"{sum((3 * i + 2 - a) ** 2 for i, a in zip(candidate_counts, actual_times))}.")
print()
print("  The second parameter is not a refinement. It lets the model say something")
print("  the one-parameter version could not say at all: that some cost is there")
print("  before the first candidate arrives.")
