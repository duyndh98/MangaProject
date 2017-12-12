from spider import *

manga_data_list = []

Spider(DOMAIN_NAME, HOMEPAGE, manga_data_list)

with open('manga_info.json', 'w', encoding='utf-8') as outfile:
	json.dump(manga_data_list, outfile)
		
outfile.close()