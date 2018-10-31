#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

"""

__author__ = "flyingbot91"
__copyright__ = "Copyright 2018"
__date__ = "2018/10/25"
__license__ = " GPLv3"
__version__ = "0.0.1"

from django.urls import path

from . import views

urlpatterns = [
    # ex: /indexes/prices/20181029/
    path('prices/<str:datestr>/', views.prices, name='prices'),
]