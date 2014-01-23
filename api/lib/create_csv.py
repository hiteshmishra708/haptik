import csv
from api.models.default import WebsiteSignups, BetaDistrib, User, Favourite
from django.core.mail import EmailMessage
import StringIO
import string

EMAIL_ADDRESS = ['swapan@haptik.co' , 'aakrit@haptik.co', 'hat@haptik.co']

def website_signup_csv():
    signups = WebsiteSignups.objects.all() 
    #with open('website_signup.csv' , 'w') as csvfile:
    csvfile=StringIO.StringIO()
    csv_writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['No.', 'country_code', 'number', 'singedup on'])
    for i, b in enumerate(signups):
        csv_writer.writerow([i+1, b.country_code.strip(), b.number.strip(), b.created_at])

    message = EmailMessage('Website Signups - Haptik', 'Website Signups', 'swapan@haptik.co' , EMAIL_ADDRESS)
    message.encoding = 'utf-8'
    message.attach('singups.csv' , csvfile.getvalue(), 'text/csv')
    #message.attach_file('/home/ubuntu/haptik_api/website_signup.csv')
    message.send()


def beta_distrib_csv():
    beta_distrib = BetaDistrib.objects.all()
    csvfile=StringIO.StringIO()
    csv_writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['No.', 'number', 'Opened'])
    for i, b in enumerate(beta_distrib):
        opened = 'No' 
        if not b.active:
            opened = 'Yes'
        csv_writer.writerow([i+1, b.number.strip(), opened])

    message = EmailMessage('Beta Links sent - Haptik', 'Beta Links Sent', 'swapan@haptik.co' ,EMAIL_ADDRESS)
    message.encoding = 'utf-8'
    message.attach('beta_singups.csv' , csvfile.getvalue(), 'text/csv')
    message.send()

   
def haptik_users():
    users = User.objects.all()
    csvfile=StringIO.StringIO()
    csv_writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['Id', 'country code', 'number', 'name'])
    for i, b in enumerate(users):
        name_fil = None
        if b.first_name:
            name = b.first_name
            name_fil = filter(lambda x: x in string.printable, name)
        csv_writer.writerow([b.id, b.country_code.strip(), b.number.strip(), name_fil])

    message = EmailMessage('Users - Haptik', 'All current Haptik Users', 'swapan@haptik.co' , EMAIL_ADDRESS)
    message.encoding = 'utf-8'
    message.attach('haptik_users.csv' , csvfile.getvalue(), 'text/csv')
    message.send()
    

def user_favorites():
    favorites = Favourite.objects.filter(active=1).order_by('user')
    csvfile=StringIO.StringIO()
    csv_writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['User Number', 'business name'])
    for i, b in enumerate(favorites):
        csv_writer.writerow([b.user.number, b.business.name])

    message = EmailMessage('User Favorites - Haptik', 'Business favorites by User', 'swapan@haptik.co' , EMAIL_ADDRESS)
    message.encoding = 'utf-8'
    message.attach('haptik_favorites.csv' , csvfile.getvalue(), 'text/csv')
    message.send()
