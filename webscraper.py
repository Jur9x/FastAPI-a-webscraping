import requests
from bs4 import BeautifulSoup
import json

URL = 'https://www.imdb.com/search/name/?match_all=true&ref_=nv_cel_m'

page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
name_links = soup.select('div.lister-item-content>h3>a')
role_links = soup.select('div.lister-item-content>p.text-muted')
info_links = soup.select('div.lister-item-content>p:not([class])')
names = [tag.text[1:-1] for tag in name_links]
roles = [tag.text[26:].split(' |')[0] for tag in role_links]
infos = [tag.text[1:-17].replace('"', '') for tag in info_links]
urls = [f'https://www.imdb.com{tag["href"]}' for tag in name_links]

with open("names.json",  "w", encoding='utf-8') as file:
    file.write('[')
    for i in range(0, 50):
        row = f'"name": "{names[i]}", "role": "{roles[i]}", "info": "{infos[i]}", "url": "{urls[i]}"'
        if i == 49:
            row = '{' + row + '} '
        else:
            row = '{' + row + '}, \n'
        file.write(row)
    file.write(']')

print(infos)