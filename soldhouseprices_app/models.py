from django.db import models

class house_transactions(models.Model):
    id = models.CharField(max_length=60, primary_key=True)
    price = models.IntegerField()
    date = models.DateField()
    zipcode = models.CharField(max_length=10)
    property_type = models.CharField(max_length=1)
    