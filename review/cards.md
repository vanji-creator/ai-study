# Review cards

Run `python3 review/review.py` to be asked these on a schedule.

Format: a card starts at a line beginning `### id:`. `Q:` and `A:` may run over several
lines. Editing a card does not reset its schedule; the id is what the schedule tracks.

A sub-topic is not finished until its cards are written here.

---

### id: tok-001
block: 1
Q: What does a tokeniser do, and what does it produce?
A: It cuts text into pieces that exist in a fixed dictionary and replaces each piece with
   its integer ID. Text in, list of integers out. The dictionary is fixed before training
   and never changes.

### id: tok-002
block: 1
Q: Why can a byte-level tokeniser never fail on an input?
A: Every input is already bytes, and all 256 byte values have rows. There is always a
   fallback piece, so no text in any script can produce a missing entry.

### id: tok-003
block: 1
Q: What decides which pieces become tokens?
A: Frequency in the counting corpus. The most frequent pair of neighbouring pieces is
   merged, and that repeats a fixed number of times.

### id: tok-004
block: 1
Q: When does the merging loop stop?
A: After a fixed number of merges chosen in advance — the vocabulary size. Not when the
   counts get small.

### id: tok-005
block: 1
Q: Does training the model change the tokeniser?
A: No. The tokeniser is built before model training and is frozen. Model training changes
   the embedding rows and the weights, never the merge list.

### id: tok-006
block: 1
Q: The same sentence gives 22 tokens on one model and 30 on another. Why?
A: Different merge lists, learned from different corpora, with different vocabulary sizes.
   The tokeniser is a property of the model.

### id: tok-007
block: 1
Q: Give both reasons a Tamil or Japanese sentence costs more tokens than its English
   translation.
A: One, UTF-8 uses about 3 bytes per character instead of 1, so the sequence starts
   longer. Two, the counting corpus was mostly English, so few merges apply and the text
   stays near the byte level.

### id: tok-008
block: 1
Q: What does the integer ID of a token mean?
A: Nothing on its own. It is a row number, like a primary key. Meaning is learned during
   model training from seeing that row in many sentences.

### id: tok-009
block: 1
Q: Why is a word-level vocabulary a bad idea, in two ways?
A: Unseen words have no row and collapse into one junk entry. And the long tail is huge —
   64.5% of distinct words in CLAUDE.md appear exactly once — so most rows would barely be
   trained. It also separates shared roots like play and playing.

### id: tok-010
block: 1
Q: Why not use single letters for everything?
A: It never fails, but sequences become roughly 4x longer and attention cost grows faster
   than linearly with length. The model must also rebuild every word from letters.

### id: tok-011
block: 1
Q: Is é ever replaced by e?
A: No. e is code point 101 and é is 233 — different characters. é is stored as bytes 195
   and 169, which decode back to é exactly. Nothing is approximated.

### id: tok-012
block: 1
Q: Why does UTF-8 use two bytes for é when 233 would fit in one byte?
A: Byte values 0–127 are reserved for ASCII. Any byte above 127 signals that more bytes
   follow, so 233 alone would be ambiguous.

### id: tok-013
block: 1
Q: What is the output of tokeniser training, and what happens to the corpus?
A: An ordered merge list plus a vocabulary mapping pieces to IDs. The corpus is discarded.

### id: tok-014
block: 1
Q: How is a word the tokeniser has never seen handled?
A: Not as a special case. The merges are replayed in order; whatever matches is joined and
   the rest stays as smaller pieces or single bytes. replaying becomes r | e | play | ing.

### id: tok-015
block: 1
Q: Why must pre-tokenisation happen before merging?
A: To stop merges crossing word boundaries. Without it a frequent pair spanning two words
   would become a single token.

### id: tok-016
block: 1
Q: Which token does a space belong to, and what follows from that?
A: The word after it. _the and the are different tokens, and a trailing space in a prompt
   leaves a rare lone-space token that forces the model into a state it seldom saw in
   training.

### id: tok-017
block: 1
Q: What makes a special token special?
A: It is a row no user text can produce. Typing the marker characters gives ordinary
   pieces with different IDs, so message boundaries live in a channel content cannot write
   into.

### id: tok-018
block: 1
Q: Who inserts special tokens, and when can a user forge one?
A: The application or the provider's server, before the model runs. A user can forge one
   only if the application tokenises user text with special-token parsing enabled and does
   not strip the markers first.

### id: tok-019
block: 1
Q: How does generation stop?
A: The model produces the end-of-turn ID itself. The serving code sees it, ends the loop,
   and does not display it.

### id: tok-020
block: 1
Q: Why can you not use tiktoken to estimate Claude costs?
A: It is OpenAI's merge list. It undercounts Claude by roughly 15–20% on ordinary English
   and more on code and non-English text. Use the provider's own counting endpoint.

### id: tok-021
block: 1
Q: After stage A2, how many rows does Pipeline A work on, and what are the two columns?
A: One row per distinct chunk — six for the nine-word corpus. Column one holds the pieces
   and changes with every merge; column two holds the count and never changes.

