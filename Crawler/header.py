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

# def get_sub_domain_name(url):
#     try:
#         return urlparse(url).netloc
#     except:
#         return ''

HOMEPAGE = 'truyentranh.net'

N_MANGA = 3
N_MANGA_PER_PAGE = 1

root_url = set(['http://truyentranh.net', 'http://truyentranh.net/blog'])
image_format = ['.jpg', '.jpeg', '.png', '.gif', '.tiff', '.bmp']

# def is_manga_url(url):
	
# 	return ('html' not in url) and ('chap' not in url.lower()) and (url not in root_url) and (url.count('/') == 3)

# def is_chapter_url(url):

# 	return ('html' not in url) and ('chap' in url.lower()) and (url not in root_url) and (url.count('/') == 4)
	
# def is_sub_url(chapter_url, manga_url):

# 	return manga_url.lower() in chapter_url.lower()

# def is_content_url(content_url):

# 	for x in image_format:
# 		if x in content_url:
# 			return True

# 	return False

def clean_string(s):
	s = " ".join(s.split())
	for x in ['<b>', '</b>', '<p>', '</p>', '<span>', '/<span>']:
		s = s.replace(x, '')

	if s[:2] == ': ':
		s = s[2:]

	return s

def intersect(s1, s2):
    for length in range(len(s2) - 1, -1, -1):
        for i in range(0, len(s2) - length + 1):
            if s2[i:i + length] in s1:
                return s2[i:i + length]

# def later(date1, date2):
# 	if date2 == '':
# 		return date1
# 	return max([date1, date2], key=lambda x: datetime.datetime.strptime(x, "%d/%m/%Y"))


def find_last_update(chapters):
	
	last_date = ''

	for chapter in chapters:
		
		date = chapter.find('span', class_='date-release').text
		last_date = date if last_date == '' else max([date, last_date], key=lambda x: datetime.datetime.strptime(x, "%d/%m/%Y"))
	
	return last_date