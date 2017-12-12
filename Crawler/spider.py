from header import *

class Spider:

    manga_list = []
    chapter_list = []
    contents = []

    def __init__(self, manga_data_list):
        
        request = requests.get('http://truyentranh.net/danh-sach.tall.html')
        soup = BeautifulSoup(request.text, 'html.parser')
        
        for url in soup.find('div', id='collapseExample').find_all('a')[1:]:
            Spider.gather_urls(url['href'], 'manga')

            if len(Spider.manga_list) >= N_MANGA:
                break

        Spider.crawl_manga_data_list(manga_data_list)

    def crawl_manga_data_list(manga_data_list):

        for i_manga_list in range(len(Spider.manga_list)):
            manga_data = {}

            manga_url = Spider.manga_list[i_manga_list]
            print(i_manga_list + 1, '---------', manga_url)
            
            request = requests.get(manga_url)
            soup = BeautifulSoup(request.text, 'html.parser')

            description_update = soup.find('p', class_='description-update')
            
            manga_data['manga_id'] = i_manga_list + 1

            manga_data['manga_name'] = soup.find('h1', class_='title-manga').text
            
            manga_data['thumbnail'] = soup.find('meta', {'property':'og:image'})['content']

            manga_data['author'] = clean_string(str((description_update.find_all('span')[3]).next_sibling))

            manga_collapse = soup.find('p', class_='manga-collapse')
            manga_data['description'] = clean_string(str(manga_collapse.text).replace(str(manga_collapse.find('b').text), ''))
            
            manga_data['categories'] = [x['title'] for x in description_update.find_all('a', class_="CateName")]
        
            manga_data['last-update'] = find_last_update(soup.find('div', class_='content mCustomScrollbar').find_all('a'))
            
            Spider.chapter_list.clear()       
            Spider.gather_urls(manga_url, 'chapter')
            
            Spider.chapter_list = sorted(Spider.chapter_list, key = lambda s : s.lower())

            chapter_data_list = []
            Spider.crawl_chapter_data_list(chapter_data_list)
            

            manga_data['chapters'] = copy.deepcopy(chapter_data_list)

            manga_data_list.append(manga_data)

    def crawl_chapter_data_list(chapter_data_list):
        
        for i_chapter_list in range(len(Spider.chapter_list)):
            
            chapter_data = {}

            chapter_url = Spider.chapter_list[i_chapter_list] 
            print(chapter_url)                         

            request = requests.get(chapter_url)
            soup = BeautifulSoup(request.text, 'html.parser')

            chapter_data['chapter_id'] = i_chapter_list + 1

            chapter_data['chapter_name'] = soup.find('h1', class_='chapter-title').text

            Spider.contents.clear()
            Spider.gather_urls(chapter_url, 'content')
            chapter_data['page_list'] = copy.deepcopy(Spider.contents)

            chapter_data_list.append(chapter_data)
        
    def gather_urls(url, type):
        
        request = requests.get(url)
        soup = BeautifulSoup(request.text, 'html.parser')

        if type == 'manga':
            n_manga = 0

            for manga in soup.find_all('div', class_='media-left cover-manga'):
                manga_url = manga.find('a')['href']
                
                if manga_url not in Spider.manga_list:
                    Spider.manga_list.append(manga_url)
                    n_manga += 1
                    
                if n_manga >= N_MANGA_PER_PAGE:
                    return

        elif type == 'chapter':
            for chapter in soup.find('div', class_='content mCustomScrollbar').find_all('a'):
                chapter_url = chapter['href']

                if chapter_url not in Spider.chapter_list:
                    Spider.chapter_list.append(chapter_url)

        elif type == 'content':     
            contents_text = soup.find('div', class_='each-page') 
            if contents_text == None:
                contents_text = soup.find('div', class_='OtherText')
            
            for content_url in contents_text.find_all('img'):
                if content_url not in Spider.contents:
                    Spider.contents.append(content_url['src'])