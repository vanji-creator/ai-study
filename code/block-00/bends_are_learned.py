# Nobody tells the model where the bends go. It finds them.
#
# The problem is the electricity bill with slabs:
#     first 100 units  at 5 per unit
#     next  100 units  at 8 per unit
#     above 200 units  at 12 per unit
#
# Working in HUNDREDS of units and HUNDREDS of rupees keeps every number small:
#     x = units / 100      y = bill / 100
#     the true answer is then rates 5, 3, 4 with bends at 0, 1 and 2
#
# One row at a time - stochastic gradient descent.
#
# Run: python3 code/block-00/bends_are_learned.py

import random


def true_bill_in_hundreds(units_in_hundreds):
    """The real slab bill, computed slab by slab, for checking against."""
    units = units_in_hundreds * 100
    bill = 0.0
    bill += 5 * min(units, 100)
    if units > 100:
        bill += 8 * min(units - 100, 100)
    if units > 200:
        bill += 12 * (units - 200)
    return bill / 100


# The measurements. This is all the model is ever shown.
training_rows = []
for step in range(1, 31):
    units_in_hundreds = step / 10
    training_rows.append((units_in_hundreds, true_bill_in_hundreds(units_in_hundreds)))


def relu(value):
    return value if value > 0 else 0.0


def predict(x, bends, rates):
    """Three straight pieces, each doing nothing until x passes its bend."""
    total = 0.0
    for bend, rate in zip(bends, rates):
        total += rate * relu(x - bend)
    return total


def train(bends, rates, learning_rate, passes):
    """One row at a time. After every single row, every parameter takes a step."""
    order = list(range(len(training_rows)))
    for pass_number in range(passes):
        random.shuffle(order)
        for row_index in order:
            x, actual = training_rows[row_index]

            predicted = predict(x, bends, rates)
            error = predicted - actual

            # Work out every gradient from this one error BEFORE moving anything.
            gradient_for_rates = []
            gradient_for_bends = []
            for bend, rate in zip(bends, rates):
                inside = x - bend
                passed_the_bend = 1.0 if inside > 0 else 0.0

                # the rate multiplies whatever got through the floor
                gradient_for_rates.append(2 * (relu(inside) * error))

                # moving the bend RIGHT moves the inside DOWN, hence the minus one
                gradient_for_bends.append(2 * (error * rate * passed_the_bend * -1.0))

            for index in range(len(bends)):
                rates[index] = rates[index] - (learning_rate * gradient_for_rates[index])
                bends[index] = bends[index] - (learning_rate * gradient_for_bends[index])

        if pass_number in (0, 4, 19, 99, 499, passes - 1):
            total_loss = sum((predict(x, bends, rates) - actual) ** 2
                             for x, actual in training_rows)
            print(f"  after pass {pass_number + 1:>4}   "
                  f"bends {[round(b, 3) for b in bends]}   "
                  f"rates {[round(r, 3) for r in rates]}   "
                  f"loss {total_loss:.6f}")

    return bends, rates


random.seed(7)

print("the truth, which the model is never told:")
print("  bends at 0, 1, 2   rates 5, 3, 4")
print()
print("starting guess, deliberately wrong:")
starting_bends = [0.4, 1.7, 2.6]
starting_rates = [1.0, 1.0, 1.0]
print(f"  bends {starting_bends}   rates {starting_rates}")
print()

print("training, one row at a time:")
bends, rates = train(list(starting_bends), list(starting_rates),
                     learning_rate=0.002, passes=3000)
print()

print("what it ended up with:")
print(f"  bends {[round(b, 3) for b in bends]}")
print(f"  rates {[round(r, 3) for r in rates]}")
print()

print("does it reproduce the bill?")
print(f"{'units':>7} {'real bill':>11} {'model':>10} {'off by':>9}")
print("-" * 40)
worst = 0.0
for units in [50, 100, 150, 200, 250, 300]:
    x = units / 100
    real = true_bill_in_hundreds(x) * 100
    model = predict(x, bends, rates) * 100
    worst = max(worst, abs(model - real))
    print(f"{units:>7} {real:>11.0f} {model:>10.1f} {model - real:>9.1f}")

print()
print(f"worst error across those six customers: {worst:.2f} rupees")
