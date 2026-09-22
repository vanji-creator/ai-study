# What happens when text arrives whose pieces were never merged.
# Trains on CLAUDE.md (English), then encodes English and Tamil sentences.
# Run: python3 code/block-01/cost_of_missing_merges.py

from collections import Counter

NUMBER_OF_MERGES = 400


def pre_tokenise(text):
    return [word if i == 0 else " " + word
            for i, word in enumerate(text.split(" ")) if word or i > 0]


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


def apply_one_merge(pieces, pair):
    out, i = [], 0
    while i < len(pieces):
        if i + 1 < len(pieces) and (pieces[i], pieces[i + 1]) == pair:
            out.append(pieces[i] + pieces[i + 1]); i += 2
        else:
            out.append(pieces[i]); i += 1
    return tuple(out)


def encode(text, merge_list):
    all_pieces = []
    for chunk in pre_tokenise(text.lower()):
        pieces = tuple(bytes([b]) for b in chunk.encode("utf-8"))
        for pair in merge_list:
            pieces = apply_one_merge(pieces, pair)
        all_pieces.extend(pieces)
    return all_pieces


merge_list = train(open("CLAUDE.md", encoding="utf-8").read().lower(), NUMBER_OF_MERGES)

english_sentence = "hello how are you"
tamil_sentence = "வணக்கம் எப்படி இருக்கிறீர்கள்"

for label, sentence in [("english", english_sentence), ("tamil", tamil_sentence)]:
    pieces = encode(sentence, merge_list)
    raw_byte_pieces = sum(1 for p in pieces if len(p) == 1)
    print(f"{label}:")
    print(f"   text            : {sentence}")
    print(f"   characters      : {len(sentence)}")
    print(f"   utf-8 bytes     : {len(sentence.encode('utf-8'))}")
    print(f"   tokens produced : {len(pieces)}")
    print(f"   of those, single-byte pieces (no merge applied): {raw_byte_pieces}")
    print()

english_tokens = len(encode(english_sentence, merge_list))
tamil_tokens = len(encode(tamil_sentence, merge_list))
print(f"ratio: tamil costs {tamil_tokens / english_tokens:.1f}x the tokens of the english sentence")
print("(this tokeniser saw no Tamil at all, so it is a worst case, not a typical one)")
