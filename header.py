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

def is_manga_link(link):
	
    root_link = set(['http://truyentranh.net', 'http://truyentranh.net/blog'])
	
    return ('html' not in link) and ('Chap' not in link) and ('chap' not in link) and (link not in root_link)