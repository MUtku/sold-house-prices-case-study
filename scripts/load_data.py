import csv
import os
from soldhouseprices_app.models import house_transactions

def run():
    file  = open("./pp-2021_clean.csv");
    file_read = csv.reader(file);
    
    house_transactions.objects.all().delete()

    for record in file_read:
        print(record)
        id=record[0][1:-1]
        price = record[1]
        transaction_date = record[2].split(' ')[0]
        zip_code = record[3].split(' ')[0]
        property_type = record[4]

        house_transactions.objects.create(id =id, price = price, date = transaction_date, zip = zip_code, property_type = property_type)
