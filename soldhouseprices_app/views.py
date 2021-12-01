from django.http.response import JsonResponse
from datetime import datetime
from rest_framework.decorators import api_view
from soldhouseprices_app.models import house_transactions

import numpy as np
import json


@api_view(['GET'])
def transactionbins(request):
    result_obj ={}
    bin_count = 8

    date_time_str = request.query_params.get('date')
    date_value = datetime.strptime(date_time_str, '%b %Y').date()  
    zipcode_value = request.query_params.get('zip')

    try:
        result_set = house_transactions.objects.filter(zipcode = zipcode_value,
         date__year = date_value.year,
          date__month = date_value.month).values('price')

        price_list = [element['price'] for element in result_set]

        histo, bin_edges = np.histogram(price_list, bin_count)

        result_obj = {'histogram': histo.tolist(), 'bin_edges': bin_edges.tolist()}
        result_obj = json.dumps(result_obj)
    except Exception as e:
        print(e)
    return JsonResponse(result_obj)