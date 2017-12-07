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

import threading
from queue import Queue
from domain import get_domain_name, get_sub_domain_name
from spider import Spider

NUM_SPIDERS = 10

HOMEPAGE = 'http://truyentranh.net/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)

Spider(DOMAIN_NAME, HOMEPAGE)
q = Queue()

# Each queued link is a new job
def create_jobs():
    for link in Spider.queue:
        q.put(link)
    q.join()
    crawl()

# Check if there are items in queue, if so crawl it
def crawl():
    if len(Spider.queue) > 0:
        print(str(len(Spider.queue)), "links in the queue")
        create_jobs()

# crawl the next url
def work():
    while True:
        url = q.get()
        Spider.crawl_page(threading.currentThread().name, url)
        q.task_done()

# Create spider threads (will be terminated when main exits)
def create_spiders():
    for x in range(NUM_SPIDERS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()

create_spiders()
crawl()
