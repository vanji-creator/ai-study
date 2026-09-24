# With ONE parameter the loss is a curve. With TWO it is a surface - a bowl.
# Drawn here as a contour map: weight across, bias up, and the character shows
# how high the loss is at that point.
#
#     data:  input 1 -> 5 seconds,  input 3 -> 11 seconds
#     truth: weight 3, bias 2
#
# Run: python3 code/block-00/the_loss_is_a_surface.py

input_values = [1, 3]
actual_times_seconds = [5, 11]
LEARNING_RATE = 0.05


def loss_at(weight, bias):
    total = 0.0
    for input_value, actual in zip(input_values, actual_times_seconds):
        error = weight * input_value + bias - actual
        total += error ** 2
    return total


def gradients_at(weight, bias):
    gradient_for_weight = gradient_for_bias = 0.0
    for input_value, actual in zip(input_values, actual_times_seconds):
        error = weight * input_value + bias - actual
        gradient_for_weight += 2 * input_value * error
        gradient_for_bias += 2 * error
    return gradient_for_weight, gradient_for_bias


# Loss bands, lowest first. The character says which band a point falls in.
BANDS = [(0.01, "#"), (0.1, "@"), (1.0, "%"), (5.0, "*"),
         (20.0, "+"), (60.0, "-"), (200.0, "."), (float("inf"), " ")]


def band_character(loss):
    for ceiling, character in BANDS:
        if loss < ceiling:
            return character
    return " "


def draw_contour_map(weight_left, weight_right, bias_bottom, bias_top,
                     path=(), width=69, height=25, title=""):
    grid = []
    for row_index in range(height):
        bias = bias_top - row_index * (bias_top - bias_bottom) / (height - 1)
        row = []
        for column_index in range(width):
            weight = weight_left + column_index * (weight_right - weight_left) / (width - 1)
            row.append(band_character(loss_at(weight, bias)))
        grid.append(row)

    # stamp the descent path on top, numbered 0,1,2,...
    for step_number, (weight, bias) in enumerate(path):
        column_index = round((weight - weight_left) / (weight_right - weight_left) * (width - 1))
        row_index = round((bias_top - bias) / (bias_top - bias_bottom) * (height - 1))
        if 0 <= row_index < height and 0 <= column_index < width:
            grid[row_index][column_index] = str(step_number) if step_number < 10 else "x"

    print(title)
    print()
    for row_index, row in enumerate(grid):
        bias = bias_top - row_index * (bias_top - bias_bottom) / (height - 1)
        label = f"{bias:>6.2f}" if row_index % 3 == 0 else "      "
        print(f"{label} |" + "".join(row))
    print("       +" + "-" * width)
    axis = [" "] * width
    weight_tick = weight_left
    while weight_tick <= weight_right + 1e-9:
        column_index = round((weight_tick - weight_left) / (weight_right - weight_left) * (width - 1))
        text = f"{weight_tick:g}"
        for offset, character in enumerate(text):
            if 0 <= column_index + offset < width:
                axis[column_index + offset] = character
        weight_tick += (weight_right - weight_left) / 6
    print("        " + "".join(axis))
    print("  bias                          weight")
    print()


print("  loss bands:   # under 0.01    @ under 0.1    % under 1    * under 5")
print("                + under 20      - under 60     . under 200")
print()

# the descent path from the hand exercise
weight, bias = 1.0, 1.0
path = [(weight, bias)]
for _ in range(9):
    gradient_for_weight, gradient_for_bias = gradients_at(weight, bias)
    weight -= LEARNING_RATE * gradient_for_weight
    bias -= LEARNING_RATE * gradient_for_bias
    path.append((weight, bias))

draw_contour_map(-1.0, 7.0, -3.0, 7.0, path=path,
                 title="PICTURE 1 - the whole bowl. 0 is where you started, then each step.")

print("  The bottom of the bowl is the single point weight 3, bias 2.")
print("  Notice the bowl is not round. It is a long, thin, tilted trough.")
print()
print()

draw_contour_map(2.0, 4.0, 1.0, 3.0, path=path,
                 title="PICTURE 2 - the same bowl, zoomed in around the answer.")

print("  Now the trough is obvious. Along the trough the ground is almost flat,")
print("  so the gradient is tiny and progress is slow. Across it the walls are")
print("  steep. Step 1 fell down a wall in one jump; everything after that is a")
print("  slow crawl along the floor.")
print()

print(f"{'step':>5} {'weight':>9} {'bias':>9} {'loss':>12} "
      f"{'grad weight':>12} {'grad bias':>11}")
print("-" * 62)
for step_number, (weight, bias) in enumerate(path):
    gradient_for_weight, gradient_for_bias = gradients_at(weight, bias)
    print(f"{step_number:>5} {weight:>9.4f} {bias:>9.4f} {loss_at(weight, bias):>12.6f} "
          f"{gradient_for_weight:>12.4f} {gradient_for_bias:>11.4f}")

print()
print("  Loss: 58 -> 1.6 -> 0.05 in three steps, then 0.008, 0.0066, 0.0061 ...")
print("  That is the trough. The steep direction was fixed almost immediately.")
print("  The flat direction takes hundreds of steps.")
print()
print("  This shape is why plain gradient descent is rarely used as-is on real")
print("  models, and why optimisers such as momentum and Adam exist: they are")
print("  ways of moving faster along the flat direction without exploding up the")
print("  steep one. We are not covering those yet - just know the shape is the reason.")
