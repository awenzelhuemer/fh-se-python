import json

from bs4 import BeautifulSoup
import requests
import re
import hashlib

url = r'https://www.wienzufuss.at/blog/'
r = requests.get(url)
doc = BeautifulSoup(r.text, 'html.parser')

print(doc.prettify())

divs = doc.findAll("div", {"class": "post"})

blog = {}

for d in divs:
    link = d.find("h2").find("a").get("href")
    header = d.find("h2").text.strip()
    comments = re.sub("[^[0-9]", "", d.find(text=re.compile("Kommentar")))
    comments = comments if comments else 0

    blog[hashlib.md5(header.encode()).hexdigest()[:10]] = {
        "title": header,
        "link": link,
        "comments": comments
    }

print(json.dumps(blog, indent=4, ensure_ascii=False))

# TODO: Kategorien und Autoren

categories = {}

for d in divs:
    header = d.find("h2").text.strip()
    category_list = [c.text for c in d.findAll("a", {"rel": "category tag"})]
    author = d.find("a", {"rel": "author"}).text
    categories[hashlib.md5(header.encode()).hexdigest()[:10]] = {
        "categories": category_list,
        "author": author
    }

print(json.dumps(categories, indent=4, ensure_ascii=False))

# TODO: Blogeintrag: Überschriften #Links, #Bilder, #Wörter

blogs_with_headers_and_links = {}

for key in blog:
    detail_r = requests.get(blog[key].get('link'))
    detail_doc = BeautifulSoup(detail_r.text, 'html.parser')

    header = detail_doc.find("title").text.strip()
    all_headers = detail_doc.find_all(re.compile('^h[1-6]$'))

    blogs_with_headers_and_links[hashlib.md5(header.encode()).hexdigest()[:10]] = {
        "headers": [h.text.strip() for h in all_headers],
        "linkCount": len(detail_doc.findAll("a")),
        "imgCount": len(detail_doc.findAll("img")),
        "words": len(detail_doc.text.strip().split(" "))
    }

print(json.dumps(blogs_with_headers_and_links, indent=4, ensure_ascii=False))

# TODO: Alle Blogeinträge durchgehen

all_blogs = {}

for key in blog:
    detail_r = requests.get(blog[key].get('link'))
    detail_doc = BeautifulSoup(detail_r.text, 'html.parser')
    header = detail_doc.find("h2").text.strip()
    all_blogs[hashlib.md5(header.encode()).hexdigest()[:10]] = {
        "header": header
    }

print(json.dumps(all_blogs, indent=4, ensure_ascii=False))

# TODO: Speichern der JSON aka 1. Datensatz zur Übungsvalidierung