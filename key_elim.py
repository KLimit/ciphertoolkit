#!/usr/bin/env python3
from ciphertoolkit import Text


# TODO: use from Text
def autocode(text, shift=0):
    """Encode text with itself, optionally shifted."""
    if not isinstance(text, Text):
        text = Text(text)
    return text.rotate(str(text)[shift:], direction=-1)


def test_shifts(cipher, possibles, maxshift=1):
    """Shift cipher and possible, and see if possible is there"""
    matches = []
    for shift in range(1, maxshift+1):
        shifted_cipher = autocode(cipher, shift)
        matches += [
            (shift, poss)
            for poss in possibles
            if autocode(poss, shift).str[:shift] in shifted_cipher
            and shift < len(poss)
        ]
    return matches
