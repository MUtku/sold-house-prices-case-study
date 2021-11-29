from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from datetime import datetime
from rest_framework.decorators import api_view

from soldhouseprices_app.models import house_transactions

@api_view(['GET'])
def transactionbins(request):
    transaction_obj = {}
    date_time_str = request.query_params.get('date')
    date_time_obj = datetime.strptime(date_time_str, '%b %Y').date()
        
    zipcode_value = request.query_params.get('zip')
    date_value = date_time_obj
    resultset = house_transactions.objects.filter(zipcode = zipcode_value,
                                                    date__year = date_value.year(), 
                                                    date__month = date_value.month())
    try:
        print(resultset)
    except Exception as e:
        print(e)
    return JsonResponse(transaction_obj)