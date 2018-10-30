#!/usr/bin/env python
from django.db import models


class UnderlyingSecurityIngestion(models.Model):
    created_on = models.DateTimeField(
        auto_now=True,
        help_text='Date and time of ingestion'
    )
    date = models.DateField(
        help_text='Synthetic index date'
    )
    synthetic_index = models.FloatField(
        help_text='Synthetic index on a specific date'
    )
    calculated_on = models.DateTimeField(
        auto_now=True,
        help_text='Date and time of synthetic index calculation'
    )

    def __str__(self):
        return '%s_%s' % (self.created_on, self.date)


class UnderlyingSecurityIndex(models.Model):
    index_id = models.PositiveIntegerField(
        help_text='Underlying security ID'
    )
    weight = models.FloatField(
        help_text='Underlying security weight'
    )

    def __str__(self):
        return '%s: %s' % (self.id, self.weight)


class UnderlyingSecurityValue(models.Model):
    ingestion = models.ForeignKey(
        'UnderlyingSecurityIngestion',
        on_delete=models.CASCADE
    )
    index = models.ForeignKey(
        'UnderlyingSecurityIndex',
        on_delete=models.CASCADE
    )
    price = models.FloatField(
        help_text='Underlying security price'
    )

    def __str__(self):
        return '%s: %s (%s)' % (self.index.id, self.price, self.ingestion.date)
