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

---

# Session 2026-09-22 · Pipeline A, gone through again

These are the points that came out of the questions asked during this session.
Written plainly, for reading cold later.

## The five stages, and a hook to remember them

```
A1   corpus                 a pile of text. nothing else.
A2   pre-tokenise + count   cut into chunks at spaces, count the distinct ones
A3   split into pieces      each distinct chunk becomes single bytes
A4   the loop               count pairs, merge the top one, repeat until the budget ends
A5   output                 ordered merge list + vocabulary. the corpus is thrown away.
```

Hook: **text, count, pieces, loop, keep.**

A5 is the one most easily forgotten, and it is the most important. A1 to A4 are work.
A5 is the only stage whose output survives, and it is exactly what a tokeniser *is*.

## The state the loop works on

After A2 the original text is gone. What remains is one table with two columns.
For the corpus `'the cat sat on the mat the cat ran'`:

```
  chunk      pieces (this column changes)      count (this column never changes)
  ------------------------------------------------------------------------------
  _the       _  t  h  e                        3
  _cat       _  c  a  t                        2
  _sat       _  s  a  t                        1
  _on        _  o  n                           1
  _mat       _  m  a  t                        1
  _ran       _  r  a  n                        1
```

Six rows, not nine. Keeping `_the` once with the number 3 is the same as keeping three
copies of it, and it is far less work.

A merge only changes the middle column. Rows are never added or removed, and the counts
are never touched.

## Where a pair's weight comes from

Nothing counts letters. A pair takes its weight from the row it sits in. If `c` + `at`
appears in a row marked x2, that pair scores 2.

A pair can also win by appearing in several rows at once. In the corpus above, `a` + `t`
scored 4 — once in `_cat` (x2), once in `_sat` (x1), once in `_mat` (x1) — and beat every
pair inside `_the`, whose row count is only 3.

## Each merge creates pairs that could not exist before

```
turn 1   a  + t   = 4     ->  new piece 'at'
turn 2   _  + t   = 3     ->  new piece '_t'
turn 3   _t + h   = 3     ->  new piece '_th'     <- this pair did not exist before turn 2
turn 4   _th + e  = 3     ->  new piece '_the'
```

By turn 4, the most common word in the corpus is a single token, and nobody told the
algorithm that `the` is a word.

## Why the merge list must stay in order

A merge joins two pieces that are next to each other **right now**. If a merge runs before
the merge that builds its ingredient, it matches nothing and is silently skipped.

```
correct order          '_the'  ->  ['_the']        1 token
merge 4 moved first    '_the'  ->  ['_th', 'e']    2 tokens
```

No error is raised. The text is simply cut differently, and worse.

This is why the merge list is stored as an ordered list, not a set. The order is the
information.

## Which merges can be reordered, and which cannot

Each merge depends only on the two pieces it joins.

```
   _the                              _cat
     ^                                 ^
   _th  +  e                         _c  +  at
     ^                                 ^      ^
   _t  +  h                          _ + c   a + t
     ^
   _  +  t
```

- **Allowed:** `_cat` before `_the`. They are different chains. Frequency decides which
  chain is bought first — if `cat` were more common than `the`, that order would be
  perfectly normal.
- **Impossible:** `_cat` before `_c`. Same chain, ingredient missing.

Training can never produce an invalid order, because a pair can only be counted once both
of its pieces already exist. An invalid order can only appear if someone rearranges the
list by hand or a library writes it out wrongly.

## The budget is a queue ordered by frequency

Nothing is excluded by nature. Things are simply bought in order of frequency until the
budget runs out. On the nine-word corpus:

```
merge 1   at      count 4
merge 4   _the    count 3
merge 6   _cat    count 2
merge 8   _sat    count 1     <- rarest, last
```

With a budget of 5 merges, `_sat` never gets a row. With a budget of 14, it does.

In a real tokeniser the budget is around 50,000 and the queue is millions long, so the
budget always runs out first. Everything below that line — rare words, names, typos, most
pieces of other scripts — has no row and falls back to smaller pieces or single bytes at
runtime.

## What that costs, measured

Our tokeniser trained only on `CLAUDE.md`, which contains no Tamil:

```
english:  "hello how are you"                     17 bytes  ->   7 tokens
tamil:    "வணக்கம் எப்படி இருக்கிறீர்கள்"              83 bytes  ->  83 tokens
          every single token was a raw byte; no merge applied to any of them

ratio: 11.9x
```

That is the worst case, because this tokeniser saw zero Tamil. Real models see some, so
some pieces do get merged, which is why the usual figure is 3–5x.

## Why we need the vocabulary when we already have the merge list

They answer two different questions.

```
merge list   HOW do I cut this text?      -> gives pieces, which are strings
vocabulary   WHAT NUMBER is this piece?   -> gives IDs, which are integers
```

The model cannot take strings. The ID is a **row number in the embedding table**, so the
vocabulary is the agreement between the tokeniser and the model's first layer. If the
tokeniser hands over 15 where the model learned 14, the model reads the wrong row and no
error is raised anywhere.

Decoding needs the vocabulary in reverse (ID → piece). The merge list cannot do that at
all; it contains no IDs.

