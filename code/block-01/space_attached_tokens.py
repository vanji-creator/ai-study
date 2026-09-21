# Train BPE on raw text WITH spaces, and see what the merges look like.
# Spaces are shown as _ so they are visible.
# Run: python3 code/block-01/space_attached_tokens.py

from collections import Counter

training_text = (
    "the dog runs. the dog sleeps. the dog eats. "
    "the cat runs. the cat sleeps. a dog barks. a cat naps. "
    "the dog and the cat. the dog is big. the cat is small."
)

number_of_merges = 12

# The whole text is ONE sequence of characters. Spaces are characters too.
pieces = tuple(training_text)


def count_adjacent_pairs(pieces):
    return Counter(zip(pieces, pieces[1:]))


def merge_pair(pieces, pair_to_merge):
    merged = []
    position = 0
    while position < len(pieces):
        if (position + 1 < len(pieces)
                and (pieces[position], pieces[position + 1]) == pair_to_merge):
            merged.append(pieces[position] + pieces[position + 1])
            position += 2
        else:
            merged.append(pieces[position])
            position += 1
    return tuple(merged)


learned_merges = []
for merge_number in range(1, number_of_merges + 1):
    pair_counts = count_adjacent_pairs(pieces)
    top_pair, top_count = pair_counts.most_common(1)[0]
    pieces = merge_pair(pieces, top_pair)
    learned_merges.append(top_pair)
    joined = "".join(top_pair).replace(" ", "_")
    print(f"merge {merge_number:>2}: '{joined}'  (count {top_count})")

print()
print("dictionary pieces longer than one character (spaces shown as _):")
print(sorted({"".join(p).replace(' ', '_') for p in
              ["".join(m) for m in learned_merges]}))


def tokenise(text, learned_merges):
    """Apply the learned merges, in order, to new text."""
    current = tuple(text)
    for pair in learned_merges:
        current = merge_pair(current, pair)
    return [piece.replace(" ", "_") for piece in current]


print()
for sample in ["the dog", "the dog ", "a dog"]:
    shown = sample.replace(" ", "_")
    tokens = tokenise(sample, learned_merges)
    print(f"  {shown!r:<12} -> {tokens}   ({len(tokens)} tokens)")
