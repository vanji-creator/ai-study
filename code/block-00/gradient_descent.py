# Gradient descent on one parameter, with three different learning rates.
# Run: python3 code/block-00/gradient_descent.py

candidate_counts = [10, 20, 50]
actual_times_seconds = [3, 6, 15]


def total_loss(weight):
    return sum((weight * candidates - actual_time) ** 2
               for candidates, actual_time in zip(candidate_counts, actual_times_seconds))


def gradient_of_loss(weight):
    """Exact slope of the loss at this weight.
    Each row contributes 2 * candidates * error, from the chain rule."""
    gradient = 0.0
    for candidates, actual_time in zip(candidate_counts, actual_times_seconds):
        error = weight * candidates - actual_time
        gradient += 2 * candidates * error
    return gradient


def train(starting_weight, learning_rate, number_of_steps):
    weight = starting_weight
    print(f"\nlearning rate = {learning_rate}")
    print(f"{'step':>5} {'weight':>12} {'loss':>14} {'gradient':>14}")
    print("-" * 48)
    for step in range(number_of_steps + 1):
        loss = total_loss(weight)
        gradient = gradient_of_loss(weight)
        print(f"{step:>5} {weight:>12.5f} {loss:>14.5f} {gradient:>14.2f}")
        weight = weight - learning_rate * gradient       # THE UPDATE RULE
    return weight


print("the answer we are looking for is weight = 0.3, loss = 0")

train(starting_weight=0.5, learning_rate=0.0001, number_of_steps=8)
train(starting_weight=0.5, learning_rate=0.0003, number_of_steps=8)
train(starting_weight=0.5, learning_rate=0.0005, number_of_steps=8)
