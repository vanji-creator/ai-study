# Fact and consequence — Blocks 0 and 1

Given in chat on 2026-10-02 and saved here so it survives the move between machines.

Why this sheet exists: on 2026-09-30 he answered eight review cards and missed six. Every
miss had the same shape — the fact on the left was right, and the consequence on the right
was missing. Read this before a review. It is for reading, not for performing.

## Block 1 · Text into numbers

| Fact | And therefore |
|---|---|
| A tokeniser swaps text for IDs from a fixed table | Text in, list of integers out. The table never changes after it is built |
| An ID is only a row number | It means nothing by itself. Meaning lives in the embedding row and is learned during training |
| Whole-word vocabularies fail | An unseen word has no row. And 64.5% of words appear once, so most rows would barely be trained |
| Single letters never fail | But sequences get about 4× longer, and the cost grows faster than the length |
| Pieces sit between the two | Common words become one token, rare words become a few pieces |
| All 256 byte values have a row | No input can ever fail. Any script falls back to bytes |
| é is code point 233, stored as bytes 195 and 169 | Nothing is approximated. é never becomes e, and it decodes back exactly |
| Bytes 0–127 are reserved for ASCII | A byte above 127 means "more bytes follow", so é cannot be stored as one byte |
| Pipeline A: **text, count, pieces, loop, keep** | A1 corpus · A2 pre-tokenise and count the chunks · A3 split into pieces · A4 the loop · A5 merge list plus vocabulary |
| A2 counts chunks, A4 counts pairs | The chunk count never changes. The pair count is redone every round |
| A4 merges **one** pair per round, then counts again | Merging creates new neighbours, so new pairs appear (`banana` → `na+na`). Sorting once can never produce them |
| Each round's merge is added to the end of the list | The list order **is** the round order. That is why it is "ordered" |
| The loop stops after a fixed number of merges | That number is the vocabulary size, chosen in advance. It does not stop because counts get small |
| Pre-tokenisation happens before merging | Merges cannot cross a word boundary |
| A merge joins two pieces that already exist | It cannot come before its own ingredient. If it does, it matches nothing and is **silently skipped** |
| Different chains are ordered by frequency alone | `_cat` may come before `_the`. Never before `_c` |
| Pipeline B replays the merges in list order | An unseen word is not a special case: `replaying` becomes `r │ e │ play │ ing` |
| The space belongs to the word after it | `_the` and `the` are different rows with different IDs |
| A prompt ending in a space leaves a lone-space token | That token is rare in training, so **the output changes** |
| Tamil costs more for **two** reasons | (1) About 3 bytes per character instead of 1 — true even with a perfect tokeniser. (2) An English corpus produced few Tamil merges |
| Tokenisation is lossless | The text always decodes back exactly |
| Lossless is not harmless | More tokens means more cost, more compute, less room in the context window |
| The tokeniser is built before training and frozen | Training changes the embedding rows, never the merge list |
| The vocabulary is a contract with the embedding table | Shift one ID and the model reads the wrong rows. No error is raised anywhere |
| A special token is a row no user text can produce | Typing its characters gives ordinary pieces. Message boundaries live where content cannot write |
| Every vocabulary row is a full vector | 50,000 × 4,096 = 204.8M parameters, 391 MB at fp16 |
| Frequency decides which merges exist | Frequent pieces get many training updates. But frequency knows nothing about meaning: 1024 may be one token while 1025 is three |
| Two trainings, two corpora | The tokeniser's corpus decides how many tokens text costs. The model's training data decides how well it handles that text |

## Block 0 · How a model learns

| Fact | And therefore |
|---|---|
| A parameter is a number training is allowed to change | Training means finding good values for them |
| The prediction is `(weight × input) + bias` | This is `y = mx + c` from school. Weight is the tilt, bias is the height |
| `error = predicted − actual` | Positive means too high, negative means too low |
| `actual` comes from data collected before training | No labels → no error → no gradient → no learning |
| For a language model, `actual` is the next token | The labels are free. Every sentence is already labelled by its own order |
| At inference there is no `actual` | No error, no gradient. The parameters stay frozen |
| `loss = error²` | One number saying how wrong the parameters currently are |
| Squaring does **two** jobs | (1) +3 and −3 count the same, so errors cannot cancel. (2) Large errors count far more: 10 becomes 100, 1 stays 1 |
| The gradient is the tilt of the loss curve where you stand | Its sign says which way is downhill. Its size says how steep |
| `gradient for weight = 2 × (input × error)` | The error appears unsquared here, so the gradient keeps the sign the loss threw away |
| `gradient for bias = 2 × (1 × error)` | The bias is a weight whose input is always 1 |
| A bigger input gives a bigger gradient for the same error | The parameter attached to it gets the bigger correction (34.8 against 11.6 on his row) |
| `new weight = weight − (learning rate × gradient)` | The gradient points **uphill**. The minus moves you the other way |
| Subtracting a negative gradient adds | A negative gradient pushes the parameter **up** |
| The gradient is chained to the error | Near the answer the error shrinks, so the steps shrink on their own. Nothing has to find the bottom |
| The learning rate is fixed, the step is not | `step = learning rate × gradient`, so the step changes every round |
| The raw gradient is far too large to use as a step | At weight 0.10 it was −1170. Right direction, catastrophic size |
| A learning rate that is too large makes the loss grow | Each overshoot lands somewhere steeper, so the next gradient is larger, so the next overshoot is larger |
| A learning rate that is too small still converges | Slow and exploding are different behaviours, not two ends of one scale |
| The safe learning rate depends on how large the inputs are | Larger inputs make steeper ground, which needs a smaller rate. This is why rates are tuned |
| Two parameters → one gradient each | Both from the same error, each scaled by its own input |
| Updating after every row is stochastic gradient descent | It is what real models use. Same destination, a less direct path |
| Summing or averaging the rows is a convention | Dividing changes the size, never the direction. The learning rate absorbs it |
| Trying every value is impossible | Ten values for each of 204.8M parameters. The model can only feel the ground where it stands |
| Two points fix a straight line exactly | If the world were straight lines, nobody would need a model |
| A straight line promises three things | The effect never changes size, never reverses, never stops |
| Real relationships break all three | The slab bill changes rate. Learning rate against loss is a valley. A line predicts a negative bill |
| Two linear stages chained = one linear stage | Four knobs, still only tilt and height. **More knobs, no new shapes** |
| `max(0, value)`: negative becomes 0, otherwise unchanged | It is not multiply-and-add, so the stages can no longer merge into one |
| That produces a bend | Flat along the floor, then climbing. A shape no straight line can make |
| The bias decides where the bend sits | Bend positions are ordinary parameters, found by gradient descent |
| A piece whose bend has not been reached contributes nothing | Its gradient is zero. That row does not correct it at all |
| A negative rate turns the line downward | Bends can turn up or down, so any up-and-down shape is reachable |
| Enough bends make any curve | Nobody needs to know the shape in advance |
| A model with more capacity than the data needs fits the noise | Better on its training rows, worse on everything else. That is overfitting |
| Low training loss is not the goal | Judge a model only on rows it never trained on |