### id: tok-022
block: 1
Q: Why can _cat come before _the in a merge list, but never before _c?
A: Different chains may be ordered by frequency, so _cat before _the is valid. _cat is the
   pair _c + at, so it cannot precede its own ingredient — it would match nothing and be
   silently skipped.

### id: tok-023
block: 1
Q: A tokeniser's corpus does not match the text a user sends. What is lost, and what is not?
A: Nothing is lost — tokenisation stays lossless and the text decodes exactly. What is paid
   is cost: more tokens, more than proportionally more attention compute, less context
   window, and indirectly some quality.

### id: tok-024
block: 1
Q: Why is a vocabulary row expensive?
A: Each row is a full vector in the embedding table. At vocabulary 50,000 and dimension
   4,096 that table alone is 204.8M parameters, 391 MB at fp16.

### id: tok-025
block: 1
Q: Name the five stages of Pipeline A.
A: A1 corpus. A2 pre-tokenise and count. A3 split into pieces. A4 the loop — count pairs,
   merge the top one, repeat. A5 output — ordered merge list plus vocabulary.
   Hook: text, count, pieces, loop, keep.

### id: tok-026
block: 1
Q: Name the stages of Pipeline B.
A: B1 raw text. B2 normalise. B3 pre-tokenise. B4 encode to bytes. B5 apply the merge list
   in order. B6 pieces to IDs. B7 the application adds special tokens.

### id: tok-027
block: 1
Q: A new special token is inserted at ID 300 and every piece above it shifts up by one.
   The model is not retrained. What does the user see?
A: Fluent, confident answers about the wrong words. The model reads shifted rows, so it
   answers a sentence nobody typed. No error is raised anywhere — every component is
   individually correct, only the agreement between them is broken.

### id: tok-028
block: 1
Q: Why does frequency, as a rule for choosing pieces, help the model?
A: Frequent pieces get many gradient updates so their rows become meaningful; sequences get
   shorter; and shared pieces like play serve playing, player, plays at once.

### id: tok-029
block: 1
Q: Where does frequency fail as a proxy?
A: It has no idea what a meaningful unit is. 1024 may be one token while 1025 splits into
   three, and rare names shatter into fragments. These are tokenisation artefacts, not
   reasoning failures.

### id: tok-030
block: 1
Q: Name the two "trainings" and the two corpora, and say what each decides.
A: Training the tokeniser is counting pairs in a corpus; training the model is gradient
   descent. The tokeniser corpus decides how many tokens text costs; the model's training
   data decides how well the model handles it.

---

### id: nn-001
block: 0
Q: What is a parameter?
A: One number inside the model that training is allowed to change. Training means finding
   good values for them.

### id: nn-002
block: 0
Q: What is the loss, and why is it squared?
A: One number saying how wrong the current parameters are on the data. Squaring makes
   negative errors count the same as positive ones, and makes large errors count much more
   than small ones.

### id: nn-003
block: 0
Q: What is a gradient, in words?
A: For one parameter: if I nudge this up a little, what happens to the loss and how fast.
   Its sign says which direction is downhill; its size says how steep the ground is.

### id: nn-004
block: 0
Q: Why does the gradient shrink as training approaches a good value?
A: Near the bottom of the valley the loss barely changes when the parameter changes. That
   gives big steps when far away and small steps when close, without anything knowing where
   the bottom is.

### id: nn-005
block: 0
Q: Write the update rule and explain the minus sign.
A: new_weight = weight − learning_rate × gradient. The gradient points uphill — it says how
   fast the loss rises if you increase the parameter — so you move the other way.

### id: nn-006
block: 0
Q: Why does the learning rate exist at all?
A: The raw gradient is far too large to use as a step. At weight 0.10 the gradient was
   −1170; subtracting it lands at 1170. The direction is right, the size is catastrophic.

### id: nn-007
block: 0
Q: Why does a learning rate that is too large make the loss get worse, not just converge
   slower?
A: Each overshoot lands further up the far side, where the ground is steeper, so the
   gradient is bigger, so the next overshoot is bigger. The loss grows without limit —
   this is what a NaN loss after a few steps looks like.

### id: nn-008
block: 0
Q: Why can training not simply try many values and pick the best?
A: A grid of ten values per parameter over 204 million parameters is 10^204,800,000
   evaluations. Searching is not slow, it is impossible. Training can only feel the ground
   where it is standing.

### id: nn-009
block: 0
Q: Name the five things gradient descent needs.
A: A parameter, a loss, a gradient, a learning rate, and repetition until the gradient is
   near zero.

### id: nn-010
block: 0
Q: In the reranker example, what were the parameter, the loss at weight 0.5, and the
   correct weight?
A: Parameter: weight in predicted_time = weight × candidates. Loss at 0.5 was 120. The
   valley bottom was weight 0.3, loss 0 — zero only because those three measurements lie
   on a perfect line.

