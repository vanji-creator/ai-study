# Progress

Last updated: 2026-09-22, end of session. Written as a handover — a new session on another
machine should be able to continue from this file alone.

---

## Current

Block: **0 — How a model learns** (part taught), then **Block 1 Part 2 — embeddings**
Started: 2026-09-16

Plan agreed 2026-09-22: finish the gaps in Blocks 0 and 1, consolidate both together with
definitions, examples and cross-questions, then let it settle for 2–3 days. Spaced
repetition is now a standing rule — `CLAUDE.md` §12.

### What is finished

**Block 1 Part 1 · Tokenisation — DONE.** Mini-check passed cold 2026-09-21. Pipeline A was
re-taught in depth on 2026-09-22 at his request. Covered: the fixed lookup table
constraint; why whole words and single letters both fail; pieces; BPE as count-pairs,
merge-the-top, repeat for a fixed budget; replaying an ordered merge list on unseen words;
code points, UTF-8 and the 256-byte safety net; the two reasons non-English costs more;
special tokens and who inserts them (Way A vs Way B); the trailing space; OpenAI's public
tokeniser vs Anthropic's private one; the tokeniser family (BPE, WordPiece, Unigram,
SentencePiece as a library); the vocabulary as a contract with the embedding table; the
embedding-table arithmetic; where frequency fails as a proxy; the two "trainings" and the
two corpora; correctness from consistency, efficiency from representativeness; lossless is
not harmless.

**Block 0 · part taught.** Parameter, loss and why it is squared, gradient as direction
and steepness, the update rule `new_weight = weight − learning_rate × gradient`, the
learning rate and both of its failure modes, gradient descent. All anchored to his own
reranker latency measurements (10/20/50 candidates → 3/6/15 s, true weight 0.3).

**Review system · built 2026-09-22.** 42 cards, Leitner boxes, verified by running a
session and by the `REVIEW_TODAY` override.

---

## How to start the next session

1. **Run the review first.** `python3 review/review.py`. Ask the due cards cold, judge
   honestly, a vague answer is a miss.
2. **Clear the one open check** (it is card `nn-007`, and he has dodged it twice):

   > Why does a learning rate that is too large make the loss get *worse*, rather than just
   > converge slowly? Use the word gradient.

   The run to show him if he needs the numbers is in `code/block-00/gradient_descent.py`,
   learning rate 0.0005: weight 0.5 → −0.1 → 1.1 → −1.3, loss 120 → 480 → 1,920 → 7,680.
   Expected answer: each overshoot lands further up the far side where the ground is
   steeper, so the gradient is larger, so the next overshoot is larger.

3. **Then teach, in this order:**

   **Next beat — from one parameter to a layer.** Extend the reranker formula to two
   parameters: `predicted_time = weight × candidates + fixed_overhead`. The loss becomes a
   surface rather than a curve, and there is now one gradient per parameter. Then: a layer
   is a matrix multiply plus one non-linear function, and without the non-linearity a stack
   of layers collapses into a single layer — show this numerically, do not assert it.
   Scripts to write: `code/block-00/two_parameters.py`, `code/block-00/why_non_linearity.py`.

   **Then — backpropagation.** A two-layer toy by hand: one forward pass with real numbers,
   then the chain rule walked backwards, checking each analytic gradient against the
   peek-to-the-right method already in `code/block-00/slope_by_two_points.py`. The point to
   land: backprop is not a different idea from gradient descent; it is how every gradient is
   obtained in one backward sweep instead of one peek per parameter.
   Script: `code/block-00/backprop_by_hand.py`. Then run the Block 0 gate (`CLAUDE.md` §6).

   **Then — Block 1 Part 2, embeddings.** Cosine, dot product and Euclidean built with
   explicit loops before any library; why normalising makes cosine and dot product
   equivalent (a listed weak spot); dimensionality anchored to LaBSE 768 catching 15 of 22
   planted errors where MiniLM 384 caught 0; bi-encoder vs cross-encoder anchored to the
   latency gap he measured.

   **Then — the Block 1 gate.** Needs a real tokeniser: `pip install tiktoken` (his choice,
   agreed). Write `code/block-01/gate_token_ratio.py` to count a Tamil sentence and its
   English translation and break the ratio into the two taught causes. If the install
   fails, fall back to the repo's own BPE and label the numbers as ours.

   **Then — consolidation across 2–3 days.** Definitions with their smallest worked example;
   cross-questions that need both blocks at once; then a cold written test in
   `notes/recall/blocks-0-1-1.md`, marked ✓ / ~ / ✗ / –, with every ✗ and – becoming a new
   card at box 1.

---

## Completed

| Block | Gate passed | Date | Notes |
|---|---|---|---|
| 1 (Part 1, tokenisation) | mini-check only | 2026-09-21 | Full Block 1 gate still not run — it needs embeddings and a real tokeniser |

---

## Weak spots to revisit

- [ ] Pipeline A stage boundaries. On 2026-09-22 he gave the sequence but not the
      numbering, merged A2/A3 wrongly, and omitted A5 — the output, which is the only
      stage whose result survives. Hook taught: **text, count, pieces, loop, keep**.
- [ ] Merge order. Thought a later merge would still apply if run early. It does not: the
      ingredient piece does not exist yet, so the merge silently does nothing.
- [ ] Believed dictionary entries carry meaning by themselves. They do not — an ID is a
      primary key, meaning is learned during model training. This one resurfaced twice.
- [ ] Thought BPE stops when counts drop. It stops after a fixed number of merges.
- [ ] Believed pieces let a tokeniser accept a small spelling mistake as the right word.
      It never corrects or approximates: `birdz` → `bird | z`, still `birdz`.
