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


class Text:

    _str = ''
    _num = []
    def __init__(self, vals=''):
        if isinstance(vals, str):
            self.str = vals

    @property
    def str(self):
        return self._str
    @str.setter(self, value):
        self._str = value.lower()

    @property
    def num(self):
        return [az_ord(n) for n in self.str]
    @num.setter(self, values):
        self.str = ''.join(az_chr(n) for n in values)
