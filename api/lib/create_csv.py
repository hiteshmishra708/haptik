import csv
from api.models.default import WebsiteSignups

def website_signup_csv():
    signups = WebsiteSignups.objects.all() 
    with open('website_signup.csv' , 'w') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csv_writer .writerow(['No.', 'country_code', 'number', 'singedup on'])
        for i, b in enumerate(signups):
            csv_writer.writerow([i+1, b.country_code.strip(), b.number.strip(), b.created_at])


