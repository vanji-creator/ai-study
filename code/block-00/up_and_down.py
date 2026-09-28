# "Can the line go down and then up again?"  -  yes, and here is the only thing needed.
#
# Four measurements that go up, down, then up:
#     1 -> 20     2 -> 40     3 -> 30     4 -> 60
#
# Run: python3 code/block-00/up_and_down.py

inputs  = [1, 2, 3, 4]
actuals = [20, 40, 30, 60]

bends = [0, 1, 2, 3]          # one bend just before each measurement


def relu(value):
    return value if value > 0 else 0.0


def predict(x, rates):
    total = 0.0
    for bend, rate in zip(bends, rates):
        total += rate * relu(x - bend)
    return total


# Solve for the rates one row at a time. Row n only involves the pieces whose bend
# it has already passed, so each row hands us exactly one new rate.
rates = []
for x, actual in zip(inputs, actuals):
    already = predict(x, rates + [0.0] * (len(bends) - len(rates)))
    activation = relu(x - bends[len(rates)])
    rates.append((actual - already) / activation)

print("the four pieces it needs:")
print()
print(f"{'bend at':>9} {'rate':>8}   what this piece does")
print("-" * 58)
for bend, rate in zip(bends, rates):
    if rate > 0:
        what = "pulls the line UP after this point"
    elif rate < 0:
        what = "pulls the line DOWN after this point"
    else:
        what = "does nothing"
    print(f"{bend:>9} {rate:>8.1f}   {what}")

print()
print("does it hit all four?")
print()
print(f"{'input':>7} {'wanted':>8} {'got':>8}")
print("-" * 25)
for x, actual in zip(inputs, actuals):
    print(f"{x:>7} {actual:>8} {predict(x, rates):>8.1f}")

print()
print("the shape between the measurements, in small steps:")
print()
print(f"{'input':>7} {'output':>9} {'rise from the step before':>27}")
print("-" * 46)
previous = None
for step in range(4, 41, 2):
    x = step / 10
    value = predict(x, rates)
    rise = "" if previous is None else f"{value - previous:+.1f}"
    print(f"{x:>7.1f} {value:>9.1f} {rise:>27}")
    previous = value

print()
print("The rise is positive, then negative, then positive. The line climbs, falls,")
print("and climbs again - and every piece of it is still (rate x input) + something.")
print()
print("The ONLY new ingredient is that one rate came out negative (-30 at bend 2).")
print("A negative rate is not a special case and needs no new rule: it is an ordinary")
print("parameter that gradient descent happened to push below zero.")
