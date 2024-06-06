#!/usr/bin/env python3
""" Advanced type-annotated function """
from typing import List, Tuple


<<<<<<< HEAD
def zoom_array(lst: Tuple, factor: int = 2) -> List:
=======
def zoom_array(lst: Tuple, factor: int = 2) -> Tuple:
    """ Return zoomed in list """
>>>>>>> b49cfc19d5eb56309e9818654e3893c750501b0d
    zoomed_in: Tuple = [
        item for item in lst
        for i in range(int(factor))
    ]
    return zoomed_in


array = [12, 72, 91]

zoom_2x = zoom_array(array)

zoom_3x = zoom_array(array, 3.0)
