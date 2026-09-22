# PIPELINE A on a tiny corpus, printing the exact state after every stage.
# Letters are used instead of bytes so the trace stays readable. The process is identical.
# Run: python3 code/block-01/pipeline_a_traced.py

from collections import Counter

corpus_text = "the cat sat on the mat the cat ran"
NUMBER_OF_MERGES = 5

print("=" * 62)
print("A1  CORPUS")
print("=" * 62)
print(f"  {corpus_text!r}")
print(f"  {len(corpus_text.split())} words, {len(corpus_text)} characters")

print()
print("=" * 62)
print("A2  PRE-TOKENISE AND COUNT")
print("=" * 62)
# every word gets a space in front, shown as "_"
chunks = ["_" + word for word in corpus_text.split()]
print(f"  chunks in order : {chunks}")
chunk_counts = Counter(chunks)
print("  distinct chunks and how often each appears:")
for chunk, count in chunk_counts.most_common():
    print(f"      {chunk:<6} x{count}")

print()
print("=" * 62)
print("A3  SPLIT EACH DISTINCT CHUNK INTO SINGLE PIECES")
print("=" * 62)
chunk_pieces = {chunk: tuple(chunk) for chunk in chunk_counts}
for chunk, pieces in chunk_pieces.items():
    print(f"      {chunk:<6} x{chunk_counts[chunk]}   ->   {' '.join(pieces)}")
print(f"  starting vocabulary: {sorted({p for ps in chunk_pieces.values() for p in ps})}")

print()
print("=" * 62)
print("A4  COUNT PAIRS, MERGE THE TOP ONE, REPEAT")
print("=" * 62)

merge_list = []
for merge_number in range(1, NUMBER_OF_MERGES + 1):
    pair_counts = Counter()
    for chunk, pieces in chunk_pieces.items():
        for left, right in zip(pieces, pieces[1:]):
            pair_counts[(left, right)] += chunk_counts[chunk]   # weighted by chunk frequency

    top_pair, top_count = pair_counts.most_common(1)[0]
    print(f"\n  --- merge {merge_number} ---")
    print("  pair counts now:")
    for (left, right), count in pair_counts.most_common(5):
        marker = "  <- highest" if (left, right) == top_pair else ""
        print(f"      {left!r:>6} + {right!r:<6} = {count}{marker}")

    new_chunk_pieces = {}
    for chunk, pieces in chunk_pieces.items():
        merged, position = [], 0
        while position < len(pieces):
            if (position + 1 < len(pieces)
                    and (pieces[position], pieces[position + 1]) == top_pair):
                merged.append(pieces[position] + pieces[position + 1])
                position += 2
            else:
                merged.append(pieces[position])
                position += 1
        new_chunk_pieces[chunk] = tuple(merged)
    chunk_pieces = new_chunk_pieces
    merge_list.append(top_pair)

    print(f"  new piece created: {''.join(top_pair)!r}")
    print("  state after this merge:")
    for chunk, pieces in chunk_pieces.items():
        print(f"      {chunk:<6} -> {' '.join(pieces)}")

print()
print("=" * 62)
print("A5  OUTPUT")
print("=" * 62)
print(f"  merge list, in order : {[left + right for left, right in merge_list]}")
starting_letters = sorted({letter for chunk in chunk_counts for letter in chunk})
vocabulary = {piece: index for index, piece in enumerate(starting_letters)}
for left, right in merge_list:
    vocabulary[left + right] = len(vocabulary)
print(f"  vocabulary           : {vocabulary}")
print("  the corpus is now thrown away. only these two things survive.")
