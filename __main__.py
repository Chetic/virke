#!/usr/bin/python3.7
import lxml
import lxml.html
import json
from urllib.request import Request, urlopen
from urllib import request

def get_page_source(url):
    req = Request(site, headers={'User-Agent': 'Mozilla/5.0'})
    return urlopen(req).read().decode("utf-8")

def get_page_source_no_download(source_filepath):
    with open(source_filepath, 'r') as file:
        return file.read().replace('\n', '')

with open('sites.txt') as file:
    sites = [line.rstrip() for line in file.readlines()]
    for site in sites:
        xml_root = lxml.html.fromstring(get_page_source_no_download('tmp.html'))
        interesting_data_element = xml_root.xpath("//script[@type='application/ld+json']")[2]
        json = json.loads(interesting_data_element.text)
        print(json[0]['name'] + ': ' + str(json[0]['offers']['price']) + ' ' + json[0]['offers']['priceCurrency'])
