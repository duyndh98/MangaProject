from domain import get_domain_name
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
class Spider:

    # Class variables (shared among all instances)
    domain_name = ''
    base_url = ''
    queue = set()
    crawled = set()

    def __init__(self, domain_name, base_url):
        print(domain_name, base_url)
        
        Spider.domain_name = domain_name
        Spider.base_url = base_url

        Spider.queue.add(base_url)
        self.crawl_page('First spider', Spider.base_url)

    @staticmethod
    def crawl_page(thread_name, page_url):
        if page_url not in Spider.crawled:
            print(thread_name + ' now crawling ' + page_url)
            print('Queue ' + str(len(Spider.queue)) + ' | ' +
                  'Crawled ' + str(len(Spider.crawled)))
            Spider.add_links_to_queue(Spider.gather_links(page_url))
            Spider.queue.remove(page_url)
            Spider.crawled.add(page_url)

    @staticmethod
    def gather_links(page_url):
        results = set()
        
        content = requests.get(page_url)
        
        soup = BeautifulSoup(content.text, 'html.parser')

        for elem in soup.find_all('a', attrs={'href': re.compile("^http://")}):
            link = urljoin(page_url, elem['href'])
            results.add(link)

        return results

    @staticmethod
    def add_links_to_queue(links):
        for url in links:
            if (url in Spider.queue) or (url in Spider.crawled):
                continue
            if Spider.domain_name != get_domain_name(url):
                continue
            Spider.queue.add(url)
