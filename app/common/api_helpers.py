import datetime
import decimal

import ujson as json
from flask import Response

from .utils import format_date, format_datetime


def json_response(obj, status_code=200, total_count=None, total_pages=None):
    response = Response(content_type='application/json;charset=utf-8')

    # default:
    json_data = obj

    if obj:
        # db models:
        if isinstance(obj, list) and hasattr(obj[0], '_fields'):
            json_data = []
            fields = obj[0].keys()
            for item in obj:
                dict_ = {}
                for f in fields:
                    value = getattr(item, f)
                    # first datetime (instance date == datetime):
                    if isinstance(value, datetime.datetime):
                        value = format_datetime(value)
                    elif isinstance(value, datetime.date):
                        value = format_date(value)
                    elif isinstance(value, decimal.Decimal):
                        value = float(value)

                    dict_[f] = value
                json_data.append(dict_)
        elif isinstance(obj, tuple) and hasattr(obj, '_fields'):
            fields = obj.keys()
            json_data = {}
            for f in fields:
                json_data[f] = getattr(obj, f)

    str_json = json.dumps(json_data, escape_forward_slashes=False)

    response.data = str_json
    response.content_length = len(str_json)
    response.status_code = status_code

    if total_count is not None:
        response.headers['X-total-count'] = total_count

    if total_pages is not None:
        response.headers['X-total-pages'] = total_pages

    return response


def calc_total_pages(items_total, page_size=25):
    total_pages = items_total / page_size
    int_total_pages = int(total_pages)

    if total_pages > int_total_pages:
        int_total_pages += 1
    return int_total_pages
