#!/usr/bin/env python3
import argparse
import sys

from ciphertoolkit import Text


def shiftleft(string, n=0):
    n %= len(string)
    return string[n:] + string[:n]


def circular_shifts(string):
    """List of string in all circular shifts."""
    return [shiftleft(string, n) for n in range(len(string))]


def main(ciphertext, knowncipher, knownplain, show_all=False):
    if ciphertext is None:
        ciphertext = sys.stdin
    else:
        ciphertext = open(ciphertext)
    ciphertext = Text(ciphertext.read())
    if knowncipher.casefold() not in ciphertext._str.casefold():
        errorout('known substring not in ciphertext')
    knownplain = knownplain.casefold()
    partial_key = Text(knowncipher) - Text(knownplain)
    if show_all:
        decodeds = applykeys(ciphertext, partial_key)
    else:
        decodeds = find_rotation(ciphertext, partial_key, knownplain)
    for key, decoded in decodeds.items():
        print(f'partial: {partial_key}')
        print(f'rotated: {key}')
        print(decoded)
        print('')
    return int(bool(decodeds and not show_all))


def applykeys(ciphertext, partial_key):
    return {key: ciphertext - key for key in circular_shifts(str(partial_key))}


def find_rotation(ciphertext, partial_key, known):
    return {
        key: val
        for key, val in applykeys(ciphertext, partial_key).items()
        if known in val
    }


def mainargs(argv=None):
    pser = argparse.ArgumentParser()
    pser.add_argument('knowncipher')
    pser.add_argument('knownplain')
    pser.add_argument('ciphertext', nargs='?')
    pser.add_argument('-a', '--show-all', action='store_true')
    args = pser.parse_args(argv)
    return vars(args)


def errorout(message):
    print(message, file=sys.stderr)
    sys.exit(1)

if __name__ == "__main__":
    sys.exit(main(**mainargs()))
