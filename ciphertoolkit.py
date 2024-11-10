#!/usr/bin/env python3
"""Utilities for working with ciphers."""
import itertools
from string import ascii_lowercase


LETTERS = ascii_lowercase
A = LETTERS[0]
Z = LETTERS[-1]
START_ORD = ord(A)
END_ORD = ord(Z)
LEN = len(LETTERS)
AZLEN = LEN


def az_ord(c):
    c = c.lower()
    return ord(c) - ord(A)
def az_chr(i):
    i %= AZLEN
    return chr(i + ord(A))


def get_nonalphas(str):
    """Get the non-alphabetical characters in (index, char) pairs."""
    return tuple((n, c) for n, c in enumerate(str) if not c.isalpha())


def get_uppers(str):
    """Get the uppercase characters as a sequence of indices."""
    return tuple(n for n, c in enumerate(str) if c.isupper())


def insert_many(string, toinsert):
    """Return string with (index, char) pairs inserted.

    Indices represent the final position of the characters,
    not where they should be inserted into the original string
    """
    outstr = list(string)
    for index, char in sorted(toinsert):
        outstr.insert(index, char)
    return ''.join(outstr)


class Text:

    _str = ''
    _nonalphas = tuple()
    _uppers = tuple()

    def __init__(self, vals='', nonalphas=None):
        if isinstance(vals, str):
            self.str = vals
        else:
            self.num = vals
        self._nonalphas = nonalphas or self._nonalphas

    @property
    def str(self):
        expanded = list(insert_many(self._str, self._nonalphas))
        for index in self._uppers:
            expanded[index] = expanded[index].upper()
        return ''.join(expanded)

    @str.setter
    def str(self, value):
        self._nonalphas = get_nonalphas(value)
        self._uppers = get_uppers(value)
        self._str = ''.join(c for c in value if c.isalpha())

    def __str__(self):
        return self.str
    def __repr__(self):
        return repr(self.str)
    def __iter__(self):
        return iter(self.str)
    def __contains__(self, value):
        return str(value) in self.str

    @property
    def num(self):
        return [az_ord(n) for n in self._str]

    @num.setter
    def num(self, values):
        self.str = ''.join(az_chr(n) for n in values)

    def rotate(self, rotateval, direction=1):
        """Return a copy of the Text rotated by rotateval.

        If rotateval is an iterable, cycle through its values
        for each alphabetical character in self.
        """
        cls = type(self)
        # special-case the single rotation value
        if isinstance(rotateval, int):
            rotateval = [rotateval]
        rotateval = cls(rotateval).num
        rotated = cls(
            (
                ord + rotate*direction
                for ord, rotate in zip(self.num, itertools.cycle(rotateval))
            ),
            nonalphas=self._nonalphas,
        )
        rotated._nonalphas = self._nonalphas
        rotated._uppers = self._uppers
        return rotated

    def autocode(self, shift=0):
        return self.rotate(str(self)[shift:], direction=-1)

    def __sub__(self, other):
        return self.rotate(str(other), direction=-1)

    def __add__(self, other):
        return self.rotate(str(other))
