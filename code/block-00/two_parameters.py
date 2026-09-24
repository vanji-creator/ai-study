# Gradient descent with TWO parameters: a weight and a bias.
#
#     predicted = weight * input + bias
#
# The data needs a bias of 2, so the one-parameter version could never fit it:
#     input 1 -> 5 seconds        input 3 -> 11 seconds        truth: 3 * input + 2
#
# Run: python3 code/block-00/two_parameters.py

input_values = [1, 3]
actual_times_seconds = [5, 11]

LEARNING_RATE = 0.05


def one_step(weight, bias, show_working=False):
    """Compute the loss and both gradients, then return the updated parameters.

    Both gradients are worked out from the SAME errors, before either parameter
    moves. That is the only new idea compared with the one-parameter version.
    """
    total_loss = 0.0
    gradient_for_weight = 0.0
    gradient_for_bias = 0.0

    for input_value, actual in zip(input_values, actual_times_seconds):
        predicted = weight * input_value + bias
        error = predicted - actual

        total_loss += error ** 2
        gradient_for_weight += 2 * input_value * error    # weight's input is the data
        gradient_for_bias += 2 * 1 * error                # bias's input is always 1

        if show_working:
            print(f"    input {input_value}, actual {actual}:  "
                  f"predicted = {weight} x {input_value} + {bias} = {predicted},  "
                  f"error = {predicted} - {actual} = {error}")

    if show_working:
        print(f"    loss            = {total_loss}")
        print(f"    gradient weight = {gradient_for_weight}")
        print(f"    gradient bias   = {gradient_for_bias}")

    new_weight = weight - LEARNING_RATE * gradient_for_weight
    new_bias = bias - LEARNING_RATE * gradient_for_bias
    return new_weight, new_bias, total_loss, gradient_for_weight, gradient_for_bias


print("STEP 1, with the working shown")
print()
weight, bias = 1.0, 1.0
new_weight, new_bias, *_ = one_step(weight, bias, show_working=True)
print(f"    new weight = {weight} - {LEARNING_RATE} x -48.0 = {new_weight}")
print(f"    new bias   = {bias} - {LEARNING_RATE} x -20.0 = {new_bias}")
print()
print()

print("EVERY STEP")
print()
print(f"{'step':>5} {'weight':>9} {'bias':>9} {'loss':>12} "
      f"{'grad weight':>12} {'grad bias':>11}")
print("-" * 62)

weight, bias = 1.0, 1.0
for step_number in range(13):
    new_weight, new_bias, loss, gradient_for_weight, gradient_for_bias = one_step(weight, bias)
    print(f"{step_number:>5} {weight:>9.4f} {bias:>9.4f} {loss:>12.6f} "
          f"{gradient_for_weight:>12.4f} {gradient_for_bias:>11.4f}")
    weight, bias = new_weight, new_bias

print()
print("target: weight 3, bias 2, loss 0")
print()
print("Notice the weight and the bias do NOT arrive together, and neither moves")
print("in a straight line to its answer. They are coupled: a bias that is too low")
print("makes the errors look like the weight is too low, so the weight overshoots")
print("first and comes back. One shared loss, two knobs, pulling on each other.")
