import csv
from soldhouseprices_app.models import house_transactions

def run():
    house_transactions.objects.all().delete()
    file_list = ['scripts/pricepaiddata/pp-2018.csv', 'scripts/pricepaiddata/pp-2019.csv', 'scripts/pricepaiddata/pp-2020.csv']
    for file in file_list:
        with open(file) as file_to_read:
            file_read = csv.reader(file_to_read)
            if(file_read):

                records = [row[0].split(';') for row in file_read]
                
                for record in records:
                    id=record[0][1:-1]
                    price = record[1]
                    transaction_date = record[2].split(' ')[0]
                    zip_code = record[3].split(' ')[0]
                    property_type = record[4]

                    house_transactions.objects.create(id =id, price = price, date = transaction_date, zipcode = zip_code, property_type = property_type)
