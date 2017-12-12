from header import *


class Spider:

    # Class variables (shared among all instances)
    domain_name = ''
    base_url = ''

    manga_list = []

    chapter_list = []

    contents = []

    def __init__(self, domain_name, base_url, manga_data_list):
        
        Spider.domain_name = domain_name
        Spider.base_url = base_url

        # crawl manga list on home page
        Spider.add_urls_to_list(Spider.gather_urls(base_url, 'manga'), 'manga')

        i_manga_list = 0
        while len(Spider.manga_list) < MAX_MANGA:
            
            Spider.add_urls_to_list(Spider.gather_urls(Spider.manga_list[i_manga_list]), 'manga')
            i_manga_list += 1

        Spider.crawl_manga_data_list(manga_data_list)

    def crawl_manga_data_list(manga_data_list):

        for i_manga_list in range(len(Spider.manga_list)):
            
            manga_data = {}

            manga = Spider.manga_list[i_manga_list]
            print(i_manga_list, '---------', manga)
            
            request = requests.get(manga)
            soup = BeautifulSoup(request.text, 'html.parser')

            description_class = soup.find('p', class_='description-update')
            description_info = description_class.find_all('br')
            
            manga_data['manga_id'] = i_manga_list + 1

            manga_data['manga_name'] = clean_string(description_info[1].previous_sibling)

            manga_data['thumbnail'] = soup.find('meta', {'property':'og:image'})['content']

            manga_data['author'] = clean_string(description_info[3].previous_sibling)

            s1 = soup.find('p', class_='manga-collapse').find('p')
            s2 = soup.find('meta', {'name':'description'})['content']
            manga_data['description'] = intersect(str(s1), str(s2))

            manga_data['categories'] = [x['title'] for x in description_class.find_all('a', class_='CateName')]
        
            manga_data['last_update'] = find_last_update(soup.find('div', class_='content mCustomScrollbar').find_all('a'))
            
            Spider.chapter_list.clear()       
            Spider.add_urls_to_list(Spider.gather_urls(manga, 'chapter'), 'chapter', manga)
            
            # insensitive sort
            Spider.chapter_list = sorted(Spider.chapter_list, key = lambda s : s.lower())

            #Spider.chapter_crawled.clear()

            chapter_data_list = []
            Spider.crawl_chapter_data_list(chapter_data_list)
            manga_data['chapters'] = chapter_data_list

            
            manga_data_list.append(manga_data)


    def crawl_chapter_data_list(chapter_data_list):
        
        for i_chapter_list in range(len(Spider.chapter_list)):
            
            chapter_data = {}

            chapter = Spider.chapter_list[i_chapter_list]                            
            print(chapter)

            Spider.contents.clear() 
            Spider.add_urls_to_list(Spider.gather_urls(chapter, 'content'), 'content')

            request = requests.get(chapter)
            soup = BeautifulSoup(request.text, 'html.parser')

            chapter_data['chapter_id'] = i_chapter_list + 1

            chapter_data['chapter_name'] = soup.find('h1', class_='chapter-title').text

            chapter_data['page_list'] = Spider.contents
            
            chapter_data_list.append(chapter_data)
        
    def gather_urls(url, type = ''):
        results = []
        
        request = requests.get(url)
        
        soup = BeautifulSoup(request.text, 'html.parser')

        if type == 'content':
            
            contents = soup.find('div', class_='each-page')
            if contents == None:
                contents = soup.find('div', class_='OtherText')
            
            imgs = contents.find_all('img')
            for img in imgs:
                results.append(img['src'])

        elif type == 'chapter':
            
            chapters = soup.find('div', class_='content mCustomScrollbar').find_all('a')

            for chapter in chapters:
                
                results.append(chapter['href'])
                
        elif type == 'manga':

            for elem in soup.find_all('a', attrs={'href': re.compile('^http://')}):
                
                url = urljoin(url, elem['href'])
                results.append(url)
        

        return results

    def add_urls_to_list(urls, type, manga_url = ''):


        for url in urls:
            if (type == 'manga') and (len(Spider.manga_list) >= MAX_MANGA):
                return

            if (type != 'content') and (Spider.domain_name != get_domain_name(url)):
                continue

            if type == 'manga':
                
                if (url in Spider.manga_list):
                    continue
                
                if is_manga_url(url):
                    Spider.manga_list.append(url)

            elif type == 'chapter':

                if (url in Spider.chapter_list) or (not is_sub_url(url, manga_url)):
                    continue

                if is_chapter_url(url):
                    Spider.chapter_list.append(url)

            elif type == 'content':

                if (url in Spider.contents):
                    continue

                if is_content_url(url):

                    Spider.contents.append(url)
