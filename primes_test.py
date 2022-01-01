#!/usr/bin/env python3

import dataclasses
import logging
import sys
import unittest

import primes

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
    Case(n = 121,
         want = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59,
                 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]),
]

class TestSieve(unittest.TestCase):
    def setUp(self):
        logging.getLogger().setLevel(logging.INFO)

    def test_cases(self):
        for c in _CASES:
            logging.info('Case %d', c.n)
            got = primes.sieve(c.n)
            self.assertEqual(got, c.want)
            self.assertTrue(all(primes.is_prime(p) for p in got))

class TestIsPrime(unittest.TestCase):
    def test_primes(self):
        for n in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 999863):
            self.assertTrue(primes.is_prime(n))

    def test_nonprimes(self):
        for n in (0, 1, 4, 6, 8, 9, 10, 12, 14, 15, 21, 25):
            self.assertFalse(primes.is_prime(n))

class TestBSearch(unittest.TestCase):
    def test_various(self):
        self.assertEqual(primes.bsearch(5, (2, 5)), 1)
        self.assertEqual(primes.bsearch(1, (2, 3, 5)), None)
        self.assertEqual(primes.bsearch(2, (2, 3, 5)), 0)
        self.assertEqual(primes.bsearch(4, (2, 3, 5)), 1)
        self.assertEqual(primes.bsearch(4, (2, 5)), 0)
        self.assertEqual(primes.bsearch(3, (2, 3, 5)), 1)
        self.assertEqual(primes.bsearch(6, (2, 3, 5)), 2)
        self.assertEqual(primes.bsearch(5, (2, 3, 5, 7)), 2)

class TestAppend(unittest.TestCase):
    def test_empty(self):
        self.assertEqual(primes.additional(1, []), [])
        self.assertEqual(primes.additional(2, []), [2])
        self.assertEqual(primes.additional(8, []), [2, 3, 5, 7])
        self.assertEqual(primes.additional(11, []), [2, 3, 5, 7, 11])

    def test_with_preexisting(self):
        initial_primes = (2, 3, 5)
        self.assertEqual(primes.additional(2, initial_primes), [])
        self.assertEqual(primes.additional(4, initial_primes), [])
        self.assertEqual(primes.additional(5, initial_primes), [])
        self.assertEqual(primes.additional(6, initial_primes), [])
        self.assertEqual(primes.additional(7, initial_primes), [7])
        self.assertEqual(primes.additional(29, initial_primes), [7, 11, 13, 17, 19, 23, 29])
        self.assertEqual(primes.additional(40, initial_primes), [7, 11, 13, 17, 19, 23, 29, 31, 37])
        self.assertEqual(primes.additional(121, initial_primes),
                         [7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
                          53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101,
                          103, 107, 109, 113])

class TestIncremental(unittest.TestCase):
    def setUp(self):
        logging.getLogger().setLevel(logging.INFO)

    def test_edge(self):
        self.assertEqual(primes.isieve(5), [2, 3, 5])
        self.assertEqual(primes.isieve(121),
                         [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37,
                         41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83,
                         89, 97, 101, 103, 107, 109, 113])

class TestGenerator(unittest.TestCase):
    def test_various(self):
        self.assertEqual(list(primes.generate(0, 2)), [2])
        self.assertEqual(list(primes.generate(10, 20)), [11, 13, 17, 19])
        self.assertEqual(list(primes.generate(10, 10)), [])
        self.assertEqual(list(primes.generate(23, 23)), [23])

if __name__ == '__main__':
    unittest.main()
