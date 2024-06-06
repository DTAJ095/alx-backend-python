#!/usr/bin/env python3
""" Type-annotated function make_multiplier that takes a float multiplier """
from typing import Callable


def make_multiplier(multiplier: float) -> callable[[float], float]:
    """ Return function that multiplies a float by multiplier """
    def multiply(n: float) -> float:
        """ Multiply n by multiplier """
        return n * multiplier
    return multiply
