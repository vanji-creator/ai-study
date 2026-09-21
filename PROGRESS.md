# Progress

## Current
Block: 1 — Text into numbers
Started: 2026-09-16
State: session 2 (2026-09-18) — restarted tokenisation from zero after he said the
first teaching was not clear. Covered, slowly and in English: tokeniser = text -> integer IDs
via fixed dictionary; KeyError on unknown words; big dictionary and nearest-spelling both fail;
letters never fail but cost ~4x tokens; hybrid (word else split into biggest known pieces);
BPE: count neighbouring pairs, merge the top one, repeat a FIXED number of times; applying
the ordered merge list to new words. He tokenised `praying` by hand correctly.
Next: bytes instead of letters, why non-English text costs more tokens, special tokens,
trailing space. Then embeddings.

## Completed

| Block | Gate passed | Date | Notes |
|---|---|---|---|

## Weak spots to revisit
- [ ] Believed word splits / dictionary entries carry meaning by themselves — came back in session 2. Meaning comes from training, IDs are like primary keys. Re-check cold.
- [ ] Thought BPE stops when counts drop — it stops after a fixed number of merges (vocabulary size). Re-check.

## Open questions
- Tamil suffix examples (வீடு / வீட்டில் / வீட்டுக்கு / வீட்டிலிருந்து) — Vikash to confirm they are correct

## Notes to tutor
- Session 1 teaching was too dense (many beats per message). He asked to rewind fully.
  What worked in session 2: Python dict as the vocabulary, one small step per message,
  a question after each step, letting him find the rule ("count what appears most").
- He asked to be taught in English, not with Tamil examples. The Block 1 gate still
  asks for a Tamil token count — raise that only at the gate.
- Vikash said the numeric guessing felt irrelevant. Use predictions only when they test
  a belief he holds, not for random numbers.
