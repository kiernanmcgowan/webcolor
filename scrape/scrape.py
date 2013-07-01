# scrape.py

# system
from urlparse import urlparse
import commands
import subprocess
import os
import csv

# db stuff
import urllib
import psycopg2 as db
conn = db.connect(dbname='webcolor', user=os.environ['user'], host='localhost', password=os.environ['pass'])
cursor = conn.cursor()

# boto
import boto
s3 = boto.connect_s3()
bucket = s3.lookup('dropdownmenu-color-img')

# regex for color
import re
regex = re.compile("#[0-9a-fA-F]+")

# grabs a url and creates an image of it
def createImageOfURL(url, imgLocation):
    try:
        generateImage = 'gnome-web-photo -m photo --file ' + url + ' ' + imgLocation
        status = commands.getstatusoutput(generateImage)
        return True
    except Exception as err:
        print err
        return False


# extracts the top 5 colors of an image
def extractPallet(img):
    getPallet = 'convert ' + img + ' +dither -colors 5 -format "%c" histogram:info:'
    status = commands.getstatusoutput(getPallet)
    colors = regex.findall(status[1])
    tmpCount = re.findall('\d+:', status[1])
    count = []
    for c in tmpCount:
        count.append(int(c.replace(':', '')))

    z = zip(count, colors)
    z.sort(reverse=True)

    return zip(*z)


def storeSite(name, display_name, colors, count):
    try:
        cursor.execute('INSERT INTO site (hostname, colors, count, display_name) VALUES(%s, %s, %s, %s)', (name, list(colors), list(count), display_name))
        conn.commit()
        return True
    except Exception as err:
        print err
        conn.rollback()
        return False


def cleanUp(img):
    os.unlink(img)


def getPalletForSite(hostname):
    # may not work all the time, but good enough
    url = 'http://' + hostname
    imageLocation = './' + hostname + '.png'
    arr = hostname.split('.')
    display_name = arr[0]

    print display_name
    try:
        if createImageOfURL(url, imageLocation):
            pallet = extractPallet(imageLocation)
            storeSite(hostname, display_name, pallet[1], pallet[0])

            key = bucket.new_key(display_name)
            key.set_contents_from_filename(imageLocation)

            # always delete the image
            cleanUp(imageLocation)
        else:
            print 'oh no! it failed'
    except Exception as err:
        print err


def processFile(srcCSV, maxCount):
    with open(srcCSV, 'rb') as csvfile:
        sites = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in sites:
            if int(row[0]) > maxCount:
                print 'hit top num - breaking'
                break
            getPalletForSite(row[1])


processFile('../data/sites.csv', 500)
#getPalletForSite('facebook.com')
