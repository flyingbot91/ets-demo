#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unittests for synthetic_index.indexes.py
"""

__author__ = "flyingbot91"
__copyright__ = "Copyright 2018"
__date__ = "2018/10/25"
__credits__ = ["flyingbot91"]
__license__ = " GPLv3"
__version__ = "0.0.1"
__maintainer__ = "flyingbot91"
__email__ = "flyingbot91@gmx.com"
__status__ = "Development"


from unittest import TestCase
from synthetic_index.indexes import *


class SyntheticIndexTestCase(TestCase):

    def setUp(self):
        self.weights = [0.23, 0.45]
        self.curr_prices = [1.026047462, 1.0026183081]
        self.prev_prices = [1.023256221, 1.0025337812]
        self.precision = 6

    def test_underlying_security(self):
        """Calculate the index underlying security on a date using 6 floating point digit precision"""

        self.assertAlmostEqual(
            underlying_security(0.4567, 0.345678),
            -0.243096,
            self.precision
        )

    def test_weighted_underlying_security_indexes(self):
        """Calculate the weighted sum of underlying security indexes"""

        self.assertAlmostEqual(
            weighted_underlying_security_index(self.weights, self.prev_prices, self.curr_prices),
            0.000665,
            self.precision
        )

    def test_calculate_index(self):
        """Calculate the current index"""

        self.assertAlmostEqual(
            calculate_index(self.weights, self.prev_prices, self.curr_prices, 98),
            98.065203,
            self.precision
        )
