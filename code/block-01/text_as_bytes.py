# Every string is stored as bytes. A byte is a number from 0 to 255.
# Run: python3 code/block-01/text_as_bytes.py

samples = ["cat", "café", "Grüße", "日本", "🙂", "வணக்கம்"]

print(f"{'text':<10} {'chars':>5} {'bytes':>5}   byte values")
print("-" * 70)
for text in samples:
    byte_values = list(text.encode("utf-8"))   # utf-8 turns text into bytes
    print(f"{text:<10} {len(text):>5} {len(byte_values):>5}   {byte_values}")

print()
print("how many different byte values are possible:", 256)
print("how many different characters Unicode defines: about 150000")
