#!/usr/bin/env python3
""" Parameterize a unit test """
import unittest
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json, memoize
import parameterized


class TestAccessNestedMap(unittest.TestCase):
    """ TestAccessNestedMap class """
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """ Test access_nested_map """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError),
    ])
    def test_access_nested_map_exception(self, nested_map, path,expected):
        """ Test access_nested_map exception """
        with self.assertRaises(KeyError) as err:
            access_nested_map(nested_map, path)
        self.assertEqual(f"KeyError('{expected}')", repr(err.exception))


class TestGetJson(unittest.TestCase):
    """ TestGetJson class """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url: str, test_payload: Dict) -> None:
        """ Test get_json """
        attrs = {'json.return_value': test_payload}
        with patch('requests.get', return_value=Mock(**attrs)) as get_request:
            self.assertEqual(get_json(test_url), test_payload)
            get_request.assert_called_once(test_url)


class TestMemoize(unittest.TestCase):
    """ TestMemoize class """
    def test_memoize(self) -> None:
        """ Test memoize """
        class TestClass():
            def a_method(self):
                return 42

        @memoize
        def a_property(self):
            """ a_property """
            return self.a_method()

        with patch.object(TestClass,
                          'a_method',
                          return_value=lambda: 42) as memo_func:
            test_class = TestClass()
            self.assertEqual(test_class.a_property(), 42)
            self.assertEqual(test_class.a_property(), 42)
            memo_func.assert_called_once()