- [ ] Why normalising makes cosine and dot product equivalent — not yet taught.
- [ ] Bi-encoder vs cross-encoder — not yet taught.

All of these exist as cards in `review/cards.md`, so the schedule will bring them back.

---

## Open questions

- Card `nn-007`, unanswered twice: why a too-large learning rate makes the loss worse
  rather than slower. Ask cold at the start of the next session.
- Tamil suffix examples used on 2026-09-16 (வீடு / வீட்டில் / வீட்டுக்கு / வீட்டிலிருந்து) —
  he has not confirmed they are correct.
- `pip install tiktoken` has not been attempted yet; internet access from this machine is
  unverified.

---

## Where things are

```
CLAUDE.md                          the teaching contract. §12 is the review rule.
AGENTS.md                          same session-start rule for the Codex side
PROGRESS.md                        this file

review/review.py                   spaced repetition runner, standard library only
review/cards.md                    42 cards: 30 tokenisation, 12 Block 0
review/schedule.json               due dates and boxes, committed so it travels

notes/block-01.md                  written notes + the 15-heading revision outline
                                   + the full 2026-09-22 Pipeline A write-up
notes/tokenisation-reference.html  the single revision reference, published as an artifact
notes/recall/TEMPLATE.md           cold-dump template for recall attempts
notes/recall/tokenisation-1.md     first recall attempt, not yet filled in

code/block-00/loss_curve.py            loss across many weights — the valley
code/block-00/slope_by_two_points.py   the gradient found by peeking one step right
code/block-00/gradient_descent.py      three learning rates: works, oscillates, explodes

code/block-01/word_frequency_tail.py      the long tail — 64.5% of words appear once
code/block-01/pair_merging_by_hand.py     BPE on low/lower/newest/widest
code/block-01/pair_merging_ing.py         BPE discovering "ing"
code/block-01/space_attached_tokens.py    merges with spaces attached
code/block-01/space_belongs_to_the_word.py  132 of 250 merges begin with a space
code/block-01/text_as_bytes.py            characters vs bytes across scripts
code/block-01/bytes_explained.py          code points, UTF-8, round trip
code/block-01/tokeniser_pipeline.py       both pipelines end to end
code/block-01/pipeline_a_traced.py        Pipeline A on nine words, every stage
code/block-01/cost_of_missing_merges.py   Tamil 83 tokens vs English 7
code/block-01/two_corpora_compared.py     English- vs Python-trained tokeniser
```

**The reference page** is published at
`https://claude.ai/artifact/HU3fWjjAnR4e1sFRBK8yeH` (version 2, private to him). It is
built from `notes/tokenisation-reference.html`; republish that same file path to update it
rather than creating a second artifact. Planned companion page for Block 0:
`notes/block-00-reference.html`, not yet written.

---

## Numbers measured in this repository

Quote these; they were run, not estimated.

```
64.5%      of distinct words in CLAUDE.md appear exactly once
1,355      distinct chunks when CLAUDE.md is pre-tokenised on spaces
656        vocabulary rows from 400 merges (256 bytes + 400)
132 / 250  of the first merges produce a piece beginning with a space
83 vs 7    tokens for a Tamil vs an English sentence, English-only tokeniser (11.9x,
           worst case — real models see some Tamil, hence the usual 3-5x)
31 vs 10   tokens for one Python line, English-trained vs Python-trained tokeniser
204.8M     parameters in a 50,000 x 4,096 embedding table (391 MB at fp16)
120 / 30   loss at weight 0.5 and 0.2 in the reranker example; the valley bottom is 0.3
```

---

## Notes to tutor

- **One row at a time. His explicit rule, given 2026-09-24.** Teach gradient descent with a
  single measurement per update — stochastic gradient descent — never a summed or averaged
  batch. He said: *"i always want to follow stochastic gradient descent only here because am
  not able to fit many probs in my context(brain)"*. Summing two rows made him lose the
  thread. One input, one error, one gradient per parameter, one update, next row.
- **Do not widen.** On 2026-09-24 he objected that once bias arrived the teaching "became
  bad" — too many assumptions about what he already held, and jumps to large problems.
  Named specifics to avoid unless he asks: parameter counts in the millions, embedding
  tables, optimiser names, loss surfaces with several rows at once.
- **Do not improve an explanation he already accepted.** He noticed the squared-error
  explanation had changed and preferred the earlier two-reason version (signs cannot cancel;
  large errors count more). Adding a third reason cost him the first two. When a sub-topic
  has landed, repeat it in the same words.
- **Bracket every group in a formula.** His request, 2026-09-24. Write
  `new weight = weight - (learning rate x gradient for weight)` and
  `predicted = (weight x input) + bias`, not the unbracketed forms. Brackets show what is
  computed first, which is where his arithmetic slips happen.
- **Teaching that works with him:** one small step per message, a question after each step,
  a Python dict or a table he can read, and letting him find the rule himself. Session 1
  failed because it was too dense — several beats per message — and he asked to rewind
  fully.
- **He does not want numeric guessing games.** Predictions only when they test a belief he
  actually holds.
- **English only in explanations.** He asked for this directly. The Block 1 gate still
  requires a Tamil token count; raise Tamil only there, or when he raises it himself.
- **He pushes back well.** On 2026-09-22 he objected to "it only costs tokens" as too
  clean, and he was right — the answer was corrected to lossless-is-not-harmless, with the
  quality claim explicitly marked as not measured here.
- **Unverified claim to keep labelled:** whether badly matched tokenisation hurts model
  quality. Reported in practice, not measured in this repository. Do not let it drift into
  a stated fact.
- **His workflow:** he types cold recall dumps into `notes/recall/`, the tutor marks them
  ✓ / ~ / ✗ / –, and only then is a reference page written or updated. Writing the page
  first removes the thing that produces the learning.
