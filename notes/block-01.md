# Block 1 — Text into numbers

## Part 1 · Tokenisation — finished 2026-09-21

---

## Your three sentences (your own words, sentence 2 corrected)

1. A tokeniser converts the given language text into numbers — IDs taken from a
   dictionary that is fixed before training and never changes afterwards.

2. Pieces are used because a single word can have different forms with the same base
   (`play`, `playing`, `player`), so the shared base gets one token and is trained more.
   Whole words fail on any unseen word; single letters never fail but cost about 4× the
   tokens. Pieces are safe *and* cheap. The tokeniser never corrects or approximates a
   mistake — `birdz` becomes `bird | z`, not `bird`.

3. The merge list is built with a fixed number of merges. The training pile is counted,
   the most frequent pair is merged into one token, and this repeats. The ordered list of
   all those merges is the tokeniser.

---

# Revision outline — every heading, in the order studied

Use this as the structure for the Freeform write-up. One heading = one panel.

## 1 · Why tokenisation exists
- The model's first layer is a lookup table: a fixed number of rows, decided before
  training and never changed.
- The model cannot read text. It can only look up a row number.
- Therefore all text must become row numbers from a frozen table. Every other fact in
  this block comes from that one constraint.

## 2 · The dictionary
- `vocabulary = {"I": 0, "like": 1, "cats": 2}` — text piece → integer ID.
- One entry = one **token**.
- The ID carries no meaning. It is a primary key, like `user_id = 2` in PostgreSQL.
- Meaning is learned later, during training, from seeing the token in many sentences.

## 3 · Approach that fails: one row per word
- Unseen word → `KeyError` → forced into a single `<UNK>` row.
- Every name, typo, new product word and non-English word collapses into the same vector.
- The long tail is not small: measured on `CLAUDE.md`, 1,071 distinct words, **64.5% of
  them appear exactly once**. A row trained on one example is close to random.
- Word tables also lose shared roots: `token`, `tokens`, `tokenisation` become unrelated rows.

## 4 · Approach that fails: nearest spelling
- Spelling closeness is not meaning closeness.
- `not` is one letter from `now`. "I did not pay" → "I did now pay". Meaning reversed,
  silently.

## 5 · Approach that is safe but expensive: one row per letter
- Never fails — every word is made of letters.
- `"I did not pay the bill"` = 6 word tokens, 22 letter tokens (~3.7×).
- A single letter means almost nothing; the model must rebuild the word from letters.
- But meaning IS recoverable from order: `c a t` vs `a c t` vs `c u t`.

## 6 · The middle way: pieces
- Rule: use the biggest pieces the dictionary knows; fall back to smaller pieces, finally
  to single characters/bytes.
- `birds → bird | s`, `playing → play | ing`, `xqz → x | q | z`.
- Dictionary holds three kinds of entries: common whole words, common word parts,
  and the single-character/byte safety net.

## 7 · BPE — Byte Pair Encoding
- Problem it solves: who decides which pieces go in the dictionary.
- Rule: count every pair of **neighbouring** pieces in a training pile, merge the most
  frequent pair into one new piece, repeat.
- Worked example (`low`×5, `lower`×2, `newest`×6, `widest`×3):
  `es → est → lo → low → ne → new`. `est` emerged as a suffix with nobody defining suffixes.
- Second example (`playing, played, player, plays, running, eating, sleeping, jumping`):
  `i+n → in`, `in+g → ing`, `p+l → pl`, `pl+a → pla`, `pla+y → play`.
- **It stops after a fixed number of merges, chosen in advance.** That number is the
  vocabulary size. It does NOT stop when counts get small.
- Counts do fall as merging continues — early merges are very common pieces.

## 8 · The merge list IS the tokeniser
- Training output is the ordered list of merges, not the corpus.
- To tokenise new text: split into bytes/characters, then replay every merge in order.
- Unseen word `replaying` → `r | e | play | ing`. No `<UNK>`, known pieces reused.
- Change the training pile → different list → different tokens for the same text.

## 9 · Bytes, code points and UTF-8
- Every character has a fixed worldwide number, its **code point**: `e` = 101,
  `é` = 233, `日` = 26085, `🙂` = 128578.
- A byte holds 0–255 only. Large code points do not fit.
- **UTF-8** is the rule for writing a code point as one to four bytes.
  Code points 0–127 → one byte (ASCII). Any byte above 127 means "more bytes follow".
- `é → [195, 169]`, `日 → [230, 151, 165]`, `🙂 → [240, 159, 153, 130]`.
- Nothing is lost: bytes convert back to the exact original text. `é` is never turned
  into `e`.
- A single byte of a multi-byte character is not a character. Byte 195 alone fails to
  decode; 195 + 169 together are `é`.

## 10 · Why the safety net is 256 rows
- Unicode has ~150,000 characters — far too many for one row each.
- Every text is bytes, and there are only 256 possible byte values.
- So: 256 rows covers every language, symbol, emoji and corrupted file. Nothing can fail.
- This is where the name comes from: **Byte** Pair Encoding.

