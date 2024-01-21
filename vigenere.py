#!/usr/bin/env python3
import argparse
import itertools
import string
import sys

letters = string.ascii_letters
lowers = string.ascii_lowercase
uppers = string.ascii_uppercase

lowerbounds = tuple(ord(lowers[n]) for n in (0, -1))
upperbounds = tuple(ord(uppers[n]) for n in (0, -1))
azlen = len(lowers)


def azindex(char, index=0):
    """Return the alphabetical index of the character."""
    char = char.lower()
    return ord(char) - lowerbounds[0] + index


def rotatechar(char, n):
    """Rotate char n characters."""
    if char not in letters or len(char) != 1:
        raise ValueError()
    start, end = lowerbounds if char.islower() else upperbounds
    new_ord = ord(char) + n
    new_ord = (new_ord - start) % azlen + start
    return chr(new_ord)


def decode(key, ciphertext, *, index=0, direction=-1):
    key = key.lower()
    ciphertext = ciphertext.lower()
    key = itertools.cycle(key)
    plaintext = ''
    for char in ciphertext:
        if char in letters:
            rot = azindex(next(key), index) * direction
            char = rotatechar(char, rot)
        plaintext += char
    return plaintext


def encode(key, plaintext):
    return decode(key, plaintext, direction=1)

def main(key, ciphertext, start_index):
    if ciphertext is not sys.stdin:
        ciphertext = open(ciphertext)
    ciphertext = ciphertext.read()
    print(decode(key, ciphertext, index=start_index))
    return 0


def mainargs(argv=None):
    pser = argparse.ArgumentParser()
    pser.add_argument('key')
    pser.add_argument('ciphertext', default=sys.stdin, nargs='?')
    pser.add_argument('--start-index', default=0, type=int)
    args = pser.parse_args(argv)
    return vars(args)


if __name__ == "__main__":
    sys.exit(main(**mainargs()))
