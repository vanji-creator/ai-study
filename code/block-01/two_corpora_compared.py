# Same algorithm, same budget, two different corpora.
# Shows that corpus choice changes COST, never correctness.
# Run: python3 code/block-01/two_corpora_compared.py

from collections import Counter
import glob

NUMBER_OF_MERGES = 400


def pre_tokenise(text):
    return [w if i == 0 else " " + w for i, w in enumerate(text.split(" ")) if w or i > 0]


def apply_one_merge(pieces, pair):
    out, i = [], 0
    while i < len(pieces):
        if i + 1 < len(pieces) and (pieces[i], pieces[i + 1]) == pair:
            out.append(pieces[i] + pieces[i + 1]); i += 2
        else:
            out.append(pieces[i]); i += 1
    return tuple(out)


def train(corpus_text, number_of_merges):
    chunk_counts = Counter(pre_tokenise(corpus_text))
    chunk_pieces = {c: tuple(bytes([b]) for b in c.encode("utf-8")) for c in chunk_counts}
    merge_list = []
    for _ in range(number_of_merges):
        pair_counts = Counter()
        for chunk, pieces in chunk_pieces.items():
            for left, right in zip(pieces, pieces[1:]):
                pair_counts[(left, right)] += chunk_counts[chunk]
        if not pair_counts:
            break
        top_pair = pair_counts.most_common(1)[0][0]
        chunk_pieces = {c: apply_one_merge(p, top_pair) for c, p in chunk_pieces.items()}
        merge_list.append(top_pair)
    return merge_list


def encode(text, merge_list):
    pieces_out = []
    for chunk in pre_tokenise(text):
        pieces = tuple(bytes([b]) for b in chunk.encode("utf-8"))
        for pair in merge_list:
            pieces = apply_one_merge(pieces, pair)
        pieces_out.extend(pieces)
    return pieces_out


english_corpus = open("CLAUDE.md", encoding="utf-8").read().lower()
python_corpus = "".join(open(path, encoding="utf-8").read()
                        for path in sorted(glob.glob("code/block-01/*.py")))

tokeniser_english = train(english_corpus, NUMBER_OF_MERGES)
tokeniser_python = train(python_corpus, NUMBER_OF_MERGES)

samples = [
    ("english prose", "the model cannot read text it only reads numbers"),
    ("python code  ", "def count_pairs(word_pieces, word_frequencies):"),
]

print(f"both tokenisers: {NUMBER_OF_MERGES} merges, byte-level fallback\n")
print(f"{'sample':<15} {'english-trained':>16} {'python-trained':>16}")
print("-" * 50)
for label, text in samples:
    a = len(encode(text, tokeniser_english))
    b = len(encode(text, tokeniser_python))
    print(f"{label:<15} {a:>13} tok {b:>13} tok")

print()
text = samples[1][1]
print("the python line, cut by each tokeniser:")
print("  english-trained:", [p.decode('utf-8', 'replace') for p in encode(text, tokeniser_english)])
print("  python-trained :", [p.decode('utf-8', 'replace') for p in encode(text, tokeniser_python)])

print()
print("both decode back to the original text:")
for name, ml in [("english-trained", tokeniser_english), ("python-trained", tokeniser_python)]:
    restored = b"".join(encode(text, ml)).decode("utf-8")
    print(f"  {name}: {restored == text}")