For plain BPE the vocabulary *is* derivable from the merge list — 256 byte rows, then one
row per merge in order. It is stored explicitly anyway, because special tokens were never
merged from anything and exist only in the vocabulary, because re-deriving it risks a
silent mismatch, and because not every tokeniser family has a merge list at all.

## Why a frequent split helps the model: a row is expensive

Every row is one full vector in the embedding table.

```
vocab  50,000 × dimension 4,096  =    204,800,000 parameters    391 MB at fp16
vocab 250,000 × dimension 4,096  =  1,024,000,000 parameters   1953 MB at fp16
```

A billion parameters before a single transformer layer exists. The vocabulary is a budget
of scarce, expensive slots, and frequency is how you decide what deserves one.

Three benefits:

1. **Every row gets enough training examples.** A row starts as random numbers and only
   becomes meaningful by being adjusted each time the model sees that token. A piece seen
   a million times gets a million adjustments; a piece seen four times stays near random.
2. **Shorter sequences.** `_the` as one token instead of four is four times less work in
   every layer above, on the most common word in English.
3. **Shared pieces generalise.** One well-trained `play` row serves `playing`, `player`,
   `plays`, `played`, `replay`.

## Where frequency, as a proxy, fails

Frequency has no idea what a meaningful unit is.

- **Numbers.** `1024` may be one token while `1025` splits into three. Two similar
  quantities become structurally different inputs.
- **Rare names and identifiers.** They shatter into fragments that individually mean
  nothing, and the model must reassemble them.

These are tokenisation artefacts, not reasoning failures. It is why models miscount
letters in a word.

## Two different "trainings", and two different corpora

This was the main confusion of the session.

```
TRAINING THE TOKENISER   counting pairs in a corpus         (Pipeline A)
TRAINING THE MODEL       adjusting billions of numbers      (gradient descent)
```

The timeline:

```
 1. collect a corpus
 2. PIPELINE A: count pairs, merge, repeat
        -> merge list + vocabulary, FROZEN from this moment
 3. tokenise the model's training data using that frozen tokeniser
 4. TRAIN THE MODEL on those token IDs
        weights change. embedding rows change. the merge list does not.
 5. INFERENCE: Pipeline B, replaying the same frozen merge list
```

The merge list order never changes — not after model training, not at inference, not ever.

The confusion comes from step 3: the model's training data passes **through** the
tokeniser, so the tokeniser is present during model training. It is being used, not
trained, exactly as at inference.

The two corpora also have separate roles, even when drawn from the same pile of text:

```
tokeniser corpus     counted once, then discarded   -> decides HOW MANY TOKENS text costs
model training data  fed to the model repeatedly    -> decides HOW WELL the model handles it
```

## Why a fixed order from one corpus is still the right thing to replay

At runtime the merge list is not a ranking of importance. It is a recipe for reproducing
**the same cutting that was used when the model's training data was tokenised**.

```
correctness  =  the same merge list is used everywhere
             NOT  the merge list matches the frequencies of the current input
```

Corpus frequency is the rule used to build that list because, when the corpus resembles
the real input, it minimises token count. When it does not resemble the input, the penalty
is cost, not correctness.

### Measured: same algorithm, same budget, two corpora

```
sample            english-trained   python-trained
english prose          14 tok            20 tok
python code            31 tok            10 tok

the same python line, cut two ways:
  english-trained:  d e f ' c' ou nt _ p a ir s ( w or d _ p i ec es, …    31 tokens
  python-trained :  'def' ' count' '_pair' 's(' 'word' '_pieces' …         10 tokens

both decode back to the original text: True, True
```

Neither tokeniser is wrong. The English-trained one handles Python perfectly correctly.
It just spends 31 tokens where 10 would do.

## Lossless is not the same as harmless

An important correction to a statement that was too clean.

```
lossless   the bytes come back exactly. no information is destroyed.   always true
harmless   the model handles the text just as well.                    not guaranteed
```

A mismatched corpus causes three things, and only the first is purely money:

1. **Cost and latency.** More tokens in, more tokens out, less context window left.
2. **Compute that grows faster than the token count.** Attention cost rises with the
   square of sequence length (to be derived in Block 2). Three times the tokens is more
   than three times the work in that part of the model.
3. **Quality, indirectly.** Meaning has to be rebuilt from fragments that carry almost
   nothing on their own, and rare pieces have poorly trained rows.

Point 3 is a real and widely observed effect, but it has **not** been measured in this
repository. Treat it as "known in practice, not derived here". Points 1 and 2 are
derivable, and point 2 will be derived in Block 2.

What genuinely corrupts output is not a mismatched corpus but a tokeniser that does not
match the model — a different merge list, or shifted IDs. In that case the model receives
words nobody typed, and nothing raises an error.

## Scripts written this session

| Script | What it shows |
|---|---|
| `code/block-01/pipeline_a_traced.py` | Pipeline A on nine words, every stage and every merge printed |
| `code/block-01/cost_of_missing_merges.py` | What unmerged text costs: Tamil 83 tokens vs English 7 |
| `code/block-01/two_corpora_compared.py` | English-trained vs Python-trained tokeniser on the same text |

## Still open

- [ ] Unanswered check: a new special token is inserted at ID 300, shifting every piece
      above it up by one, and the model is unchanged. What does the user see?
- [ ] The Block 1 gate: Tamil and English token counts with a real tokeniser.
- [ ] Embeddings, after Block 0.
