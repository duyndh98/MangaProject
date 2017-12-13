from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import scrapy
import json
import textwrap
import lxml.html
import hashlib
import datetime
import copy

def get_domain_name(url):
    try:
        results = get_sub_domain_name(url).split('.')
        return results[-2] + '.' + results[-1]
    except:
        return ''

HOMEPAGE = 'truyentranh.net'

N_MANGA = 200
N_MANGA_PER_PAGE = 4

root_urls = set(['http://truyentranh.net', 'http://truyentranh.net/blog'])
image_formats = ['.jpg', '.jpeg', '.png', '.gif', '.tiff', '.bmp']

def clean_string(s):
	s = " ".join(s.split())
	for x in ['<b>', '</b>', '<p>', '</p>', '<span>', '/<span>']:
		s = s.replace(x, '')

	if s[:2] == ': ':
		s = s[2:]

	return s

def find_last_update(chapters):
	
	last_date = ''

	for chapter in chapters:
		
		date = chapter.find('span', class_='date-release').text
		last_date = date if last_date == '' else max([date, last_date], key=lambda x: datetime.datetime.strptime(x, "%d/%m/%Y"))
	
	return last_date