from bs4 import BeautifulSoup
import requests

url = r'https://www.fh-ooe.at'
r = requests.get(url)

soup = BeautifulSoup(r.text, 'html.parser')
print(soup.prettify())
print(soup.title)
print(soup.title.text)
print(soup.h2)
print(soup.find("a").get("href"))
print(soup.findAll("h2"))
