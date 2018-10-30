#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Synthetic indexes calculation
"""

__author__ = "flyingbot91"
__copyright__ = "Copyright 2018"
__date__ = "2018/10/25"
__license__ = " GPLv3"
__version__ = "0.0.1"

from openpyxl import load_workbook


def underlying_security(prev_price, curr_price):
    """
    Calculate the underlying security for the index 'i' on date 't'
    :param prev_price: (float) Price of the underlying security index 'i' on date 't-1' (previous)
    :param curr_price: (float) Price of the underlying security index 'i' on date 't' (current)
    :return: (float)
    """

    return (curr_price / prev_price) - 1


def weighted_underlying_security_index(weights, prev_prices, curr_prices):
    """
    Calculate the total weighted sum for underlying security indexes.
    :param weights: (list) Weights corresponding to the underlying security indexes
    :param prev_prices: (list) Underlying security indexes on date 't-1' (previous)
    :param curr_prices: (list) Underlying security indexes on date 't' (current)
    :return: (float)
    """

    prices = [underlying_security(prev, curr) for prev, curr in zip(prev_prices, curr_prices)]
    return sum([a * b for a, b in zip(weights, prices)])


def calculate_index(weights, prev_prices, curr_prices, previous_index):
    """
    Calculate the current index
    :param weights: (list) Weights corresponding to the underlying security indexes
    :param prev_prices: (list) Underlying security indexes on date 't-1' (previous)
    :param curr_prices: (list) Underlying security indexes on date 't' (current)
    :param previous_index: (float) Previous index
    :return: (float)
    """

    index_on_date_t = weighted_underlying_security_index(weights, prev_prices, curr_prices)
    current_index = previous_index * (1 + index_on_date_t)
    return current_index


def read_data():
    wb = load_workbook(filename='dummy/Data.xlsx', read_only=True)
    wsheet = wb.active

    weights = wsheet["B2:Z2"]
    for row in weights:
        print([cell.value for cell in row])

    wsheet = wsheet["B2:OK3"]
    for row in wsheet:
        a = [cell.value for cell in row]


if __name__ == '__main__':
    read_data()
