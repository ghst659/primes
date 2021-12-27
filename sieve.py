#!/usr/bin/env python3
"""Sieve of Eratosthenes."""

import logging

def sieve(n: int) -> list[int]:
    """"Returns the list of prime numbers up to and including N."""
    return sieve_array(n)

def sieve_array(n: int) -> list[int]:
    """"Array implementation."""
    if n < 2:
        return []
    is_prime = [True] * n
    is_prime[0] = False
    for i in range(n):
        if not is_prime[i]:
            continue
        p = i + 1
        for v in range(2 * p, n + 1, p):
            is_prime[v - 1] = False
    result = [i + 1 for i in range(n) if is_prime[i]]
    return result
