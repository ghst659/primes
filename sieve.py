#!/usr/bin/env python3
"""Sieve of Eratosthenes."""

import logging

def sieve(n: int) -> list[int]:
    """"Returns the list of prime numbers up to and including N."""
    if n < 2:
        return []
    size = n + 1
    is_prime = [True] * size  # One slot for each int up to n.
    is_prime[0:2] = (False, False)  # 0 and 1 are not primes.
    for p in range(size):
        if is_prime[p]:
            for v in range(p * p, size, p):
                is_prime[v] = False
    return [p for p in range(size) if is_prime[p]]

def is_prime(n: int) -> bool:
    """Checks if a positive integer N is a prime number by brute force."""
    return n > 1 and all(n % d != 0 for d in range(2, n))
