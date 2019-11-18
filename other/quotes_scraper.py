import csv
import os
import requests

from bs4 import BeautifulSoup


def scrape_quotes():
    '''
    Scrapes motivational quotes from site using bs4 
    and exports them by means of a CSV. 
    '''
    if os.path.exists('Discord-Bot/data/motivational_quotes.csv'):
        return 'Quotes already scraped.'

    result = requests.get('https://motivationping.com/quotes/')
    soup = BeautifulSoup(result.text, 'html.parser')
    body = soup.find(
        'body', class_='post-template-default single single-post postid-122 single-format-standard')

    raw_quotes = [article.text for article in body.find(
        'div').find_all('strong')]
    quotes = raw_quotes[1:-7]

    with open('Discord-Bot/data/motivational_quotes.csv', 'w', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(quotes)