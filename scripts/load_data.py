import csv
from soldhouseprices_app.models import house_transactions

def run():
    house_transactions.objects.all().delete()
    file_list = ['scripts/pricepaiddata/pp-2018.csv', 'scripts/pricepaiddata/pp-2019.csv', 'scripts/pricepaiddata/pp-2020.csv']
    for file in file_list:
        count = 0
        with open(file) as file_to_read:
            try:
                file_read = csv.reader(file_to_read)
            except Exception as e:
                print(e)
            
            if(file_read):
                records = [row[0].split(';') for row in file_read]
                
                for record in records:
                    id=record[0][1:-1]
                    price = record[1]
                    transaction_date = record[2].split(' ')[0]
                    zip_code = record[3].split(' ')[0]
                    property_type = record[4]

                    # If any of the fields are empty, do not put into database
                    if(id and price and transaction_date and zip_code and property_type):
                        house_transactions.objects.create(id =id, price = price, date = transaction_date, zipcode = zip_code, property_type = property_type)
                        count += 1
                    else:
                        pass
                    if(count == 3000):
                        break
