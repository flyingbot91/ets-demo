#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Basic script to populate the synthetic index data with the dummy Excel file
"""

__author__ = "flyingbot91"
__copyright__ = "Copyright 2018"
__date__ = "2018/10/25"
__license__ = " GPLv3"
__version__ = "0.0.1"

import logging
import os

from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from indexes.models import UnderlyingSecurityIngestion, UnderlyingSecurityIndex, UnderlyingSecurityValue
from indexes.synthetic import calculate_index
from openpyxl import load_workbook
from time import sleep

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


class Command(BaseCommand):
    help = 'Populate the synthetic index data'

    def handle(self, *args, **options):
        self.run_demo()

    def run_demo(self):
        """
        Demo main method
        :return:
        """

        logger.info("** PROCESS STARTED **")

        # Parse Excel file
        logger.debug("Parsing data file...")
        app_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        wb = load_workbook(
            filename=os.path.join(app_path, 'dummy', 'Data.xlsx'),
            read_only=True
        )
        wbsheet = wb.active
        logger.debug("File parsed")

        self.cleanup()
        self.update_weights(wbsheet)
        self.update_prices(wbsheet)
        logger.info("** PROCESS FINISHED **")

    def cleanup(self):
        """
        Delete existing dummy data in the DB
        :return:
        """

        UnderlyingSecurityIngestion.objects.all().delete()
        UnderlyingSecurityIndex.objects.all().delete()
        logging.info("Deleted existing dummy data")


    def update_weights(self, wbsheet):
        """
        Update index weight data
        :param wbsheet: Excel spreadshseet
        :return:
        """

        # Create weight entries
        weight_row = wbsheet["B2:OK2"]
        for row in weight_row:
            weights = [UnderlyingSecurityIndex(index_id=idx + 1, weight=cell.value) for idx, cell in enumerate(row)]
        UnderlyingSecurityIndex.objects.bulk_create(weights)
        logger.debug("Weights created (%s entries)" % len(weights))

    def update_prices(self, wbsheet):
        """
        Update synthetic index prices.
        Iterate through each row in the file 'Data.xlsx'
        :param wbsheet: Excel spreadshseet
        :return:
        """

        indexes = UnderlyingSecurityIndex.objects.all()

        wsheet = wbsheet["B2:OK4108"]
        for row in wsheet:
            #a = [cell.value for cell in row]
            #logger.debug("Sending new data (%s prices)" % len(a))

            # Dumb simulation of Http POST query at specific time interval (in seconds)
            sleep(5)

            ingestion = UnderlyingSecurityIngestion.objects.create(date=datetime.now())
            prices = [
                UnderlyingSecurityValue(
                    ingestion=ingestion,
                    index=indexes.get(index_id=idx+1),
                    price=cell.value) for idx, cell in enumerate(row)
            ]
            UnderlyingSecurityValue.objects.bulk_create(prices)

            # Previous ingestion
            try:
                previous_ingestion = ingestion.get_previous_by_created()
                previous_index = previous_ingestion.synthetic_index
                previous_prices = previous_ingestion.underlyingsecurityvalue_set.values_list('price', flat=True)
                current_prices = ingestion.underlyingsecurityvalue_set.values_list('price', flat=True)

                # Calculate the synthethic index
                new_index = calculate_index(
                    indexes.values_list('weight', flat=True),
                    previous_prices,
                    current_prices,
                    previous_index
                )
            # First entry
            except UnderlyingSecurityIngestion.DoesNotExist:
                new_index = 100
            finally:
                # Update ingestion missing fields
                ingestion.calculated = timezone.now()
                ingestion.synthetic_index = new_index
                ingestion.save()
                logging.debug("INDEX: %s" % new_index)
