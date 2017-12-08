# import scrapy
# import json
# import re
# import textwrap

# # open the file "filename" in write ("w") mode
# file = open("manga_info.json", "w")

# # just an example dictionary to be dumped into "filename"
# output = {"stuff": [1, 2, 3]}


# # dumps "output" encoded in the JSON format into "filename"
# json.dump(output, file)
# file.close()

from header import *
from spider import Spider

Spider(DOMAIN_NAME, HOMEPAGE)

for x in Spider.manga_list:
    print(x)
