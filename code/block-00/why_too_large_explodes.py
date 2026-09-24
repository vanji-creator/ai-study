# Why a too-large learning rate makes the loss grow instead of converging slowly.
#
# The companion to gradient_descent.py. That script shows WHAT happens.
# This one shows WHY, by reducing the whole update to a single multiplier.
#
# Run: python3 code/block-00/why_too_large_explodes.py

candidate_counts = [10, 20, 50]
actual_times_seconds = [3, 6, 15]

TRUE_WEIGHT = 0.3          # because 3 = 0.3*10, 6 = 0.3*20, 15 = 0.3*50 exactly


def total_loss(weight):
    return sum((weight * candidates - actual_time) ** 2
               for candidates, actual_time in zip(candidate_counts, actual_times_seconds))


def gradient_of_loss(weight):
    """The same function as in gradient_descent.py: 2 * candidates * error, summed."""
    gradient = 0.0
    for candidates, actual_time in zip(candidate_counts, actual_times_seconds):
        error = weight * candidates - actual_time
        gradient += 2 * candidates * error
    return gradient


# ----------------------------------------------------------------------------
# Part 1.  The gradient is not a constant. It is proportional to how far the
#          weight is from the right answer.
# ----------------------------------------------------------------------------

# Doing the algebra on gradient_of_loss by hand gives:
#     error    = candidates * (weight - 0.3)
#     gradient = 2 * (10^2 + 20^2 + 50^2) * (weight - 0.3)
#              = 6000 * (weight - 0.3)
sum_of_squared_candidate_counts = sum(candidates ** 2 for candidates in candidate_counts)
gradient_per_unit_of_distance = 2 * sum_of_squared_candidate_counts     # 6000

print("Part 1 - the gradient is 6000 times the distance from the answer")
print(f"  2 * (10^2 + 20^2 + 50^2) = {gradient_per_unit_of_distance}")
print()
print(f"{'weight':>10} {'distance':>10} {'gradient run':>14} {'6000 x distance':>17}")
print("-" * 55)
for weight in [0.5, 0.3, -0.1, 1.1, -1.3]:
    distance = weight - TRUE_WEIGHT
    print(f"{weight:>10.2f} {distance:>10.2f} {gradient_of_loss(weight):>14.2f} "
          f"{gradient_per_unit_of_distance * distance:>17.2f}")

# ----------------------------------------------------------------------------
# Part 2.  Put that gradient into the update rule and the whole step collapses
#          into one multiplication.
#
#     new_weight   = weight - learning_rate * 6000 * (weight - 0.3)
#     new_distance = distance * (1 - 6000 * learning_rate)
#
#          |multiplier| < 1  ->  shrinks, converges
#          multiplier  < 0   ->  crosses to the other side of the valley
#          |multiplier| > 1  ->  grows, and keeps growing
# ----------------------------------------------------------------------------

print()
print("Part 2 - one multiplier decides everything")
print()

def multiplier_for(learning_rate):
    return 1 - gradient_per_unit_of_distance * learning_rate


def trace(starting_weight, learning_rate, number_of_steps=6):
    multiplier = multiplier_for(learning_rate)

    if abs(multiplier) < 1:
        verdict = "converges" if multiplier > 0 else "oscillates inward"
    elif abs(multiplier) == 1:
        verdict = "bounces forever, never settles"
    else:
        verdict = "EXPLODES"

    print(f"learning rate {learning_rate}   "
          f"multiplier = 1 - {gradient_per_unit_of_distance} x {learning_rate} "
          f"= {multiplier:+.2f}   -> {verdict}")
    print(f"{'step':>5} {'weight':>12} {'distance':>12} {'loss':>16}")
    print("-" * 49)

    weight = starting_weight
    for step in range(number_of_steps + 1):
        print(f"{step:>5} {weight:>12.4f} {weight - TRUE_WEIGHT:>12.4f} "
              f"{total_loss(weight):>16.4f}")
        weight = weight - learning_rate * gradient_of_loss(weight)
    print()


trace(starting_weight=0.5, learning_rate=0.0001)
trace(starting_weight=0.5, learning_rate=0.0003)
trace(starting_weight=0.5, learning_rate=0.0005)

# ----------------------------------------------------------------------------
# Part 3.  Where the cliff edge is.
#
#     converges while  |1 - 6000 * learning_rate| < 1
#     which means      0 < learning_rate < 2 / 6000
# ----------------------------------------------------------------------------

largest_learning_rate_that_works = 2 / gradient_per_unit_of_distance

print("Part 3 - the exact cliff edge for THIS problem")
print(f"  converges while 0 < learning rate < 2/{gradient_per_unit_of_distance} "
      f"= {largest_learning_rate_that_works:.6f}")
print()
print(f"{'learning rate':>15} {'multiplier':>12} {'loss after 20 steps':>22}")
print("-" * 51)
for learning_rate in [0.0001, 0.0003, 0.000333, 0.000334, 0.0004, 0.0005]:
    weight = 0.5
    for _ in range(20):
        weight = weight - learning_rate * gradient_of_loss(weight)
    print(f"{learning_rate:>15} {multiplier_for(learning_rate):>12.4f} "
          f"{total_loss(weight):>22.6g}")

print()
print("Nothing in the code knows where 0.3 is, and nothing knows about the cliff.")
print("Both fall out of the data: 6000 came from the candidate counts alone.")
print("Change candidate_counts to [100, 200, 500] and the safe learning rate")
print("becomes 100 times smaller. That is why learning rates are tuned, not chosen.")
