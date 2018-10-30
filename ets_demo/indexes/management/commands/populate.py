#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Basic script to populate the synthetic index data
"""

__author__ = "flyingbot91"
__copyright__ = "Copyright 2018"
__date__ = "2018/10/25"
__license__ = " GPLv3"
__version__ = "0.0.1"

import os

from django.core.management.base import BaseCommand, CommandError
from openpyxl import load_workbook


class Command(BaseCommand):
    help = 'Populate the synthetic index data'

    def handle(self, *args, **options):
        self.populate_weights()
        print("Done!")


    def populate_weights(self, *args, **kwargs):
        app_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        wb = load_workbook(
            filename=os.path.join(app_path, 'dummy', 'Data.xlsx'),
            read_only=True
        )

        # Get weights
        wsheet = wb.active
        weights = wsheet["B2:OK2"]
        for row in weights:
            print([cell.value for cell in row])

        # wsheet = wsheet["B2:OK3"]
        # for row in wsheet:
        #     a = [cell.value for cell in row]
