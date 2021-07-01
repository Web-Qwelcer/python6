import requests
from bs4 import BeautifulSoup
from datetime import date, datetime
from pprint import pprint
import json
URL = 'https://quotes.toscrape.com/'


def getResponse(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup

def gg(authorName, quoteText):
    for elem in quotes_list:
        # print(elem)
        if authorName in elem['author']:
            elem['quote'].append(quoteText)
            return True
    return False

quotes_list = []
page = 1

while True:
    soup = getResponse(f"{URL}page/{page}/")
    page += 1
    quotes = soup.find_all('span', class_="text")
    if len(quotes) == 0:
        break
    authors = soup.find_all('small', class_="author")
    # tags = soup.find_all('div', class_="tags")
    # pprint(authors)
    for i in range(0, len(quotes)):
        authorName = authors[i].text.strip()
        quoteText = quotes[i].text.strip()
        if gg(authorName, quoteText) == True:
            continue
        quote = {}
        quote['author'] = authorName
        quote['quote'] = []
        quote['quote'].append(quoteText)
        quote['author_info'] = URL + authors[i].find_next_sibling().get('href')[1:]
        quotes_list.append(quote)

quotes_list = sorted(quotes_list, key=lambda quotes_list: quotes_list['author'], reverse=False)
# pprint(quotes_list)
# pprint(quotes_list)

# authors_list = []
for i, item in enumerate(quotes_list):
    if i > 0 and item["author"] == quotes_list[i-1]['author']:
        continue
    soup = getResponse(item['author_info'])
    # author = {}
    item['born'] = soup.find('span', class_="author-born-date").text.strip()
    item['location'] = soup.find('span', class_="author-born-location").text.strip()
    item['description'] = soup.find('div', class_="author-description").text.strip()

pprint(quotes_list)
with open('quotes.json', 'w') as file:
    json.dump(quotes_list, file, indent=4, )
    file.close()
