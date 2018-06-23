# Copyright [Olivier Goutay] [name of copyright owner]
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# import libraries
import urllib
import urllib2
import re
import os
import time
from bs4 import BeautifulSoup

# --------------- Method defs ---------------

number_of_images = 0

base_folder = "images/"

if not os.path.exists(base_folder):
    os.makedirs(base_folder)

def urlOpenAndSoup(url):
    """ Waits for 100ms, loads an URL and converts it to a BeautifulSoup object """
    time.sleep(0.1)
    print "Requesting " + url
    try:
        return BeautifulSoup(urllib2.urlopen(url, timeout = 5), "html.parser")
    except Exception as e:
        print(e)
        return urlOpenAndSoup(url)

def getPictureFromUrl(url):
    """ If not already present, retrieve an image from an URL and stores it (by name = text after last occurence of "/") """
    global number_of_images
    number_of_images += 1
    file_name = base_folder + url.split('/')[-1]
    if not os.path.exists(file_name):
        urllib.urlretrieve(url, file_name)
        print `number_of_images` + " images have been downloaded"
    else:
        print "Already there. Won't download image " + `number_of_images`

def downloadAllImagesFromPage(soup):
    """ Find all product images links, load these pages, and take the image """
    product_imgs = soup.find_all("div", attrs={"class": "productImg"})
    for product in product_imgs:
        print base_url + product.find("a")['href']
        product_soup = urlOpenAndSoup(base_url + product.find("a")['href'])
        img_link = base_url + product_soup.find("div", attrs={"class": "productImg"}).find("img")["src"]
        if "shiner" not in img_link and "generic" not in img_link:
            getPictureFromUrl(img_link)

# --------------- End Method defs ---------------

# Base defs
base_url = "http://www.klwines.com"
next_pattern = re.compile('next')
wines = base_url + "/Products/r?r=57+4294967216&d=1&t=&o=8&z=False"
sparklings = base_url + "/Products/r?d=1&r=57+4294967273&p=0&o=8&t=&z=False"
spirits = base_url + "/Spirits"

url_to_scrape = wines

# Query pages (from first to 25)
soup = urlOpenAndSoup(url_to_scrape)
for i in range(1, 9):
    downloadAllImagesFromPage(soup)
    next_url = base_url + soup.find("a", text = next_pattern)["href"]
    soup = urlOpenAndSoup(next_url)
