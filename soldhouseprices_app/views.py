from django.db.models.functions.datetime import TruncYear
from django.http.response import JsonResponse
from django.db.models.aggregates import Avg
from django.db.models.functions import TruncMonth, TruncYear
from datetime import datetime
from rest_framework.decorators import api_view
from soldhouseprices_app.models import house_transactions

import numpy as np
import json


@api_view(['GET'])
def transactionbins(request):
    result_obj ={}
    bin_count = 8

    try:
        #Get parameters from front-end
        date_time_str = request.query_params.get('date')
        date_value = datetime.strptime(date_time_str, '%b %Y').date()  
        zipcode_value = request.query_params.get('zip')

        result_set = house_transactions.objects.filter(zipcode = zipcode_value,
         date__year = date_value.year,
          date__month = date_value.month).values('price')

        price_list = [element['price'] for element in result_set]

        histo, bin_edges = np.histogram(price_list, bin_count)

        result_obj = {'histogram': histo.tolist(), 'bin_edges': bin_edges.tolist()}
        result_obj = json.dumps(result_obj)
    except Exception as e:
        print(e)

    return JsonResponse(result_obj, safe=False)

@api_view(['GET'])
def averagehouseprices(request):
    result_obj = {}

    try:
        #Get parameters from front-end
        from_date_str = request.query_params.get('from')
        from_date_value = datetime.strptime(from_date_str, '%b %Y').date()  
        to_date_str = request.query_params.get('to')
        to_date_value = datetime.strptime(to_date_str, '%b %Y').date()
        zipcode_value = request.query_params.get('zip')

        detached_result_set = house_transactions.objects.filter(zipcode = zipcode_value,
            date__year__gte = from_date_value.year, date__month__gte = from_date_value.month,
                date__year__lte = to_date_value.year, date__month__lte = to_date_value.month,
                    property_type = 'D').annotate(month = TruncMonth('date'), year = TruncYear('date'))\
                        .values('month').annotate(average_price = Avg('price')).values('month', 'year', 'average_price')

        print(detached_result_set)
    except Exception as e:
        print(e)
    return JsonResponse(result_obj)