### id: nn-011
block: 0
Q: Why does real training not find gradients by peeking a small step to the right?
A: Peeking costs one extra loss evaluation per parameter and is only approximate. Calculus
   gives the exact slope, and backpropagation gets it for every parameter in one backward
   sweep.

### id: nn-012
block: 0
Q: An embedding row starts as random numbers. What makes it meaningful?
A: Being adjusted each time the model sees that token in training. A piece seen a million
   times gets a million adjustments; a piece seen four times stays close to random.

### id: nn-013
block: 0
Q: Draw the loss curve for one parameter. What is on each axis, what shape is it, and what
   does training mean on that picture?
A: Weight across the bottom, loss up the side. A valley, lowest at the correct weight.
   Training means walking to the bottom while never being allowed to see the picture — the
   model only knows the one spot it is standing on.

### id: nn-014
block: 0
Q: What is the gradient, described using the loss curve rather than a formula?
A: The tilt of the ground at the one spot you are standing on, as a single number. Its sign
   says which way the ground slopes; its size says how steep. At weight 5 the tilt was 16,
   at the bottom it was 0.

### id: nn-015
block: 0
Q: Two learning rates, 0.000333 and 0.000334, on the same problem. One converges, one
   explodes. What single quantity decides it?
A: The multiplier 1 - (2 x sum of squared inputs) x learning_rate. While its size is under
   1 the distance from the answer shrinks each step; over 1 it grows. Because the inputs
   set that number, the safe learning rate depends on the scale of the input data — which
   is why inputs are normalised and learning rates are tuned, not derived.

### id: nn-016
block: 0
Q: With two parameters instead of one, what exactly is "the gradient"?
A: Not one number — one per parameter. Standing at a point you ask two separate questions:
   if I move only the weight, which way and how steeply does the loss go? And the same for
   the bias. The gradient is the pair of answers, one tilt per direction you could move in.

### id: nn-017
block: 0
Q: Where does `actual` come from, and what is the loop called that has it?
A: Somebody supplies it — a measurement made before training. Those supplied answers are
   labels, and learning from them is supervised learning. No labels, no error, no gradient.
   A language model gets its labels free: the actual is the next token in the text.

### id: nn-018
block: 0
Q: What is the difference between training and inference, stated in terms of `actual`?
A: During training an actual exists for every row, so an error and a gradient exist and the
   parameters change. At inference there is no actual — that is why you are asking — so no
   error, no gradient, and the parameters are frozen.

### id: nn-019
block: 0
Q: Why is the bias's gradient `2 x (1 x error)` while the weight's is `2 x (input x error)`?
A: The factor is how far the prediction moves when that parameter moves by 1. The weight is
   multiplied by the input, so its influence is the input. The bias is only added, so its
   influence is 1 whatever the input. The bias is a weight whose input is always 1.

### id: nn-020
block: 0
Q: You chain two weight-and-bias stages with nothing between them. What do you get, and why?
A: A straight line — exactly what one stage gives. Substituting collapses it to
   ((weight2 x weight1) x input) + ((weight2 x bias1) + bias2), two numbers. Any number of
   such stages equals one of them, because multiplying and adding cannot produce anything
   else. Adding parameters this way buys nothing.

### id: nn-021
block: 0
Q: State the ReLU rule, and say what it produces when placed between two stages.
A: If the value is negative it becomes 0, otherwise it is left alone. It breaks the collapse:
   the output becomes straight pieces joined at bends, so the gaps between predictions stop
   being constant. One ReLU gives one bend; enough bends trace any curve.

### id: nn-022
block: 0
Q: Why does the field use one simple non-linear rule everywhere instead of picking the right
   curve for each problem, like input squared?
A: Picking input squared requires already knowing the answer's shape. Real data does not tell
   you, and with several inputs you would also have to guess how they combine. Many learned
   bends need only data.

### id: nn-023
block: 0
Q: What decides WHERE a ReLU bend sits?
A: The bias feeding it. With weight1 = 1 and bias1 = -2 the bend is at input 2. Change the
   bias and the bend moves, so the position of every bend is an ordinary learned parameter.

### id: nn-024
block: 0
Q: A layer's hidden values are all positive for your data. What has the ReLU done?
A: Nothing. It only bends the function where it actually blocks a negative value, so for
   that data the layer is still a plain straight line.

### id: nn-025
block: 0
Q: Updating after every single row instead of adding rows together — is that wrong, and does
   it have a name?
A: Not wrong. It is stochastic gradient descent, and it is what real models use, because
   billions of rows cannot be added up before one step. It reaches the same place by a
   wandering path rather than a straight one.

### id: nn-026
block: 0
Q: Is the loss the SUM of the squared errors or the AVERAGE? What turns on the answer?
A: Either — it is a convention, not a law. Dividing by the number of rows makes every
   gradient that many times smaller, and the learning rate cancels it exactly; the direction
   never changes. People divide so the learning rate keeps working when the number of rows
   per step changes.
