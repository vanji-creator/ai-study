# Forward pass and backward pass for one tiny model, one data row.
#
#   z    = (x * w) + b            stage 1: a weight and a bias
#   h    = ReLU(z)                stage 2: negative becomes 0, otherwise unchanged
#   loss = 0.5 * (h - y) ** 2     how wrong the model is
#
# Run: python3 code/block-00/backprop_by_hand.py

input_value = 2          # x, the data
weight = 3               # w, a number we may change
bias = 1                 # b, a number we may change
actual = 5               # y, the correct answer


def relu(value):
    """If the value is negative it becomes 0, otherwise it is left alone."""
    return max(0, value)


def forward(weight, bias):
    """Run the model from the input to the loss and keep every value along the way."""
    z_value = (input_value * weight) + bias
    hidden_value = relu(z_value)
    loss = 0.5 * (hidden_value - actual) ** 2
    return z_value, hidden_value, loss


# ---------------------------------------------------------------------------
# Forward pass: input -> z -> h -> loss
# ---------------------------------------------------------------------------
z_value, hidden_value, loss = forward(weight, bias)
print("FORWARD PASS")
print(f"  z    = ({input_value} x {weight}) + {bias} = {z_value}")
print(f"  h    = ReLU({z_value}) = {hidden_value}")
print(f"  loss = 0.5 x ({hidden_value} - {actual})^2 = {loss}")
print()

# ---------------------------------------------------------------------------
# Backward pass: start at the loss and walk back, one box at a time.
# Each line is the slope of ONE box: how much its output moves when its input moves by 1.
# ---------------------------------------------------------------------------
loss_slope_per_hidden = hidden_value - actual          # box: loss = 0.5 * (h - y)^2
hidden_slope_per_z = 1 if z_value > 0 else 0           # box: h = ReLU(z)
z_slope_per_weight = input_value                       # box: z = x * w + b
z_slope_per_bias = 1                                   # box: z = x * w + b

# The chain: multiply the slopes of the boxes between the loss and the number we want.
gradient_of_z = loss_slope_per_hidden * hidden_slope_per_z
gradient_of_weight = gradient_of_z * z_slope_per_weight
gradient_of_bias = gradient_of_z * z_slope_per_bias

print("BACKWARD PASS")
print(f"  loss slope per h     = h - y           = {loss_slope_per_hidden}")
print(f"  h slope per z        = (1 if z > 0)    = {hidden_slope_per_z}")
print(f"  gradient of z        = {loss_slope_per_hidden} x {hidden_slope_per_z} = {gradient_of_z}")
print(f"  z slope per weight   = x               = {z_slope_per_weight}")
print(f"  z slope per bias     = 1               = {z_slope_per_bias}")
print(f"  gradient of weight   = {gradient_of_z} x {z_slope_per_weight} = {gradient_of_weight}")
print(f"  gradient of bias     = {gradient_of_z} x {z_slope_per_bias} = {gradient_of_bias}")
print()

# ---------------------------------------------------------------------------
# Check by nudging: no chain rule, just move one number a tiny step and watch the loss.
# ---------------------------------------------------------------------------
tiny_step = 0.0001
_, _, loss_after_weight_nudge = forward(weight + tiny_step, bias)
_, _, loss_after_bias_nudge = forward(weight, bias + tiny_step)
print("CHECK BY NUDGING")
print(f"  weight: {(loss_after_weight_nudge - loss) / tiny_step:.3f}   (backward pass said {gradient_of_weight})")
print(f"  bias  : {(loss_after_bias_nudge - loss) / tiny_step:.3f}   (backward pass said {gradient_of_bias})")
print()

# ---------------------------------------------------------------------------
# One update with learning rate 0.1: new = old - (learning_rate x gradient)
# ---------------------------------------------------------------------------
learning_rate = 0.1
new_weight = weight - (learning_rate * gradient_of_weight)
new_bias = bias - (learning_rate * gradient_of_bias)
_, _, new_loss = forward(new_weight, new_bias)
print("UPDATE (learning rate 0.1)")
print(f"  new weight = {weight} - (0.1 x {gradient_of_weight}) = {new_weight}")
print(f"  new bias   = {bias} - (0.1 x {gradient_of_bias}) = {new_bias}")
print(f"  loss goes from {loss} to {new_loss}")
print()

# ---------------------------------------------------------------------------
# What if z were negative? Change bias to -9 to see: ReLU blocks the whole backward pass.
# ---------------------------------------------------------------------------
z_negative, h_negative, _ = forward(weight, -9)
print("WHEN ReLU BLOCKS (bias = -9)")
print(f"  z = {z_negative}, h = {h_negative}, h slope per z = {1 if z_negative > 0 else 0}"
      f"  -> every gradient behind that box is 0")
