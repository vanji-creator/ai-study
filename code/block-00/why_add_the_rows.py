# Two questions, both asked by Vikash:
#
#   1. Why add the rows together instead of handling them one at a time?
#   2. If we do add them, shouldn't we divide by the number of rows?
#
# Run: python3 code/block-00/why_add_the_rows.py

input_values = [1, 3]
actual_times_seconds = [5, 11]        # truth: predicted = 3 * input + 2

TRUE_WEIGHT, TRUE_BIAS = 3, 2


def predict(weight, bias, input_value):
    return weight * input_value + bias


# ---------------------------------------------------------------------------
# Part 1.  THE REASON WE ADD: there is only one weight, and it must serve
#          every row at once.
# ---------------------------------------------------------------------------

print("Part 1 - why the rows cannot be solved separately")
print()
print("  What weight and bias fit ONLY row 1 (input 1 -> 5 seconds)?")
print("    weight 3, bias 2  gives 5.  correct")
print("    weight 0, bias 5  gives 5.  also correct")
print("    weight 4, bias 1  gives 5.  also correct")
print()
print("  Row 1 alone has infinitely many perfect answers. Same for row 2 alone.")
print("  Only ONE pair fits both at the same time. That is why the loss has to be")
print("  a single number covering all the data: there is one knob, not one per row.")
print()

print("  Check that claim - each row's own best fit, and what it does to the other:")
print()
print(f"{'fits':>8} {'weight':>8} {'bias':>7} {'row 1 error':>13} {'row 2 error':>13}")
print("-" * 54)
for label, weight, bias in [("row 1", 0, 5), ("row 1", 4, 1),
                            ("row 2", 0, 11), ("row 2", 4, -1),
                            ("both", TRUE_WEIGHT, TRUE_BIAS)]:
    errors = [predict(weight, bias, i) - a
              for i, a in zip(input_values, actual_times_seconds)]
    print(f"{label:>8} {weight:>8} {bias:>7} {errors[0]:>13} {errors[1]:>13}")

print()
print()

# ---------------------------------------------------------------------------
# Part 2.  Vikash's instinct - one row at a time - IS a real algorithm.
#          It works, it zig-zags, and it has a name.
# ---------------------------------------------------------------------------

LEARNING_RATE = 0.05


def train_on_all_rows_together(number_of_steps):
    """Add every row's contribution, then take one step. 'Batch' gradient descent."""
    weight, bias = 1.0, 1.0
    history = []
    for _ in range(number_of_steps):
        gradient_for_weight = gradient_for_bias = 0.0
        for input_value, actual in zip(input_values, actual_times_seconds):
            error = predict(weight, bias, input_value) - actual
            gradient_for_weight += 2 * input_value * error
            gradient_for_bias += 2 * error
        weight -= LEARNING_RATE * gradient_for_weight
        bias -= LEARNING_RATE * gradient_for_bias
        history.append((weight, bias))
    return history


def train_one_row_at_a_time(number_of_steps):
    """Take a step after EVERY row. This is stochastic gradient descent."""
    weight, bias = 1.0, 1.0
    history = []
    row_index = 0
    for _ in range(number_of_steps):
        input_value = input_values[row_index]
        actual = actual_times_seconds[row_index]
        error = predict(weight, bias, input_value) - actual
        weight -= LEARNING_RATE * (2 * input_value * error)
        bias -= LEARNING_RATE * (2 * error)
        history.append((weight, bias))
        row_index = (row_index + 1) % len(input_values)
    return history


print("Part 2 - your idea (one row at a time) against adding them")
print()
print(f"{'step':>5}   {'all rows added':>22}   {'one row at a time':>22}")
print(f"{'':>5}   {'weight':>10} {'bias':>11}   {'weight':>10} {'bias':>11}")
print("-" * 60)

together = train_on_all_rows_together(8)
separately = train_one_row_at_a_time(8)
for step_number, ((weight_a, bias_a), (weight_b, bias_b)) in enumerate(
        zip(together, separately), start=1):
    print(f"{step_number:>5}   {weight_a:>10.4f} {bias_a:>11.4f}   "
          f"{weight_b:>10.4f} {bias_b:>11.4f}")

print()
print("  Both reach roughly weight 3, bias 2. Your instinct is NOT wrong.")
print("  Taking a step after every row is a real, named algorithm: stochastic")
print("  gradient descent. It is what real models actually use, because adding up")
print("  every row first is impossible when there are billions of rows.")
print()
print("  The difference is the path, not the destination. One row at a time steps")
print("  in the direction that is right for THAT row, which is the wrong direction")
print("  for the others, so it zig-zags. Adding the rows first gives the direction")
print("  that is least wrong for all of them at once.")
print()
print()

# ---------------------------------------------------------------------------
# Part 3.  Should we divide by the number of rows?  Yes, you may. It changes
#          nothing except the size, and the learning rate absorbs it exactly.
# ---------------------------------------------------------------------------

print("Part 3 - sum or average? the learning rate absorbs the whole difference")
print()

def train(use_average, learning_rate, number_of_steps):
    weight, bias = 1.0, 1.0
    history = []
    number_of_rows = len(input_values)
    for _ in range(number_of_steps):
        gradient_for_weight = gradient_for_bias = 0.0
        for input_value, actual in zip(input_values, actual_times_seconds):
            error = predict(weight, bias, input_value) - actual
            gradient_for_weight += 2 * input_value * error
            gradient_for_bias += 2 * error
        if use_average:
            gradient_for_weight /= number_of_rows
            gradient_for_bias /= number_of_rows
        weight -= learning_rate * gradient_for_weight
        bias -= learning_rate * gradient_for_bias
        history.append((weight, bias))
    return history


summed = train(use_average=False, learning_rate=0.05, number_of_steps=6)
averaged = train(use_average=True, learning_rate=0.10, number_of_steps=6)

print("  sum of squared errors, learning rate 0.05")
print("  average (mean) squared error, learning rate 0.10   <- twice the rate, 2 rows")
print()
print(f"{'step':>5}   {'summed':>22}   {'averaged':>22}   {'same?':>6}")
print(f"{'':>5}   {'weight':>10} {'bias':>11}   {'weight':>10} {'bias':>11}")
print("-" * 70)
for step_number, ((weight_s, bias_s), (weight_a, bias_a)) in enumerate(
        zip(summed, averaged), start=1):
    identical = abs(weight_s - weight_a) < 1e-12 and abs(bias_s - bias_a) < 1e-12
    print(f"{step_number:>5}   {weight_s:>10.4f} {bias_s:>11.4f}   "
          f"{weight_a:>10.4f} {bias_a:>11.4f}   {'yes' if identical else 'NO':>6}")

print()
print("  Identical, every step. Dividing by the number of rows makes every gradient")
print("  2 times smaller here, and doubling the learning rate puts it straight back.")
print()
print("  So: sum or average is a CONVENTION, not a law. It changes the size of the")
print("  gradient, never its direction, and the learning rate cancels the change.")
print()
print("  Why almost everybody divides anyway: with the average, the learning rate")
print("  keeps working when you change how many rows you look at per step.")

print()
for number_of_rows in [2, 8, 1000]:
    print(f"    {number_of_rows:>4} rows  ->  summed gradient is about {number_of_rows} times "
          f"bigger; averaged gradient stays the same size")
print()
print("  With the sum, moving from 8 rows per step to 1000 would multiply every")
print("  gradient by 125 and blow the model up unless you also changed the learning")
print("  rate. With the average, you change nothing. That is the only reason.")
