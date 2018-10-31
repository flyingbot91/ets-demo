#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from datetime import datetime
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from indexes.models import UnderlyingSecurityIngestion


def prices(request, datestr):
    date = datetime.strptime(datestr, '%Y%m%d')
    ingestion = UnderlyingSecurityIngestion.objects.filter(date=date).order_by('-created').last()
    data = ingestion.underlyingsecurityvalue_set.values_list('index__index_id', 'price')
    return HttpResponse(json.dumps(list(data), cls=DjangoJSONEncoder), content_type="application/json")
