#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  test_integration.py
#  

'''

The :class:`TestBasic` class is a unittest class.
The :class:`TestComplexData` class is a unittest class.
'''

import unittest

class TestBasic(unittest.TestCase):
    def setUp(self):
        # Load test data
        self.app = App(database='fixtures/test_basic.json')

    def test_customer_count(self):
        self.assertEqual(len(self.app.customers), 100)

    def test_existence_of_customer(self):
        customer = self.app.get_customer(id=10)
        self.assertEqual(customer.name, "Org XYZ")
        self.assertEqual(customer.address, "10 Red Road, Reading")


class TestComplexData(unittest.TestCase):
    def setUp(self):
        # load test data
        self.app = App(database='fixtures/test_complex.json')

    def test_customer_count(self):
        self.assertEqual(len(self.app.customers), 10)

    def test_existence_of_customer(self):
        customer = self.app.get_customer(id=9)
        self.assertEqual(customer.name, u"バナナ")
        self.assertEqual(customer.address, "10 Red Road, Akihabara, Tokyo")

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