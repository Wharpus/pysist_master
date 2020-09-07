#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  test_sum.py
#  

'''
The :class:`TestSum` class is a unittest class.
'''

import unittest

class TestSum(unittest.TestCase):

    def test_sum_dict(self):
        self.assertEqual(sum({1, 2}), 3, "Should be 3")

    def test_sum_list(self):
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")

    def test_sum_tuple(self):
        self.assertEqual(sum((3, 2, 1)), 6, "Should be 6")

if __name__ == '__main__':
    unittest.main()

'''
Method 			Equivalent to
.assertEqual(a, b) 	a == b
.assertTrue(x) 		bool(x) is True
.assertFalse(x) 	bool(x) is False
.assertIs(a, b) 	a is b
.assertIsNone(x) 	x is None
.assertIn(a, b) 	a in b
.assertIsInstance(a, b) isinstance(a, b)

.assertIs(), .assertIsNone(), .assertIn(), and .assertIsInstance() 
all have opposite methods, named .assertIsNot(), and so forth.
'''