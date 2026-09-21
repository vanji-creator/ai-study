# Progress

## Current
Block: 1 — Text into numbers
Started: 2026-09-16
State: TOKENISATION FINISHED (2026-09-21), mini-check passed.
Covered: tokeniser = text -> integer IDs from a fixed dictionary; why whole words and
single letters both fail; pieces; BPE (count neighbouring pairs, merge the top one, fixed
number of merges); applying an ordered merge list to unseen words; code points, utf-8 and
why the 256 byte values are the safety net; why non-English costs more tokens (more bytes
per character AND fewer merges learned for it); special tokens and who inserts them;
OpenAI tokeniser public via tiktoken, Anthropic's is not (count_tokens endpoint,
model-specific; tiktoken undercounts Claude by ~15-20%); trailing space (the space belongs
to the word after it, so a trailing space leaves a rare lone-space token).
Mini-check: 4 questions cold. 3 right first pass. Q3 (two reasons non-English costs more)
needed a merge-list recap, then correct.
NOT yet done in Block 1: the gate (Tamil vs English token count needs a real tokeniser),
and the whole embeddings half.
Next, agreed order: Block 0 (neural network basics) -> embeddings -> Block 1 gate.
Block 0 beat 1 was already started: reranker latency example, weight as a parameter,
squared error loss = 120 at weight 0.5. He has not yet computed loss at weight 0.2.

## Completed

| Block | Gate passed | Date | Notes |
|---|---|---|---|

## Weak spots to revisit
- [ ] The merge list: where it comes from, that it is built once by counting before
      training, and that frequency in THAT corpus decides the vocabulary. Needed a
      recap on 2026-09-21. Re-check cold.
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
