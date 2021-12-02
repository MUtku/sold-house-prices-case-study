from django.db.models.functions.datetime import TruncYear
from django.http.response import JsonResponse
from django.db.models.aggregates import Avg
from django.db.models.functions import TruncMonth
from datetime import datetime
from rest_framework.decorators import api_view
from soldhouseprices_app.models import house_transactions

import numpy as np
import json
import calendar


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

        result_obj = {'histogram': list(histo), 'bin_edges': list(bin_edges)}
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
        last_day_of_month = calendar.monthrange(to_date_value.year, to_date_value.month)[1]
        to_date_value = datetime(to_date_value.year, to_date_value.month, last_day_of_month)
        zipcode_value = request.query_params.get('zip')

        result_set = house_transactions.objects.filter(zipcode = zipcode_value,
            date__range = [from_date_value, to_date_value])\
                .annotate(month = TruncMonth('date')).values('month')\
                        .annotate(average_price = Avg('price')).values('property_type', 'month', 'average_price')

        result_obj = {list(result_set)}
        result_obj = json.dumps(result_obj)
        # detached_result_set = house_transactions.objects.filter(zipcode = zipcode_value,
        #     date__range = [from_date_value, to_date_value], property_type = 'D')\
        #         .annotate(month = TruncMonth('date')).values('month')\
        #                 .annotate(average_price = Avg('price')).values('month', 'average_price')

        # semi_detached_result_set = house_transactions.objects.filter(zipcode = zipcode_value,
        #     date__range = [from_date_value, to_date_value], property_type = 'S')\
        #         .annotate(month = TruncMonth('date')).values('month')\
        #                 .annotate(average_price = Avg('price')).values('month', 'average_price')

        # terraced_result_set = house_transactions.objects.filter(zipcode = zipcode_value,
        #     date__range = [from_date_value, to_date_value], property_type = 'T')\
        #         .annotate(month = TruncMonth('date')).values('month')\
        #                 .annotate(average_price = Avg('price')).values('month', 'average_price')

        # flats_result_set = house_transactions.objects.filter(zipcode = zipcode_value,
        #     date__range = [from_date_value, to_date_value], property_type = 'F')\
        #         .annotate(month = TruncMonth('date')).values('month')\
        #                 .annotate(average_price = Avg('price')).values('month', 'average_price')

        # result_obj = {'detached': list(detached_result_set), 
        #                 'semi_detached': list(semi_detached_result_set),
        #                 'terraced': list(terraced_result_set),
        #                 'flats': list(flats_result_set)}
        # result_obj = json.dumps(result_obj)
    except Exception as e:
        print(e)
    return JsonResponse(result_obj)