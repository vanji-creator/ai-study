# The complete tokeniser pipeline, both halves, run for real.
#
#   PIPELINE A (offline, once):  corpus  -> merge list + vocabulary
#   PIPELINE B (runtime, always): text   -> token IDs -> text again
#
# Run: python3 code/block-01/tokeniser_pipeline.py

from collections import Counter

NUMBER_OF_MERGES = 400
CORPUS_PATH = "CLAUDE.md"


def show(piece_as_bytes):
    """Display a piece. Printable ASCII as characters, a space as '_', anything else as <n>."""
    text_out = ""
    for byte_value in piece_as_bytes:
        if byte_value == 32:
            text_out += "_"
        elif 33 <= byte_value <= 126:
            text_out += chr(byte_value)
        else:
            text_out += f"<{byte_value}>"
    return text_out


def pre_tokenise(text):
    """STAGE 2. Cut the text into chunks. The space stays attached to the word AFTER it."""
    chunks = []
    for index, word in enumerate(text.split(" ")):
        chunks.append(word if index == 0 else " " + word)
    return [chunk for chunk in chunks if chunk]


# ----------------------------------------------------------------------------
# PIPELINE A — build the tokeniser
# ----------------------------------------------------------------------------
corpus_text = open(CORPUS_PATH, encoding="utf-8").read().lower()

chunk_frequencies = Counter(pre_tokenise(corpus_text))          # A2: count chunks

# A3: every chunk becomes a tuple of single bytes
chunk_pieces = {
    chunk: tuple(bytes([byte_value]) for byte_value in chunk.encode("utf-8"))
    for chunk in chunk_frequencies
}

merge_list = []                                                  # A4: the loop
for merge_number in range(NUMBER_OF_MERGES):
    pair_counts = Counter()
    for chunk, pieces in chunk_pieces.items():
        for left, right in zip(pieces, pieces[1:]):
            pair_counts[(left, right)] += chunk_frequencies[chunk]
    if not pair_counts:
        break
    top_pair, top_count = pair_counts.most_common(1)[0]

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

# A5: the vocabulary. 256 byte rows first, then one row per merge, then special tokens.
vocabulary = {bytes([byte_value]): byte_value for byte_value in range(256)}
for merge_index, (left, right) in enumerate(merge_list):
    vocabulary[left + right] = 256 + merge_index

special_tokens = {"START_OF_TURN": len(vocabulary), "END_OF_TURN": len(vocabulary) + 1}

print("PIPELINE A — build the tokeniser (runs once, offline)")
print(f"  corpus                : {CORPUS_PATH}, {len(corpus_text)} characters")
print(f"  distinct chunks counted: {len(chunk_frequencies)}")
print(f"  merges performed      : {len(merge_list)}")
print(f"  vocabulary size       : {len(vocabulary)} rows "
      f"(256 bytes + {len(merge_list)} merges) + {len(special_tokens)} special")
print(f"  first 6 merges        : "
      f"{[show(left) + ' + ' + show(right) for left, right in merge_list[:6]]}")
print()


# ----------------------------------------------------------------------------
# PIPELINE B — use the tokeniser
# ----------------------------------------------------------------------------
def encode(text, show_stages=False):
    if show_stages:
        print(f"  STAGE 1  raw text        : {text!r}")

    normalised_text = text.lower()                                # STAGE 1b
    if show_stages:
        print(f"  STAGE 2  normalised      : {normalised_text!r}")

    chunks = pre_tokenise(normalised_text)                        # STAGE 3
    if show_stages:
        print(f"  STAGE 3  pre-tokenised   : {chunks}")

    token_ids = []
    for chunk in chunks:
        pieces = tuple(bytes([b]) for b in chunk.encode("utf-8")) # STAGE 4
        if show_stages:
            print(f"  STAGE 4  {chunk!r:<12} as bytes: {list(chunk.encode('utf-8'))}")

        for left, right in merge_list:                            # STAGE 5
            merged, position = [], 0
            while position < len(pieces):
                if (position + 1 < len(pieces)
                        and (pieces[position], pieces[position + 1]) == (left, right)):
                    merged.append(pieces[position] + pieces[position + 1])
                    position += 2
                else:
                    merged.append(pieces[position])
                    position += 1
            pieces = tuple(merged)

        if show_stages:
            print(f"           {chunk!r:<12} after merges: {[show(p) for p in pieces]}")
        token_ids.extend(vocabulary[piece] for piece in pieces)   # STAGE 6

    return token_ids


def decode(token_ids):
    id_to_piece = {token_id: piece for piece, token_id in vocabulary.items()}
    all_bytes = b"".join(id_to_piece[token_id] for token_id in token_ids)
    return all_bytes.decode("utf-8")


print("PIPELINE B — use the tokeniser (runs on every request)")
sentence = "The café is not open"
token_ids = encode(sentence, show_stages=True)

id_to_piece = {token_id: piece for piece, token_id in vocabulary.items()}
print(f"  STAGE 6  pieces          : {[show(id_to_piece[i]) for i in token_ids]}")
print(f"  STAGE 6  token IDs       : {token_ids}")

with_special = [special_tokens["START_OF_TURN"]] + token_ids + [special_tokens["END_OF_TURN"]]
print(f"  STAGE 7  + special tokens: {with_special}")
print()
print(f"  DECODE   IDs back to text: {decode(token_ids)!r}")
print()
print(f"  token count: {len(token_ids)} for {len(sentence)} characters")
