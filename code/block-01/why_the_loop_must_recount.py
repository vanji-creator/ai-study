# Why stage A4 is a LOOP and not "count the pairs once and sort them descending".
#
# Written on 2026-09-30 after a review answer described A4 as a single descending
# sort. It is not. Merging CREATES pairs that did not exist in the first count, so
# any list built from one count can never contain them.
#
# Run: python3 code/block-01/why_the_loop_must_recount.py

from collections import Counter

WORD = "banana"


def count_neighbouring_pairs(pieces):
    """Every adjacent pair, counted. This is what A4 does at the top of each round."""
    return Counter(zip(pieces, pieces[1:]))


def apply_one_merge(pieces, pair_to_merge):
    """Join every occurrence of this pair into a single piece, left to right."""
    joined = []
    index = 0
    while index < len(pieces):
        if (index + 1 < len(pieces)
                and (pieces[index], pieces[index + 1]) == pair_to_merge):
            joined.append(pieces[index] + pieces[index + 1])
            index += 2
        else:
            joined.append(pieces[index])
            index += 1
    return joined


def show(label, pieces):
    print(f"  {label:<22} {' | '.join(pieces)}")


print(f'the corpus is one word: "{WORD}"')
print()

# ---------------------------------------------------------------------------
# The WRONG method: count once, sort descending, take the merges in that order.
# ---------------------------------------------------------------------------

pieces = list(WORD)
first_count = count_neighbouring_pairs(pieces)

print("count the pairs ONCE, sort descending:")
print()
for pair, count in sorted(first_count.items(), key=lambda item: (-item[1], item[0])):
    print(f"  {pair[0]} + {pair[1]}   appears {count}")
print()
print("  Those three pairs are the ONLY merges this method can ever produce.")
print()
print()

# ---------------------------------------------------------------------------
# The RIGHT method: count, merge the top one, then COUNT AGAIN.
# ---------------------------------------------------------------------------

print("now the real loop - count, merge the top, recount:")
print()

pieces = list(WORD)
show("start", pieces)
merge_list = []

for round_number in range(1, 4):
    counts = count_neighbouring_pairs(pieces)
    if not counts:
        break
    top_pair, top_count = max(counts.items(), key=lambda item: (item[1], item[0]))

    print()
    print(f"  round {round_number}   pairs now: "
          + ",  ".join(f"{a}+{b}={n}" for (a, b), n in
                       sorted(counts.items(), key=lambda i: (-i[1], i[0]))))
    was_in_first_count = top_pair in first_count
    print(f"  round {round_number}   merging {top_pair[0]} + {top_pair[1]} "
          f"(count {top_count})"
          + ("" if was_in_first_count
             else "   <-- THIS PAIR DID NOT EXIST IN THE FIRST COUNT"))

    merge_list.append(top_pair)
    pieces = apply_one_merge(pieces, top_pair)
    show(f"after round {round_number}", pieces)

print()
print("the merge list the loop produced:")
for position, (left, right) in enumerate(merge_list, 1):
    marker = "" if (left, right) in first_count else "   <-- unreachable by sorting once"
    print(f"  {position}. {left} + {right}{marker}")

print()
print("Merging changes what the neighbours ARE, so it changes which pairs exist.")
print("n+a was merged, which put two 'na' pieces next to each other and created the")
print("pair na+na out of nothing. No amount of sorting the first count can reach it.")
print()
print("That is why A4 is a loop: count pairs, merge the single best one, recount,")
print("repeat. One count, one merge. Never one count and many merges.")
