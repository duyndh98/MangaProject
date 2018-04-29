# Manga Reading

Project Task: Manga Crawler and Manga Viewer
This is project, we will build a simple system for manga reading. The system contains two separated modules: a Manga Crawler and a Manga Viewer.
Programming languages requirements: Python. You can use TCP, UDP for communication

## 1. Manga Crawler
For this module, you can choose one or many of the following sites to get data: truyentranh.net, or truyentranhtuan.com. You may suggest any other manga site.
The crawl module needs to get info of at least 100 manga
For each manga, the following need to be stored:
-	Manga name
-	Author
-	Description
-	Categories
-	Last update
-	Chapter name and list of pages
The info must be stored in JSON file manga_info.json. A sample file is provided

### Result
Site to get data: truyentranh.net
128 manga crawled and stored in manga_info.json

Instructions:

Programming language: Python 3

Firstly, I declare Spider class and create a spider to perform the crawl and extract structured data from the site. A spider should have behaviours such as initialize, crawl, gather_urls, …

The manga_info.json instruction:

![](https://github.com/duyndh/MangaProject/blob/master/crawler.png)

After trying and failing, I found the most effective method to crawl more than 100 manga from this site. 

The crawlers can be divided into 3 modules: 
-	Preprocessing: from http://truyentranh.net/danh-sach.tall.html, the spider gather manga urls in alphabetical order, with 5 manga urls whose title start with each letter.
-	Manga crawling: the spider visits each manga url gathered in above step, gathers manga informations (name, thumbnail, author, description, categories, last update) and all the chapter urls on that page.
-	Chapter crawling: the spider visits each chapter url gathered in above step, gather chapter name and all the contents (images) on that page.

Each step splited into 3 step:
-	Extract: HTTP request, fetch the HTML (and resolve the domain).
-	Transform: take features out of the HTML (title, images, content…) + run NLP algorithms.
-	Store: save to the JSON.

## 2. Manga Viewer
Build a simple webserver to feed data for web browser to read manga base on the info constructed in the above module
The webserver read info from manga_info.json and construct the html:
-	`/allmanga.html`: list of all manga, name, author and author of each manga are shown
-	`/manga_info.html?id=<manga_id>`: show detailed info of a manga with manga_id include manga name, description, author, categories, chapter list….
-	`/chapter.html?id=<chapter_id>`: view all the page of a chapter with chapter_id

![](https://github.com/duyndh/MangaProject/blob/master/viewer0.png)

![](https://github.com/duyndh/MangaProject/blob/master/viewer1.png)

![](https://github.com/duyndh/MangaProject/blob/master/viewer2.png)
