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

def get_main_menu(url):
    xml_root = lxml.html.fromstring(get_page_source_no_download('mainpage.tmp'))
    return xml_root.xpath("//*[@class='level2 first parent']")[0]

def print_price(xml_root):
    interesting_data_element = xml_root.xpath("//script[@type='application/ld+json']")[2]
    j = json.loads(interesting_data_element.text)
    print(j[0]['name'] + ': ' + str(j[0]['offers']['price']) + ' ' + j[0]['offers']['priceCurrency'])

def print_element(element):
    print(lxml.etree.tostring(element, pretty_print=True).decode('utf-8'))

if __name__ == '__main__':
    with open('sites.txt') as file:
        sites = [line.rstrip() for line in file.readlines()]
        for site in sites:
            main_menu = get_main_menu(site)
            for menu_choice in main_menu.xpath('ul/li'):
                for list_page_url in menu_choice.xpath('a/@href')[0]:
                    xml_root = lxml.html.fromstring(get_page_source_no_download('listpage.tmp'))
                    # TODO: Loop over prices here
            xml_root = lxml.html.fromstring(get_page_source_no_download('mainpage.tmp'))
            print_price(xml_root)
