#!/usr/bin/env python3
""" Type-annotated function make_multiplier that takes a float multiplier """


def make_multiplier(multiplier: float) -> float:
    """ Return function that multiplies float by multiplier """
    def multiply(n: float) -> float:
        return n * multiplier
    return multiply
