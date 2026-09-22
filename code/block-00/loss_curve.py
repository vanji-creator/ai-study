# The loss for many different weights, so you can see the shape.
# Run: python3 code/block-00/loss_curve.py

# The measurements we are trying to fit.
candidate_counts = [10, 20, 50]
actual_times_seconds = [3, 6, 15]


def total_loss(weight):
    """Sum of squared errors for one value of the weight."""
    loss = 0.0
    for candidates, actual_time in zip(candidate_counts, actual_times_seconds):
        predicted_time = weight * candidates
        error = predicted_time - actual_time
        loss += error ** 2
    return loss


print(f"{'weight':>7} {'loss':>9}   shape")
print("-" * 60)

weights_to_try = [round(0.05 * step, 2) for step in range(0, 13)]
largest_loss = max(total_loss(weight) for weight in weights_to_try)

for weight in weights_to_try:
    loss = total_loss(weight)
    bar_length = int(44 * loss / largest_loss)
    marker = "  <- lowest" if loss == min(total_loss(w) for w in weights_to_try) else ""
    print(f"{weight:>7.2f} {loss:>9.2f}   {'#' * bar_length}{marker}")
