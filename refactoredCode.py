import requests
from bs4 import BeautifulSoup
import pprint

# URLs for the pages to scrape
urls = ['https://news.ycombinator.com/', 'https://news.ycombinator.com/news?p=2']

# Fetch and parse both pages using list comprehension
soups = [BeautifulSoup(requests.get(url).text, 'html.parser') for url in urls]

# Combine the links and subtext from both pages
links = sum([soup.select('.titleline > a') for soup in soups], [])
subtext = sum([soup.select('.subtext') for soup in soups], [])

# Sort stories by votes
def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)

# Create custom Hacker News list
def create_custom_hn(links, subtext):
    return sort_stories_by_votes([
        {'title': link.getText(), 'link': link.get('href', None), 'votes': int(votes[0].getText().replace(' points', ''))}
        for idx, link in enumerate(links)
        if (votes := subtext[idx].select('.score')) and int(votes[0].getText().replace(' points', '')) >= 100
    ])

pprint.pprint(create_custom_hn(links, subtext))