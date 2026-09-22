# Standing at one weight, look at the loss just to the right of it.
# The change tells you which way is downhill, and how steep the ground is.
# Run: python3 code/block-00/slope_by_two_points.py

candidate_counts = [10, 20, 50]
actual_times_seconds = [3, 6, 15]


def total_loss(weight):
    loss = 0.0
    for candidates, actual_time in zip(candidate_counts, actual_times_seconds):
        error = weight * candidates - actual_time
        loss += error ** 2
    return loss


tiny_step = 0.01     # how far to the right we peek

print(f"{'weight':>7} {'loss here':>10} {'loss a tiny step right':>24} {'change':>9} {'slope':>10}")
print("-" * 68)

for weight in [0.00, 0.10, 0.20, 0.29, 0.30, 0.31, 0.40, 0.50]:
    loss_here = total_loss(weight)
    loss_to_the_right = total_loss(weight + tiny_step)
    change = loss_to_the_right - loss_here
    slope = change / tiny_step          # rise divided by run
    print(f"{weight:>7.2f} {loss_here:>10.2f} {loss_to_the_right:>24.2f} "
          f"{change:>9.2f} {slope:>10.1f}")

print()
print("sign of the slope  -> which direction is downhill")
print("size of the slope  -> how steep the ground is where you are standing")