## 11 · Why non-English text costs more tokens — two separate reasons
1. **More bytes per character** — 3 bytes per character for Tamil or Japanese vs 1 for
   English. The sequence starts longer before any merging.
2. **Fewer merges apply** — the counting pile is mostly English, so English pairs win the
   counts and get rows. Other scripts stay near the byte level.
- Both push the same way. Result: roughly 3–5× more tokens.

## 12 · Special tokens
- Extra rows that correspond to no text: end of text, start/end of turn, padding, mask.
- They are normal rows to the model; it learns their meaning from training.
- The tokeniser will **not** produce them from user text — typing the characters gives
  ordinary word pieces with different IDs.
- Purpose: put the message boundaries in a channel the user cannot write into.
- The model produces the end-of-turn token itself on the way out; serving code stops there.

## 13 · Who inserts special tokens — two shapes
- The **application**, not the model. Before the model runs.
- **Way A (common):** build one string containing the markers plus the message text, then
  tokenise the whole string with special-token parsing enabled. Convenient, and the place
  where forged boundaries become possible if user content is not stripped.
- **Way B (safer):** tokenise each message separately with special tokens **disabled**,
  then join the ID lists with special IDs your code inserts.
- First concrete security control of the course. Returns in Block 9.

## 14 · The space belongs to the word after it
- Measured on `CLAUDE.md`: 132 of the first 250 merges produce a piece that starts with a
  space. The first merge learned was space + letter.
- `_the` is a token; bare `the` may not even exist as a piece.
- `"...France is"` → last token `_is`, next natural token `_Paris`.
- `"...France is "` → an extra lone-space token; `_Paris` is now impossible, the model must
  emit a bare `Paris`. Both the lone space and the bare piece are rare in training.
- Rule: never end a prompt with a trailing space or an unintended newline. Worst in
  completion-style calls and hand-built few-shot examples.

## 15 · Real tokenisers
- **OpenAI** — public. `tiktoken`, open source, inspectable. Different encodings per model
  generation (~100k vocabulary for the GPT-4 era, ~200k for newer). *Check current.*
- **Anthropic** — not public. Count tokens with `POST /v1/messages/count_tokens`, and pass
  the model ID because counts are model-specific. The tokeniser introduced with Opus 4.7
  produces ~1×–1.35× the tokens of the earlier one on the same text. *Check current.*
- `tiktoken` undercounts Claude by ~15–20% on ordinary English, more on code and
  non-English. Another company's merge list does not apply to your text.
- **Open-weight models** (Llama, Mistral, Qwen, LaBSE, bge-reranker) ship the tokeniser
  inside the model folder. You can open it — and you build the token list yourself, so
  Way A / Way B becomes your decision.
- With a hosted chat API you send `{"role": ..., "content": ...}` and the server builds the
  token list. That is Way B enforced at the API boundary.

---

# Where tokenisation sits in the pipeline

```
   text
     |
 [ 1 tokeniser ]          <- DONE. counting and string splitting, no maths
     |
   token IDs
     |
 [ 2 embedding table ]    <- next after Block 0. ID -> vector
     |
   vectors + position
     |
 [ 3 transformer layers ] <- Block 2. attention
     |
   logits (one score per row in the vocabulary)
     |
 [ 4 softmax + sampling ] <- Block 3. temperature, top-k, top-p
     |
   one token ID, appended, loop back to step 2
     |
 [ 5 detokenise ]         <- IDs back to text, stop at end-of-turn
```

Everything in Block 1 Part 1 is box 1. Nothing in it involves a neural network, which is
why it could be learned first.

---

# Numbers worth memorising from this part

- 1 token ≈ 4 characters ≈ 0.75 English words
- Indic / CJK text: 3–5× more tokens than the English translation
- English letters, digits, punctuation: 1 byte. Other scripts: 2–4 bytes
- Byte values possible: 256. Unicode characters: ~150,000
- Long tail measured on `CLAUDE.md`: 64.5% of distinct words appear once
- `tiktoken` vs Claude: undercounts by ~15–20%

---

# Runnable scripts for this part

| Script | Shows |
|---|---|
| `code/block-01/word_frequency_tail.py` | the long tail of word frequency, shared roots |
| `code/block-01/pair_merging_by_hand.py` | BPE on `low / lower / newest / widest` |
| `code/block-01/pair_merging_ing.py` | BPE finding `ing` from eight words |
| `code/block-01/text_as_bytes.py` | characters vs bytes across scripts |
| `code/block-01/bytes_explained.py` | code points, UTF-8, round trip, single-byte failure |
| `code/block-01/space_belongs_to_the_word.py` | merges learn `_the`, not `the` |

---

# Still open in Block 1

- [ ] **Gate not run.** Needs a real tokeniser: count tokens in a Tamil sentence and its
      English translation, explain the ratio.
- [ ] **Part 2 — embeddings** not started. Comes after Block 0.
