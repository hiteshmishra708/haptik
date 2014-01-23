from api.models.default import Business, User, Favourite, Faqs, CountriesSupported
import csv


def insert_countries():
    with open('/home/ubuntu/countries.csv', 'rb') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csv_reader:
            country = row[0]
            code = row[1]
            callcode = row[3]
            print country
            print code
            print callcode
            a = CountriesSupported()
            a.code = code
            a.country = country
            a.callcode = callcode
            a.active = 0
            a.save()
            
    
