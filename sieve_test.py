#!/usr/bin/env python3

import dataclasses
import logging
import sys
import unittest

import sieve

@dataclasses.dataclass
class Case:
    n: int
    want: list[int]

_CASES = [
    Case(n = 20,
         want = [2, 3, 5, 7, 11, 13, 17, 19]),
    Case(n = 2,
         want = [2]),
    Case(n = 3,
         want = [2, 3]),
    Case(n = 4,
         want = [2, 3]),
    Case(n = 10,
         want = [2, 3, 5, 7]),
    Case(n = -1,
         want = []),
    Case(n = 0,
         want = []),
    Case(n = 1,
         want = []),
    Case(n = 47,
         want = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]),
    Case(n = 100,
         want = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
                 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]),
]

class TestSieve(unittest.TestCase):

    def setUp(self):
        logging.getLogger().setLevel(logging.INFO)

    def test_cases(self):
        for c in _CASES:
            logging.info('Case %d', c.n)
            self.assertEqual(sieve.sieve(c.n), c.want)

if __name__ == '__main__':
    unittest.main()
