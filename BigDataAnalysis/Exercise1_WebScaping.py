# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import random

# Define the function
def scrapeWikiArticle(url, remaining_steps = 10):
    # url defines the Wikipedia webpage to start
    # remaining_step defines how many steps to run
    if remaining_steps > 0:
        # Connect to the url
        response = requests.get(url=url)
        
        # Retrieve the webpage content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find and print the title of the webpage
        title = soup.find(id="firstHeading")
        print(title.text)
        
        # Find all the urls within the webpage
        allLinks = soup.find(id="bodyContent").find_all("a")
        random.shuffle(allLinks)
        linkToScrape = 0
        
         # Find the next url to visit
        for link in allLinks:
            # We are only interested in other wiki articles
            if link['href'].find("/wiki/") == -1: 
                continue
            if link['href'].find("https:") != -1:
                continue
            if link['href'].find("Commons:") != -1:
                continue
            if link['href'].find("Special:") != -1:
                continue
    
            # Use this link to scrape
            linkToScrape = link
            break
        # print(linkToScrape['href'])
        
        # Recursive function
        try:
            scrapeWikiArticle(
                "https://en.wikipedia.org" + linkToScrape['href'],
                remaining_steps = remaining_steps - 1
            )
        except:
            print(linkToScrape['href'])

# Run the main function
scrapeWikiArticle("https://en.wikipedia.org/wiki/Hong_Kong")