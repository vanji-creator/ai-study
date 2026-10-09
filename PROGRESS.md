# Progress

Last updated: 2026-10-07, on the Mac. From 2026-10-06 he studies only on the Mac. Written so
that a fresh session can continue from this file alone.

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
produces a rare lone-space token. A fact-and-consequence sheet was made on 2026-10-02
(`notes/fact-and-consequence.md`). He read it on 2026-10-06, found it unclear, and disputes
the diagnosis. It is retired — do not suggest it.

He then took a few days off on 2026-10-01 — tired, finding study hard. Do not open the next
session with twelve cards. Use `--limit 4`.

---

## Session 2026-10-06/07 — what happened

- Pulled the Acer's work onto the Mac. The Acer is retired.
- He read `notes/fact-and-consequence.md` and found it unclear. It is now **retired**.
- Review: 1 card asked (nn-002, loss and why square) — **miss**, recorded. The other three
  were not reached.
- Teaching went wrong. The tutor gave `gradient = 2 × (input) × (error)` before its meaning
  and asked him to compute with it. He memorised the formula and lost that *the gradient is
  the slope of the loss*. He also has no maths background, and words like "smooth at zero"
  and "aims at the average" were used without teaching them.
- Fix, at his request: research-backed teaching contract in `CLAUDE.md` §1.2, a
  per-message checklist hook (`.claude/settings.json` → `review/teaching_check.sh`),
  `notes/maths-for-ml.md`, Block 0 cards rewritten to test meaning (nn-002, 005, 010, 015,
  019, 027) and four new cards (nn-028 to nn-031).

Research behind §1.2 (checked 2026-10-07): conceptual-first teaching transfers better and
lowers maths anxiety ([ERIC](https://files.eric.ed.gov/fulltext/EJ1469567.pdf),
[EJMSTE](https://www.ejmste.com/download/the-effect-of-teaching-conceptual-knowledge-on-students-achievement-anxiety-about-and-attitude-12938.pdf));
Mazur's ConcepTests — questions that cannot be answered by calculation
([SERC](https://serc.carleton.edu/sp/library/conceptests/what.html)); hinge questions whose
wrong options are known misconceptions
([guide](https://www.structural-learning.com/post/hinge-questions-teachers-complete-guide));
elaborative interrogation and self-explanation, Dunlosky et al. 2013
([PDF](https://www.whz.de/fileadmin/lehre/hochschuldidaktik/docs/dunloskiimprovingstudentlearning.pdf));
concreteness fading
([ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0959475212000333)).

## How to start the next session

**Method changed 2026-10-09: he self-studies from `notes/self-study-list.md`, the tutor
verifies by cold recall.** He did not want more lectures. Backpropagation was taught
briefly on 2026-10-09 (chain rule; two-box example, gradients −2 and −12, checked by
nudging); List 1 there is what he studies next, then the Block 0 gate.

1. **Review, four cards, judged on meaning.** `python3 review/review.py --limit 4`. Note
   the runner orders by due date, so never-seen cards come first; put the 2026-09-30 misses
   (nn-005, tok-007, tok-016, tok-022, tok-025) and nn-002 first by hand. A recited formula
   without its meaning is a miss.
2. ~~Re-teach "the gradient is the slope of the loss"~~ — done 2026-10-07. What it was: the question → the valley picture (`code/block-00/see_the_valley.py`) → measure the
   slope by nudging (`code/block-00/slope_by_two_points.py`, code computes, he reads) →
   only then the shortcut `2 × (input) × (error)`, as "a faster way to get what we measured,
   for loss = error² only". Check with meaning questions, never arithmetic.
3. **Backpropagation.** Finishes Block 0. He wants paper and pen for it. Two stages, one
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

### Parked

An interview referral (Infobell, Junior AI/ML Engineer) came up on 2026-10-04. On
2026-10-05 he said to ignore it for now. Do not raise it. If he brings an interview back
with a date, apply the interview override in `CLAUDE.md` §6 Track A. The one script written
for it stays: `code/interview/01_agent_loop_plain_python.py`.

---

## Completed

| Block | Gate passed | Date | Notes |
|---|---|---|---|
| 1 (Part 1, tokenisation) | mini-check only | 2026-09-21 | Full Block 1 gate still not run — it needs embeddings and a real tokeniser |

---

## Weak spots to revisit

- [x] **Memorised the gradient formula; lost that the gradient is the slope of the loss**
      (2026-10-07). Re-taught the same day on the §1.2 ladder: question → valley →
      measured by nudging → sign from after − before → derived 2 × input × error with
      (a + b)². He judged it "understanding required for engineering level". Cards nn-028,
      nn-031, nn-033, nn-034 will test it cold.
- [ ] **Thought the gradient is the height of a point above the minimum** (2026-10-07).
      Fixed with weights 0.1 and 0.5: same loss 16, gradients −160 and +160. Card nn-032.
- [ ] Why we square, and why a loss is needed at all (nn-002, nn-030, nn-031). The
      "smooth at zero" and "aims at the average" reasons were not understood — they need
      `maths-for-ml.md` entries taught first (median not yet taught).

- [ ] ~~Gives the fact, drops the consequence~~ — he disputes this diagnosis (2026-10-07);
      the misses are better explained by teaching that gave facts without understanding.
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
notes/fact-and-consequence.md      RETIRED 2026-10-07 — unclear to him; history only
notes/maths-for-ml.md              every maths idea taught, in his terms. Check before
                                   using any maths word (CLAUDE.md §1.2 C)
review/teaching_check.sh           checklist printed before every reply by the hook in
                                   .claude/settings.json (CLAUDE.md §1.2)
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

- **2026-10-07 — teaching failures, in order, so they are not repeated.** (1) Formula
  before meaning; he memorised `2 × input × error` as "the gradient". (2) Arithmetic
  questions ("what is the gradient if the error is 0.1?") — he: "one can do that with a
  calculator". (3) Maths words without teaching. (4) Answered a narrower question than the
  one asked, then defended it; he had to ask for an online check. (5) Widening — source
  tables, extra reasons. (6) The fact→consequence sheet, built on an assumption. All six
  are now rules in `CLAUDE.md` §1.2, with a checklist hook that prints every turn.
- **He has no maths background** (2026-10-07). Teach the maths when a concept needs it,
  with numbers, and record it in `notes/maths-for-ml.md`.
- **He was right that one row was broken** (2026-10-06): the tutor summed two rows to show
  why squaring matters, against his one-row rule. With one row, the reason is: without the
  square, −4 is "smaller" than 0, so no error is not the lowest point.

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
