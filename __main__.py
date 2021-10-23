#!/usr/bin/python3.7
import lxml
import lxml.html
import json
import subprocess
import sqlite3
import time
import re
from urllib.request import Request, urlopen
from urllib import request

def get_page_source(url):
    with open('wget.log', 'w') as wget_logfile:
        ret = subprocess.call('wget -O download.tmp ' + url, shell=True, stdout=wget_logfile, stderr=wget_logfile)
    if ret != 0:
        raise ChildProcessError('Failed to download with wget')
    return get_page_source_no_download('download.tmp')

def get_page_source_with_python(url):
    req = Request(site, headers={'User-Agent': 'Wget/1.20.1 (linux-gnueabihf)'})
    return urlopen(req).read().decode("utf-8")

def get_page_source_no_download(source_filepath):
    with open(source_filepath, 'r') as file:
        return file.read().replace('\n', '')

def get_main_menu(url):
    xml_root = lxml.html.fromstring(get_page_source(url))
    return xml_root.xpath("//*[@class='level2 first parent']")[0]

def get_interesting_json(xml_root):
    interesting_data_element = xml_root.xpath("//script[@type='application/ld+json']")[2]
    return json.loads(interesting_data_element.text)

def print_price_from_product_page(j):
    print(j[0]['name'] + ': ' + str(j[0]['offers']['price']) + ' ' + j[0]['offers']['priceCurrency'])

def print_element(element):
    print(lxml.etree.tostring(element, pretty_print=True).decode('utf-8'))

def write_to_file(content, filename):
    with open(filename, 'w') as f:
        f.write(content)

if __name__ == '__main__':
    db = sqlite3.connect('virke.db')
    with db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS Prices (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                sku TEXT,
                retrieved INTEGER,
                name TEXT,
                price INTEGER,
                priceCurrency TEXT,
                source TEXT
            );
        """)
        with open('sites.txt') as file:
            sites = [line.rstrip() for line in file.readlines()]
            print('version 1.0')
            for site in sites:
                print('site: ' + site)
                main_menu = get_main_menu(site)
                for menu_choice in main_menu.xpath('ul/li'):
                    for list_page_url in menu_choice.xpath('a/@href'):
                        list_page_url = list_page_url.replace('ä','%C3%A4').replace('å','%C3%A5').replace('ö','%C3%B6')
                        print('source: ' + list_page_url)
                        page_source = get_page_source(list_page_url)
                        xml_root = lxml.html.fromstring(page_source)
                        j = get_interesting_json(xml_root)
                        for product in j['mainEntity']['itemListElement']:
                            sku = product['sku']
                            retrieved = int(time.time())
                            name = product['name']
                            price = product['offers']['price']
                            price_currency = product['offers']['priceCurrency']
                            source = list_page_url
                            query = 'INSERT INTO Prices (sku, retrieved, name, price, priceCurrency, source) values (?, ?, ?, ?, ?, ?)'
                            data = [(sku, retrieved, name, price, price_currency, source)]
                            print(str(sku) + " " + str(retrieved) + " " + name + ": " + str(price) + ' ' + str(price_currency))
                            db.executemany(query, data)
