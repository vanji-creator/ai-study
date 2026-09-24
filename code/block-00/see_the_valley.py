# Drawing the loss as a picture, so "gradient" stops being a word and becomes a slope.
#
# Same problem you did by hand:
#     input = 2 (hundreds of candidates), actual = 6 seconds, true weight = 3
#
# Run: python3 code/block-00/see_the_valley.py

INPUT = 2
ACTUAL_SECONDS = 6
LEARNING_RATE = 0.1


def loss_at(weight):
    """How wrong this weight is. One number."""
    predicted = weight * INPUT
    error = predicted - ACTUAL_SECONDS
    return error ** 2


def gradient_at(weight):
    """The steepness of the loss curve at this weight. 2 * input * error."""
    predicted = weight * INPUT
    error = predicted - ACTUAL_SECONDS
    return 2 * INPUT * error


# ---------------------------------------------------------------------------
# A small ASCII plotter. Nothing clever: a grid of characters, and we work out
# which row and column each (weight, loss) pair falls into.
# ---------------------------------------------------------------------------

CANVAS_WIDTH = 71
CANVAS_HEIGHT = 21
WEIGHT_LEFT, WEIGHT_RIGHT = 0.0, 6.0
LOSS_BOTTOM, LOSS_TOP = 0.0, 40.0


def column_for_weight(weight):
    fraction = (weight - WEIGHT_LEFT) / (WEIGHT_RIGHT - WEIGHT_LEFT)
    return round(fraction * (CANVAS_WIDTH - 1))


def row_for_loss(loss):
    fraction = (loss - LOSS_BOTTOM) / (LOSS_TOP - LOSS_BOTTOM)
    return (CANVAS_HEIGHT - 1) - round(fraction * (CANVAS_HEIGHT - 1))


def blank_canvas():
    return [[" "] * CANVAS_WIDTH for _ in range(CANVAS_HEIGHT)]


def draw_point(canvas, weight, loss, mark):
    column = column_for_weight(weight)
    row = row_for_loss(loss)
    if 0 <= row < CANVAS_HEIGHT and 0 <= column < CANVAS_WIDTH:
        canvas[row][column] = mark


def draw_loss_curve(canvas, mark="."):
    steps = CANVAS_WIDTH * 4          # denser than the grid, so no gaps appear
    for step in range(steps + 1):
        weight = WEIGHT_LEFT + (WEIGHT_RIGHT - WEIGHT_LEFT) * step / steps
        draw_point(canvas, weight, loss_at(weight), mark)


def print_canvas(canvas, title):
    print(title)
    print()
    for row_index, row in enumerate(canvas):
        loss_value = LOSS_TOP - row_index * (LOSS_TOP - LOSS_BOTTOM) / (CANVAS_HEIGHT - 1)
        label = f"{loss_value:>5.0f}" if row_index % 2 == 0 else "     "
        print(f"{label} |" + "".join(row))
    print("      +" + "-" * CANVAS_WIDTH)
    axis = [" "] * CANVAS_WIDTH
    for weight_tick in range(int(WEIGHT_RIGHT) + 1):
        column = column_for_weight(weight_tick)
        axis[column] = str(weight_tick)
    print("       " + "".join(axis))
    print(" loss                            weight")
    print()


# ---------------------------------------------------------------------------
# Picture 1. The loss is a function of the weight. Draw the function.
# ---------------------------------------------------------------------------

canvas = blank_canvas()
draw_loss_curve(canvas)
print_canvas(canvas, "PICTURE 1  -  the loss curve: one dot for every possible weight")

print("  Every dot is one setting of the knob, and how wrong it is.")
print("  weight 0 -> loss 36      weight 3 -> loss 0      weight 6 -> loss 36")
print("  Training means: get to the bottom, without being allowed to see this picture.")
print()
print()

# ---------------------------------------------------------------------------
# Picture 2. The gradient IS the steepness of this curve, at one spot.
#            Draw the straight line that just touches the curve at weight 5.
# ---------------------------------------------------------------------------

def draw_tangent_line(canvas, weight_here, mark):
    """The straight line with the same steepness as the curve at weight_here."""
    loss_here = loss_at(weight_here)
    slope = gradient_at(weight_here)
    steps = CANVAS_WIDTH * 4
    for step in range(steps + 1):
        weight = WEIGHT_LEFT + (WEIGHT_RIGHT - WEIGHT_LEFT) * step / steps
        loss_on_the_line = loss_here + slope * (weight - weight_here)
        draw_point(canvas, weight, loss_on_the_line, mark)


for weight_here in [5.0, 3.4, 3.0]:
    canvas = blank_canvas()
    draw_tangent_line(canvas, weight_here, "-")
    draw_loss_curve(canvas)
    draw_point(canvas, weight_here, loss_at(weight_here), "O")
    print_canvas(canvas,
                 f"PICTURE 2  -  standing at weight {weight_here}.  "
                 f"O is you, the straight line is the ground under your feet.")
    print(f"  loss here     = {loss_at(weight_here):.4f}")
    print(f"  gradient here = {gradient_at(weight_here):.4f}   "
          f"<- the tilt of that straight line")
    print()

print("  Steep tilt far away. Flat at the bottom. The gradient is that tilt,")
print("  as a number. It is not a separate idea from the picture - it IS the picture,")
print("  measured at one spot.")
print()
print()

# ---------------------------------------------------------------------------
# Picture 3. The walk you did by hand, drawn on the curve.
# ---------------------------------------------------------------------------

canvas = blank_canvas()
draw_loss_curve(canvas)

weight = 5.0
walk = []
for step_number in range(6):
    walk.append(weight)
    draw_point(canvas, weight, loss_at(weight), str(step_number))
    weight = weight - LEARNING_RATE * gradient_at(weight)

print_canvas(canvas, "PICTURE 3  -  your own six rows, walked down the curve")

print(f"{'step':>5} {'weight':>10} {'loss':>12} {'gradient':>12} {'step size':>12}")
print("-" * 55)
for step_number, weight in enumerate(walk):
    print(f"{step_number:>5} {weight:>10.4f} {loss_at(weight):>12.4f} "
          f"{gradient_at(weight):>12.4f} "
          f"{abs(LEARNING_RATE * gradient_at(weight)):>12.4f}")

print()
print("  The numbers 0,1,2 on the curve are your three hand-worked rows.")
print("  They bunch up near the bottom. Nothing told them to slow down -")
print("  the ground got flatter, so the gradient got smaller, so the steps got smaller.")
