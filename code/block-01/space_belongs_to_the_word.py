# Real tokenisers attach the space to the word that FOLLOWS it.
# We show this by training our own merges on real English text (CLAUDE.md).
# The space is displayed as "_" so you can see it.
# Run: python3 code/block-01/space_belongs_to_the_word.py

from collections import Counter

SPACE = "_"          # how we display a space character
NUMBER_OF_MERGES = 250

corpus_text = open("CLAUDE.md", encoding="utf-8").read().lower()

# Pre-split: keep the space attached to the front of each word, exactly as real BPE does.
words_with_leading_space = []
for word in corpus_text.split(" "):
    cleaned_word = word.strip("\n\t.,:;()`*\"'|—-[]#?!")
    if cleaned_word.isalpha():                       # keep plain words only, for clarity
        words_with_leading_space.append(SPACE + cleaned_word)

word_frequencies = Counter(words_with_leading_space)
word_pieces = {word: tuple(word) for word in word_frequencies}


def count_adjacent_pairs(word_pieces, word_frequencies):
    pair_counts = Counter()
    for word, pieces in word_pieces.items():
        for left_piece, right_piece in zip(pieces, pieces[1:]):
            pair_counts[(left_piece, right_piece)] += word_frequencies[word]
    return pair_counts


def merge_pair_in_word(pieces, pair_to_merge):
    merged_pieces, position = [], 0
    while position < len(pieces):
        if (position + 1 < len(pieces)
                and (pieces[position], pieces[position + 1]) == pair_to_merge):
            merged_pieces.append(pieces[position] + pieces[position + 1])
            position += 2
        else:
            merged_pieces.append(pieces[position])
            position += 1
    return tuple(merged_pieces)


learned_merges = []
for merge_number in range(NUMBER_OF_MERGES):
    pair_counts = count_adjacent_pairs(word_pieces, word_frequencies)
    if not pair_counts:
        break
    top_pair, top_count = pair_counts.most_common(1)[0]
    word_pieces = {w: merge_pair_in_word(p, top_pair) for w, p in word_pieces.items()}
    learned_merges.append((top_pair, top_count))

# Which merges produced a piece that STARTS with a space?
pieces_starting_with_space = [
    "".join(pair) for pair, count in learned_merges if "".join(pair).startswith(SPACE)
]

print(f"trained {len(learned_merges)} merges on CLAUDE.md")
print()
print("first 12 merges, in order:")
for pair, count in learned_merges[:12]:
    print(f"   {pair[0]!r:>8} + {pair[1]!r:<8} -> {''.join(pair)!r:<10} count {count}")

print()
print(f"pieces that begin with a space: {len(pieces_starting_with_space)} of {len(learned_merges)}")
print("   examples:", pieces_starting_with_space[:20])

print()
print("Is the space-version a different piece from the bare word?")
final_pieces = {piece for pieces in word_pieces.values() for piece in pieces}
for bare in ["the", "a", "not", "do"]:
    print(f"   {SPACE + bare!r:<8} in vocabulary: {(SPACE + bare) in final_pieces:<5}"
          f"   {bare!r:<6} as a separate piece: {bare in final_pieces}")
