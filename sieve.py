#!/usr/bin/env python3
"""Sieve of Eratosthenes."""

import logging
import threading
import typing

from collections.abc import Sequence

def sieve(n: int) -> list[int]:
    """"Returns the list of prime numbers up to and including N."""
    if n < 2:
        return []
    size = n + 1
    is_prime = [True] * size  # One slot for each int up to n.
    is_prime[0:2] = (False, False)  # 0 and 1 are not primes.
    for p in range(size):
        if is_prime[p]:
            for v in range(p * p, size, p if p < 3 else 2 * p):
                is_prime[v] = False
    return [p for p in range(size) if is_prime[p]]

def is_prime(n: int) -> bool:
    """Checks if a positive integer N is a prime number by brute force."""
    return n > 1 and all(n % d != 0 for d in range(2, n // 2 + 1))

def bsearch(n: int, ary: Sequence[int]) -> typing.Optional[int]:
    """Finds the array index of the highest of ARY equal to or less than N, or None"""
    if not ary or n < ary[0]:
        return None
    if n >= ary[-1]:
        return len(ary) - 1
    lo = 0
    hi = len(ary)
    while hi - lo > 1:
        mid = (hi + lo + 1) // 2
        v = ary[mid]
        if n == v:
            return mid
        elif n > v:
            lo = mid
        else:  # n < v
            hi = mid
    return lo

_primes: list[int] = []  # Cache of previously calculated primes
_primes_lock = threading.Lock()  # Concurrency lock for _primes

def isieve(n: int) -> list[int]:
    """Incremental sieve."""
    global _primes
    global _primes_lock
    if n < 2:
        return []
    with _primes_lock:
        last_idx = len(_primes) - 1
        hi_idx = bsearch(n, _primes)
        if hi_idx is None:   # hi_idx == 0 is a valid found prime
            # Use the non-incremental algorithm.
            _primes = sieve(n)
            return _primes[:]
        elif hi_idx < last_idx:
            # n is in the middle; return copy slice of _primes
            return _primes[:hi_idx + 1]
        elif hi_idx == last_idx:
            # extend primes if necessary, then return a copy
            extension = additional(n, _primes)
            _primes.extend(extension)
            return _primes[:]
        else:
            raise IndexError(f'invalid index: {hi_idx} vs {last_idx}')

def additional(n: int, previous_primes: Sequence[int]) -> list[int]:
    vbase = previous_primes[-1]
    if n == vbase:
        return []
    # Create an scratch array for numbers between the previous_primes and n.
    is_prime = [True] * (n - vbase)  # does not include vbase
    def i2v(i: int) -> int:
        """Maps an is_prime array index to the integer value it represents."""
        return vbase + i + 1
    def v2i(v: int) -> int:
        """Maps a value to an is_prime index."""
        return v - vbase - 1
    # Mark array with multiples of previous primes
    for i in range(len(is_prime)):
        value_to_check = i2v(i)
        for p in previous_primes:
            if value_to_check % p == 0:
                is_prime[i] = False
                break
    # Identify new primes to be returned.
    new_primes = []
    # Mark is_prime for newly discovered primes
    for i in range(len(is_prime)):
        p = i2v(i)
        if is_prime[i]:
            new_primes.append(p)
            for v in range(p * p, n + 1, p):
                k = v2i(v)
                is_prime[k] = False
    return new_primes
