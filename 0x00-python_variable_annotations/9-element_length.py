#!/usr/bin/env python3
""" Type annotated function element_length that takes a list of strings and returns a list of tuples"""
from typing import List, Tuple, Sequence, Iterable


def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """ Return values with the appropriate types """
    return [(i, len(i)) for i in lst]
