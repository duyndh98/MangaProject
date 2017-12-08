from header import *

class Spider:

    # Class variables (shared among all instances)
    domain_name = ''
    base_url = ''

    manga_list = []
    manga_crawled = []
    
    def __init__(self, domain_name, base_url):
        
        Spider.domain_name = domain_name
        Spider.base_url = base_url

        Spider.manga_list.append(base_url)
        
        while (len(Spider.manga_list) + len(Spider.manga_crawled) < 100):
            Spider.crawl_page()

        Spider.manga_list = Spider.manga_list + Spider.manga_crawled
        print(len(Spider.manga_list))

    #@staticmethod
    def crawl_page():
        page_url = Spider.manga_list[len(Spider.manga_list) - 1]
        
        Spider.manga_list.pop()
        
        if (is_manga_link(page_url)):
            Spider.manga_crawled.append(page_url)
        
        Spider.add_links_to_list(Spider.gather_links(page_url))
        
        
    #@staticmethod
    def gather_links(page_url):
        
        results = []
        
        content = requests.get(page_url)
        
        soup = BeautifulSoup(content.text, 'html.parser')

        for elem in soup.find_all('a', attrs={'href': re.compile('^http://')}):
            link = urljoin(page_url, elem['href'])
            results.append(link)
            
        return results

    #@staticmethod
    def add_links_to_list(links):

        for url in links:

            if (url in Spider.manga_list) or (url in Spider.manga_crawled):
                continue
            if Spider.domain_name != get_domain_name(url):
                continue
            
            if is_manga_link(url):
                Spider.manga_list.append(url)
