# "Will it overfit?" - yes, and here is what that looks like.
#
# Same electricity bill as bends_are_learned.py, but now the measurements carry
# small reading errors, the way real measurements do. Two models are trained on
# the SAME rows:
#
#     a small model    3 bends
#     a large model   30 bends
#
# Then both are tested on customers neither model was trained on.
#
# One row at a time - stochastic gradient descent.
#
# Run: python3 code/block-00/overfitting.py

import random

random.seed(11)


def true_bill_in_hundreds(units_in_hundreds):
    """The real slab rule. It exists, but nobody ever shows it to the models."""
    units = units_in_hundreds * 100
    bill = 5 * min(units, 100)
    if units > 100:
        bill += 8 * min(units - 100, 100)
    if units > 200:
        bill += 12 * (units - 200)
    return bill / 100


READING_ERROR = 0.8           # hundreds of rupees, so about 80 rupees either way


def measure(units_in_hundreds):
    """What you actually write down: the true bill plus a reading error."""
    return true_bill_in_hundreds(units_in_hundreds) + random.uniform(-READING_ERROR,
                                                                    READING_ERROR)


# 8 customers we have measured. This is the training data, errors included.
training_rows = []
for step in range(8):
    x = 0.3 + step * 0.4
    training_rows.append((x, measure(x)))

# 7 DIFFERENT customers, sitting between the trained ones, measured the same way.
# Neither model ever sees these.
test_rows = []
for step in range(7):
    x = 0.5 + step * 0.4
    test_rows.append((x, measure(x)))


def relu(value):
    return value if value > 0 else 0.0


def predict(x, bends, rates):
    total = 0.0
    for bend, rate in zip(bends, rates):
        total += rate * relu(x - bend)
    return total


def train(bends, learning_rate, passes):
    """Bends are fixed here so the ONLY difference between the two models is how
    many pieces they have. Only the rates are learned."""
    rates = [0.0] * len(bends)
    order = list(range(len(training_rows)))
    for _ in range(passes):
        random.shuffle(order)
        for row_index in order:
            x, actual = training_rows[row_index]
            error = predict(x, bends, rates) - actual
            for index, bend in enumerate(bends):
                gradient = 2 * (relu(x - bend) * error)
                rates[index] = rates[index] - (learning_rate * gradient)
    return rates


def average_miss(rows, bends, rates):
    return sum(abs(predict(x, bends, rates) - actual) for x, actual in rows) / len(rows)


def average_miss_against_the_truth(bends, rates):
    """How far the model is from the real slab rule, measured densely. We can only
    do this because we invented the rule; in real work this number is unavailable."""
    total = 0.0
    checks = 0
    for step in range(1, 301):
        x = step / 100
        total += abs(predict(x, bends, rates) - true_bill_in_hundreds(x))
        checks += 1
    return total / checks


small_bends = [0.0, 1.0, 2.0]
large_bends = [step * 0.1 for step in range(30)]

small_rates = train(small_bends, learning_rate=0.004, passes=12000)
large_rates = train(large_bends, learning_rate=0.004, passes=12000)

print("8 customers measured, with reading errors of up to about 80 rupees.")
print("Two models trained on exactly those 8 rows.")
print()
print(f"{'':>14} {'pieces':>8} {'miss on the 8':>15} "
      f"{'miss on 7 unseen':>18} {'miss vs the rule':>18}")
print("-" * 80)
for label, bends, rates in [("small model", small_bends, small_rates),
                            ("large model", large_bends, large_rates)]:
    print(f"{label:>14} {len(bends):>8} "
          f"{average_miss(training_rows, bends, rates) * 100:>12.0f} rs "
          f"{average_miss(test_rows, bends, rates) * 100:>15.0f} rs "
          f"{average_miss_against_the_truth(bends, rates) * 100:>15.0f} rs")

print()
print("The large model is BETTER on the rows it was trained on and WORSE on")
print("everybody else. That gap is overfitting, and it is the only thing that")
print("matters, because every real customer is an unseen customer.")
print()

print("Customer by customer, on the seven neither model was shown:")
print()
print(f"{'units':>7} {'measured':>10} {'true bill':>11} "
      f"{'small says':>12} {'large says':>12}")
print("-" * 56)
for x, measured in test_rows:
    print(f"{x * 100:>7.0f} {measured * 100:>10.0f} {true_bill_in_hundreds(x) * 100:>11.0f} "
          f"{predict(x, small_bends, small_rates) * 100:>12.0f} "
          f"{predict(x, large_bends, large_rates) * 100:>12.0f}")

print()
print("And what each model thinks the rate is, between two training points:")
print()
print(f"{'from':>6} {'to':>6} {'true rate':>11} {'small':>9} {'large':>9}")
print("-" * 46)
for start_units in [60, 110, 160, 210, 260]:
    end_units = start_units + 10
    start, end = start_units / 100, end_units / 100
    true_rate = (true_bill_in_hundreds(end) - true_bill_in_hundreds(start)) / (end - start)
    small_rate = (predict(end, small_bends, small_rates)
                  - predict(start, small_bends, small_rates)) / (end - start)
    large_rate = (predict(end, large_bends, large_rates)
                  - predict(start, large_bends, large_rates)) / (end - start)
    print(f"{start_units:>6} {end_units:>6} {true_rate:>11.2f} "
          f"{small_rate:>9.2f} {large_rate:>9.2f}")

print()
print("The small model has three pieces, and the rule has three slabs, so its only")
print("way to reduce the loss is to find the rule. The large model has thirty pieces")
print("and eight rows, so it has spare pieces with nothing to do - and it spends them")
print("bending towards the reading errors, which are not part of any rule.")
