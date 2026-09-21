# How many distinct words in a text appear only once?
# If a word appears once, a word-level model sees its row trained on one example.
# Run: python3 code/block-01/word_frequency_tail.py

from collections import Counter

corpus_path = "CLAUDE.md"   # change this to any text file you want to test

with open(corpus_path, encoding="utf-8") as corpus_file:
    corpus_text = corpus_file.read().lower()   # lower-case so "The" and "the" count as one word

# Split on whitespace, then strip punctuation from the edges of each word
all_words = [word.strip(".,:;()`*\"'|—-[]#?!") for word in corpus_text.split()]
all_words = [word for word in all_words if word]   # drop empty strings left after stripping

count_per_word = Counter(all_words)   # word -> how many times it appears

total_word_occurrences = len(all_words)
distinct_word_count = len(count_per_word)
words_seen_once = [word for word, count in count_per_word.items() if count == 1]

print(f"total words in file      : {total_word_occurrences}")
print(f"distinct words           : {distinct_word_count}")
print(f"distinct words seen once : {len(words_seen_once)}  "
      f"({100 * len(words_seen_once) / distinct_word_count:.1f}% of distinct words)")
print()
print("some words seen only once:", sorted(words_seen_once)[:25])
print()
print("most common 10:", count_per_word.most_common(10))

# Words that share a root but would get unrelated rows in a word-level table
print()
for root in ["token", "embed", "rank", "train"]:
    family = sorted(word for word in count_per_word if word.startswith(root))
    print(f"words starting with '{root}':", family)
