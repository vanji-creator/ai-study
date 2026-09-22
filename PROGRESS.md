# Progress

## Current

Block: 0 — How a model learns (inserted 2026-09-21), then Block 1 Part 2 — embeddings
Started: 2026-09-16

Plan agreed 2026-09-22: finish the gaps in Blocks 0 and 1, consolidate both together with
definitions, examples and cross-questions, then marinate for 2-3 days. Spaced repetition is
now a standing rule — see CLAUDE.md §12.

State:
- Block 1 Part 1, tokenisation — FINISHED, mini-check passed cold 2026-09-21.
  Pipeline A re-taught in depth 2026-09-22 after he asked for it again.
- Block 0 — parameter, loss, gradient (sign and size), the update rule, learning rate and
  its two failure modes, gradient descent. All taught with the reranker latency example
  and run in code/block-00/.
- Review system built 2026-09-22: review/review.py, review/cards.md (42 cards),
  review/schedule.json. Scheduling verified by running a session and by REVIEW_TODAY.

Remaining, in order:
1. Block 0: a layer (matrix multiply + non-linearity, and why the non-linearity is
   required), then backpropagation. Then the Block 0 gate.
2. Block 1 Part 2: embeddings — cosine vs dot vs Euclidean by hand, why normalising makes
   them equivalent, dimensionality, bi-encoder vs cross-encoder.
3. Block 1 gate: Tamil vs English token count with tiktoken (to be installed).
4. Consolidation: definitions + examples in one pass, cross-questions, then a cold written
   test in notes/recall/blocks-0-1-1.md.

Open check carried over, ask cold: why does a learning rate that is too large make the
loss get worse rather than merely converge slowly?

## Completed

| Block | Gate passed | Date | Notes |
|---|---|---|---|

## Weak spots to revisit
- [ ] Pipeline A stage boundaries. On 2026-09-22 he could give the sequence but not the
      numbering, merged A2/A3 wrongly, and omitted A5 (the output — merge list +
      vocabulary, the only thing that survives). Hook taught: text, count, pieces, loop, keep.
- [ ] Merge order. Thought a later merge would still apply if run early. It does not:
      the ingredient piece does not exist yet, so the merge silently does nothing.
- [ ] The merge list: where it comes from, that it is built once by counting before
      training, and that frequency in THAT corpus decides the vocabulary. Needed a
      recap on 2026-09-21. Re-check cold.
- [ ] Believed word splits / dictionary entries carry meaning by themselves — came back in session 2. Meaning comes from training, IDs are like primary keys. Re-check cold.
- [ ] Thought BPE stops when counts drop — it stops after a fixed number of merges (vocabulary size). Re-check.

## Open questions
- Unanswered check, ask at the start of the next session: a new special token is inserted
  at ID 300, shifting every piece above it up by one, and the model is unchanged.
  What does the user see? (Tests whether the vocabulary-as-contract point landed.)
- Tamil suffix examples (வீடு / வீட்டில் / வீட்டுக்கு / வீட்டிலிருந்து) — Vikash to confirm they are correct

## Notes to tutor
- Session 1 teaching was too dense (many beats per message). He asked to rewind fully.
  What worked in session 2: Python dict as the vocabulary, one small step per message,
  a question after each step, letting him find the rule ("count what appears most").
- He asked to be taught in English, not with Tamil examples. The Block 1 gate still
  asks for a Tamil token count — raise that only at the gate.
- Vikash said the numeric guessing felt irrelevant. Use predictions only when they test
  a belief he holds, not for random numbers.
