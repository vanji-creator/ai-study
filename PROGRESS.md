# Progress

Last updated: 2026-10-05. Written as a handover — a new session on another machine should
be able to continue from this file alone.

---

## Current

Week 4 of 16 begins 2026-10-07. Started 2026-09-16.

**The syllabus was revised on 2026-10-05**, at his request, to cover everything an AI/ML
engineer is expected to know. Added: Block M (machine learning foundations), prompt
engineering inside Block 5, scaling laws inside Block 2, Block 10 (multimodal, one session),
Track A (applied tools — PyTorch to MLOps), Track C (timed coding challenges), Track S
(behavioural stories). The schedule went from twelve weeks to sixteen. All of it is in
`CLAUDE.md` §6 and §11.

Block in progress: **Block 0 — How a model learns.** Everything taught except
backpropagation.

### What is finished

**Block 1 Part 1 · Tokenisation — taught.** Mini-check passed cold 2026-09-21. The full
Block 1 gate has not run: it needs embeddings and a real tokeniser.

**Block 0 · taught except backprop.** Parameter; loss and why it is squared (two reasons);
gradient as the tilt of the loss curve; the update rule; both learning-rate failure modes
and why a large one explodes; stochastic gradient descent, one row at a time; two
parameters; the bias as a weight whose input is always 1; where `actual` comes from, and
that a language model gets it free from the next token; two linear stages collapse into
one; `max(0, value)` and the bend; bend positions found by gradient descent; negative rates
turning the line downward; overfitting, shown with 3 pieces against 30 on noisy data.

**Review system.** Built 2026-09-22. 59 cards. First real session run 2026-09-30.

### The review result that matters

2026-09-30, eight cards answered cold: **2 right, 6 missed.** Every miss had the same
shape — the fact was right, the consequence attached to it was missing. Example: he named
the space as belonging to the following word, but not that a trailing space in a prompt
produces a rare lone-space token. A fact-and-consequence sheet for both blocks was given
in chat on 2026-10-02 for him to read before the next review.

He then took a few days off on 2026-10-01 — tired, finding study hard. Do not open the next
session with twelve cards. Use `--limit 4`.

---

## How to start the next session

1. **Review, four cards.** `python3 review/review.py --limit 4`. The six misses from
   2026-09-30 are overdue and come first. Judge honestly: a fact without its consequence is
   a miss, and say which half was missing.
2. **Backpropagation.** Finishes Block 0. He wants paper and pen for it. Two stages, one
   data row, small numbers, brackets on every group. Walk the error backwards one stage at
   a time and check each gradient against the nudge method in
   `code/block-00/slope_by_two_points.py`. The bridge is already laid: in
   `bends_are_learned.py` the gradient for a bend had to pass back through the `max`, and a
   piece whose bend was not reached got a gradient of zero. Script:
   `code/block-00/backprop_by_hand.py`.
3. **Block 0 gate** (`CLAUDE.md` §6). Then Track C: a two-layer network with backprop by
   hand.
4. **Block M and A1 PyTorch** — week 4. Anchor Block M to Clikk (§7).
5. **Block 1 Part 2, embeddings, and the Block 1 gate** — week 5. The gate needs
   `pip install tiktoken`; system Python here is 3.12 with pip 24.0, so use a virtual
   environment. If the install fails, use the repo's own BPE and label the numbers as ours.

### If an interview gets a date

He has a referral for **Junior AI/ML Engineer at Infobell IT Solutions, Bangalore**. The
referrer was applying on 2026-10-05; no interview is scheduled. The JD names LangGraph,
LangChain, LlamaIndex, CrewAI, vector databases, RAG, agentic AI, cloud, Docker,
Kubernetes. His resume lists most of those as "working knowledge / currently learning", and
names LangGraph in the HopTrace project.

When a date exists, apply the interview override in `CLAUDE.md` §6 Track A: A5 LangGraph
and Block 8 first, then A3 vector databases, then Block 4 inference (Infobell builds an
inference framework for AMD hardware), then resume defence of every bullet. A ten-day plan
for this was drafted in chat on 2026-10-04, and the first script exists:
`code/interview/01_agent_loop_plain_python.py` — a two-hop question answered by a plain
Python loop, before LangGraph. He was asked to predict its output and had not yet answered.

---

## Completed

| Block | Gate passed | Date | Notes |
|---|---|---|---|
| 1 (Part 1, tokenisation) | mini-check only | 2026-09-21 | Full Block 1 gate still not run — it needs embeddings and a real tokeniser |

---

## Weak spots to revisit

- [ ] **Gives the fact, drops the consequence.** The pattern behind six of eight misses on
      2026-09-30. In an interview this is exactly where the follow-up question lands.
- [ ] Described Pipeline A stage A4 as "count once and sort descending". It is a loop:
      count pairs, merge one, recount. Proof: `code/block-01/why_the_loop_must_recount.py`
      (`banana` creates `na+na`, which was not in the first count). Cards `tok-031`, `tok-032`.
- [ ] Two reasons Tamil costs more: he gives the corpus reason and forgets the bytes reason.
- [ ] Squaring the error does two jobs; he gives only "removes the sign".
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
review/cards.md                    59 cards: 32 tokenisation, 27 Block 0
review/schedule.json               due dates and boxes, committed so it travels

notes/block-01.md                  written notes + the 15-heading revision outline
                                   + the full 2026-09-22 Pipeline A write-up
notes/tokenisation-reference.html  the single revision reference, published as an artifact
notes/recall/TEMPLATE.md           cold-dump template for recall attempts
notes/recall/tokenisation-1.md     first recall attempt, not yet filled in

code/block-00/loss_curve.py            loss across many weights — the valley
code/block-00/slope_by_two_points.py   the gradient found by peeking one step right
code/block-00/gradient_descent.py      three learning rates: works, oscillates, explodes
code/block-00/why_too_large_explodes.py   the update collapses to one multiplier
code/block-00/see_the_valley.py           the loss curve drawn; gradient as its tilt
code/block-00/two_parameters.py           weight and bias together
code/block-00/bias_is_a_weight_with_input_one.py  influence; gradient measured, not asserted
code/block-00/why_add_the_rows.py         stochastic vs batch; sum vs average
code/block-00/the_loss_is_a_surface.py    two-parameter loss as a contour map
code/block-00/why_non_linearity.py        linear stages collapse; max(0, ...) breaks it
code/block-00/bends_are_learned.py        slab-bill bends found by gradient descent
code/block-00/overfitting.py              3 pieces vs 30 on noisy rows
code/block-00/up_and_down.py              20, 40, 30, 60 fitted with a negative rate

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
code/block-01/why_the_loop_must_recount.py  merging creates pairs the first count lacked

code/interview/01_agent_loop_plain_python.py  two-hop question, plain Python, pre-LangGraph

notes/bending-the-line.html        interactive page on layers and the bend, published at
                                   https://claude.ai/artifact/AjzmYxQ4fbeMwuZw6aXqyc
notes/questions-for-another-model.md  his twelve open questions as a paste-ready prompt
                                   (he used his own prompt instead)
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
