# Questions to paste into another model

Copy everything between the lines below. It carries the instructions, what I already
know, and the questions in my own words.

---

## INSTRUCTIONS

Answer in blunt, plain statements of fact. Specifically:

- No build-up, no "great question", no encouragement, no summaries of what you are
  about to say. Start with the answer.
- No analogies, no metaphors, no stories. If a thing is a comparison of two numbers,
  say that.
- One clearly separated answer per numbered question. Keep each under 200 words.
- Use small concrete numbers where numbers help. Show the arithmetic, do not describe it.
- Put brackets around every group in a formula, like
  `new weight = weight - (learning rate x gradient)`.
- If a question rests on a wrong assumption, say so in the first sentence.
- If you are not certain about something, say "I am not certain" rather than answering
  smoothly. Do not invent history, paper results, or numbers.
- Distinguish these three explicitly whenever they come up: a mathematical fact, a
  convention people follow, and a practice that is reported to work but is not proven.

## WHO IS ASKING

Software engineer, about two years of production experience in Python/FastAPI,
React/Next.js, PostgreSQL. Beginner in machine learning theory, not in engineering.
Do not explain what an API or a loop is. English is my third language: plain words,
no idioms.

Weak at mathematical notation and at holding several numbers in my head at once. I
follow arithmetic fine when it is one row of data at a time, with small numbers. I lose
the thread when several data rows are summed or averaged into one step.

## WHAT I ALREADY UNDERSTAND - DO NOT RE-EXPLAIN THESE

- A parameter is one number inside the model that training is allowed to change.
- The loss is one number saying how wrong the current parameters are. It is squared so
  that positive and negative errors cannot cancel, and so large errors count more.
- The gradient of one parameter is the tilt of the loss curve at the point where the
  parameters currently are. Its sign says which direction is downhill, its size says how
  steep.
- The update rule is `new weight = weight - (learning rate x gradient)`.
- A gradient of `2 x (input x error)` for a weight, and `2 x (1 x error)` for a bias,
  because the bias's influence on the prediction is always 1.
- Steps shrink automatically near the answer because the gradient is chained to the error.
- A learning rate that is too large makes the loss grow without limit, because each
  overshoot lands somewhere steeper, so the next gradient is larger.
- Stochastic gradient descent: update after every single row. I prefer this form.
- Chaining two `(weight x input) + bias` stages with nothing between them produces a
  straight line, identical to one stage.
- `max(0, value)` returns the value if positive and 0 if negative, and putting it between
  two stages creates a bend. The bias decides where the bend sits.
- Several bends added together, some with negative rates, can make a curve go up, down
  and up again.
- Overfitting: a model with more capacity than the data needs will fit measurement noise,
  be better on its training rows and worse on unseen rows.
- Tokenisation: BPE, merge lists, byte fallback, why non-English text costs more tokens,
  special tokens, that a token ID is only a row number and meaning is learned.

## WHAT I HAVE NOT BEEN TAUGHT YET

Backpropagation. Attention and transformers. Anything about optimisers beyond plain
gradient descent.

## THE QUESTIONS

1. I understand a gradient as the tilt of the loss curve for ONE parameter. When there
   are two parameters, what exactly is "the gradient"? Is it one number or two? Answer
   in terms of what is being measured, not in terms of notation.

2. Slope as rise divided by run: why does dividing by the size of the nudge give the
   steepness? I can do the arithmetic but I do not see why the division is there.

3. Why is the bias needed at all? Give a case where a model with only a weight gives a
   plainly wrong answer and a bias fixes it.

4. Why do people sum or average the error across many data rows into one update, when
   updating after each row separately also works? What specifically is better about each,
   and does dividing by the number of rows change the result or only the size?

5. Where does `actual` come from in a real model? For a language model specifically, what
   exactly is the actual value being compared against, at one position in one sentence?

6. In a real model, how does the position of a bend get found? Nobody tells the model
   where the bend belongs, so what is the mechanism that moves it?

7. If the goal is for the model's curve to pass through the data points, and overfitting
   means passing through them too well, then what is the actual target? How does anyone
   know when to stop?

8. Take a real language model. Tell me concretely which thing is the data point, which
   thing is the curve, and which thing is one parameter. Then walk the whole chain from
   me typing a sentence to me reading the model's output, saying at each step what kind
   of object exists at that point.

9. Why do we need curves at all? What breaks if a model is only allowed straight lines?
   Give a case where the straight-line answer is not merely less accurate but plainly
   absurd.

10. Why `max(0, value)` in particular? What was the requirement it was chosen to meet,
    and what else would have met that requirement? Was it chosen for a mathematical
    reason or a practical one?

11. Backpropagation. I have not been taught it. Explain what it computes and why it is
    needed, given that I already know what a gradient is and what the update rule is.
    Use a two-stage example with real small numbers, one data row only.

12. When a model has hundreds of millions of parameters instead of two, what genuinely
    changes about everything above, and what does not change at all?

---
