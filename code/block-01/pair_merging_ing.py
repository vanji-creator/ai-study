# Build a vocabulary by repeatedly merging the most frequent adjacent pair.
# Plain Python, no libraries. Change `number_of_merges` or the corpus and re-run.
# Run: python3 code/block-01/pair_merging_by_hand.py

from collections import Counter

# Training corpus: each word and how many times it appears.
word_frequencies = {
    "playing": 1, "played": 1, "player": 1, "plays": 1,
    "running": 1, "eating": 1,
    "sleeping": 1,
    "jumping": 1,
}

number_of_merges = 4   # how many new tokens to create

# Start with every word split into single characters.
# A word is stored as a tuple of its current pieces, e.g. ("l", "o", "w").
word_pieces = {word: tuple(word) for word in word_frequencies}


def count_adjacent_pairs(word_pieces, word_frequencies):
    """Count every pair of neighbouring pieces, weighted by how often the word appears."""
    pair_counts = Counter()
    for word, pieces in word_pieces.items():
        for left_piece, right_piece in zip(pieces, pieces[1:]):
            pair_counts[(left_piece, right_piece)] += word_frequencies[word]
    return pair_counts


def merge_pair_in_word(pieces, pair_to_merge):
    """Replace every occurrence of the pair (a, b) with the single piece 'ab'."""
    merged_pieces = []
    position = 0
    while position < len(pieces):
        is_pair_here = (
            position + 1 < len(pieces)
            and (pieces[position], pieces[position + 1]) == pair_to_merge
        )
        if is_pair_here:
            merged_pieces.append(pieces[position] + pieces[position + 1])
            position += 2   # skip both pieces, they are now one
        else:
            merged_pieces.append(pieces[position])
            position += 1
    return tuple(merged_pieces)


starting_vocabulary = sorted({char for word in word_frequencies for char in word})
print("starting vocabulary (characters):", starting_vocabulary)
print("starting pieces:", {word: " ".join(pieces) for word, pieces in word_pieces.items()})
print()

learned_merges = []   # the ordered list of merges IS the tokeniser

for merge_number in range(1, number_of_merges + 1):
    pair_counts = count_adjacent_pairs(word_pieces, word_frequencies)
    most_frequent_pair, pair_count = pair_counts.most_common(1)[0]

    print(f"merge {merge_number}: top pairs = {pair_counts.most_common(4)}")
    print(f"         merging {most_frequent_pair} (count {pair_count}) -> '{''.join(most_frequent_pair)}'")

    word_pieces = {
        word: merge_pair_in_word(pieces, most_frequent_pair)
        for word, pieces in word_pieces.items()
    }
    learned_merges.append(most_frequent_pair)
    print("         now:", {word: " ".join(pieces) for word, pieces in word_pieces.items()})
    print()

print("learned merges, in order:", learned_merges)
