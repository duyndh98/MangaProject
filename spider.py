from header import *


class Spider:

    # Class variables (shared among all instances)
    domain_name = ''
    base_url = ''

    manga_list = []
    manga_crawled = []

    chapter_list = []
    chapter_crawled = []

    contents = []

    def __init__(self, domain_name, base_url, data):
        
        Spider.domain_name = domain_name
        Spider.base_url = base_url

        # crawl manga list
        Spider.manga_list.append(base_url)
        
        while (len(Spider.manga_list) + len(Spider.manga_crawled) < MAX_MANGA):
            Spider.crawl()
      
        Spider.manga_list = Spider.manga_list + Spider.manga_crawled
        Spider.manga_crawled.clear()


        index = 1
        # crawl manga chapters
        while len(Spider.manga_list) > 0:
            
            manga = Spider.manga_list[len(Spider.manga_list) - 1]
            print('---------', manga)
            manga_data = {}

            request = requests.get(manga)
            soup = BeautifulSoup(request.text, 'html.parser')

            description_class = soup.find('p', class_='description-update')
            description_info = description_class.find_all('br')
            
            manga_data['manga_id'] = index

            manga_data['manga_name'] = clean(description_info[1].previous_sibling)

            manga_data['thumbnail'] = ''

            manga_data['author'] = clean(description_info[3].previous_sibling)

            s1 = soup.find('p', class_='manga-collapse').find('p')
            s2 = soup.find('meta', {'name':'description'})['content']
            manga_data['description'] = intersect(str(s1), str(s2))

            manga_data['categories'] = [x['title'] for x in description_class.find_all('a', class_='CateName')]
        
            manga_data['last_update'] = ''

            manga_data['chapters'] = []
            
            Spider.manga_list.pop()
            Spider.manga_crawled.append(manga)

            Spider.add_urls_to_list(Spider.gather_urls(manga), 'chapter', manga)
            
            # insensitive sort
            Spider.chapter_list = sorted(Spider.chapter_list, key = lambda s : s.lower())

            Spider.chapter_crawled.clear()

            # print('-------', manga)
            # for chapter in Spider.chapter_list:
            #     print(chapter)


            # crawl contents
            # while len(Spider.chapter_list) > 0:
                
            #     chapter = Spider.chapter_list[len(Spider.chapter_list) - 1]                
            #     print("------------", chapter)

            #     Spider.chapter_list.pop()
            #     Spider.chapter_crawled.append(chapter)

            #     Spider.add_urls_to_list(Spider.gather_urls(chapter, 'content'), 'content')

            #     # for content in Spider.contents:
            #     #     print(content)

            #     Spider.contents.clear()

            Spider.chapter_list.clear()
            
            index += 1
            
            data.append(manga_data)

        
    def crawl():
        url = Spider.manga_list[len(Spider.manga_list) - 1]
        
        Spider.manga_list.pop()

        if (is_manga_url(url)):
            Spider.manga_crawled.append(url)

        Spider.add_urls_to_list(Spider.gather_urls(url), 'manga')
        
    def gather_urls(url, type = ''):
        results = []
        
        request = requests.get(url)
        
        soup = BeautifulSoup(request.text, 'html.parser')

        #print(soup)

        if (type == 'content'):
            # for elem in soup.find_all('img', attr={'src': }):
                
            #     url = urljoin(url, elem['href'])
            #     results.append(url)
            pass
        else:
            for elem in soup.find_all('a', attrs={'href': re.compile('^http://')}):
                
                url = urljoin(url, elem['href'])
                results.append(url)
        
        return results

    def add_urls_to_list(urls, type, manga_url = ''):
        
        for url in urls:
            if (type == 'manga') and (len(Spider.manga_list) + len(Spider.manga_crawled) >= MAX_MANGA):
                return

            if Spider.domain_name != get_domain_name(url):
                continue

            if type == 'manga':
                
                if (url in Spider.manga_list) or (url in Spider.manga_crawled):
                    continue
                
                if is_manga_url(url):
                    Spider.manga_list.append(url)

            elif type == 'chapter':

                if (url in Spider.chapter_list) or (not is_sub_url(url, manga_url)):
                    continue

                if is_chapter_url(url):
                    Spider.chapter_list.append(url)

            elif type == 'content':

                #print(url)

                if (url in Spider.contents):
                    continue

                if is_content_url(url):
                    Spider.contents.append(url)
