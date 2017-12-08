from header import *

class Spider:

    # Class variables (shared among all instances)
    domain_name = ''
    base_url = ''

    manga_list = []
    manga_crawled = []

    chapter_list = []

    def __init__(self, domain_name, base_url):
        
        Spider.domain_name = domain_name
        Spider.base_url = base_url

        # crawl manga list
        Spider.manga_list.append(base_url)
        
        while (len(Spider.manga_list) + len(Spider.manga_crawled) < 100):
            Spider.crawl()

        Spider.manga_list = Spider.manga_list + Spider.manga_crawled
        Spider.manga_crawled.clear()

        # crawl manga chapters
        i = 1
        while len(Spider.manga_list) > 0:
            manga = Spider.manga_list[len(Spider.manga_list) - 1]
            
            print(i, "---------", manga)
            
            Spider.manga_list.pop()
            Spider.manga_crawled.append(manga)

            Spider.add_urls_to_list(Spider.gather_urls(manga), 'chapter', manga)
            
            # insensitive sort
            Spider.chapter_list = sorted(Spider.chapter_list, key = lambda s : s.lower())

            if (len(Spider.chapter_list) == 0):
                print("empty")

            for chapter in Spider.chapter_list:
                print(chapter)

            Spider.chapter_list.clear()

            i += 1
        
    def crawl():
        url = Spider.manga_list[len(Spider.manga_list) - 1]
        
        Spider.manga_list.pop()
        
        if (is_manga_url(url)):
            Spider.manga_crawled.append(url)
        
        Spider.add_urls_to_list(Spider.gather_urls(url), 'manga')
        
    def gather_urls(url):
        
        results = []
        
        content = requests.get(url)
        
        soup = BeautifulSoup(content.text, 'html.parser')

        for elem in soup.find_all('a', attrs={'href': re.compile('^http://')}):
            url = urljoin(url, elem['href'])
            results.append(url)
            
        return results

    def add_urls_to_list(urls, type, manga_url = ''):
        
        for url in urls:
            if Spider.domain_name != get_domain_name(url):
                continue

            if type == 'manga':
                if (url in Spider.manga_list) or (url in Spider.manga_crawled):
                    continue
                
                if is_manga_url(url):
                    Spider.manga_list.append(url)

            else:

                if (url in Spider.chapter_list) or (not is_sub_url(url, manga_url)):
                    continue

                if is_chapter_url(url):
                    Spider.chapter_list.append(url)
