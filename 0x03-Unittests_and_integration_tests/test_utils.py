#!/usr/bin/env python3
""" Parameterize a unit test """
import unittest
from unittest.mock import patch, Mock
from unittest import TestCase
from utils import access_nested_map, get_json, memoize
import parameterized
from typing import Dict, Tuple, Union


class TestAccessNestedMap(TestCase):
    """ TestAccessNestedMap class """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
        # ({"a": 1}, ["a"], 1),
        # ({"a": {"b": 2}}, ["a", "b"], 2),
    ])
    
    def test_access_nested_map(self,
                               nested_map: Dict,
                               path: Tuple[str],
                               expected: Union[int, Dict]) -> None:
        """ Test access_nested_map """
        self.assertEqual(access_nested_map(nested_map, path), expected)
    
    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError),
    ])
    
    def test_access_nested_map_exception(self,
                                         nested_map: Dict,
                                         path: Tuple[str],
                                         expected: Exception) -> None:
        with self.assertRaises(expected):
            access_nested_map(nested_map, path)


class TestGetJson(TestCase):
    """ TestGetJson class """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    
    def test_get_json(self, test_url: str, test_payload: Dict) -> None:
        """ Test get_json """
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        with patch('requests.get', return_value=mock_response):
            self.assertEqual(get_json(test_url), test_payload)


class TestMemoize(TestCase):
    """ TestMemoize class """
    def test_memoize(self) -> None:
        """ Test memoize """
        class TestClass():
            def a_method(self):
                return 42

        @memoize
        def a_property(self):
            return self.a_method()
        
        with patch.object(TestClass,
                          'a_method',
                          return_value=lambda: 42) as mock_method:
            test_class = TestClass()
            self.assertEqual(test_class.a_property(), 42)
            self.assertEqual(test_class.a_property(), 42)
            mock_method.assert_called_once()
            # def __init__(self):
            #     self._nb = 0
            
            # @memoize
            # def nb_calls(self):
            #     """ nb_calls """
            #     self._nb += 1
            #     return self._nb
        
        # test = TestClass()
        # self.assertEqual(test.nb_calls(), 1)
        # self.assertEqual(test.nb_calls(), 1)
        # self.assertEqual(test.nb_calls(), 1)