from spider import *

data = []

Spider(DOMAIN_NAME, HOMEPAGE, data)

with open('manga_info.json', 'w', encoding='utf-8') as outfile:
	json.dump(data, outfile)
		
outfile.close()