from . import Scrape, Listing
from bs4 import BeautifulSoup

class DomuScrape(Scrape):

  base_url = 'https://www.domu.com'

  def __init__(self, soup: BeautifulSoup):
    self.matches = soup.find_all(name="div", attrs={'class': "domu-search-listing"})#soup.find_all(name="section", attrs={'data-name': "DetailedInfoContainer"})



  def parse_listings(self):
    acc = []
    print(f"Matches is {self.matches}")
    for match in self.matches:
      try:
        price = match.find(name="h3", attrs={'class': 'listing-price'}).getText()
        address = match.find(name="div", attrs={'class': 'listing-address'}).getText()
        title_element = match.find(name="a", attrs={'class': 'listing-title'}, href=True)
        title = title_element.getText()
        link = title_element["href"]
        listing = Listing(address=address, price=price, title=title, url=link)
        acc.append(listing)
        # print(f"price is {price}")
        # print(f'address is {address}, title {title}')
        # print(f'link is {self.base_url}{link}')
      except AttributeError:
        # We aren't going to add an element, print statement
        continue

    return acc