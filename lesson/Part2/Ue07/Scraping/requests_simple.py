import requests
import json
from bs4 import BeautifulSoup

url = r'https://www.fh-ooe.at'
r = requests.get(url)

print(r.status_code)
print(json.dumps(dict(r.headers), indent=4))