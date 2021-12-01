from django.urls import path

from . import views

urlpatterns = [
    path('transactionbins', views.transactionbins, name='transactionbins'),
    path('averagehouseprices', views.averagehouseprices, name='averagehouseprices'),
]