from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

def get_domain_name(url):
    try:
        results = get_sub_domain_name(url).split('.')
        return results[-2] + '.' + results[-1]
    except:
        return ''


def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc
    except:
        return ''

HOMEPAGE = 'http://truyentranh.net/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
root_url = set(['http://truyentranh.net', 'http://truyentranh.net/blog'])

def is_manga_url(url):
	
	return ('html' not in url) and ('/Chap-' not in url) and ('/chap-' not in url) and (url not in root_url)

def is_chapter_url(url):

	return ('html' not in url) and (('/Chap-' in url) or ('/chap-' in url)) and (url not in root_url)
	
def is_sub_url(chapter_url, manga_url):

	return manga_url.lower() in chapter_url.lower()