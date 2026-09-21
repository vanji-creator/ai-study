# What a character really is, and what "bytes" means.
# Run: python3 code/block-01/bytes_explained.py

print("STEP 1: every character has an agreed number (its Unicode code point)")
for character in ["A", "a", "c", "e", "é", "ü", "日", "🙂"]:
    print(f"   character {character!r:<6} -> number {ord(character)}")

print()
print("STEP 2: a byte can only hold 0 to 255. Numbers bigger than 255 do not fit.")
print("   'e' is 101 -> fits in one byte")
print("   'é' is 233 -> fits, but utf-8 still uses 2 bytes (see step 3)")
print("   '日' is 26085 -> does NOT fit in one byte")
print("   '🙂' is 128578 -> does NOT fit in one byte")

print()
print("STEP 3: utf-8 is the rule for writing those numbers as a sequence of bytes")
for character in ["e", "é", "日", "🙂"]:
    byte_values = list(character.encode("utf-8"))
    print(f"   {character!r:<6} code point {ord(character):<7} -> bytes {byte_values}")

print()
print("STEP 4: the bytes turn back into the exact same character. Nothing is lost.")
original_text = "café"
byte_values = original_text.encode("utf-8")
print(f"   '{original_text}' -> bytes {list(byte_values)} -> back to '{byte_values.decode('utf-8')}'")

print()
print("STEP 5: a single byte of a multi-byte character means nothing on its own")
try:
    bytes([195]).decode("utf-8")
except UnicodeDecodeError as error:
    print(f"   decoding just byte 195 fails: {error}")
print(f"   decoding bytes 195 and 169 together gives: {bytes([195, 169]).decode('utf-8')!r}")

print()
print("STEP 6: 'e' and 'é' are completely different numbers. One is not a version of the other.")
print(f"   'e' -> {list('e'.encode('utf-8'))}")
print(f"   'é' -> {list('é'.encode('utf-8'))}")
