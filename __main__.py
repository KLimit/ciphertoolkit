#!/usr/bin/env python3
import argparse
import operator

from ciphertoolkit import Text


def main(cipher, key, encode):
    cipher = Text(cipher.read())
    key = Text(key)
    op = operator.sub
    if encode:
        op = operator.add
    # decoded = op(cipher, key)
    print(op(cipher, key))


def mainargs(argv=None):
    pser = argparse.ArgumentParser()
    pser.add_argument('cipher', type=argparse.FileType('r'), default='-', help='file (- for stdin) with cipher')
    pser.add_argument('key')
    pser.add_argument('-e', '--encode', action='store_true')
    args = pser.parse_args(argv)
    return vars(args)


if __name__ == '__main__':
    main(**mainargs())
