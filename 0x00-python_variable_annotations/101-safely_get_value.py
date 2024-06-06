#!/usr/bin/env python3
""" Type-annotated function safely_get_value """
from typing import Union, Any, Mapping, TypeVar


def safely_get_value(dct: Mapping, key: Any, default: Union[TypeVar('T'), None]
                     = None) -> Union[Any, TypeVar('T')]:
    """ Return value of key if it exists, otherwise return default """
    if key in dct:
        return dct[key]
    else:
        return default
