import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "haptik_api.settings")

from bs4 import BeautifulSoup
from urllib2 import urlopen
import re
from api.models.default import AkoshaBusiness
import Queue
import threading
from time import sleep
import random
import csv

BASE_URL = 'http://akosha.com'
q_category = Queue.Queue(maxsize = 0)
q_business = Queue.Queue(maxsize=0)

num_worker_threads = 1
business_count = 0
category_count = 0

def get_base_business(category_url):
    random_sleep = random.randint(80,240)
    print 'cateogry sleeping for : ', random_sleep
    sleep(random_sleep)
    try:
        full_url = '%s%s' % (BASE_URL, category_url)
        html = urlopen(full_url).read()
        soup = BeautifulSoup(html)
        table = soup.find("table" , {"class" : "table"})
        tbody = table.find("tbody")
        rows = tbody.findAll("tr")


        #find next page link
        paginator = soup.find("ul", {"class" : "paginator"})
        rows_p = paginator.findAll("li")
        row_p = rows_p[-1]
        next_url = row_p.a["href"]
        print 'next url : ', next_url
        if next_url == '#':
            print 'next url is # hence not entering'
            print 'current url : ', full_url
        else:
            q_category.put(next_url)
        print '-- processed categories --'

        #parse each business
        businesses = []
        for row in rows:
            try:
                tds = row.findAll("td")
                business_url = tds[3].a["href"]
                sector = tds[2].find('h3').contents[0]
                business_name = tds[1].find('h3').contents[0]
                print 'putting business : ', business_name
                a = {'url' : business_url, 'name' : business_name, 'sector': sector}
                businesses.append(a)
                #q_business.put((business_url, business_name, sector))
            except Exception, e:
                print '-*' * 40
                print 'unable to get business data from html : ', row
                print 'error: ', e
                print '-*' * 40
        if len(businesses)> 0:
            parse_business(businesses)
        
    except Exception, e:
        print 'unable to parse category with url : ', category_url
        print '-*' * 20


def parse_business(businesses):
    with open('/home/ubuntu/akosha/akosha_media.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for a in businesses:
            url = a['url']
            name = a['name']
            sector = a['sector']
            random_sleep = random.randint(10,60)
            print 'business sleeping for : ', random_sleep
            sleep(random_sleep)
            full_url = '%s%s' % (BASE_URL, url)
            html = urlopen(full_url).read()
            soup = BeautifulSoup(html)
            try:
                phone = soup.find('div' , {'id' : 'phoneSupport'}).findAll('p')[-1].find('span').contents[0]
                phone = phone.replace(',' , '-')
                phone = phone.replace('\n', ' ').replace('\r', '')
                if 'No phone' in phone:
                    phone = None
            except:
                phone = None
            try:
                email = soup.find('div' , {'id' : 'emailSupport'}).find('a').contents[0]
                email = email.replace('\n', ' ').replace('\r', '')
            except:
                email = None
            try:
                address= soup.find('div' , {'id' : 'address'}).findAll('p')[-1].find('span').contents[0]
                address = address.replace('\n', ' ').replace('\r', '').replace(',' , '-')
            except:
                address = None
            try:
                info_rows = soup.find('div' , {'id' : 'usefulInformation'}).findAll('div')
                if len(info_rows) == 0:
                    info_rows = soup.find('div' , {'id' : 'usefulInformation'}).findAll('span')
                info_text = ''
                for row in info_rows:
                    for r in row.contents:
                        try:
                            info_text +=  '%s' % re.sub('<[^<]+?>', '', r.encode('utf-8').strip())
                            info_text = info_text.replace('\n', ' ').replace('\r', '').replace(',' , '-')
                        except Exception, e:
                            print 'some exception : ', e
                            pass
            except Exception, e:
                print  'nothie expcetioon : ',e
                info_text = None
            try: 
                writer.writerow([name, full_url, sector, phone, email, address, info_text])
                #business = AkoshaBusiness()
                #business.name = name
                #business.url = full_url
                #business.category = sector
                #business.phone = phone
                #business.email = email
                #business.address = address
                #business.info = info_text
                #business.save()
                print '-*-*-*-* processed businesses -*-*-*-*'
            except Exception, e:
                print 'unable to save business %s at url %s' % (name, full_url)
                print 'reason : ', e



def category_worker():
    while True:
        url = q_category.get()
        get_base_business(url)
        q_category.task_done()


#def business_worker():
#    while True:
#        items = q_business.get()
#        parse_business(items[0], items[1], items[2])
#        q_business.task_done()


if __name__ == "__main__":
    #get_base_business('/Airlines-complaint-1.html' ,1)
    #parse_business('/Air-Arabia-customer-care-434.html', 0,0)
    #parse_business('/United-Airlines-customer-care-5522.html' ,0, 0)
    category_thread = threading.Thread(target=category_worker)
    category_thread.start()
    #business_thread = threading.Thread(target=business_worker)
    #business_thread.start()

    q_category.put('/Media-complaint-20.html')

    q_category.join()
    #q_business.join()

    print "Processing Complete"
