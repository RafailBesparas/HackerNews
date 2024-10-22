import requests
from bs4 import BeautifulSoup
import pprint

res = requests.get('https://news.ycombinator.com/')
res2 = requests.get('https://news.ycombinator.com/news?p=2')

soup = BeautifulSoup(res.text, 'html.parser')
soup2 = BeautifulSoup(res2.text, 'html.parser')

links = soup.select('.titleline > a')
subtext = soup.select('.subtext')

links2 = soup2.select('.titleline > a')
subtext2 = soup2.select('.subtext')

# combine the links
mega_links = links + links2
mega_subtext = subtext + subtext2

def sort_stories_by_votes(hnlist):
    # sort the dictionary by using a lamda function on votes
    return sorted(hnlist, key = lambda k:k['votes'], reverse=True)

def create_custom_hn(links, subtext):
    hn = []
    #grab the index of each item
    for idx, item in enumerate(links):
        # we get the title of each of the articles
        title = links[idx].getText()
        href = links[idx].get('href', None)
        votes = subtext[idx].select('.score')

        # If vote is not zero
        if len(votes) != 0:
            points = int(votes[0].getText().replace(' points', ''))
            if points >= 100:
                 hn.append({'title':title, 'link':href, 'votes':points})

    return sort_stories_by_votes(hn)

pprint.pprint(create_custom_hn(mega_links, mega_subtext))